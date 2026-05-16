import json
from pathlib import Path

lang_path = Path(__file__).parent
users_lang = {}

def load_lang(lang_code):
    with open(lang_path / f"{lang_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_text(key, lang_code="ar"):
    texts = load_lang(lang_code)
    return texts.get(key, key)

def get_language(user_id):
    return users_lang.get(user_id, "ar")

def set_language(user_id, lang_code):
    users_lang[user_id] = lang_code
