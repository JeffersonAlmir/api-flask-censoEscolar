from flask_restful import fields as flaskFields
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from marshmallow import Schema, fields, validate


from helpers.database import db

microrregiao_fields = {
    "co_microrregiao": flaskFields.Integer,
    "no_microrregiao": flaskFields.String,
    "uf": flaskFields.Nested({
        "co_uf": flaskFields.Integer,
    }),
}

class Microrregiao(db.Model):
    __tablename__ ="tb_microrregiao"

    co_microrregiao: Mapped[int] = mapped_column(Integer, primary_key=True)
    no_microrregiao: Mapped[str] = mapped_column(String(50))
    co_uf: Mapped[int] = mapped_column(ForeignKey("tb_uf.co_uf"))

    uf = relationship( "Uf", back_populates="microrregiao")
    municipio = relationship("Municipio", back_populates="microrregiao")
    instituicao = relationship("InstituicaoEnsino", back_populates="microrregiao")


    def __init__(self, co_microrregiao:int, no_microrregiao:str, co_uf:int):
        self.co_microrregiao = co_microrregiao
        self.no_microrregiao = no_microrregiao
        self.co_uf = co_uf


class MicrorregiaoSchema(Schema):
    co_microrregiao = fields.Integer(required=True, error_messages={
                                 "required": "Código da Microrregião é obrigatório."})
    no_microrregiao = fields.String(validate=validate.Length(min=2, max=100),
                                required=True, error_messages={"required": "Nome da Microrregião é obrigatório."})
    uf = fields.Nested("UfSchema",only=["co_uf"])