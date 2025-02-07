'''
import requests

# Replace this with your Hugging Face API key
API_KEY = "Hanging_face_Api_Key"

# Use a publicly available model
MODEL_NAME = "tiiuae/falcon-7b-instruct"

# Hugging Face API endpoint
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_recipe(ingredients):
    """Send a request to Hugging Face API to generate a recipe"""
    # Updated prompt with more detailed instructions for the model
    prompt = (
        f"Create a detailed recipe using these ingredients: {ingredients}. "
        "List the ingredients first, followed by step-by-step cooking instructions. "
        "Include measurements for the ingredients and cooking times for each step. "
        "Make sure the recipe is easy to follow and suitable for beginners."
    )
    
    # Send the prompt to the Hugging Face API
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    
    # Handle the response and return the generated recipe
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"Error: {response.json()}"

# Example usage
ingredients = input("Enter your ingredients (comma-separated): ")
recipe = get_recipe(ingredients)
print("\nGenerated Recipe:\n", recipe)
'''