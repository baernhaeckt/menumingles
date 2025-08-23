from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/recommender", tags=["api menu recommender"], status_code=200)
def inventory_recommender(request: Request, ingredients: list[str]):
    recommender_service = request.app.state.recommender_service
    top_k_recipes = recommender_service.get_recommendations(ingredients)

    return JSONResponse(status_code=200, content={"top_recipes": top_k_recipes})

@router.get("/menusampler", tags=["api menu recommender"], status_code=200)
def next_menu_sampler():
    return JSONResponse(status_code=200, content={"dishes": [
        {
            "dish_name": "Chicken Stir Fry with Bun",
            "ingredients": ["chicken", "rice"]
        },
        {
            "dish_name": "Spaghetti with Tomato Sauce",
            "ingredients": ["potatoes", "water"]
        }
    ]})


