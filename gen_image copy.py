import os
from flask import Flask, request, jsonify, send_file
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps
from io import BytesIO
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
import typing
import IPython.display
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from portia import (
    Config,
    LLMModel,
    LLMProvider,
    Portia,
    example_tool_registry,
)

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# =================================== Twitter api's ===========================
import requests

# Replace with your Bearer Token
bearer_token1 ='AAAAAAAAAAAAAAAAAAAAAE820gEAAAAA6Lu0XKbbaF%2BYWNJ72o0AGjnby8k%3DldwO3II4SDU6DWI7XLF1VMexlHv8Wx7ypdQdvx7pA1O6XVhaxh'

bearer_token2 ='AAAAAAAAAAAAAAAAAAAAAMI20gEAAAAAysuDAw5CHj3IL5G5vU%2FYZb9keg8%3Daatt6jyjQngINMWKTzuFPzafb0pY5JBAmqjflYxOjOmkNv0cQu'
bearer_token3 = 'AAAAAAAAAAAAAAAAAAAAANI20gEAAAAACgEEwK6BX8JO5BI3BWPCdy8e%2BGY%3DLLdIpm0pnxwpktKehi6owvkJTKcVN4mwHiYAY4LZsmTgE26Ob8'
bearer_token4 = 'AAAAAAAAAAAAAAAAAAAAAAE10gEAAAAA6RlNYT70q%2F2KzqlDBNM3XkpLiS0%3DkDxyCD6ZINl8Lbq3HcfoissHnM5YpE4rIqL5n9uYt3ahovG3Y4' 
max_result=2

# =================================== Gen AI =========================
# Create a default Portia config with LLM provider set to Google GenAI and model set to Gemini 2.0 Flash
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
    llm_model_name=LLMModel.GEMINI_2_0_FLASH,
    google_api_key=GOOGLE_API_KEY
)

# Instantiate a Portia instance. Load it with the config and with the example tools.
portia = Portia(config=google_config, tools=example_tool_registry)


def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token1}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']['id']

def get_user_tweets(user_id,bearer_tokens, max_results=max_result):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    print(url)
    headers = {"Authorization": f"Bearer {bearer_tokens}"}
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,text"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Function to convert image to bytes
def image_to_bytes(image: PIL_Image.Image) -> bytes:
    byte_io = BytesIO()
    image.save(byte_io, format='PNG')  # Save image as PNG
    byte_io.seek(0)  # Go to the beginning of the byte stream
    return byte_io.read()  # Return image bytes

# Function to save the image to a file
def save_image(image: PIL_Image.Image, file_path: str) -> None:
    image.save(file_path, format='PNG')  # Save image to the specified path
    print(f"Image saved as {file_path}")

# Load environment variables if needed
# load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\projects\kani\Hackathon\single-patrol-456519-c3-0a1feab2fd15.json"

# Initialize Vertex AI
vertexai.init(project="single-patrol-456519-c3", location="us-central1")
generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

# Endpoint to generate meme image based on prompt
@app.route('/generate_meme', methods=['GET'])
def generate_meme():
    tweets_data=hash_trend()
    if tweets_data=='':
        return jsonify({"error": "An error occurred"}), 500
    else:
        # Improved structured prompt
        user_prompt = request.args.get('prompt', '')
        prompt_ = str(tweets_data)+user_prompt

    plan_run = portia.run(prompt)
    # Get the 'prompt' query parameter from the URL

    if user_prompt == '':
        user_prompt='''
        I would like to generate a cool meme image based on the following input:

        Tweet Trend: Trump and China trade tariffs

        Meaning of the Trend: China has increased tariff rates.

        I want to combine two or more images related to this trend, merging them into a meme with vibrant colors and large images. Add a funny dialogue that fits the theme and makes the meme fun and engaging.
        '''
    else:
        user_prompt=user_prompt

    # Generate images using the prompt
    images = generation_model.generate_images(
        prompt=user_prompt,
        number_of_images=1,  # Only generate one image for simplicity
        aspect_ratio="1:1",
        negative_prompt="",
        person_generation="",
        safety_filter_level="",
        add_watermark=True,
    )

    # Get the generated image
    generated_image = images[0]._pil_image  # Assuming the image is returned as a PIL image

    # Save the image to a file
    file_path = 'generated_meme_image.png'
    save_image(generated_image, file_path)

    # Convert the image to bytes for API response
    image_bytes = image_to_bytes(generated_image)

    # Return the image as a response
    return send_file(BytesIO(image_bytes), mimetype='image/png', as_attachment=True, download_name='generated_meme_image.png')

# Endpoint to generate meme image based on prompt
@app.route('/hash_trend', methods=['GET'])
def hash_trend():
    # user_id = get_user_id(username)
        
    ids={bearer_token1:'1802642686710837249',bearer_token2:'1852674305517342720',bearer_token3:'test',bearer_token4:'test'}
    tweets_str=''

    for bearer_token, user_id in ids.items():
        try:
            print(f"Fetching tweets for user: {user_id} with token: {bearer_token}")
            tweets = get_user_tweets(user_id, bearer_token)
            for tweet in tweets['data']:
                tweet_text = tweet['text']
                tweets_str += f"{tweet['created_at']} - {tweet_text}\n"
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            continue
    return tweets_str
    
# Endpoint to generate meme image based on prompt
@app.route('/base_trend', methods=['POST'])
def base_trend():

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True)



# # Define the base URL of your Flask API
# base_url = "http://127.0.0.1:5000/generate_meme"

# # Define a prompt for testing
# test_prompt = "Create a funny meme about Trump and China trade tariffs, with vibrant colors and witty dialogue."

# # Encode the prompt into the query parameter (URL encoding)
# params = {
#     "prompt": test_prompt
# }

# # Send a GET request to the Flask API with the prompt
# response = requests.get(base_url, params=params)