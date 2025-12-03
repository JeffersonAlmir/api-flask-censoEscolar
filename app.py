from helpers.application import app , api
from helpers.CORS import cors

from helpers.database import db
from resources.IndexResource import IndexResource
from resources.InstituicaoResource import InstituicoesResource, InstituicoesAno
from resources.UfResource import UfsResource, UfMatriculasResource, UfQuantidadesResource
from resources.MunicipioResource import MunicipiosResource , MunicipioMatriculasResource
from resources.MesorregiaoResource import MesorregioesResource


from models.Uf import Uf
from models.Mesorregiao import Mesorregiao
from models.Microrregiao import Microrregiao
from models.Municipio import Municipio
from models.InstituicaoEnsino import InstituicaoEnsino

cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicoesAno, '/instituicaoAnos')

api.add_resource(UfsResource,'/ufs')
api.add_resource(UfMatriculasResource, '/uf/matriculas')
api.add_resource(UfQuantidadesResource,'/uf/total_municipios_matriculas')




api.add_resource(MesorregioesResource,'/mesorregioes')
api.add_resource(MunicipiosResource,'/municipio')
api.add_resource(MunicipioMatriculasResource,'/municipio/matriculas')
# api.add_resource(InstituicaoResource, '/instituicoes/<int:id>')
# api.add_resource(InstituicoesConsultaResource, '/instituicoes/anos')


# api.add_resource(InstituicoesPorCidadeResource, '/instituicoes_cidades')











    