#encoding = utf-8
import unittest
import requests
import json
import HTMLTestRunner
import random
import os
import re
from gloryRoadApi.common.util import md5Hash
from gloryRoadApi.common.log import logger

reportPath = 'D:\\flask\\apiServerGloryRoad0607\\gloryRoadApi\\report\\report.html'

class TestApiServer(unittest.TestCase):

    # 所有用例前执行一次
    @classmethod
    def setUpClass(cls):
        cls.host = "http://39.106.41.11:8080"
        cls.api_client = requests.Session()

    @classmethod
    def tearDownClass(cls):
        pass


    def register_user(self, username, password, email):
        url = "%s/register/" % self.host
        logger.info("register_user->url: %s" % url)

        data = {"username": username, "password": password, "email": email}
        requestData = json.dumps(data)
        logger.info("requestData of register: %s" % requestData)
        resp = self.api_client.post(url, data = requestData)
        logger.info("resp of register: %s" % resp.json())
        return resp

    def login_user(self, username, password):
        url = "%s/login/" % self.host
        data = json.dumps({"username": username, "password": password})
        logger.info("request data of login_user: %s" % data)
        return self.api_client.post(url, data = data)

    def create_blog(self, userid, token, title, content):
        #{"userid": "2", "token": "4282a87824884246aa0d8ef6974bbbf5", "title":"dddddd", "content":"HttpRunner is a api test interface"}
        url = "%s/create/" % self.host
        data = json.dumps({"userid": userid, "token": token, "title": title, "content": content})
        logger.info("request data of create_blog: %s" % data)
        return self.api_client.post(url, data = data)

    def get_blog_content(self,articleId):
        url = "%s/getBlogContent/%s"% (self.host, articleId)
        return self.api_client.get(url)

    def get_blogs_content(self,articleIds):
        # 'articleIds=' 后边传'1,2'这样的值
        url = "%s/getBlogsContent/articleIds=%s" % (self.host, articleIds)
        logger.info("url of get_blogs_content: %s" % url)
        return self.api_client.get(url)

    def get_blogs_of_user(self, userid, token):
        #{"userid":"4", "token": "2d406f40e9544b45a162289af15145b4","offset": "1", "lines": "1"}
        url = "%s/getBlogsOfUser/" % (self.host)
        data = json.dumps({"userid":userid, "token": token})
        logger.info("request data of get_blogs_of_user: %s" % data)
        return self.api_client.post(url = url, data = data)

    def update_blog(self, userid, token, articleId, title, content):
        url = "%s/update/" % (self.host)
        data = json.dumps({"userid": userid, "token": token, "articleId":articleId, "title": title, "content": content})
        logger.info("request data of update_blog: %s" % data)
        return self.api_client.put(url, data = data)

    def delete_blog(self, userid, token, articleIdList):
        #{"userid":1, "token": "2d406f40e9544b45a162289af15145b4", "articleId":[1]}
        url = "%s/delete/" % (self.host)
        logger.info("url for delete: %s" % url)
        logger.info("articleIdList: %s" % articleIdList)
        data = json.dumps({"userid": userid, "token": token, "articleId": articleIdList})
        logger.info("request data of delete_blog: %s" % data)
        return self.api_client.post(url, data = data)

    # 测试注册新用户
    def test_register_user_not_existed(self):
        logger.info("############test_register_user_not_existed############")
        # 先注册，记录username和password（md5)
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister")
        # 若已经存在，重试1次
        for i in range(2):
            logger.info("try times: %s" % int(i + 1))
            try:
                username = 'wulao%s' % random.randrange(1000)
                logger.info("username: %s" % username)
                resp = self.register_user(username, passwordToRegister, 'wulao@qq.com')
                logger.info("resp of test_register_user_not_existed: %s" % resp.json())
                self.assertEqual(200, resp.status_code)
                self.assertEqual("00", resp.json()['code'])
                break
            except Exception as e:
                logger.info("error in test_register_user_not_existed: %s" % e)


    # 测试注册已经存在的用户
    def test_register_user_existed(self):
        logger.info("############test_register_user_existed############")
        username = 'wulao%s' % random.randrange(100)
        resp = self.register_user(username, 'wulaoshi2019', 'wulao@qq.com')
        resp = self.register_user(username, 'wulaoshi2019', 'wulao@qq.com')
        logger.info("resp of test_register_user_existed: %s" % resp.json())
        self.assertEqual(200, resp.status_code)
        self.assertEqual("01", resp.json()['code'])

    # 测试登录不存在的用户
    def test_login_user_not_existed(self):
        logger.info("############test_login_user_not_existed############")
        username = 'wulao%s' % random.randrange(1000)
        passwordToLogin = md5Hash("wulaoshi2019")

        # 登录用户
        resp = self.login_user(username,passwordToLogin)
        logger.info("resp of test_login_user_not_existed: %s" % resp.json())
        self.assertEqual(200, resp.status_code)
        # 登录的用户不存在，返回"03": 参数错误
        self.assertEqual("03", resp.json()['code'])

    # 测试登录用户
    def test_login_user_existed(self):
        logger.info("############test_create_blog############")
        username = 'wulao%s' % random.randrange(100)
        passwordToRegister = "wulaoshi2019"

        # 注册新用户
        resp = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        passwordToLogin = md5Hash(passwordToRegister)
        logger.info("username: %s" % username)
        logger.info("passwordToLogin: %s" % passwordToLogin)

        # 登录用户
        resp = self.login_user(username, passwordToLogin)
        logger.info("resp of test_login_user_existed: %s" % resp.json())
        self.assertEqual(200, resp.status_code)
        self.assertEqual("00", resp.json()['code'])

    # 测试创建博文
    def test_create_blog(self):
        logger.info("############test_create_blog############")
        username = 'wulao%s' % random.randrange(1000)
        logger.info("username: %s" % username)
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister")

        # 注册新用户，记录password(md5)
        respOfRegister = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        logger.info("respOfRegister: %s" % respOfRegister.json())
        passwordToLogin = md5Hash(passwordToRegister)
        logger.info("passwordToLogin: %s" % passwordToLogin)

        # 登录用户，记录userid和token
        respOfLogin = self.login_user(username, passwordToLogin)
        logger.info("respOfLogin: %s" % respOfLogin.json())
        useridOfRegister = respOfLogin.json()['userid']
        logger.info("useridOfRegister: %s" % useridOfRegister)
        tokenOfLogin = respOfLogin.json()['token']
        logger.info("tokenOfLogin: %s" % tokenOfLogin)

        # 创建博文并断言
        respOfCreate = self.create_blog(useridOfRegister, tokenOfLogin, title = "mysql", content = "mysql learn")
        logger.info("resp of test_create_blog: %s" % respOfCreate.json())
        self.assertEqual(200, respOfCreate.status_code)
        self.assertEqual("00", respOfCreate.json()['code'])

    # 测试查询用户的博文
    def test_get_blogs_of_user(self):
        logger.info("############test_get_blogs_of_user############")
        # 先注册，记录username和password（md5)
        username = 'wulao%s' % random.randrange(1000)
        logger.info("username: %s" % username)
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister: %s" % passwordToRegister)
        respOfRegister = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        logger.info("respOfRegister: %s" % respOfRegister.json())

        # 记录password的md5加密串
        passwordOfUser = md5Hash(passwordToRegister)
        logger.info("passwordToLogin: %s" % passwordOfUser)

        # 然后登录，获取token和userid
        respOfLogin = self.login_user(username, passwordOfUser)
        logger.info("respOfLogin: %s" % respOfLogin.json())
        # 获取登录返回的userid
        useridOfUser = respOfLogin.json()['userid']
        logger.info("useridOfUser: %s" % useridOfUser)
        # 获取登录返回token
        tokenOfUser = respOfLogin.json()['token']
        logger.info("tokenOfUser: %s" % tokenOfUser)

        # 创建博文
        respOfCreate = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog: %s" % respOfCreate.json())

        # 查询用户博文，需要参数：userid、token
        respOfGetBlogsOfUser = self.get_blogs_of_user(useridOfUser, tokenOfUser)
        logger.info("respOfGetBlogsOfUser: %s" % respOfGetBlogsOfUser.json())
        self.assertEqual(200, respOfGetBlogsOfUser.status_code)
        self.assertEqual("00", respOfGetBlogsOfUser.json()['code'])


    # 测试更新用户博文
    def test_update_blog(self):
        logger.info("############test_update_blog############")
        # 先注册用户
        username = 'wulao%s' % random.randrange(1000)
        logger.info("username: %s" % username)
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister: %s" % passwordToRegister)
        respOfRegister = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        logger.info("respOfRegister: %s" % respOfRegister.json())

        # 记录password的md5加密串
        passwordOfUser = md5Hash(passwordToRegister)
        logger.info("passwordToLogin: %s" % passwordOfUser)

        # 然后登录，获取token和userid
        respOfLogin = self.login_user(username, passwordOfUser)
        logger.info("respOfLogin: %s" % respOfLogin.json())
        # 获取登录返回的userid
        useridOfUser = respOfLogin.json()['userid']
        logger.info("useridOfUser: %s" % useridOfUser)
        # 获取登录返回token
        tokenOfUser = respOfLogin.json()['token']
        logger.info("tokenOfUser: %s" % tokenOfUser)

        # 创建博文
        respOfCreate = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog: %s" % respOfCreate.json())
        # 查询用户博文，获取articleId，，需要参数：userid、token
        respOfGetBlogsOfUser = self.get_blogs_of_user(useridOfUser, tokenOfUser)
        logger.info("respOfGetBlogsOfUser: %s" % respOfGetBlogsOfUser.json())
        articleId = respOfGetBlogsOfUser.json()['data'][0]['articleId']
        logger.info("articleId: %s" % articleId)

        # 更新博文
        # update接口参数：userid，token，articleid, title, content
        respOfUpdate = self.update_blog(useridOfUser,tokenOfUser, articleId, "update title", "update blog content")
        logger.info("resp of update_blog: %s" % respOfUpdate)
        self.assertEqual(200, respOfUpdate.status_code)
        self.assertEqual("00", respOfUpdate.json()['code'])

    # 测试查询博文内容
    def test_get_blog_content(self):
        logger.info("############test_get_blog_content############")
        # 先注册用户
        username = 'wulao%s' % random.randrange(1000)
        logger.info("username: %s" % username)
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister: %s" % passwordToRegister)
        respOfRegister = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        logger.info("respOfRegister: %s" % respOfRegister.json())

        # 记录password的md5加密串
        passwordOfUser = md5Hash(passwordToRegister)
        logger.info("passwordToLogin: %s" % passwordOfUser)

        # 然后登录，获取token和userid
        respOfLogin = self.login_user(username, passwordOfUser)
        logger.info("respOfLogin: %s" % respOfLogin.json())
        # 获取登录返回的userid
        useridOfUser = respOfLogin.json()['userid']
        logger.info("useridOfUser: %s" % useridOfUser)
        # 获取登录返回token
        tokenOfUser = respOfLogin.json()['token']
        logger.info("tokenOfUser: %s" % tokenOfUser)

        # 创建博文
        respOfCreate = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog: %s" % respOfCreate.json())

        # 查询用户博文，获取articleId，需要参数：userid、token
        respOfGetBlogsOfUser = self.get_blogs_of_user(useridOfUser, tokenOfUser)
        logger.info("respOfGetBlogsOfUser: %s" % respOfGetBlogsOfUser.json())
        articleId = respOfGetBlogsOfUser.json()['data'][0]['articleId']
        logger.info("articleId: %s" % articleId)

        # 查询博文内容参数：articleId
        respOfGetBlogContent = self.get_blog_content(articleId)
        logger.info("respOfGetBlogContent: %s" % respOfGetBlogContent)
        self.assertEqual(200, respOfGetBlogContent.status_code)
        self.assertEqual("00", respOfGetBlogContent.json()['code'])


    # 测试批量查询博文
    def test_get_blogs_content(self):
        logger.info("############test_get_blog_content############")

        # 先注册用户
        username = 'wulao%s' % random.randrange(1000)
        logger.info("username: %s" % username)
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister: %s" % passwordToRegister)
        respOfRegister = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        logger.info("respOfRegister: %s" % respOfRegister.json())

        # 记录password的md5加密串
        passwordOfUser = md5Hash(passwordToRegister)
        logger.info("passwordToLogin: %s" % passwordOfUser)

        # 然后登录，获取token和userid
        respOfLogin = self.login_user(username, passwordOfUser)
        logger.info("respOfLogin: %s" % respOfLogin.json())
        # 获取登录返回的userid
        useridOfUser = respOfLogin.json()['userid']
        logger.info("useridOfUser: %s" % useridOfUser)
        # 获取登录返回token
        tokenOfUser = respOfLogin.json()['token']
        logger.info("tokenOfUser: %s" % tokenOfUser)

        # 创建第一个博文
        respOfCreate1 = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog1: %s" % respOfCreate1.json())
        # 再创第二个博文
        respOfCreate2 = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog2: %s" % respOfCreate2.json())
        # 再创第三个博文
        respOfCreate3 = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog3: %s" % respOfCreate3.json())

        # 查询用户博文，获取articleIds，需要参数：userid、token
        respOfGetBlogsOfUser = self.get_blogs_of_user(useridOfUser, tokenOfUser)
        logger.info("respOfGetBlogsOfUser: %s" % respOfGetBlogsOfUser.json())
        logger.info("respOfGetBlogsOfUser.text: %s" % respOfGetBlogsOfUser.text)

        # 正则表达式获取响应结果中所有的articleId，拼成字符串，如"1,2,3"
        reFindArticleIdsRes = re.findall(r'"articleId": (\d+)', respOfGetBlogsOfUser.text)
        logger.info("reFindArticleIdsRes: %s" % reFindArticleIdsRes)
        articleIdsRes = ",".join(reFindArticleIdsRes)
        logger.info("articleIdsRes: %s" % articleIdsRes)

        # 批量查询博文内容
        respOfGetBlogsContent = self.get_blogs_content(articleIdsRes)
        logger.info("respOfGetBlogsContent: %s" %respOfGetBlogsContent.json())
        self.assertEqual(200, respOfGetBlogsContent.status_code)
        self.assertEqual("00", respOfGetBlogsContent.json()['code'])


    # 测试删除博文接口
    def test_delete_blogs(self):
        logger.info("############test_delete_blogs############")
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister")
        # 先注册用户
        username = 'wulao%s' % random.randrange(1000)
        logger.info("username: %s" % username)
        passwordToRegister = "wulaoshi2019"
        logger.info("passwordToRegister: %s" % passwordToRegister)
        respOfRegister = self.register_user(username, passwordToRegister, 'wulao@qq.com')
        logger.info("respOfRegister: %s" % respOfRegister.json())

        # 记录password的md5加密串
        passwordOfUser = md5Hash(passwordToRegister)
        logger.info("passwordToLogin: %s" % passwordOfUser)

        # 然后登录，获取token和userid
        respOfLogin = self.login_user(username, passwordOfUser)
        logger.info("respOfLogin: %s" % respOfLogin.json())
        # 获取登录返回的userid
        useridOfUser = respOfLogin.json()['userid']
        logger.info("useridOfUser: %s" % useridOfUser)
        # 获取登录返回token
        tokenOfUser = respOfLogin.json()['token']
        logger.info("tokenOfUser: %s" % tokenOfUser)

        # 创建第一个博文
        respOfCreate1 = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog1: %s" % respOfCreate1.json())
        # 再创第二个博文
        respOfCreate2 = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog2: %s" % respOfCreate2.json())
        # 再创第三个博文
        respOfCreate3 = self.create_blog(useridOfUser, tokenOfUser, title="mysql", content="mysql learn")
        logger.info("resp of create_blog3: %s" % respOfCreate3.json())

        # 查询用户博文，获取articleIds，需要参数：userid、token
        respOfGetBlogsOfUser = self.get_blogs_of_user(useridOfUser, tokenOfUser)
        logger.info("respOfGetBlogsOfUser: %s" % respOfGetBlogsOfUser.json())
        logger.info("respOfGetBlogsOfUser.text: %s" % respOfGetBlogsOfUser.text)

        # 正则表达式获取响应结果中所有的articleId，拼成字符串，如"1,2,3"
        reFindArticleIdsRes = re.findall(r'"articleId": (\d+)', respOfGetBlogsOfUser.text)
        logger.info("reFindArticleIdsRes: %s" % reFindArticleIdsRes)
        articleIdsListStr = [int(articleId) for articleId in reFindArticleIdsRes]


        # 删除博文
        respOfDeleteBlogs = self.delete_blog(useridOfUser, tokenOfUser, articleIdsListStr)
        logger.info("respOfDeleteBlogs: %s" % respOfDeleteBlogs.json())
        self.assertEqual(200, respOfDeleteBlogs.status_code)
        self.assertEqual("00", respOfDeleteBlogs.json()['code'])


if __name__ == '__main__':
    # 根据给定的测试类，获取其中的所有以“test”开头的测试方法，并返回一个测试套件
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestApiServer)
    # 将测试类加载到测试套件中
    suite = unittest.TestSuite([suite1])
    # 以二进制方式打开文件，准备写
    fp = open(reportPath, 'wb')
    # 使用HTMLTestRunner配置参数，输出报告路径、报告标题、描述，均可以配
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Unittest Report', description='Report Description')
    # 运行测试集合
    runner.run(suite)




