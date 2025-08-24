import { z } from 'zod'

/*
{
    "monday": {
        "name": "Homemade Marinated Pork Roast",
        "ingredients": [
            "sugar",
            "lemon juice",
            "soy sauce",
            "all-purpose",
            "water",
            "ginger ale",
            "garlic",
            "center",
            "green pepper"
        ]
    },
    "tuesday": {
        "name": "Baked Rice With Vegetables And Eggs",
        "ingredients": [
            "milk",
            "mozzarella cheese",
            "eggs",
            "onion",
            "ground black pepper",
            "vegetables",
            "parsley",
            "rice",
            "garlic",
            "salt"
        ]
    },
    "wednesday": {
        "name": "Fairy Bread Pinwheels",
        "ingredients": [
            "white bread",
            "red sprinkles",
            "margarine"
        ]
    },
    "thursday": {
        "name": "Zucchini Soup",
        "ingredients": [
            "zucchini",
            "sweet italian sausage",
            "tomatoes",
            "oregano",
            "onion",
            "beef broth",
            "water",
            "basil",
            "parsley",
            "garlic",
            "green pepper"
        ]
    },
    "friday": {
        "name": "Roasted Pineapple with Rum-Vanilla Sauce and Coconut",
        "ingredients": [
            "sugar",
            "vanilla bean",
            "shredded coconut",
            "raisin ice cream",
            "water",
            "cornstarch",
            "white rum",
            "pineapple",
            "salt"
        ]
    },
    "saturday": {
        "name": "My Chicken Parm",
        "ingredients": [
            "oil",
            "egg",
            "chicken breasts",
            "flour",
            "breadcrumbs",
            "parmesan cheese",
            "roma tomatoes",
            "garlic",
            "fresh basil",
            "friulano cheese",
            "salt"
        ]
    },
    "sunday": {
        "name": "Swiss-Style Cheese Fondue",
        "ingredients": [
            "Swiss cheese",
            "white wine",
            "garlic",
            "cornstarch",
            "bread cubes",
            "pickles",
            "cured meats"
        ]
    }
}
*/

export const calendarMenusSchema = z.object({
  monday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  tuesday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  wednesday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  thursday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  friday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  saturday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
  sunday: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
  }),
})
