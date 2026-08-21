from fastapi import FastAPI
from app.routes.users_routes import router as users_router

app = FastAPI()


# localhost:8000/
@app.get("/")
def root():
    return "Hello World!"


# localhost:8000/about
@app.get("/about")
def about_root():
    return "Welcome to About Page!"


# localhost:8000/contact
@app.get("/contact")
def contact_root():
    return "Welcome to Contact Page!"


app.include_router(users_router)
# To run
# uv run uvicorn app.main:app --reload
