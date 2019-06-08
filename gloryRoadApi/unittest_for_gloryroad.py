#encoding = utf-8
import unittest
import requests
import json
import random
import os
from gloryRoadApi.common.util import md5Hash
from gloryRoadApi.common.log import logger



class TestApiServer(unittest.TestCase):

    def setUp(self):
        self.host = "http://39.106.41.11:8080"
        self.api_client = requests.Session()


    def tearDown(self):
        super(TestApiServer, self).tearDown()


    def register_user(self, username, password, email):
        url = "%s/register/" % self.host
        data = {"username": username, "password": password, "email": email}
        return self.api_client.post(url, json = data)

    def login_user(self, username, password):
        url = "%s/login/" % self.host
        data = {"username": username, "password": password}
        return self.api_client.post(url, json=data)

    def create_blog(self, userid, token, title, content):
        #{"userid": "2", "token": "4282a87824884246aa0d8ef6974bbbf5", "title":"dddddd", "content":"HttpRunner is a api test interface"}
        url = "%s/create/" % self.host
        data = {"userid": userid, "token": token, "title": title, "content": content}
        return self.api_client.post(url, json=data)

    def get_blog_content(self,articleId):
        url = "%s/getBlogContent/%s"% (self.host, articleId)
        return self.api_client.get(url)

    def get_blogs_content(self,articleIds):
        url = "%s/getBlogsContent/%s" % (self.host, articleIds)
        return self.api_client.get(url)

    def get_blogs_of_user(self, userid, token, offset, lines):
        #{"userid":"4", "token": "2d406f40e9544b45a162289af15145b4","offset": "1", "lines": "1"}
        url = "%s/getBlogsOfUser/" % (self.host)
        data = {"userid":userid, "token": token,"offset": offset, "lines": lines}
        return self.api_client.post(url = url, json = data)

    def update_blog(self, userid, token, articleId, title, content):
        url = "%s/update/" % (self.host)
        data = {"userid":4, "token": token, "articleId":articleId, "title": title, "content": content}
        return self.api_client.post(url, json = data)

    def delete_blog(self, userid, token, articleId):
        #{"userid":1, "token": "2d406f40e9544b45a162289af15145b4", "articleId":[1]}
        url = "%s/delete/" % (self.host)
        data = {"userid": userid, "token": token, "articleId": articleId}
        return self.api_client.delete(url)


    def test_retister_user_not_existed(self):
        username = 'wulao%s' % random.randrange(1000)
        resp = self.register_user(username, 'wulaoshi2019', 'wulao@qq.com')
        logger.info("resp of test_retister_user_not_existed: %s" % resp.json())
        self.assertEqual(200, resp.status_code)
        self.assertEqual("00", resp.json()['code'])

    def test_register_user_existed(self):
        username = 'wulao%s' % random.randrange(100)
        resp = self.register_user(username, 'wulaoshi2019', 'wulao@qq.com')
        resp = self.register_user(username, 'wulaoshi2019', 'wulao@qq.com')
        logger.info("resp of test_register_user_existed: %s" % resp.json())
        self.assertEqual(200, resp.status_code)
        self.assertEqual("01", resp.json()['code'])

    def test_register_user_without_username_password_parameter(self):
        # "03": 参数错误，没传全
        pass

    def test_login_user_not_existed(self):
        logger.info("User.query.all(): %s" % User.query.all())
        username = 'wulao%s' % random.randrange(100)
        passwordToLogin = md5Hash("wulaoshi2019")
        resp = self.login_user(username,passwordToLogin)
        logger.info("resp of test_login_user_not_existed: %s" % resp.json())
        self.assertEqual(200, resp.status_code)
        self.assertEqual("02", resp.json()['code'])

    def test_login_user_existed(self):
        logger.info("User.query.all(): %s" % User.query.all())
        username = 'wulao%s' % random.randrange(100)
        passwordToRegister = "wulaoshi2019"
        # 注册新用户
        resp = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        passwordToLogin = md5Hash(passwordToRegister)
        resp = self.login_user(username, passwordToLogin)
        logger.info("resp of test_login_user_existed: %s" % resp.json())
        self.assertEqual(200, resp.status_code)
        self.assertEqual("00", resp.json()['code'])

    def test_login_user_without_password_parameter(self):
        # "03": 参数错误，没传全
        pass

    def test_create_blog_with_right_token_and_userid_existed(self):
        # "00": 成功
        pass

    def test_create_blog_with_right_token_and_userid_not_existed(self):
        # "02": user不存在
        pass

    def test_create_blog_with_wrong_token_and_userid_existed(self):
        # "02": token不正确
        pass

    def test_create_blog_without_token_parameter(self):
        # "03": 参数错误，没传全
        pass










if __name__ == '__main__':
    unittest.main()

