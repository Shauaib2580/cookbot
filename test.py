
import requests



# Use a publicly available model
MODEL_NAME = "tiiuae/falcon-7b-instruct"

# Hugging Face API endpoint
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}



# Predefined calories for some ingredients (you can expand this list or use an API)
ingredient_calories = {
    "egg": 72,         # per egg
    "flour": 455,      # per 1 cup (120g)
    "sugar": 387,      # per 100g
    "butter": 102,     # per 1 tbsp (14g)
    "oil": 119,        # per 1 tbsp (14g)
    # Carbs
    "rice": 130,     # per 1 cup cooked (158g)
    "brown_rice": 111,     # per 1 cup cooked (158g)
    "whole_wheat_bread": 69, # per slice
    "pasta": 200,          # per 1 cup cooked (140g)
    "potato": 77,          # per 100g
    "sweet_potato": 86,    # per 100g

    # Fruits
    "apple": 52,           # per 100g
    "banana": 89,          # per 100g
    "grapes": 69,          # per 100g
    "orange": 47,          # per 100g
    "strawberries": 32,    # per 100g
    "watermelon": 30,      # per 100g
    "blueberries": 57,     # per 100g

    # Vegetables
    "broccoli": 55,        # per 100g
    "spinach": 23,         # per 100g
    "carrot": 41,          # per 100g
    "tomato": 18,          # per 100g
    "cucumber": 16,        # per 100g
    "lettuce": 15,         # per 100g
    "zucchini": 17,        # per 100g

    # Proteins
    "chicken": 165, # per 100g
    "beef": 250,           # per 100g (lean ground)
    "salmon": 206,         # per 100g
    "tofu": 70,            # per 100g
    "lentils": 116,        # per 1 cup cooked (198g)
    "black_beans": 227,    # per 1 cup cooked (172g)

    # Dairy
    "milk": 103,           # per 1 cup (244g)
    "cheese": 113,         # per 1 slice (28g)
    "yogurt": 59,          # per 100g (plain)
    "butter": 102,         # per 1 tbsp (14g)
    "cream_cheese": 99,    # per 1 tbsp (14g)

    # Fats
    "avocado": 234,        # per 100g
    "olive_oil": 119,      # per 1 tbsp (14g)
    "peanut_butter": 588,  # per 100g
    "almonds": 579,        # per 100g
    "coconut_oil": 117,    # per 1 tbsp (14g)

    # Snacks & Sweets
    "chocolate": 546,      # per 100g
    "chips": 536,          # per 100g
    "cookies": 502,        # per 100g
    "ice_cream": 207,      # per 100g
    "popcorn": 375,        # per 100g

    # Grains & Cereals
    "oats": 389,           # per 100g
    "cornmeal": 365,       # per 100g
    "quinoa": 120,         # per 1 cup cooked (185g)
    "couscous": 176,       # per 1 cup cooked (157g)
    "barley": 354,         # per 100g
    "whole_wheat_flour": 407, # per 1 cup (120g)
    "pancakes": 227,       # per 1 medium pancake (45g)

    # Nuts & Seeds
    "walnuts": 654,        # per 100g
    "cashews": 553,        # per 100g
    "pistachios": 562,     # per 100g
    "sunflower_seeds": 584, # per 100g
    "chia_seeds": 486,     # per 100g
    "flaxseeds": 534,      # per 100g
    "pumpkin_seeds": 559,  # per 100g

    # Beverages
    "coffee": 2,           # per 1 cup (240ml, black)
    "tea": 2,              # per 1 cup (240ml, black)
    "orange_juice": 45,    # per 100ml
    "apple_juice": 46,     # per 100ml
    "soda": 150,           # per 1 can (355ml)
    "lemonade": 53,        # per 100ml
    "smoothie": 180,       # per 1 cup (240ml)

    # Condiments & Sauces
    "ketchup": 112,        # per 100g
    "mayonnaise": 680,     # per 100g
    "mustard": 66,         # per 100g
    "soy_sauce": 10,       # per 1 tbsp (15g)
    "barbecue_sauce": 72,  # per 1 tbsp (20g)
    "hot_sauce": 5,        # per 1 tbsp (15g)

    # Baking & Sweeteners
    "honey": 304,          # per 100g
    "maple_syrup": 260,    # per 100g
    "brown_sugar": 380,    # per 100g
    "white_sugar": 387,    # per 100g
    "corn_syrup": 286,     # per 100g
    "molasses": 290,       # per 100g

    # Spices & Herbs
    "salt": 0,             # per 1 tsp (5g)
    "pepper": 6,           # per 1 tsp (2.3g)
    "turmeric": 29,        # per 1 tsp (3g)
    "garlic_powder": 5,    # per 1 tsp (2.8g)
    "cinnamon": 6,         # per 1 tsp (2.6g)
    "ginger": 5,           # per 1 tsp (2.3g)

    # Miscellaneous
    "tofu": 70,            # per 100g
    "tempeh": 192,         # per 100g
    "seitan": 370,         # per 100g
    "hummus": 166,         # per 100g
    "kimchi": 15,          # per 100g
    "pickles": 12,         # per 100g
    "sauerkraut": 19,      # per 100g
    "popcorn": 375,        # per 100g (plain)
    "soy_milk": 33,        # per 100ml
    "almond_milk": 13,     # per 100ml
}

# Define healthiness thresholds
def is_healthy(calories, sugar, fat):
    """Assess if the recipe is healthy based on calorie and nutrient content"""
    if calories < 500 and sugar < 15 and fat < 15:
        return "Healthy"
    else:
        return "Unhealthy"

def get_recipe(ingredients):
    """Send a request to Hugging Face API to generate a recipe"""
    # Updated prompt with more detailed instructions for the model
    prompt = (
        f"Create a detailed recipe using these ingredients: {ingredients}. "
        "List the ingredients first, followed by step-by-step cooking instructions. "
        "Include measurements for the ingredients and cooking times for each step. "
        "Make sure the recipe is easy to follow and suitable for beginners."
    )
    
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"Error: {response.json()}"

def calculate_calories(ingredients):
    """Calculate total calories from the ingredients"""
    total_calories = 0
    for ingredient in ingredients.split(","):
        ingredient = ingredient.strip().lower()
        if ingredient in ingredient_calories:
            total_calories += ingredient_calories[ingredient]
        else:
            print(f"Warning: Nutritional information not available for {ingredient}")
    return total_calories

# Example usage
ingredients = input("Enter your ingredients (comma-separated): ")

# Generate recipe
recipe = get_recipe(ingredients)
print("\nGenerated Recipe:\n", recipe)

# Calculate calories
total_calories = calculate_calories(ingredients)
print("\nTotal Calories:", total_calories)

# Health assessment (for now, assume default values for sugar and fat)
health_status = is_healthy(total_calories, sugar=20, fat=10)  # Placeholder values for sugar and fat
print(f"The recipe is: {health_status}")
