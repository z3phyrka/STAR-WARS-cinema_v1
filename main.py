from concurrent.futures import thread
from fastapi import FastAPI, Form, status, HTTPException, Depends, Request, Response, Query
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, select, create_engine
from models import User
from database import engine
from sqlalchemy import create_engine
from fastapi import FastAPI, Form, status, Depends
from sqlalchemy.orm import Session, sessionmaker
from typing import Optional, Annotated
import sys
import time
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler




DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SQLModel.metadata.create_all(engine)

app = FastAPI(description='STAR WARS cinema')

templates = Jinja2Templates('templates')

session = Session(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/login', tags=['Pages'])
async def get_login_page(request: Request):
    cookie = request.cookies.get('id')

    if cookie != None:
        return RedirectResponse(f'/profile/{cookie}', status_code=302)

    return templates.TemplateResponse('reg.html', {'request': request})

@app.get('/reg', tags=['Pages'])
async def get_registration_page(request: Request):
    return templates.TemplateResponse('reg.html', {'request': request})

@app.post('/reg', status_code=status.HTTP_201_CREATED, 
          response_class=RedirectResponse, tags=['Account'])
async def create_a_customer(first_name: str = Form(...), 
                            second_name: str = Form(...), 
                            email: str = Form(...), 
                            password: str = Form(...),
                            remember: Optional[bool] = Form(default=False)) -> RedirectResponse:
    
    statement = select(User).where(User.email == email)
    result = session.exec(statement).one_or_none()

    new_cust = User(first_name=first_name, second_name=second_name,
                        email=email, password=password)

    if result is None:
        session.add(new_cust)
        session.commit()

        response = RedirectResponse(f'/profile/{str(new_cust.id)}', status_code=302)
        if remember == True:
            response.set_cookie(key="id", value=str(new_cust.id), max_age=15695000)
        return response

    return RedirectResponse('/registration', status_code=302)

@app.get("/reg.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

@app.get("/reg2.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("reg2.html", {"request": request})

@app.get("/reg3.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("reg3.html", {"request": request})

@app.get("/reg4.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("reg4.html", {"request": request})

@app.get("/reg5.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("reg5.html", {"request": request})

@app.get("/reg6.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("reg6.html", {"request": request})

@app.get("/ep2.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("ep2.html", {"request": request})

@app.get("/ep3.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("ep3.html", {"request": request})

@app.get("/ep4.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("ep4.html", {"request": request})

@app.get("/ep5.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("ep5.html", {"request": request})

@app.get("/ep6.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("ep6.html", {"request": request})

@app.get("/ep1.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("ep1.html", {"request": request})

@app.get("/home.html", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

ip = "127.0.0.1"
port = 8000
url = f"http://{ip}:{port}/home.html"


def start_server():
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


threading.Thread(target=start_server).start()
webbrowser.open_new(url)

        
def get_session() -> Session:
    try:
        yield session
    finally:
        session.close()
        
@app.get("/home.html")
async def serve_html():
    return FileResponse("templates/home.html")
        
