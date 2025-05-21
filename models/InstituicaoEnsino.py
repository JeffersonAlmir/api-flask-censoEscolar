class InstituicaoEnsino:
    
    def __init__(self,co_entidade, co_regiao, no_regiao, no_uf, sg_uf, no_municipio, 
    no_mesorregiao, no_microrregiao, no_entidade, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, 
    qt_mat_med_ct, qt_mat_med_nm, qt_mat_prof, qt_mat_prof_tec, qt_mat_eja, qt_mat_esp):
        
        self.co_entidade = co_entidade
        self.co_regiao = co_regiao
        self.no_regiao = no_regiao
        self.no_uf = no_uf
        self.sg_uf = sg_uf
        self.no_municipio = no_municipio
        self.no_mesorregiao = no_mesorregiao
        self.no_microrregiao = no_microrregiao
        self.no_entidade = no_entidade
from marshmallow import Schema, fields, validate

class InstituicaoEnsino:
    
    def __init__(self,co_entidade, no_entidade, co_uf, no_uf, sg_uf ,co_municipio ,no_municipio, 
    co_mesorregiao, no_mesorregiao, co_microrregiao, no_microrregiao, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, 
    qt_mat_med_ct, qt_mat_med_nm, qt_mat_prof, qt_mat_prof_tec, qt_mat_eja, qt_mat_esp):
        
        self.co_entidade = co_entidade
        self.no_entidade = no_entidade
        self.co_uf = co_uf
        self.no_uf = no_uf
        self.sg_uf = sg_uf
        self.co_municipio = co_municipio
        self.no_municipio = no_municipio
        self.co_mesorregiao = co_mesorregiao
        self.no_mesorregiao = no_mesorregiao
        self.co_microrregiao = co_microrregiao
        self.no_microrregiao = no_microrregiao
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_inf = qt_mat_inf
        self.qt_mat_fund = qt_mat_fund
        self.qt_mat_med = qt_mat_med
        self.qt_mat_med_ct = qt_mat_med_ct
        self.qt_mat_med_nm = qt_mat_med_nm
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_prof_tec = qt_mat_prof_tec
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp

    def toDict(self):
        return {
        "co_entidade": self.co_entidade,
        "co_regiao": self.co_regiao,
        "no_regiao": self.no_regiao,
        "no_uf": self.no_uf,
        "sg_uf": self.sg_uf,
        "no_municipio": self.no_municipio,
        "no_mesorregiao": self.no_mesorregiao,
        "no_microrregiao": self.no_microrregiao,
        "no_entidade": self.no_entidade,
        "no_entidade": self.no_entidade,
        "co_uf": self.co_uf,
        "no_uf": self.no_uf,
        "sg_uf": self.sg_uf,
        "co_municipio": self.co_municipio,
        "no_municipio": self.no_municipio,
        "co_mesorregiao": self.co_mesorregiao,
        "no_mesorregiao": self.no_mesorregiao,
        "co_microrregiao": self.co_microrregiao,
        "no_microrregiao": self.no_microrregiao,
        "qt_mat_bas": self.qt_mat_bas,
        "qt_mat_inf": self.qt_mat_inf,
        "qt_mat_fund": self.qt_mat_fund,
        "qt_mat_med": self.qt_mat_med,
        "qt_mat_med_ct": self.qt_mat_med_ct,
        "qt_mat_med_nm": self.qt_mat_med_nm,
        "qt_mat_prof": self.qt_mat_prof,
        "qt_mat_prof_tec": self.qt_mat_prof_tec,
        "qt_mat_eja": self.qt_mat_eja,
        "qt_mat_esp": self.qt_mat_esp
        } 
         
    


class InstituicaoEnsinoSchema(Schema):
    co_entidade = fields.Integer(required=True, 
                                 error_messages={"required": "Código da Entidade é obrigatório."})
    no_entidade = fields.String(validate=validate.Length(min=2, max=100),
                                required=True, error_messages={"required": "Nome da Entidade é obrigatório."})
    co_uf = fields.Integer(required=True, error_messages={
                                 "required": "Código da UF é obrigatório."})
    no_uf = fields.String(validate=validate.Length(min=2, max=50),
                                required=True, error_messages={"required": "Nome da UF é obrigatório."})
    sg_uf = fields.String(validate=validate.Length(min=2, max=2),
                                required=True, error_messages={"required": "Sigla da UF é obrigatório."})
    co_municipio = fields.Integer(required=True, error_messages={
                                 "required": "Código do Município é obrigatório."})
    no_municipio = fields.String(validate=validate.Length(min=2, max=150),
                                required=True, error_messages={"required": "Nome do Município é obrigatório."})
    co_mesorregiao = fields.Integer(required=True, error_messages={
                                 "required": "Código da Mesorregião é obrigatório."})
    no_mesorregiao = fields.String(validate=validate.Length(min=2, max=100),
                                required=True, error_messages={"required": "Nome da Mesorregião é obrigatório."})
    co_microrregiao = fields.Integer(required=True, error_messages={
                                 "required": "Código da Microrregião é obrigatório."})
    no_microrregiao = fields.String(validate=validate.Length(min=2, max=100),
                                required=True, error_messages={"required": "Nome da Microrregião é obrigatório."})
    qt_mat_bas = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula básicas é obrigatório."})
    qt_mat_inf = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula infantil é obrigatório."})
    qt_mat_fund = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula fundamental é obrigatório."})
    qt_mat_med = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula médio é obrigatório."})
    qt_mat_med_ct = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula médio_ct é obrigatório."})
    qt_mat_med_nm = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula médio_nm é obrigatório."})
    qt_mat_prof = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula profissional é obrigatório."})
    qt_mat_prof_tec = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula profissional_tec é obrigatório."})
    qt_mat_eja = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula eja é obrigatório."})
    qt_mat_esp = fields.Integer(required=True, error_messages={
                                 "required": "Quantidade de matricula especial é obrigatório."})
