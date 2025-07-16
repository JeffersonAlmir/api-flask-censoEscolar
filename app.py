from helpers.application import app , api
from helpers.CORS import cors


from resources.IndexResource import IndexResource
from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource, InstituicoesConsultaResource, InstituicoesConsultaPorAnoResource,InstituicoesPorCidadeResource
from resources.UfResource import UfResource


cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:id>')

api.add_resource(InstituicoesConsultaResource, '/instituicoes/anos')

api.add_resource(InstituicoesConsultaPorAnoResource, '/instituicoes_consulta')

api.add_resource(InstituicoesPorCidadeResource, '/instituicoes_cidades')


api.add_resource(UfResource,'/ufs')











    