from database import Base
from sqlalchemy import Integer, String, Column
from pydantic import BaseModel


class Clientes(Base):
    __tablename__ = 'clientes'
    
    id: Column(Integer, primary_key=True, index=True)
    nombre: Column(String)
    plato_favorito: Column(String) 
    status_pedido: Column(str)


class ClientesRequest(BaseModel):
    nombre: str
    plato_favorito: str

    class Config:
        json_schema_extra = {
            'example': {
                "nombre": "Nome_aqui",
                "plato_favorito": "nome_do_prato",
                "status_pedido": False,
            }
        }

    