from fastapi import FastAPI, Request, Form, status, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from models import ClientesRequest, Clientes
from typing import Annotated

app = FastAPI()

templates = Jinja2Templates(directory='templates')

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/taco-clients', response_class=HTMLResponse)
async def get_clients(request: Request, db: db_dependency ):
    '''
    Função que retorna uma lista dos clientes com seus respectivos pratos.
    '''
    clientes = db.query(Clientes).all()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request,"taco_clients": clientes}
    )
 
#  Post urls
@app.get('/form', response_class=HTMLResponse)
async def get_form(request: Request):
    '''
    View que retorna o arquivo post.html.
    '''
    return templates.TemplateResponse(
        "post.html", 
        {"request": request}
    )

# obs:pip install python-multipart 
@app.post('/post-client')
async def post_client(db: db_dependency, nombre: str = Form(...), plato_favorito: str = Form(...)):
    '''
    Função que cria um novo cliente a partir dos seus respectivos dados informados.
    '''
    
    cliente_model = Clientes(nombre=nombre, plato_favorito=plato_favorito)
    db.add(cliente_model)
    db.commit()
    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)

# update urls
@app.get('/edit-client/{id}')
async def get_by_id(id: int, request: Request, db: db_dependency):
    '''
    ## Retorna do banco de dados o cliente com o respectivo `ID` e passa pra um form com
    o objeto pra ser editado.
    '''
    cliente = db.query(Clientes).filter(Clientes.id == id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail='Cliente not found')
    return templates.TemplateResponse(
        "edit.html", 
        {"request": request, 'client': cliente}
    )

    
@app.post('/update-client/{id}')
async def update_client(db: db_dependency, id: int, nombre: str = Form(...), plato_favorito: str = Form(...)):
    client_model = db.query(Clientes).filter(Clientes.id == id).first()
    
    if client_model is None:
        raise HTTPException(status_code=404, detail='Cliente not found')
    
    client_model.nombre = nombre
    client_model.plato_favorito = plato_favorito

    db.add(client_model)
    db.commit()

    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)

#  delete url
@app.get('/delete-client/{id}')
async def delete_client(id: int, db: db_dependency):
    '''
    ## Deleta linha na table `clientes` no banco de dados.

    ### Parametros:
    - `id`: id do cliente
    '''
    cliente_model = db.query(Clientes).filter(Clientes.id == id).first()
    if cliente_model is None:
        raise HTTPException(status_code=404, detail='Cliente not found')    
    db.query(Clientes).filter(Clientes.id == id).delete()
    db.commit()
    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)
