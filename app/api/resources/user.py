from flask_restful import Resource, abort


def abort_if_user_doesnt_exist(user_id):
    # if user_id not in users:
    #     abort(404, message="User {} doesn't exist".format(user_id))
    pass


class UserResource(Resource):
    def get(self, user_id):
        # abort_if_user_doesnt_exist(user_id)
        # return users[user_id]
        pass

    def put(self, user_id):
        pass
