from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')



taco_clients = [
    {
        'id': 1,
        'nombre': 'Jóse',
        'plato_favorito': 'Cuacamole',
    },
    {
        'id': 2,
        'nombre': 'Valetina',
        'plato_favorito': 'Chilli com carne',
    },
]

@app.get('/taco-clients', response_class=HTMLResponse)
async def get_clients(request: Request):
    '''
    Função que retorna uma lista dos clientes com seus respectivos pratos.
    '''
    return templates.TemplateResponse(
        "index.html", 
        {"request": request,"taco_clients": taco_clients}
    )
 
#  Post urls
@app.get('/form', response_class=HTMLResponse)
async def get_form(request: Request):
    '''
    Função que retorna o arquivo post.html.
    '''
    return templates.TemplateResponse(
        "post.html", 
        {"request": request}
    )

# obs:pip install python-multipart 
@app.post('/post-client')
async def post_client(nombre: str = Form(...), plato_favorito: str = Form(...)):
    '''
    Função que cria um novo cliente a partir dos seus respectivos dados informados.
    '''
    taco_client_dict = {
        'id': len(taco_clients) + 1,
        'nombre': nombre,
        'plato_favorito': plato_favorito,
    } 
    
    taco_clients.append(taco_client_dict)
    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)

# update urls
@app.get('/edit-client/{id}')
async def get_by_id(id: int, request: Request):
    '''
    Função que retorna o arquivo edit.html.
    '''
    id_int = int(id)
    client = get_client_by_id(id_int)
    return templates.TemplateResponse(
        "edit.html", 
        {"request": request, 'client': client}
    )

def get_client_by_id(id):
    '''
    Função que retorna um cliente através do ID informado.
    '''
    client_id = {}
    for client in taco_clients:
    
       if client['id'] == id:
            client_id = client
    return client_id
    
@app.post('/update-client/{id}')
async def update_client(id: int, nombre: str = Form(...), plato_favorito: str = Form(...)):
    '''
    Função que recebe um formulário e atualiza o banco de dados.
    '''
    id_int = int(id)
    for client in taco_clients:
        if client['id'] == id_int:
            client['nombre'] = nombre
            client['plato_favorito'] = plato_favorito

    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)

@app.post('/update-status/{id}')
async def update_status(id: int, request: Request, nombre: str = Form(...), plato_favorito: str = Form(...)):
    '''
    Função que recebe um formulário e atualiza o banco de dados.
    '''
    id_int = int(id)
    for client in taco_clients:
        if client['id'] == id_int:
            client['status_pedido'] = status
            
    return templates.TemplateResponse(
        "status_pedido.html", 
        {"request": request, 'client': client}
    )


#  delete url
@app.get('/delete-client/{id}')
async def delete_client(id: int):
    '''
    Função que apaga um cadastro a partir do ID informado.
    '''
    id_int = int(id)
    for client in taco_clients:
        if client['id'] == id_int:
            taco_clients.remove(client)

    return RedirectResponse(url=app.url_path_for("get_clients"), status_code=status.HTTP_303_SEE_OTHER)
