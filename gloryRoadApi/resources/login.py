#encoding=utf-8
from gloryRoadApi.application import db
from gloryRoadApi.models import User
from flask_restful import reqparse
from flask import request
from flask_restful import Resource
import time
from gloryRoadApi.common import util
from gloryRoadApi.common.log import logger


# login接口
class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, help='用户名验证错误', location = 'json')
        # location = 'json'表示请求的参数是json格式的
        self.reqparse.add_argument('password', type=str, help='密码验证错误',location = 'json')
        self.args = self.reqparse.parse_args()

    # login接口处理post请求和参数验证
    def post(self):
        try:
            logger.info("########################[Login]########################")
            logger.info("args.keys(): %s" % self.args.keys())
            json_data = request.get_json(force=True)
            logger.info("json_data: %s" % json_data)
            userName = json_data['username'] if ('username' in json_data.keys()) else ""
            logger.info("username: %s" % userName)
            userPassword = json_data['password'] if ('password' in json_data.keys()) else ""
            logger.info("userPassword: %s" % userPassword)
            neededParams = self.args.keys()  # 记录self.reqparse.add_argument中添加的参数列表
            logger.info("neededParams: %s" % neededParams)
            requestParams = request.json.keys()  # 记录发送请求中携带的参数列表
            logger.info("requestParams: %s " % requestParams)

            # 判断参数是否都有传过来，都传过来了，并且没有多传或少传，继续做参数值的校验，否则返回“参数错误”
            if userName and userPassword  and util.paramsNumResult(neededParams, requestParams):
                #到表里查询，是否存在这个用户，如果存在则校验密码
                userToLogin = User.query.filter(User.username == userName).first()
                logger.info("userToLogin: %s" % userToLogin)

                #判断用户是否存在db中
                if userToLogin: #如果数据库中有这个user，则校验密码是否正确
                    passwordResult = util.validateMd5Password(userPassword, userName)  # 验证发过来的密码是否和用户存在db里的密码加密后相等
                    if passwordResult: # 如果密码正确，处理token和loginTime
                        #先把用户的token取出来
                        userTokenInDB = userToLogin.token
                        logger.info("userTokenInDB: %s" %userTokenInDB)
                        #userToken = generateUUID() if not userTokenInDB else generateUUID() #这样更简洁一些
                        # 登录的时候，把数据库里的loginTime和token都做更新
                        userToken = util.generateUUID()
                        userToLogin.token = userToken
                        timeStr = time.strftime("%Y-%m-%d %H:%M:%S")
                        userToLogin.loginTime = timeStr
                        db.session.commit()
                        return {"token": "%s" % userToken, "code": "00", "userid": int(userToLogin.id), "login_time": "%s" %timeStr}
                    else: #密码不正确
                        return {"code": "02", "message": u"参数值不合法，密码不正确"}
                else:
                    # 数据库中没有这个user
                    return {"code": "02", "message": u"参数值不合法，用户不存在"}

            else:
                return {"code": "03","message": u"参数错误，可能原因：参数少传了、多传了、写错了、参数值为空"}

        except Exception as e:
            logger.error("error of login: %s" % e)
            return {"code": "999","message": u"未知错误"}
