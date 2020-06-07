import re
from datetime import datetime

import mysql.connector


class Database:

    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.database = config['database']
        self.user = config['user']
        self.password = config['password']


    def get_db_conn(self):

        conn = mysql.connector.connect(host=self.host,
                                       port=self.port,
                                       database=self.database,
                                       user=self.user,
                                       password=self.password)
        return conn


    def save(self, table, target_object):
        if table == 'SocialNetworkUser':
            self.add_users(target_object)
        elif table == 'WallPost':
            self.add_post(target_object)
        elif table == 'Comment':
            self.add_comment(target_object)
        else:
            print('Table %s does not exist' % table)


    def add_users(self, users_object):
        print("user", users_object)
        if users_object['BirthDate'] == "":
            users_object['BirthDate'] = datetime.strptime('Jun 1 1990  1:33PM', '%b %d %Y %I:%M%p')


        add_SocialNetworkUser = ("INSERT INTO SocialNetworkUser"
                                 
                                 "(SocialNetworkId, OuterId, NameAlias, FirstName, LastName, BirthDate, \
                                 City, FriendsQuantity) "
                                 
                                 "VALUES (%(SocialNetworkId)s, %(OuterId)s, %(NameAlias)s, %(FirstName)s, \
                                 %(LastName)s, %(BirthDate)s, %(City)s, %(FriendsQuantity)s)")

        self.execute(add_SocialNetworkUser, users_object)



    def add_post(self, post_object):
        print('post', post_object)
        if post_object['PublishDateTime'] == '':
            post_object['PublishDateTime'] = datetime.strptime('Jun 1 1990  1:33PM', '%b %d %Y %I:%M%p')

        post_object['Text'] = ' '.join(list(filter(None, re.split('\W|\d', post_object['Text']))))


        add_WallPost = ("INSERT INTO WallPost"
                        
                        "(OuterId, PublishDateTime, Text, WallOwnerOuterId, \
                        LikesQuantity, RepostQuantity, CommentQuantity, ViewsQuantity) "
                        
                        "VALUES (%(OuterId)s, %(PublishDateTime)s, %(Text)s, %(WallOwnerOuterId)s, \
                                 %(LikesQuantity)s, %(RepostQuantity)s, %(CommentQuantity)s, %(ViewsQuantity)s)")

        self.execute(add_WallPost, post_object)


    def add_comment(self, comit_obgect):
        print("comment", comit_obgect)
        if comit_obgect['PublishDateTime'] == '':
            comit_obgect['PublishDateTime'] = datetime.strptime('Jun 1 1990  1:33PM', '%b %d %Y %I:%M%p')

        comit_obgect['Text'] = ' '.join(list(filter(None, re.split('\W|\d', comit_obgect['Text']))))


        add_WallPost = ("INSERT INTO Comment"
                        
                        "(OuterId, LikesQuantity, WallPostId, Text, \
                        PublishDateTime, OuterAuthorId, CommentsQuantity) "
                        
                        "VALUES (%(OuterId)s, %(LikesQuantity)s, %(WallPostId)s, %(Text)s, \
                                 %(PublishDateTime)s, %(OuterAuthorId)s, %(CommentsQuantity)s)")

        self.execute(add_WallPost, comit_obgect)


    def execute(self, sql, added_object):
        cnx = self.get_db_conn()
        cursor = cnx.cursor()
        cursor.execute(sql, added_object)
        cnx.commit()

        cursor.close()
        cnx.close()


