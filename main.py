import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')


# Создаем или подключаемся к базе данных
conn = sqlite3.connect('movie_ratings.db', check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу для хранения оценок, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS ratings (
    user_id INTEGER,
    movie_id TEXT,
    rating INTEGER,
    PRIMARY KEY (user_id, movie_id)
)
''')
conn.commit()


current_movie_id = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Начать', callback_data='menu'))
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Просмотреть сетку', callback_data='view_grid'))
    markup.add(types.InlineKeyboardButton('Показать все оценки', callback_data='show_ratings'))
    bot.send_message(call.message.chat.id, 'Выбор за вами', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'view_grid')
def view_grid(call):
    markup = types.InlineKeyboardMarkup()
    action = types.InlineKeyboardButton('Боевик', callback_data='action_movies')
    horror = types.InlineKeyboardButton('Хорор', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    trailer = types.InlineKeyboardButton('Триллер', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    romantic = types.InlineKeyboardButton('Романтика', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    adventure = types.InlineKeyboardButton('Приключения', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    tragedy = types.InlineKeyboardButton('Трагедия', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    music = types.InlineKeyboardButton('Мюзикл', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    detective = types.InlineKeyboardButton('Детектив', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    comedic = types.InlineKeyboardButton('Комедия', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUIcmlja3JvbGw%3D')
    markup.row(action, horror, trailer)
    markup.row(romantic, adventure, tragedy)
    markup.row(music, detective, comedic)
    bot.send_message(call.message.chat.id, 'Вот ваша сетка!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'action_movies')
def action_movies(call):
    markup = types.InlineKeyboardMarkup()
    movie1 = types.InlineKeyboardButton('Гнев человеческий', callback_data='movie1')
    movie2 = types.InlineKeyboardButton('Дом у дороги', callback_data='movie2')
    movie3 = types.InlineKeyboardButton('Никто', callback_data='movie3')
    markup.row(movie1, movie2, movie3)
    bot.send_message(call.message.chat.id, 'Выберите фильм:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['movie1', 'movie2', 'movie3'])
def send_movie_poster(call):
    global current_movie_id
    current_movie_id = int(call.data[-1])

    movie_posters = {
        'movie1': 'https://upload.wikimedia.org/wikipedia/ru/5/55/%D0%93%D0%BD%D0%B5%D0%B2_%D1%87%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%28%D0%BF%D0%BE%D1%81%D1%82%D0%B5%D1%80%29.png',
        'movie2': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmBFKc1iNdtZFQXGtAUBZMcPDC35jTeIBMyg&s',
        'movie3': 'https://upload.wikimedia.org/wikipedia/ru/3/3a/%D0%9F%D0%BE%D1%81%D1%82%D0%B5%D1%80_%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%B0_%C2%AB%D0%9D%D0%B8%D0%BA%D1%82%D0%BE%C2%BB.jpg'
    }
    movie_info = {
        'movie1': 'Гнев человеческий, неплохой фильм говорят. Оцените пж',
        'movie2': 'Дом у дороги, тоже ничего. Оцените пж',
        'movie3': 'Никто, тут точно не знаю. Оцените пж',
    }
    poster_url = movie_posters.get(call.data)
    info = movie_info.get(call.data)

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('1', callback_data=f'rating_{call.data}_1')
    btn2 = types.InlineKeyboardButton('2', callback_data=f'rating_{call.data}_2')
    btn3 = types.InlineKeyboardButton('3', callback_data=f'rating_{call.data}_3')
    btn4 = types.InlineKeyboardButton('4', callback_data=f'rating_{call.data}_4')
    btn5 = types.InlineKeyboardButton('5', callback_data=f'rating_{call.data}_5')
    markup.row(btn1, btn2, btn3, btn4, btn5)

    if poster_url:
        bot.send_photo(call.message.chat.id, poster_url, caption=info, reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, 'Ошибка: фильм не найден.')


@bot.callback_query_handler(func=lambda call: call.data.startswith('rating_'))
def rating(call):
    global current_movie_id

    _, movie_id, user_rating = call.data.split('_')
    user_id = call.from_user.id

    # Проверяем, оценил ли пользователь уже этот фильм
    cursor.execute('SELECT rating FROM ratings WHERE user_id = ? AND movie_id = ?', (user_id, movie_id))
    existing_rating = cursor.fetchone()

    menu_markup = types.InlineKeyboardMarkup()
    menu = types.InlineKeyboardButton('Меню', callback_data='menu')
    next_movie = types.InlineKeyboardButton('Смотреть дальше', callback_data='movie' + str((current_movie_id % 3) + 1))
    menu_markup.add(menu, next_movie)

    if existing_rating:
        bot.send_message(call.message.chat.id, f'Вы уже оценили фильм на {existing_rating[0]}!', reply_markup=menu_markup)
    else:
        # Сохраняем оценку в базе данных
        cursor.execute('''
                INSERT INTO ratings (user_id, movie_id, rating)
                VALUES (?, ?, ?)
                ''', (user_id, movie_id, int(user_rating)))
        conn.commit()

        bot.send_message(call.message.chat.id, f'Спасибо за вашу оценку {user_rating} для фильма с ID {movie_id}!', reply_markup=menu_markup)


@bot.callback_query_handler(func=lambda call: call.data == 'show_ratings')
def show_ratings(call):
    global current_movie_id

    # Выполнение запроса для получения всех оценок
    cursor.execute("SELECT user_id, movie_id, rating FROM ratings")
    ratings = cursor.fetchall()

    menu_markup = types.InlineKeyboardMarkup()
    menu = types.InlineKeyboardButton('Меню', callback_data='menu')
    next_movie = types.InlineKeyboardButton('Смотреть дальше', callback_data='movie' + str((current_movie_id % 3) + 1))
    menu_markup.add(menu, next_movie)

    # Формирование сообщения
    if ratings:
        response = "Оценки пользователей:\n"
        for user_id, movie_id, rating in ratings:
            response += f"Пользователь: {user_id}, Фильм: {movie_id}, Оценка: {rating}\n"
    else:
        response = "Нет оценок в базе данных."

    # Отправка результата пользователю
    bot.send_message(call.message.chat.id, response, reply_markup=menu_markup)


bot.polling(none_stop=True)

# Закрываем соединение с базой данных при завершении программы
conn.close()
