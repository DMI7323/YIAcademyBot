import telebot

# Встав свій токен сюди (НЕ публікуй у відкритих місцях!)
BOT_TOKEN = "8071401341:AAFP8TVUplsB9cDzat6kx93JUP-QdFeoREc"

bot = telebot.TeleBot(BOT_TOKEN)

# Словник валідних кодів доступу — заміни на свої реальні коди та посилання
valid_codes = {
    "ABC123": {
        "video_link": "https://t.me/+channel_video_link",
        "chat_link": "https://t.me/+chat_link"
    },
    "XYZ789": {
        "video_link": "https://t.me/+another_channel_link",
        "chat_link": "https://t.me/+another_chat_link"
    }
}

# Запам'ятовуємо активованих користувачів, щоб не давати доступ повторно
used_users = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_text = (
        "👋 Вітаємо в офіційному боті для перевірки доступу до закритих каналів і чатів школи Юлії Іщук!\n\n"
        "⚠️ Увага! Всі курси, відеоуроки та чати перевірок доступні лише за офіційними посиланнями після верифікації в цьому боті.\n\n"
        "🔐 Як це працює:\n"
        "1️⃣ Введіть свій персональний код доступу, який отримали після оплати курсу.\n"
        "2️⃣ Бот перевірить його справжність та активність.\n"
        "3️⃣ Якщо все гаразд — отримаєте активне посилання на закритий канал і чат вашого курсу.\n"
        "4️⃣ Якщо код недійсний або вже використаний — бот повідомить про це.\n\n"
        "📌 Важливо!\n"
        "Усі коди індивідуальні та діють лише для одного користувача. Передача доступу третім особам заборонена.\n\n"
        "Без верифікації доступ до закритих матеріалів неможливий.\n\n"
        "Напишіть /code, щоб ввести свій код."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=["code"])
def ask_code(message):
    msg = bot.send_message(message.chat.id, "🔐 Введи свій персональний код доступу:")
    bot.register_next_step_handler(msg, check_code)

def check_code(message):
    user_id = message.chat.id
    code = message.text.strip().upper()

    if user_id in used_users:
        bot.send_message(user_id, "✅ Ти вже активував доступ.\n"
                                  f"📥 Відеоуроки: {used_users[user_id]['video']}\n"
                                  f"💬 Чат: {used_users[user_id]['chat']}")
        return

    if code in valid_codes:
        links = valid_codes[code]
        used_users[user_id] = {
            "code": code,
            "video": links["video_link"],
            "chat": links["chat_link"]
        }
        bot.send_message(user_id, "✅ Чудово! Ось твої посилання:\n"
                                  f"📥 Відеоуроки: {links['video_link']}\n"
                                  f"💬 Чат: {links['chat_link']}")
    else:
        bot.send_message(user_id, "❌ Невірний код. Спробуй ще раз або звернися до підтримки.")

bot.polling()
