from flask_restful import Resource

class IndexResource(Resource):
    def get():
        versao = {"versao":"0.0.1"}
        return versao,200