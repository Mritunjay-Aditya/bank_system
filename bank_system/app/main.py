from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth, loan
import os

app = FastAPI()


# Mount the static folder for CSS, JS, images, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates for HTML rendering

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
 
@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Include the authentication and loan routers  
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(loan.router, prefix="/loan", tags=["Loan"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
