import time
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import token
from logic import TextAnalysis

bot = telebot.TeleBot(token)


# ---------- UI ----------

def gen_markup_for_text():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton('Получить ответ', callback_data='text_ans'),
        InlineKeyboardButton('Перевести сообщение', callback_data='text_translate')
    )
    return markup


# ---------- HUMAN TYPING ----------

def split_text(text, max_length=120):
    words = text.split()
    chunks = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= max_length:
            current += (" " + word if current else word)
        else:
            chunks.append(current)
            current = word

    if current:
        chunks.append(current)

    return chunks


def send_human_typing_message(chat_id, text):
    chunks = split_text(text)

    for chunk in chunks:
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(random.uniform(0.6, 2.2))
        bot.send_message(chat_id, chunk)
        time.sleep(random.uniform(0.3, 1.0))


# ---------- CALLBACKS ----------

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    obj = TextAnalysis.memory[call.from_user.username][-1]

    # сначала typing — потом вычисления
    bot.send_chat_action(call.message.chat.id, 'typing')
    time.sleep(random.uniform(1.0, 2.5))

    if call.data == "text_ans":
        text = obj.get_answer()

    elif call.data == "text_translate":
        text = obj.get_translation()
    else:
        return

    send_human_typing_message(call.message.chat.id, text)


# ---------- MESSAGES ----------

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # имитация «прочитал сообщение»
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(random.uniform(0.8, 1.6))

    # ТОЛЬКО сохраняем сообщение, ничего не считаем
    TextAnalysis(message.text, message.from_user.username)

    bot.send_message(
        message.chat.id,
        "Я получил сообщение 👀\n"
        "Что ты хочешь с ним сделать?",
        reply_markup=gen_markup_for_text()
    )


# ---------- START ----------

bot.infinity_polling(none_stop=True)
