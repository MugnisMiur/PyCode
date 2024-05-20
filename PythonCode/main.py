import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api.handlers import user_router
from api.login_handler import login_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()

main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)
# app.mount("/static", StaticFiles(directory="get_media"), name="media")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
