#encoding=utf-8

from gloryRoadApi.application import app, db
from gloryRoadApi.DBInitialize import initializeDBAndTables
from flask_restful import Resource, Api, reqparse, request, fields, marshal
from gloryRoadApi.common import util
from gloryRoadApi.resources.login import Login
from gloryRoadApi.resources.register import Register
from gloryRoadApi.resources.create import Create
from gloryRoadApi.resources.update import Update
from gloryRoadApi.resources.getBlogContent import GetBlogContent
from gloryRoadApi.resources.getBlogsContent import GetBlogsContent
from gloryRoadApi.resources.getBlogsOfUser import GetBlogsOfUser
from gloryRoadApi.resources.delete import Delete
from gloryRoadApi.common.log import logger


api = Api(app)



api.add_resource(Register, '/register/', endpoint = 'register')
api.add_resource(Login, '/login/', endpoint = 'login')
api.add_resource(Create, '/create/', endpoint = 'create')
api.add_resource(Update, '/update/', endpoint = 'update')
api.add_resource(GetBlogsOfUser, '/getBlogsOfUser/', endpoint = 'getBlogsOfUser')
api.add_resource(GetBlogContent, '/getBlogContent/<string:articleId>', endpoint = 'getBlogContent')
api.add_resource(GetBlogsContent, '/getBlogsContent/<string:articleIdString>', endpoint = 'getBlogsContent')
api.add_resource(Delete, '/delete/', endpoint = 'delete')



# 注册shell上下文处理函数
@app.shell_context_processor
def make_shell_context():
    return dict(db = db, User = User, UserBlog = UserBlog)



if __name__ == '__main__':
    initializeDBAndTables()
    app.run(debug=True)
































