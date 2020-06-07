import datetime

class Controller:
    def __init__(self, config):
        self.friends_threshold = config['friends_threshold']
        self.year_threshold = config['year_threshold']

    def handle_date(self, unixtime):
        value = datetime.datetime.fromtimestamp(unixtime)
        date = value.strftime('%Y-%m-%d %H:%M:%S')
        return date

    def save_data_to_bd(self, bd, table, target_object):
        bd.save(table, target_object)

    def get_target_user(self, resource, group_id):

        for user in resource.get_users(id_=group_id):
            user_target_object = {'SocialNetworkId': 1, 'FirstName': '', 'LastName': '', 'BirthDate': '', 'City': '',
                                  'Domain': '', 'FriendsQuantity': 0}

            try:
                if user['is_closed']:
                    continue

                user_id = user['id']
                user_target_object['OuterId'] = user_id

                if user['can_post'] == 1:

                    try:
                        user_target_object['NameAlias'] = user['screen_name']
                    except KeyError:
                        pass
                    try:
                        user_target_object['FirstName'] = user['first_name']
                    except KeyError:
                        pass
                    try:
                        user_target_object['LastName'] = user['last_name']
                    except KeyError:
                        pass
                    try:
                        user_target_object['BirthDate'] = user['bdate']
                    except KeyError:
                        pass
                    try:
                        user_target_object['City'] = user['city']['title']
                    except KeyError:
                        pass

                    try:
                        friends_count = user['followers_count']
                        if friends_count <= self.friends_threshold:
                            continue

                        user_target_object['FriendsQuantity'] = friends_count
                    except KeyError:
                        pass

                    yield user_target_object
            except KeyError:
                continue
            except TypeError as e:
                print('value', e)

    def get_target_post(self, resource, user_id):

        for post in resource.get_user_wall_data(owner_id=user_id):

            target_post_object = {}

            try:
                post_id = post['id']
                post_text = post['text']
                post_author = post['from_id']

                try:
                    date = self.handle_date(post['date'])

                    dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    if dt.year < self.year_threshold:
                        continue

                except KeyError:
                    post['date'] = ''
                try:
                    like_count = post['likes']['count']
                except KeyError:
                    like_count = 0
                try:
                    views_count = post['views']['count']
                except KeyError:
                    views_count = 0
                try:
                    reposts_count = post['reposts']['count']
                except KeyError:
                    reposts_count = 0
                try:
                    comments_count = post['comments']['count']
                    target_post_object['CommentQuantity'] = comments_count
                except KeyError:
                    comments_count = 0

                target_post_object['Text'] = post_text
                target_post_object['OuterId'] = post_id
                target_post_object['WallOwnerOuterId'] = user_id
                target_post_object['OuterAuthorId'] = post_author
                target_post_object['PublishDateTime'] = post['date']
                target_post_object['LikesQuantity'] = like_count
                target_post_object['ViewsQuantity'] = views_count
                target_post_object['RepostQuantity'] = reposts_count
                target_post_object['CommentQuantity'] = comments_count

                yield target_post_object

            except KeyError as e:
                print('User id %s error %s' % (user_id, e))

    def get_target_comments(self, resource, user_id, post_id):
        for comment in resource.get_comments(user_id, post_id):

            target_comment_object = {}

            comment_id = comment['id']
            comment_date = comment['date']
            comment_text = comment['text']
            comment_author = comment['from_id']

            try:
                like_count = comment['likes']['count']
            except KeyError:
                like_count = 0
            try:
                comment_thread_count = comment['thread']['count']
            except KeyError:
                comment_thread_count = 0

            target_comment_object['OuterId'] = comment_author
            target_comment_object['LikesQuantity'] = like_count
            target_comment_object['WallPostId'] = post_id
            target_comment_object['Text'] = comment_text
            target_comment_object['PublishDateTime'] = comment_date
            target_comment_object['OuterAuthorId'] = comment_id
            target_comment_object['CommentsQuantity'] = comment_thread_count

            yield target_comment_object