"""Offline reply templates for the voice assistant's supported languages."""

LANGUAGES = {
    "en": {"name": "English", "locale": "en-IN"},
    "hi": {"name": "हिन्दी", "locale": "hi-IN"},
    "hinglish": {"name": "Hinglish", "locale": "hi-IN"},
    "ta": {"name": "தமிழ்", "locale": "ta-IN"},
    "bn": {"name": "বাংলা", "locale": "bn-IN"},
    "mr": {"name": "मराठी", "locale": "mr-IN"},
    "gu": {"name": "ગુજરાતી", "locale": "gu-IN"},
    "te": {"name": "తెలుగు", "locale": "te-IN"},
    "kn": {"name": "ಕನ್ನಡ", "locale": "kn-IN"},
}

CONTROL_REPLIES = {
    "en": {"slower": "I will speak more slowly.", "skip": "Okay, moving on."},
    "hi": {"slower": "मैं धीरे बोलूँगा।", "skip": "ठीक है, आगे बढ़ते हैं।"},
    "hinglish": {"slower": "Main dheere bolunga.", "skip": "Theek hai, aage badhte hain."},
    "ta": {"slower": "நான் மெதுவாகப் பேசுகிறேன்.", "skip": "சரி, அடுத்ததற்குச் செல்வோம்."},
    "bn": {"slower": "আমি ধীরে বলব।", "skip": "ঠিক আছে, এগিয়ে যাই।"},
    "mr": {"slower": "मी हळू बोलेन.", "skip": "ठीक आहे, पुढे जाऊया."},
    "gu": {"slower": "હું ધીમે બોલીશ.", "skip": "ઠીક છે, આગળ વધીએ."},
    "te": {"slower": "నేను నెమ్మదిగా మాట్లాడతాను.", "skip": "సరే, ముందుకు వెళ్దాం."},
    "kn": {"slower": "ನಾನು ನಿಧಾನವಾಗಿ ಮಾತನಾಡುತ್ತೇನೆ.", "skip": "ಸರಿ, ಮುಂದುವರಿಯೋಣ."},
}


def reply(language: str, message: str, **values) -> str:
    """Return a short spoken reply in the selected language."""
    templates = {
        "en": {
            "summary": "Today's sales are Rs {sales}. {low} items are low on stock. Would you like to approve the order?",
            "sale": "Sale recorded. What else would you like to do?",
            "stock": "{item}: {stock} {unit} remaining.",
            "approve": "The order has been approved.",
            "reject": "Okay, I will not place the order.",
            "repeat": "Please repeat your question.",
            "unknown": "I could not understand that. Please try again.",
            "correct": "The order quantity has been updated.",
        },
        "hi": {
            "summary": "आज की बिक्री {sales} रुपये है। {low} सामान कम बचा है। क्या ऑर्डर मंज़ूर कर दूँ?",
            "sale": "बिक्री दर्ज कर ली है। और कुछ बताइए।",
            "stock": "{item}: {stock} {unit} बचा है।",
            "approve": "ऑर्डर मंज़ूर कर दिया है।",
            "reject": "ठीक है, ऑर्डर नहीं भेजूँगा।",
            "repeat": "कृपया अपना सवाल फिर से बताइए।",
            "unknown": "माफ़ कीजिए, समझ नहीं आया। कृपया फिर से बोलिए।",
            "correct": "ऑर्डर की मात्रा बदल दी है।",
        },
        "hinglish": {
            "summary": "Aaj ki sale Rs {sales} hai. {low} items ka stock kam hai. Order approve karna hai?",
            "sale": "Sale note kar li. Aur kuch?",
            "stock": "{item} ke {stock} {unit} bache hain.",
            "approve": "Order approve kar diya hai.",
            "reject": "Theek hai, order nahi bhejunga.",
            "repeat": "Apna sawaal phir se boliye.",
            "unknown": "Samajh nahi aaya. Ek baar phir boliye.",
            "correct": "Order ki quantity badal di hai.",
        },
        "ta": {
            "summary": "இன்றைய விற்பனை {sales} ரூபாய். {low} பொருட்களின் இருப்பு குறைவாக உள்ளது. ஆர்டரை உறுதி செய்யவா?",
            "sale": "விற்பனை பதிவு செய்யப்பட்டது. வேறு ஏதாவது வேண்டுமா?",
            "stock": "{item}: {stock} {unit} மீதம் உள்ளது.",
            "approve": "ஆர்டர் உறுதி செய்யப்பட்டது.",
            "reject": "சரி, ஆர்டர் அனுப்பப்படாது.",
            "repeat": "உங்கள் கேள்வியை மீண்டும் சொல்லுங்கள்.",
            "unknown": "புரியவில்லை. மீண்டும் சொல்லுங்கள்.",
            "correct": "ஆர்டர் அளவு மாற்றப்பட்டது.",
        },
        "bn": {
            "summary": "আজকের বিক্রি {sales} টাকা। {low}টি পণ্যের স্টক কম। অর্ডারটি অনুমোদন করব?",
            "sale": "বিক্রির তথ্য রাখা হয়েছে। আর কিছু?",
            "stock": "{item}: {stock} {unit} বাকি আছে।",
            "approve": "অর্ডার অনুমোদন করা হয়েছে।",
            "reject": "ঠিক আছে, অর্ডার পাঠানো হবে না।",
            "repeat": "আপনার প্রশ্নটি আবার বলুন।",
            "unknown": "বুঝতে পারিনি। আবার বলুন।",
            "correct": "অর্ডারের পরিমাণ বদলানো হয়েছে।",
        },
        "mr": {
            "summary": "आजची विक्री {sales} रुपये आहे. {low} वस्तूंचा साठा कमी आहे. ऑर्डर मंजूर करू?",
            "sale": "विक्री नोंदवली आहे. आणखी काही?",
            "stock": "{item}: {stock} {unit} शिल्लक आहे.",
            "approve": "ऑर्डर मंजूर केली आहे.",
            "reject": "ठीक आहे, ऑर्डर पाठवणार नाही.",
            "repeat": "कृपया तुमचा प्रश्न पुन्हा सांगा.",
            "unknown": "समजले नाही. कृपया पुन्हा सांगा.",
            "correct": "ऑर्डरचे प्रमाण बदलले आहे.",
        },
        "gu": {
            "summary": "આજનું વેચાણ {sales} રૂપિયા છે. {low} વસ્તુઓનો સ્ટોક ઓછો છે. ઓર્ડર મંજૂર કરું?",
            "sale": "વેચાણ નોંધ્યું છે. બીજું કંઈ?",
            "stock": "{item}: {stock} {unit} બાકી છે.",
            "approve": "ઓર્ડર મંજૂર કર્યો છે.",
            "reject": "ઠીક છે, ઓર્ડર મોકલવામાં નહીં આવે.",
            "repeat": "કૃપા કરીને તમારો પ્રશ્ન ફરીથી કહો.",
            "unknown": "સમજાયું નથી. કૃપા કરીને ફરીથી કહો.",
            "correct": "ઓર્ડરનો જથ્થો બદલ્યો છે.",
        },
        "te": {
            "summary": "ఈరోజు అమ్మకాలు {sales} రూపాయలు. {low} వస్తువుల నిల్వ తక్కువగా ఉంది. ఆర్డర్‌ను ఆమోదించనా?",
            "sale": "అమ్మకాన్ని నమోదు చేశాను. ఇంకేమైనా కావాలా?",
            "stock": "{item}: {stock} {unit} మిగిలి ఉంది.",
            "approve": "ఆర్డర్‌ను ఆమోదించాను.",
            "reject": "సరే, ఆర్డర్ పంపను.",
            "repeat": "మీ ప్రశ్నను మళ్లీ చెప్పండి.",
            "unknown": "అర్థం కాలేదు. దయచేసి మళ్లీ చెప్పండి.",
            "correct": "ఆర్డర్ పరిమాణాన్ని మార్చాను.",
        },
        "kn": {
            "summary": "ಇಂದಿನ ಮಾರಾಟ {sales} ರೂಪಾಯಿ. {low} ವಸ್ತುಗಳ ಸಂಗ್ರಹ ಕಡಿಮೆಯಿದೆ. ಆರ್ಡರ್ ಅನುಮೋದಿಸಲೇ?",
            "sale": "ಮಾರಾಟವನ್ನು ದಾಖಲಿಸಿದ್ದೇನೆ. ಇನ್ನೇನಾದರೂ ಬೇಕೇ?",
            "stock": "{item}: {stock} {unit} ಉಳಿದಿದೆ.",
            "approve": "ಆರ್ಡರ್ ಅನುಮೋದಿಸಲಾಗಿದೆ.",
            "reject": "ಸರಿ, ಆರ್ಡರ್ ಕಳುಹಿಸುವುದಿಲ್ಲ.",
            "repeat": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಮತ್ತೆ ಹೇಳಿ.",
            "unknown": "ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಹೇಳಿ.",
            "correct": "ಆರ್ಡರ್ ಪ್ರಮಾಣವನ್ನು ಬದಲಾಯಿಸಲಾಗಿದೆ.",
        },
    }
    language = language if language in LANGUAGES else "hinglish"
    if message in CONTROL_REPLIES[language]:
        return CONTROL_REPLIES[language][message]
    return templates[language][message].format(**values)
