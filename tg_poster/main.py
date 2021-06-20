import config as conf
import requests
import time

def get_new_posts(post_api_url, over_time, tg_url, chanel_id, base_dir):

    response = requests.get(post_api_url)
    res = response.json()
    res_id = res[0]['id']

    if res_id == conf.POST_ID:
        print("Сравнялись")
        return
                
    else:

        conf.POST_ID = res_id

        slug = base_dir + "/" + res[0]['post_slug']

        message = "Ссылка на ресурс: {}".format(slug)

        publish_from_tg_chanel(chanel_id, tg_url, message)
                

def publish_from_tg_chanel(chanel_id, tg_url, message):
    
    params = {'chat_id': chanel_id, 'text': message}
    response = requests.get(tg_url + 'sendMessage', data=params)

    return

if __name__ == "__main__":

    while True:

        time.sleep(5)

        get_new_posts(
            conf.URL_POST_API,
            conf.OVER_TIME,
            conf.URL_TG_API,
            conf.CHANEL_ID,
            conf.BASE_DIR
        )