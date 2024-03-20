
import telebot
from datetime import datetime
import time
import threading

# Токен бота
TOKEN = "INPUT YOUR TOKIN"

# Словарь для хранения задач и времени
tasks = {}

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /add_task
@bot.message_handler(commands=['add_task'])
def add_task(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Введите задачу и время через двоеточие (например, Позвонить другу, 15:00)")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    task_data = message.text.split(',')
    if len(task_data) == 2:
        task = task_data[0].strip()
        time = task_data[1].strip()
        tasks[user_id] = (task, time)
        bot.send_message(user_id, f"Задача '{task}' добавлена на {time}")
    else:
        bot.send_message(user_id, "Неверный формат. Введите задачу и время через двоеточие.")

# Функция для отправки сообщений по расписанию
def send_task_reminder(user_id):
    while True:
        if user_id in tasks:
            current_time = datetime.now().strftime("%H:%M")
            task, time = tasks[user_id]
            print(current_time)
            print(time)
            if time <= current_time:
                bot.send_message(TARGET_USER_ID, f"Напоминание: {task}")
        time.sleep(60)

# ID пользователя, который будет получать уведомления о задачах
TARGET_USER_ID = 283883368

# Запускаем поток для отправки сообщений по расписанию для каждого пользователя
for user_id in tasks.keys():
    threading.Thread(target=send_task_reminder, args=(user_id,)).start()

# Запускаем бота
bot.polling()


#Замените `YOUR_TELEGRAM_BOT_TOKEN` на актуальный токен вашего телеграм бота, а
# `YOUR_TARGET_USER_ID` на ID пользователя, который будет получать уведомления о задачах.

#Этот код создает телеграм бота, в котором один пользователь может добавлять задачи
# и время для их выполнения, а другой пользователь будет получать уведомления о задачах
# в указанное время. Каждый пользователь имеет свой список задач.