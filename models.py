from database import Base
from sqlalchemy import Integer, String, Column
from pydantic import BaseModel


class Clientes(Base):
    '''
    Objeto que interage com a table `clientes` no banco de dados.
    '''
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    plato_favorito = Column(String) 

class ClientesRequest(BaseModel):
    '''
    ## Objeto Cliente que recebe o request do form pra adcionar ou modificar clientes.

    '''
    nombre: str
    plato_favorito: str

    class Config:
        json_schema_extra = {
            'example': {
                "nombre": "Nome_aqui",
                "plato_favorito": "nome_do_prato"
            }
        }

    