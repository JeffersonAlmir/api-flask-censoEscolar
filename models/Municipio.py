from flask_restful import fields as flaskFields
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from marshmallow import Schema, fields, validate
from helpers.database import db

municipio_fields = {
    "co_municipio": flaskFields.Integer,
    "no_municipio": flaskFields.String,
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
}

class Municipio(db.Model):
    __tablename__ = "tb_municipio"

    co_municipio: Mapped[int] = mapped_column(Integer, primary_key=True)
    no_municipio: Mapped[str] = mapped_column(String(50))
    co_uf: Mapped[int] = mapped_column(ForeignKey("tb_uf.co_uf"))
    co_mesorregiao: Mapped[int] = mapped_column(ForeignKey("tb_mesorregiao.co_mesorregiao"))
    co_microrregiao: Mapped[int] = mapped_column(ForeignKey("tb_microrregiao.co_microrregiao"))

    uf = relationship("Uf", back_populates="municipio")
    microrregiao = relationship("Microrregiao", back_populates="municipio")
    mesorregiao = relationship("Mesorregiao", back_populates="municipio") 
    instituicao = relationship("InstituicaoEnsino", back_populates="municipio")

    def __init__(self, co_municipio: int, no_municipio: str, co_uf: int, 
                 co_mesorregiao: int, co_microrregiao: int):
        self.co_municipio = co_municipio
        self.no_municipio = no_municipio
        self.co_uf = co_uf
        self.co_mesorregiao = co_mesorregiao
        self.co_microrregiao = co_microrregiao  

class MunicipioSchema(Schema):
    co_municipio = fields.Integer(required=True, error_messages={
        "required": "Código do Município é obrigatório."})
    no_municipio = fields.String(validate=validate.Length(min=2, max=150),
                                required=True, error_messages={"required": "Nome do Município é obrigatório."})
    uf = fields.Nested("UfSchema", only=["co_uf"])  
    mesorregiao = fields.Nested("MesorregiaoSchema", only=["co_mesorregiao"])  
    microrregiao = fields.Nested("MicrorregiaoSchema", only=["co_microrregiao"]) 