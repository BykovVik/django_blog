"""

    Conf file from TG PUBLISHER

"""
URL_POST_API = "http://161.97.136.242:8000/api/posts" #API моего сайта
TOKEN = "1697782059:AAFjljUF5wWwzHQdF-P7r4LtXJckmeo1u0w" #TOKEN для TG бота
URL_TG_API = "https://api.telegram.org/bot{}/".format(TOKEN) #Рабочий link для запросов к TG API
OVER_TIME = 5 #Время в секундах
CHANEL_ID = '-1001326226066' #ID канала в который будем публиковать посты
POST_ID = 0 #Здесь мы будем запоминать ID последнего поста который опубликовал бот
BASE_DIR = URL_POST_API.split('/api')[0]

