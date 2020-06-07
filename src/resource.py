import vk_api


class VK:
    def __init__(self, config):

        vk_session = vk_api.VkApi(login=config['login'], password=config['password'], scope=140488159)
        vk_session.auth(token_only=True)
        self.vk = vk_session.get_api()
        self.tools = vk_api.VkTools(vk_session)

    def get_user_wall_data(self, owner_id):
        wall = self.tools.get_all_iter('wall.get', 100, {'owner_id': owner_id, 'extended': 1, 'filter': 'owner'})
        return wall

    def get_comments(self, owner_id, post_id):
        comments = self.tools.get_all_iter('wall.getComments', 100, {'owner_id': owner_id, 'post_id': post_id,
                                                                     'need_likes': 1, 'count': 100, 'extended': 1})
        return comments

    def get_users(self, id_):
        users = self.tools.get_all_iter('groups.getMembers', 100, {'group_id': id_, "fields": ['bdate',
                                                                                               'city',
                                                                                               'can_post',
                                                                                               'screen_name',
                                                                                               'followers_count',
                                                                                               'wall_default'],
                                                                                    'version': '5.107'})
        return users
