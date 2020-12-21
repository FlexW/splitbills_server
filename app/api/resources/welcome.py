from flask_restful import Resource


class WelcomeResource(Resource):
    def get(self):
        welcome_message = "Welcome to the SplitBills Api. More Information can be found on https://github.com/FlexW/splitbills_server"

        return {"message": welcome_message}, 200
