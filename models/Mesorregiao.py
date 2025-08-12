from flask_restful import fields as flaskFields
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from marshmallow import Schema, fields, validate


from helpers.database import db

mesorregiao_fields = {
    "co_mesorregiao": flaskFields.Integer,
    "no_mesorregiao": flaskFields.String,
    "uf": flaskFields.Nested({
        "co_uf": flaskFields.Integer,
    }),
}

class Mesorregiao(db.Model):
    __tablename__ ="tb_mesorregiao"

    co_mesorregiao: Mapped[int] = mapped_column(Integer, primary_key=True)
    no_mesorregiao: Mapped[str] = mapped_column(String(50))
    co_uf: Mapped[int] = mapped_column(ForeignKey("tb_uf.co_uf"))

    uf = relationship( "Uf", back_populates="mesorregiao")
    municipio = relationship("Municipio", back_populates="mesorregiao")
    instituicao = relationship("InstituicaoEnsino", back_populates="mesorregiao")


    def __init__(self, co_mesorregiao:int, no_mesorregiao:str, co_uf:int):
        self.co_mesorregiao = co_mesorregiao
        self.no_mesorregiao = no_mesorregiao
        self.co_uf = co_uf


class MesorregiaoSchema(Schema):
    co_mesorregiao = fields.Integer(required=True, error_messages={
                                 "required": "Código da Mesorregião é obrigatório."})
    no_mesorregiao = fields.String(validate=validate.Length(min=2, max=100),
                                required=True, error_messages={"required": "Nome da Mesorregião é obrigatório."})
    uf = fields.Nested("UfSchema",only=["co_uf"])