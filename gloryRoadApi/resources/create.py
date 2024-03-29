#encoding=utf-8
from gloryRoadApi.application import db
from gloryRoadApi.models import User, UserBlog
# from gloryRoadApi.commands import forge,initdb
from flask_restful import Resource, Api
import time
from flask_restful import reqparse
from flask_restful import request
from flask_restful import fields, marshal_with
from gloryRoadApi.common import util
from gloryRoadApi.common.log import logger

# 处理新增博文接口
class Create(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('userid', type = int, help =u"userid输入错误", location = 'json' )
        self.reqparse.add_argument('token', type = str, help= u"token校验错误", location = 'json')
        self.reqparse.add_argument('title', type = str, help = u"标题校验错误", location = 'json')
        self.reqparse.add_argument('content', type = str, help = u"内容校验错误", location = 'json')
        self.args = self.reqparse.parse_args()

    #处理新增博文post请求
    def post(self):
        try:
            logger.info("########################[Create]########################")
            logger.info("self.args.keys(): %s" % self.args.keys())
            json_data = request.get_json(force=True)
            userid = json_data['userid'] if ('userid' in json_data.keys()) else ""
            logger.info("userid: %s" % userid)
            userToken = json_data['token'] if ('token' in json_data.keys()) else ""
            logger.info("userToken: %s" % userToken)
            blogTitle = json_data['title'] if ('title' in json_data.keys()) else ""
            logger.info("blogTitle: %s" % blogTitle)
            blogContent = json_data['content'] if ('content' in json_data.keys()) else ""
            logger.info("blogContent: %s" % blogContent)
            neededParams = self.args.keys()  # 记录self.reqparse.add_argument中添加的参数列表
            logger.info("neededParams: %s" % neededParams)
            requestParams = request.json.keys()  # 记录发送请求中携带的参数列表
            logger.info("requestParams: %s" % requestParams)
            requestTimestamp = time.time()


            #校验是否参数都有传过来，不多不少
            if userid and userToken and blogTitle and blogContent and util.paramsNumResult(neededParams, requestParams):
                # 用userid查询用户
                getUserInDB = User.query.filter(User.id == userid).first()
                logger.info("getUserInDB: %s" %getUserInDB)
                # 如果用户存在，判断表中是否有登录时间和token
                if getUserInDB:
                    userLoginTimeInDB = getUserInDB.loginTime #取出用户的登录时间
                    logger.info("userLoginTimeInDB: %s" % userLoginTimeInDB)
                    # 获取用户在DB中的token
                    userTokenInDB = getUserInDB.token
                    logger.info("userTokenInDB: %s" % userTokenInDB)
                    # 判断表中是否有登录时间和token，如果有则继续校验token是否过期
                    if userLoginTimeInDB and userTokenInDB:
                        # 校验登录时间是否超过1小时
                        if util.calculateTimeDiff(userLoginTimeInDB, requestTimestamp) >= 1:
                            return {"code": "02", "message": u"参数值不合法，token已过期，请重新登录"}

                        # 登录时间没超过1小时,继续校验token是否和useid是否相匹配
                        else:
                            # 判断token和userid是否相匹配，如果匹配，则存表并返回
                            if userToken == userTokenInDB:
                                # 先获取到创建博文的时间
                                createBlogTimeString = time.strftime("%Y-%m-%d %H:%M:%S",
                                                                     time.localtime(requestTimestamp))
                                logger.info("createBlogTimeString: %s" % createBlogTimeString)
                                # 存表: blogTitle、blogContent、user_id(User表中的id),createTime
                                blogNew = UserBlog(blogTitle=blogTitle, blogContent=blogContent, user_id=userid,
                                                   createTime=createBlogTimeString)
                                db.session.add(blogNew)
                                db.session.commit()
                                # 返回成功
                                return {"data": [{"content": blogContent, "title": blogTitle}], "code": "00",
                                        "userid": userid, "articleId": blogNew.articleId}
                            # token和userid不匹配，说明token不正确
                            else:
                                return {"code": "02", "message": u"参数值不合法，token不正确"}
                    # 没有登录时间和token，返回参数值不合法，token不正确，请登录并获取token
                    else:
                        return {"code": "02", "message": u"参数值不合法，token不正确，请登录并获取token"}

                # 如果用户不存在
                else:
                    return {"code": "02", "message": u"参数值不合法，用户不存在"}
            else:
                #参数没传全，或参数写错了，或参数多了
                return {"code": "03", "message": u"参数错误，可能原因：参数少传了、多传了、写错了、参数值为空"}

        except Exception as e:
            logger.info("error of create: %s" % e)
            return {"code": "999", "message": u"未知错误"}