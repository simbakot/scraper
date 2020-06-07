import re
import datetime
from time import sleep

import vk_api.exceptions

from src.resource import VK
from src.database import Database
from src.controller import Controller
from config_parser import Config


config = Config('configs.yaml')

vk = VK(config.vk)
database = Database(config.database)
controller = Controller(config.controller)


def get_data(file_path):
    with open(file_path) as f:
        rows = f.readlines()
        for row in rows:
            yield row.strip()

def handle_date(unixtime):
    value = datetime.datetime.fromtimestamp(unixtime)
    date = value.strftime('%Y-%m-%d %H:%M:%S')
    return date

group_urls_path = 'data/vk/group_short_url.txt'

while True:
    for url in get_data(group_urls_path):
        print(url)
        try:
            users = controller.get_target_user(resource=vk, group_id=url)
            for user in users:

                user['BirthDate'] = handle_date(user['BirthDate'])

                controller.save_data_to_bd(bd=database, table='SocialNetworkUser', target_object=user)

                posts = controller.get_target_post(resource=vk, user_id=user['OuterId'])
                for post in posts:

                    post['Text'] = ' '.join(list(filter(None, re.split('\W|\d', post['Text']))))
                    post['PublishDateTime'] = handle_date(post['PublishDateTime'])

                    controller.save_data_to_bd(bd=database, table='WallPost', target_object=post)

                    comments = controller.get_target_comments(resource=vk, user_id=user['OuterId'], post_id=post['OuterId'])
                    for comment in comments:

                        comment['Text'] = ' '.join(list(filter(None, re.split('\W|\d', comment['Text']))))
                        comment['PublishDateTime'] = handle_date(comment['PublishDateTime'])

                        controller.save_data_to_bd(bd=database, table='Comment', target_object=comment)

        except vk_api.exceptions.VkToolsException as e:
            print(e)
        except Exception as e:
            print(e)


    print('End pars group_urls_path')
    sleep(60*60)