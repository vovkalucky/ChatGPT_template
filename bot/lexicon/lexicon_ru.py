from bot.config_data.config import load_config
config = load_config()

LEXICON_RU: dict[str, str] = {
    'loading_model': '⌛ Ответ генерируется. Пожалуйста подождите...',
    'back': '↩️ Назад',
    '/cancel': '🗑️ Контекст диалога очищен 🗑️\n\nВы можете начать новый диалог в любой момент',
    'gpt_start_dialog': 'Привет! Как я могу помочь вам?',
    'response_null': '😔 К сожалению, API ChatGPT платный и вы исчерпали лимит бесплатных обращений.\n\n' 
                    'Если функционал вас заинтересовал и хотите увеличить число обращений к '
                     'новейшей модели ChatGPT - напишите @ekgardt',
    'admin_contact': '🗣️ Связаться с админом',
    'admin': '💻 Админка',
    'admin_menu': '💻 Это главное меню админки',
    'admin_users': '👥 Пользователи',
    'admin_response': '🔢 Осталось запросов',
    'no_response': '🤷‍♂️ Ответ от ChatGPT не получен. \nПовторите попытку ️⬇️',
    'subscribe_channel': f'Чтобы пользовать ChatGPT, нужно быть подписчиком моей группы ⬇️\n\n {config.tg_bot.group_link}'
}

LEXICON_COMMANDS_RU: dict[str, str] = {'/start': 'Запуск бота', '/cancel': '🗑️ Очистить контекст'}
