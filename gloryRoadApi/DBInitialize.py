#encoding=utf-8
import os
import time
from gloryRoadApi.common.log import logger
from sqlalchemy import create_engine
from sqlalchemy_utils import  database_exists, create_database
from gloryRoadApi.application import db
from gloryRoadApi.settings import dbUrl, dbname
from gloryRoadApi.models import UserBlog, User


#初始化db连接，不做连接成功校验
engine = create_engine(dbUrl)

def initializeDataBase():
    logger.info("The database name we need to initialize is : %s" % dbname)
    try:
        # 尝试三次创建数据库，如果不成功则提示失败
        for i in range(3):
            logger.info("Try to initialize database attempt times: %s" % int(i + 1 ))
            # 判断dbUrl中末尾的dbname是否存在，不存在则新建
            logger.info("Whether database %s exists? : %s" % (dbname, database_exists(engine.url)))
            # dbname存在，退出循环
            if database_exists(engine.url):
                break
            if not database_exists(engine.url):
                create_database(engine.url)
                time.sleep(0.1)
                # 判断是否创建成功
                if database_exists(engine.url):
                    logger.info("Create new database '%s' successfully, dbUrl: %s" % (dbname, dbUrl))
                    logger.info("database_exists(engine.url): %s" % (database_exists(engine.url)))
                    break
        # 3次都没有执行break，说明没创建成功，提示db创建失败
        else:
            logger.info("Create new database '%s' failed" % dbUrl)

    except Exception as e:
        logger.error("initializeDataBase error: %s" % e)

def initializeTables():
    # 尝试三次创建表，如果不成功则提示失败
    for i in range(3):
        logger.info("Try to initialize tables attempt times: %s" % int(i + 1 ))
        try:
            # 创建表，提交db会话
            db.create_all()
            time.sleep(0.1)
            db.session.commit()
            # 查询User表，如果报错说明查不到，则到except分支创建表
            logger.info("Try to find table User: %s" % User.query.first())
            logger.info("Try to find table UserBlog: %s" % UserBlog.query.first())
            logger.info("User and UserBlog table existed ！")
            # 表存在，则退出循环
            break

        except Exception as e:
            logger.info("Error occurs when searching the tables : '%s', now trying to create again ... " % e)

    # 3次都没有执行break，说明没成功，则在这里提示表创建失败
    else:
        logger.info("Create tables failed")


def initializeDBAndTables():
    initializeDataBase()
    initializeTables()

if __name__ == '__main__':
    pass

    #db.init_app(app)
    # db.create_all()
    # db.session.commit()

    #print(User.query.all())















