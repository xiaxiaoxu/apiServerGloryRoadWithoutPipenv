#encoding=utf-8
import logging
import logging.config
from gloryRoadApi.settings import project_path


#读取日志的配置文件
logging.config.fileConfig(project_path+"\\gloryRoadApi\\common\\Logger.conf")
#选择一个日志格式
logger=logging.getLogger("example01") #example01


if __name__=="__main__":
    print ("conf file path:", project_path+"\\gloryRoadApi\\common\\Logger.conf")
    logger.info("hi")
    logger.error("world!")
    logger.warning("gloryroad!")