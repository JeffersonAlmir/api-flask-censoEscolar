from sqlalchemy import Integer, String
from sqlalchemy.orm import  Mapped, mapped_column,relationship
from flask_restful import fields as flaskFields
from marshmallow import Schema, fields, validate


from helpers.database import db



uf_fields ={
    "co_uf": flaskFields.Integer,
    "no_uf": flaskFields.String,
    "sg_uf": flaskFields.String,
}


class Uf(db.Model):
    __tablename__ ="tb_uf"

    co_uf: Mapped[int] = mapped_column(Integer, primary_key=True)
    no_uf: Mapped[str] = mapped_column(String(100))
    sg_uf: Mapped[str] = mapped_column(String(2))
    
    mesorregiao = relationship("Mesorregiao", back_populates="uf" )
    microrregiao = relationship("Microrregiao", back_populates="uf" )
    municipio = relationship("Municipio", back_populates="uf")
    instituicao = relationship("InstituicaoEnsino", back_populates="uf")
    

    def __init__(self, co_uf:int, no_uf:str, sg_uf:str):
        self.co_uf = co_uf
        self.no_uf = no_uf
        self.sg_uf = sg_uf

class UfSchema(Schema):
    co_uf = fields.Integer(required=True, error_messages={
                                 "required": "Código da UF é obrigatório."})
    no_uf = fields.String(validate=validate.Length(min=2, max=50),
                                required=True, error_messages={"required": "Nome da UF é obrigatório."})
    sg_uf = fields.String(validate=validate.Length(min=2, max=2),
                                required=True, error_messages={"required": "Sigla da UF é obrigatório."})