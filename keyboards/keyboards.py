from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_keyboard(lang: str = "ar") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🆘 Support" if lang == "en" else "🆘 الدعم الفني", callback_data="support"),
        InlineKeyboardButton(text="🌍 Language" if lang == "en" else "🌍 اللغة", callback_data="switch_lang")
    )
    builder.row(
        InlineKeyboardButton(text="⭐ دعم المطور" if lang == "ar" else "⭐ Support Dev", callback_data="dev_support")
    )
    return builder.as_markup()

def get_stars_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    amounts = [50, 150, 250, 500]
    for amount in amounts:
        builder.row(InlineKeyboardButton(text=f"⭐ {amount} نجمة", callback_data=f"star_{amount}"))
    builder.row(InlineKeyboardButton(text="🔢 كمية مخصصة", callback_data="star_custom"))
    builder.row(InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_main"))
    return builder.as_markup()
