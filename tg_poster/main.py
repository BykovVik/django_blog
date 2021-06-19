import config as conf
import requests
import time


def get_new_posts(post_api_url, over_time, tg_url, chanel_id, post_id):

    #создаём точку отсчета
    start = time.monotonic()

    while True:

        #вычиляем необходимое время для завершения работы таймера
        if time.monotonic() - start > over_time:

            response = requests.get(post_api_url)
            res = response.json()
            res_id = res[0]['id']

            if res_id == post_id:

                continue

            else:

                publish_from_tg_chanel(chanel_id, tg_url)
                continue

def publish_from_tg_chanel(chanel_id, tg_url):

    params = {'chat_id': chanel_id, 'text': "Хобаааааааа"}
    response = requests.get(tg_url + 'sendMessage', data=params)

if __name__ == "__main__":

    get_new_posts(
        conf.URL_POST_API,
        conf.OVER_TIME,
        conf.URL_TG_API,
        conf.CHANEL_ID,
        conf.POST_ID
    )