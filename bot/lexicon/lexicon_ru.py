from bot.config_data.config import load_config
config = load_config()

LEXICON_RU: dict[str, str] = {
    'loading_model': '⌛ Ответ генерируется. Пожалуйста подождите...',
    'back': '↩️ Назад',
    '/cancel': '🗑️ Контекст диалога очищен 🗑️\n\nВы можете начать новый диалог, отправив команду /gpt',
    '/start': (""
               "Здравствуйте! 😊\nВ этом боте реализована база знаний профессионального юриста "
               "\n\n"
               "🔹 Обучен на данных вашего бизнеса!\n"
               "🔹 Ведет текстовый диалог с собеседником\n"
               "🔹 Запоминает историю сообщений\n"
               "🔥 Способен принимать речь собеседника, переводить в текст и отправлять в ChatGPT.\n" 
               "🔹 Генерирует потрясающие изображения через нейросеть Dalle-3\n"
               "🔹 Проверяет подписку на вашу группу или канал, тем самым увеличивая вашу аудиторию!\n"
               "🔹 Общается с пользователями в вашей группе при обращении к боту\n\n"
               f"🔹 В демо-версии доступно <b>{config.tg_bot.request_count} обращений</b> к боту! Если нужно увеличить лимит для тестирования - напишите {config.tg_bot.admin_username}\n\n"
               "<b>Основные команды:</b>\n"
               "🗣️ /gpt - запуск диалога с ChatGpt\n"
               "🎨 /dalle - генерация изображений\n"
               "🗑️ /cancel - Очистить память (контекст) при работе с ChatGPT \n\n"
               "Для демонстрации функционала под ваш бизнес или задачу напишите в личку @chat_bot_for_all"
               " и я обучу бот на ваших данных и покажу его в работе."),
    'gpt_start_dialog': 'Привет! Как я могу помочь вам?',
    'about': 'О боте',
    'response_null': '😔 К сожалению, API ChatGPT платный и вы исчерпали лимит бесплатных обращений.\n\n' 
                    'Если функционал вас заинтересовал и хотите увеличить число обращений к '
                     f'новейшей модели ChatGPT - напишите {config.tg_bot.admin_username}',
    'admin_contact': '🗣️ Связаться с админом',
    'admin': '💻 Админка',
    'admin_menu': '💻 Это главное меню админки',
    'admin_users': '👥 Пользователи',
    'admin_response': '🔢 Осталось запросов',
    'admin_send': '✉️ Рассылка пользователям',
    'admin_analytic': '🤓 Аналитика',
    'admin_send_message': 'Отправь текст для рассылки ⬇️',
    'gpt': '🗣️ GPT',
    'dalle': '🎨 Создать изображение',
    'no_response': '🤷‍♂️ Ответ от OpenAI не получен. Сервера перегружены\nПовторите попытку ️⬇️',
    'subscribe_channel': f'Чтобы пользовать ChatGPT, нужно быть подписчиком моей группы ⬇️\n\n {config.tg_bot.group_link}',
    'create_image_cancel': 'Вы можете продолжить создавать изображения, введя текст ниже ⬇️\n',
    'create_image': 'Введите текстовое описание желаемого изображения ⬇️',
    'yes': '✅ Да',
    'no': '❌ Нет',
    'repeat_voice_message': 'Повторите ваш запрос ⬇️',
    'translate_complete': '✅ Текст извлечен из аудио\n\nChatGPT делает краткий пересказ...\n\n'
                          '⌛ Это объемная задача, ожидание может занять 30-80 сек.',
    'translate_audio': '🎵 Отправь аудио на иностранном языке.\n\nChatGPT переведет его и сделает краткий пересказ\n\n'
                         '⚠️ Размер файла не должен превышать 20Мб!'
    #'translate_mistake': '‼️ Произошла ошибка:\n\n {er}! \n\nВы можете повторите запрос ⏬'
}

LEXICON_COMMANDS_RU: dict[str, str] = {'/start': '🤖 Запуск бота', '/gpt': '🗣️ ChatGPT', '/dalle': '🎨 Dalle',
                                       '/pereskaz': '📚 Пересказ по аудио', '/cancel': '🗑️ Очистить контекст'}
