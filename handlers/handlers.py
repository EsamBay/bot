from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from bot.config.config import ADMIN_ID
from bot.keyboards.keyboards import get_main_keyboard, get_stars_keyboard
from bot.languages.manager import get_text, set_language, get_language

router = Router()

# تتبع بسيط للمستخدمين (للإحصائيات)
users_db = set()

class SupportStates(StatesGroup):
    waiting_for_custom_stars = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    users_db.add(message.from_user.id)
    lang = get_language(message.from_user.id)
    await message.answer(get_text("start_message", lang), reply_markup=get_main_keyboard(lang))

@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    await callback.message.answer(get_text("support_prompt", lang))
    await callback.answer()

@router.message(F.text, ~CommandStart())
async def handle_support_message(message: Message):
    if await SupportStates.waiting_for_custom_stars.get_state(message.bot, message.from_user.id) is not None:
        return
    lang = get_language(message.from_user.id)
    admin_msg = get_text("admin_received", lang).format(
        user_id=message.from_user.id,
        message=message.html_text
    )
    try:
        await message.bot.send_message(ADMIN_ID, admin_msg, parse_mode="HTML")
        await message.answer(get_text("support_received", lang))
    except Exception:
        await message.answer("⚠️ حدث خطأ أثناء الإرسال للدعم.")

@router.callback_query(F.data == "switch_lang")
async def switch_lang(callback: CallbackQuery):
    current = get_language(callback.from_user.id)
    new_lang = "en" if current == "ar" else "ar"
    set_language(callback.from_user.id, new_lang)
    await callback.message.answer(get_text("language_changed", new_lang))    await cmd_start(callback.message)
    await callback.answer()

@router.callback_query(F.data == "dev_support")
async def dev_support(callback: CallbackQuery):
    lang = get_language(callback.from_user.id)
    await callback.message.answer(get_text("dev_support", lang), reply_markup=get_stars_keyboard())
    await callback.answer()

@router.callback_query(F.data.startswith("star_"))
async def star_selection(callback: CallbackQuery, bot: Bot):
    lang = get_language(callback.from_user.id)
    if callback.data == "star_custom":
        await callback.message.answer(get_text("enter_custom_amount", lang))
        await SupportStates.waiting_for_custom_stars.set()
        await callback.answer()
        return

    amount = int(callback.data.split("_")[1])
    await send_star_invoice(callback.message, amount, bot)
    await callback.answer()

@router.message(SupportStates.waiting_for_custom_stars, F.text)
async def handle_custom_stars(message: Message, bot: Bot, state: FSMContext):
    lang = get_language(message.from_user.id)
    try:
        amount = int(message.text.strip())
        if amount <= 0:
            await message.answer(get_text("invalid_amount", lang))
            return
        await send_star_invoice(message, amount, bot)
        await state.clear()
    except ValueError:
        await message.answer(get_text("invalid_amount", lang))

async def send_star_invoice(msg, amount: int, bot: Bot):
    lang = get_language(msg.from_user.id)
    await bot.send_invoice(
        chat_id=msg.from_user.id,
        title="دعم المطور" if lang == "ar" else "Support Developer",
        description=f"{amount} نجوم" if lang == "ar" else f"{amount} Stars",
        payload=f"dev_support_{amount}",
        currency="XTR",
        prices=[LabeledPrice(label="Stars", amount=amount)],
        provider_token=""  # مطلوب لنظام نجوم تيليجرام
    )
    await msg.answer(get_text("thanks_support", lang))

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):    await cmd_start(callback.message)
    await callback.answer()
