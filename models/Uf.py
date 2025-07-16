from flask_restful import fields as flaskFields

uf_fields ={
    "co_uf": flaskFields.Integer,
    "no_uf": flaskFields.String,
    "sg_uf": flaskFields.String,
}

class Uf:
    def __init__(self, co_uf, no_uf, sg_uf):
        self.co_uf = co_uf
        self.no_uf = no_uf
        self.sg_uf = sg_uf