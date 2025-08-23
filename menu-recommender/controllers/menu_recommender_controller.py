from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/recommender", tags=["api menu recommender"], status_code=200)
def inventory_recommender(ingredients: list[str]):
    return JSONResponse(status_code=200, content=[
        {
            "dish_name": "Fried Chicken",
            "ingredients": ["chicken", "rice"]
        },
        {
            "dish_name": "Golden Cream Potato Soup",
            "ingredients": ["potatoes", "water"]
        }
    ])

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


