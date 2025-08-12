from marshmallow import Schema, fields, validate
from flask_restful import fields as flaskFields
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from helpers.database import db

ano_fields = {
    'nu_ano_censo': flaskFields.Integer,
}

instituicao_fields = {
    "co_entidade": flaskFields.Integer,
    "no_entidade": flaskFields.String,
    "uf": flaskFields.Nested({
        "co_uf": flaskFields.Integer,
        "no_uf": flaskFields.String,
        "sg_uf": flaskFields.String
    }),
    "mesorregiao": flaskFields.Nested({
        "co_mesorregiao": flaskFields.Integer,
        "no_mesorregiao": flaskFields.String
    }),
    "microrregiao": flaskFields.Nested({
        "co_microrregiao": flaskFields.Integer,
        "no_microrregiao": flaskFields.String
    }),
    "municipio": flaskFields.Nested({
        "co_municipio": flaskFields.Integer,
        "no_municipio": flaskFields.String
    }),
    "qt_mat_bas": flaskFields.Integer,
    "qt_mat_inf": flaskFields.Integer,
    "qt_mat_fund": flaskFields.Integer,
    "qt_mat_med": flaskFields.Integer,
    "qt_mat_med_ct": flaskFields.Integer,
    "qt_mat_med_nm": flaskFields.Integer,
    "qt_mat_prof": flaskFields.Integer,
    "qt_mat_prof_tec": flaskFields.Integer,
    "qt_mat_eja": flaskFields.Integer,
    "qt_mat_esp": flaskFields.Integer,
    "nu_ano_censo": flaskFields.Integer,
}

class InstituicaoEnsino(db.Model):
    __tablename__ ="tb_instituicao_ensino"

    co_entidade: Mapped[int] = mapped_column(Integer,primary_key=True)
    no_entidade:Mapped[str] = mapped_column(String(100))
    nu_ano_censo: Mapped[int] = mapped_column(Integer,primary_key=True)

    co_uf: Mapped[int] = mapped_column(ForeignKey("tb_uf.co_uf"))                            
    co_municipio: Mapped[int] = mapped_column(ForeignKey("tb_municipio.co_municipio"))
    co_mesorregiao: Mapped[int] = mapped_column(ForeignKey("tb_mesorregiao.co_mesorregiao"))
    co_microrregiao : Mapped[int] = mapped_column(ForeignKey("tb_microrregiao.co_microrregiao"))
    
    qt_mat_bas : Mapped[int] = mapped_column(Integer)
    qt_mat_inf : Mapped[int] = mapped_column(Integer)
    qt_mat_fund : Mapped[int] = mapped_column(Integer)
    qt_mat_med: Mapped[int] = mapped_column(Integer)
    qt_mat_med_ct : Mapped[int] = mapped_column(Integer)
    qt_mat_med_nm : Mapped[int] = mapped_column(Integer)
    qt_mat_prof: Mapped[int] = mapped_column(Integer)
    qt_mat_prof_tec: Mapped[int] = mapped_column(Integer)
    qt_mat_eja : Mapped[int] = mapped_column(Integer)
    qt_mat_esp : Mapped[int] = mapped_column(Integer)

    uf = relationship("Uf",back_populates="instituicao")
    microrregiao = relationship("Microrregiao", back_populates="instituicao",cascade="save-update")
    mesorregiao = relationship("Mesorregiao", back_populates="instituicao",cascade="save-update")
    municipio = relationship("Municipio", back_populates="instituicao",cascade="save-update")


    
    def __init__(self, co_entidade:int, no_entidade:str, co_uf:int, co_municipio:int, 
                co_mesorregiao:int, co_microrregiao:int, qt_mat_bas:int, qt_mat_inf:int, qt_mat_fund:int,
                  qt_mat_med:int, qt_mat_med_ct:int, qt_mat_med_nm:int, qt_mat_prof:int, qt_mat_prof_tec:int, 
                  qt_mat_eja:int, qt_mat_esp:int, nu_ano_censo:int):
        
        self.co_entidade = co_entidade
        self.no_entidade = no_entidade
        self.co_uf = co_uf
        self.co_municipio = co_municipio
        self.co_mesorregiao = co_mesorregiao
        self.co_microrregiao = co_microrregiao
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
        self.nu_ano_censo = nu_ano_censo

    

class InstituicaoEnsinoSchema(Schema):
    co_entidade = fields.Integer(required=True, 
                                 error_messages={"required": "Código da Entidade é obrigatório."})
    no_entidade = fields.String(validate=validate.Length(min=2, max=100),
                                required=True, error_messages={"required": "Nome da Entidade é obrigatório."})
    
    uf = fields.Nested("UfSchema",only=["co_uf", "no_uf", "sg_uf"])
    municipios = fields.Nested("MunicipioSchema", only=["co_municipio","no_municipio"])
    mesorregiao = fields.Nested("MesorregiaoSchema", only=["co_mesorregiao","no_mesorregiao"] )
    microrregiao = fields.Nested("MicrorregiaoSchema", only=["co_microrregiao", "no_microrregiao"])
    
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
    nu_ano_censo = fields.Integer(required=True, error_messages={
                                 "required": "Ano do censo é obrigatório."})
