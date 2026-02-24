from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
from app.search.semantic import load_products, build_index, load_index
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists('faiss.index'):
        products = load_products()
        build_index(products)
    load_index()


    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
