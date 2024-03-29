#encoding=utf-8
import time
from gloryRoadApi.models import User
import re
import uuid
from gloryRoadApi.common.log import logger



# 正则验证email
def validateEmail(emailStr):
    p = re.compile(r'^[a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$')
    if p.match(emailStr):
        return True
    else:
        return False

# 正则验证username
def validateUsername(username):

    # if re.compile(u'[\u4e00-\u9fa5]',username):
    #     print "has chinese"
    if re.match(r'\w+', username) and (len(username) in range(2, 21)):
        #print type(username)
        return True
    else:
        return False

# 正则验证email格式
def validatePassword(password):
    if re.search(r'[a-zA-Z]+', password) and re.search(r'[\d+]', password) and (len(password) in range(2, 21)):
        return True
    else:
        return False

# 验证请求中的参数是否有要求之外的，如果有，返回False
def paramsNumResult(neededParams, requestParams):
    for param in requestParams:
        if param not in neededParams:
            logger.info("param not in needed params: %s" % param)
            return False
    return True



# md5加密方法，用于调试
def md5Hash(password):
    """md5 加密分为digest和hexdigest两种格式，前者是二进制，后者是十六进制格式，这里默认为十六进制"""
    try:
        m5 = hashlib.md5()
        m5.update(password.encode(encoding = 'utf-8'))
        pwd = m5.hexdigest()
        return pwd
    except Exception as e:
        logger.info("md5Hash error: %s" % e)

#判断两个字符串用md5加密后是否相等，用于调试
import hashlib

def compareMd5Pwd(str1, str2):
    md51 = hashlib.md5()
    md51.update(str1)
    pwd1 = md51.hexdigest()
    logger.info("pwd1: %s" % pwd1)
    md52 = hashlib.md5()
    md52.update(str2)
    pwd2 = md52.hexdigest()
    logger.info("pwd2: %s" % pwd2)
    return True if (pwd1 == pwd2) else False
    #print "pwd1 = pwd2" if (pwd1 == pwd2) else "pwd1 != pwd2"


# 登录接口发送的密码是md5加密的，需要从数据库里找到这个username对应的password，进行加密后和用户发送的加密串是否一致
def validateMd5Password(passwordFromPost,usernameFromPost):
    try:
        logger.info("passwordFromPost: %s" % passwordFromPost)
        logger.info("usernameFromPost: %s" % usernameFromPost)
        userInDb = User.query.filter(User.username == usernameFromPost).first()
        logger.info("userInDb: %s" %userInDb)
        if userInDb:
            passwordInDb = userInDb.password
            logger.info("passwordInDb: %s" % passwordInDb)
            passwordInDbMd5 = md5Hash(passwordInDb)
            logger.info("passwordInDbMd5: %s" % passwordInDbMd5)
        else:
            passwordInDbMd5 = None
            logger.info("passwordInDbMd5: %s" % passwordInDbMd5)

        if passwordFromPost == passwordInDbMd5:
            return True
        else:
            return False

    except Exception as e:
        logger.info("validateMd5Password Error: %s " %e)


# 验证用户名是否在数据库中存在
def validateUsernameExistInDB(userName):
    try:
        if User.query.filter(User.username == userName).all(): # 查询数据库里是否存在userName
            return True
        else:
            return False
    except Exception as e:
        logger.info("error : %s" % e)

#生成uuid，用uuid模块的uuid4()方法
def generateUUID():
    try:
        uuidStr = uuid.uuid4().hex
        return uuidStr
    except Exception as e:
        logger.info("uuidGenerate Error :%s" %e)


#计算时间差（单位：小时）
#第一个参数传入数据库里用户的登录时间字符串，第二个参数是当前时间戳
def calculateTimeDiff(userLoginTimeStr, timestamp):
    try:
        timestampNew = timestamp
        logger.info("timestampNew : time when post request: %s" % timestampNew)
        timeArray = time.strptime(userLoginTimeStr, "%Y-%m-%d %H:%M:%S") # 把userLogin时间字符串转成时间元祖
        logger.info("timeArray after time.strptime func: %s" % str(timeArray))
        timestampOld = time.mktime(timeArray) # 把时间元祖转换成时间戳
        logger.info("timestampOld format from timeArray: %s" % timestampOld)
        timeStampDiff = timestampNew - timestampOld # 两个时间戳相减，得出时间差（单位：秒）
        logger.info("timeStampDiff: %s" % timeStampDiff)

        if timeStampDiff > 0:
            timeHourDiff = int(divmod(timeStampDiff,3600)[0]) # 把时间差（秒）换算成小时，处理3600，得到一个元祖，第一个值为小时
            logger.info("the time difference is : %s hour" % timeHourDiff)
            return timeHourDiff
        else:
            logger.error("timestamp different is negative")
            return "wrong"
    except Exception as e:
        logger.error("calculate time difference error: %s" % e)


'''
responseDict = {"data": [], "code": "00", "userid": userid}
userOfBlog = User.query.filter(User.id == userid).first()
blogs = userOfBlog.blogs
'''
# 用于查询用户博文接口，填充返回字典responseDict
def fillInResponseDict(responseDict, blogs):
    # 遍历用户的所有博文，把博文的各字段赋值给博文字典的各个值（按照接口文档的格式）
    #blogDict = {}
    for blog in blogs:
        # 定义一个临时字典，组装博文的数据
        blogDict = {}# 如果定义在for前面，由于append的是blogDict的引用，在填充完response后，存的blogDict最后都会替换为最后一次blogDict的值
        logger.info("----blog: %s" % blog)
        blogDict["update_time"] = blog.updateTime
        blogDict["title"] = blog.blogTitle
        blogDict["content"] = blog.blogContent
        blogDict["articleId"] = blog.articleId
        blogDict["owner"] = blog.user.id
        blogDict["posted_on"] = blog.createTime
        logger.info("blogDict: %s" % blogDict)
        #遍历完一个博文后，把blogDict添加到responseDict的"data"列表中
        responseDict["data"].append(blogDict)
        logger.info("responseDict: %s" % responseDict)
    #把blogs内容填充到responseDict后，把responseDict返回
    return responseDict


if __name__ == '__main__':
    print(md5Hash('sdfsdf'))
    # blogs = User.query.filter(User.id == 1).first().blogs
    # #print blogs
    # responseDict = {"data": [], "code": "00", "userid": 1}
    # logger.info(fillInResponseDict(responseDict, blogs))

