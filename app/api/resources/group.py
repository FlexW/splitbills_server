from flask_restful import Resource
from app import auth


class GroupResource(Resource):

    @auth.login_required
    def put(self, group_id):
        pass
