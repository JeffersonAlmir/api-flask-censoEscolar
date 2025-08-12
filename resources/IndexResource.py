from flask_restful import Resource

class IndexResource(Resource):
    def get(self):
        versao = {"versao":"0.0.3"}
        return versao,200