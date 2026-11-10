from datetime import datetime


def mock_call(owner: str, summary_text: str) -> dict:
    return {"status": "mocked", "owner": owner, "message": summary_text, "called_at": datetime.now().isoformat()}


def mock_send_order(order: list[dict]) -> dict:
    return {"status": "sent", "channel": "whatsapp", "items": order, "sent_at": datetime.now().isoformat()}

