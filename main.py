import json
import os
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .db import connect, init_db, rows
from .analytics import daily_summary
from .reorder import build_order
from .intents import extract_intent
from .gnani_llm import phrase
from .scheduler import start_scheduler
from .telephony import mock_send_order
from .languages import LANGUAGES, reply as localized_reply

load_dotenv()
init_db()
app = FastAPI(title="Dukaan Mitra")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
async def startup(): 
    if os.getenv("DISABLE_SCHEDULER", "false").lower() != "true":
        start_scheduler()


@app.get("/api/summary")
async def summary():
    result = daily_summary(threshold_days=float(os.getenv("LOW_STOCK_DAYS", "2")))
    result["order_draft"] = build_order(result, float(os.getenv("LEAD_DAYS", "3")), float(os.getenv("SAFETY_FACTOR", "1.5")))
    return result


@app.get("/api/products")
async def products():
    return rows("SELECT * FROM products ORDER BY name")


@app.get("/api/settings")
async def settings():
    return {
        "closing_time": os.getenv("CLOSING_TIME", "21:00"),
        "lead_days": float(os.getenv("LEAD_DAYS", "3")),
        "safety_factor": float(os.getenv("SAFETY_FACTOR", "1.5")),
        "supplier_contact": os.getenv("SUPPLIER_CONTACT", ""),
    }


@app.get("/api/languages")
async def languages():
    return [{"code": code, **details} for code, details in LANGUAGES.items()]


@app.get("/api/sales/history")
async def sales_history():
    return rows("""SELECT date(sold_at) day, ROUND(SUM(qty*price),2) total
        FROM sales GROUP BY date(sold_at) ORDER BY day DESC LIMIT 30""")

@app.post("/api/order/approve")
async def approve_order():
    result = await summary()
    sent = mock_send_order(result["order_draft"])
    with connect() as db:
        db.execute("INSERT INTO orders(status,created_at,payload) VALUES(?,?,?)", ("sent", datetime.now().isoformat(), json.dumps(sent)))
    return sent


@app.post("/api/import")
async def import_csv(file: UploadFile = File(...)):
    import csv, io
    data = csv.DictReader(io.StringIO((await file.read()).decode("utf-8")))
    count = 0
    with connect() as db:
        for row in data:
            product = db.execute("SELECT id FROM products WHERE name=?", (row["item"],)).fetchone()
            if not product:
                db.execute("INSERT INTO products(name,unit,stock,price) VALUES(?,?,?,?)", (row["item"], row.get("unit", "piece"), float(row.get("stock", 0)), float(row.get("price", 0))))
                product = db.execute("SELECT id FROM products WHERE name=?", (row["item"],)).fetchone()
            db.execute("INSERT INTO sales(product_id,qty,price,sold_at,sale_type,customer) VALUES(?,?,?,?,?,?)", (product["id"], float(row["qty"]), float(row.get("price", 0)), row.get("date", date.today().isoformat()), row.get("type", "cash"), row.get("customer")))
            count += 1
    return {"imported": count}


@app.websocket("/ws/voice")
async def voice(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw_message = await websocket.receive_text()
            try:
                payload = json.loads(raw_message)
            except json.JSONDecodeError:
                payload = {"text": raw_message}
            if not isinstance(payload, dict):
                payload = {"text": raw_message}
            message = str(payload.get("text", "")).strip()
            language = str(payload.get("language", os.getenv("OWNER_LANGUAGE", "hinglish"))).lower()
            if language not in LANGUAGES:
                language = "hinglish"
            parsed = extract_intent(message)
            if parsed["intent"] == "log_sale":
                with connect() as db:
                    for entity in parsed["entities"]:
                        product = db.execute("SELECT id FROM products WHERE lower(name)=?", (entity["item"].lower(),)).fetchone()
                        if product:
                            db.execute("INSERT INTO sales(product_id,qty,price,sold_at,sale_type) SELECT id,?,?,?,? FROM products WHERE id=?", (entity["qty"], db.execute("SELECT price FROM products WHERE id=?", (product["id"],)).fetchone()["price"], date.today().isoformat(), entity["type"], product["id"]))
                            db.execute("UPDATE products SET stock=stock-? WHERE id=?", (entity["qty"], product["id"]))
                reply = localized_reply(language, "sale")
            elif parsed["intent"] == "stock_query":
                product = next((p for p in rows("SELECT * FROM products") if p["name"].lower() in parsed["entities"]["item"]), None)
                reply = localized_reply(language, "stock", item=product["name"], stock=product["stock"], unit=product["unit"]) if product else localized_reply(language, "unknown")
            elif parsed["intent"] == "approve_order":
                result = await summary()
                mock_send_order(result["order_draft"])
                reply = localized_reply(language, "approve")
            elif parsed["intent"] == "reject_order":
                reply = localized_reply(language, "reject")
            elif parsed["intent"] == "repeat":
                reply = localized_reply(language, "repeat")
            elif parsed["intent"] == "correct_order":
                reply = localized_reply(language, "correct")
            elif parsed["intent"] == "slower":
                reply = localized_reply(language, "slower")
            elif parsed["intent"] == "skip":
                reply = localized_reply(language, "skip")
            else:
                reply = await phrase(await summary(), language)
            await websocket.send_json({"transcript": message, "intent": parsed, "reply": reply, "language": language, "summary": await summary()})
    except WebSocketDisconnect:
        return


@app.get("/")
async def frontend():
    return FileResponse(Path(__file__).parent.parent / "frontend" / "index.html")
