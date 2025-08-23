import pickle
from contextlib import asynccontextmanager

import joblib
import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from controllers import health_controller, menu_recommender_controller
from helpers.logger import logger
from models.recipie_embedding_model import RecipeEmbeddingModel
from services.recommender_service import RecommenderService


@asynccontextmanager
async def lifespan(app: FastAPI):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the ingredient index
    with open("./dataset/ingredient2idx.pkl", "rb") as f:
        ingredient2idx = pickle.load(f)

    # Load the pre-calculated embeddings
    recipe_embeddings = torch.load("./embeddings/recipe_embeddings.pt")

    # Load the recipe dataset
    recipies = joblib.load("./dataset/recipes_for_app.pkl")

    model = RecipeEmbeddingModel(vocab_size=len(ingredient2idx), embedding_dim=128).to(device)
    model.load_state_dict(torch.load("./models/recipe_embedding_model.pt", map_location=device))
    app.state.recommender_service = RecommenderService(
        model=model,
        ingredient_vocab=ingredient2idx,
        recipe_embeddings=recipe_embeddings,
        recipe_dataset=recipies
    )

    yield

def app_factory() -> FastAPI:
    # Init fast api
    app: FastAPI = FastAPI(title="Menu Recommender Service", lifespan=lifespan)

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Add router
    app.include_router(health_controller.router, prefix="/api/v1/health")
    app.include_router(menu_recommender_controller.router, prefix="/api/v1/menu")

    # Logging
    logger.info(f"Starting app with profile: {config.settings.ENV}")

    return app
