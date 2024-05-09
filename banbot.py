from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatPermissions

# Токен вашего бота
TOKEN = 'YOUR_BOT_TOKEN'

# Список запрещенных слов
ban_words = []

# Функция для проверки сообщений на наличие запрещенных слов
def check_for_banned_words(update, context):
    message_text = update.message.text.lower()
    for word in ban_words:
        if word in message_text:
            # Удаляем сообщение с запрещенным словом
            update.message.delete()
            # Запрещаем пользователю писать в группе
            context.bot.restrict_chat_member(update.message.chat.id, update.message.from_user.id, ChatPermissions(can_send_messages=False))
            # Пожаловаться на пользователя за спам
            context.bot.send_message(update.message.chat.id, f'Пользователь @{update.message.from_user.username} пожаловался на спам. Слово: {word}')
            return

# Обработчик администраторских команд для добавления и удаления запрещенных слов
def admin_controls(update, context):
    if update.message.from_user.id == YOUR_ADMIN_ID:  # Замените YOUR_ADMIN_ID на ваш ID в Telegram
        command = context.args[0].lower()

        if command == 'addword':
            word_to_ban = context.args[1].lower()
            ban_words.append(word_to_ban)
            update.message.reply_text(f'Слово "{word_to_ban}" добавлено в список запрещенных слов.')
        elif command == 'removeword':
            word_to_remove = context.args[1].lower()
            if word_to_remove in ban_words:
                ban_words.remove(word_to_remove)
                update.message.reply_text(f'Слово "{word_to_remove}" удалено из списка запрещенных слов.')
            else:
                update.message.reply_text(f'Слово "{word_to_remove}" не найдено в списке запрещенных слов.')

# Создание обработчика команд для административной панели
admin_handler = CommandHandler('admin', admin_controls)

# Создание обработчика сообщений для проверки на наличие запрещенных слов
message_handler = MessageHandler(Filters.text & (~Filters.command), check_for_banned_words)

# Инициализация бота и добавление обработчиков
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(admin_handler)
dispatcher.add_handler(message_handler)

# Запуск бота
updater.start_polling()
updater.idle()