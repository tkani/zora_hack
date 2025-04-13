import os
from flask import Flask, request, jsonify, send_file
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps
from io import BytesIO
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
import typing
import IPython.display
import os
import json
from dotenv import load_dotenv
import base64
from google.genai import types
from google import genai

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
bearer_token1 ='AAAAAAAAAAAAAAAAAAAAAAE10gEAAAAA3pMA2HfKbr7BTJbmy9ouVy0W6KY%3DsUH4wi1m01vRpn3MRsX7oVqvG1XuKCW2UFwkRMPKwvquAZaRHD'

bearer_token2 ='AAAAAAAAAAAAAAAAAAAAAMI20gEAAAAAysuDAw5CHj3IL5G5vU%2FYZb9keg8%3Daatt6jyjQngINMWKTzuFPzafb0pY5JBAmqjflYxOjOmkNv0cQu'
bearer_token3 ='AAAAAAAAAAAAAAAAAAAAANI20gEAAAAACgEEwK6BX8JO5BI3BWPCdy8e%2BGY%3DLLdIpm0pnxwpktKehi6owvkJTKcVN4mwHiYAY4LZsmTgE26Ob8'
bearer_token4 ='AAAAAAAAAAAAAAAAAAAAAE820gEAAAAA6Lu0XKbbaF%2BYWNJ72o0AGjnby8k%3DldwO3II4SDU6DWI7XLF1VMexlHv8Wx7ypdQdvx7pA1O6XVhaxh' 
max_result=5
base_prompt=''

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

def hash_trend():
    # user_id = get_user_id(username)
        
    # ids={bearer_token1:'1802642686710837249',bearer_token2:'1852674305517342720',bearer_token3:'1876696076499222528',bearer_token4:'1856925315286601728'}
    ids={bearer_token3:'1876696076499222528',bearer_token4:'1856925315286601728'}
    #ids={bearer_token1:'1802642686710837249',bearer_token2:'1852674305517342720'}
    tweets_str=''

    for bearer_token, user_id in ids.items():
        bearer_token = str(bearer_token)
        user_id = str(user_id)
        try:
            print(f"Fetching tweets for user: {user_id} with token: {bearer_token}\n\n")
            tweets = get_user_tweets(user_id, bearer_token)
            print('tweets===================',tweets)
            for tweet in tweets['data']:
                tweet_text = tweet['text']
                tweets_str = tweets_str+ str(tweet['created_at']) +' '+str(tweet_text)
            print('==================================',tweets_str)
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            continue
    return tweets_str

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


# Combained image
def generate(user_image1,user_image2,final_prompt):
    client = genai.Client(
        vertexai=True,
        project="single-patrol-456519-c3",
        location="us-central1",
    )
    
    msg1_image1 = types.Part.from_bytes(
        data=base64.b64decode((user_image1)),
    mime_type="image/png",
    )

    msg1_image2 = types.Part.from_bytes(
    data=base64.b64decode((user_image2)),
    mime_type="image/png",
    )   

    msg1_text1=types.Part.from_text(text=final_prompt)

    model = "gemini-2.0-flash-exp"
    contents = [
    types.Content(
    role="user",
    parts=[
        msg1_image1,
        msg1_image2,
        msg1_text1
        ]
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
    temperature = 0.2,
    top_p = 0.95,
    seed = 0,
    max_output_tokens = 1024,
    response_modalities = ["TEXT", "IMAGE"],
    safety_settings = [types.SafetySetting(
    category="HARM_CATEGORY_HATE_SPEECH",
    threshold="OFF"
    ),types.SafetySetting(
    category="HARM_CATEGORY_DANGEROUS_CONTENT",
    threshold="OFF"
    ),types.SafetySetting(
    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
    threshold="OFF"
    ),types.SafetySetting(
    category="HARM_CATEGORY_HARASSMENT",
    threshold="OFF"
    )],
    )

    image_bytes = None
    for chunk in client.models.generate_content_stream(
        model = model,
        contents = contents,
        config = generate_content_config,
        ):
        for candidate in chunk.candidates:
            for part in candidate.content.parts:
                if hasattr(part, "inline_data") and part.inline_data:
                    image_bytes = part.inline_data.data
                elif hasattr(part, "text") and part.text:
                    print("Text:", part.text)
    
    if image_bytes:
        image = PIL_Image.open(BytesIO(image_bytes))
        image.save("generated_meme.png")
        return base64.b64encode(image_bytes).decode("utf-8")
    else:
        return 'no image'
    
    
    
# ============================================================ Main function =========================================
# Load environment variables if needed
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\projects\kani\Hackathon\single-patrol-456519-c3-0a1feab2fd15.json"

# Initialize Vertex AI
vertexai.init(project="single-patrol-456519-c3", location="us-central1")
generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

# Endpoint to generate meme image based on prompt
@app.route('/generate_meme', methods=['POST'])
def generate_meme():
    # base_prompt = request.args.get('prompt')
    data = request.get_json()

    if not data or 'prompt' not in data or 'image_data_1' not in data or 'image_data_2' not in data:
        return jsonify({"error": "Prompt and both image data are required in JSON body"}), 400

    base_prompt = data['prompt']
    image_data_1 = data['image_data_1']
    image_data_2 = data['image_data_2']

    if not base_prompt:
        return jsonify({"error": "Prompt is required"}), 400
    else:
        base_prompt=base_prompt

    # =============================================== unlock ==========================
    tweets_data=hash_trend()
#     tweets_data='''
#          tweet trend or anything similar: $MIND with keywords like Eradicate, Omnipotent, Entropy
# - meaning of the trend or similar: essence of user interests, intentions, or current focal points. Examining recurring themes unveils trends.Create a funny meme from these images
#         '''
    if tweets_data=='':
        return jsonify({"error": "No tweets data, may be api limit exceed"}), 500
    else:
        # Improved structured prompt
        base_X_prompt_= '''
                           
                                                    ---
                            \n\nbased on the tweets try to find out something.
                            Return the output in this format:
                            - tweet trend or anything similar: (only one)
                            - meaning of the trend or similar (only one)

                        '''
        prompt_ = str(tweets_data)+base_X_prompt_
        plan_run = portia.run(prompt_)
        plan_run_output = plan_run.model_dump_json(indent=2)
        if isinstance(plan_run_output, str):
            plan_run_output = json.loads(plan_run_output)

        print(json.dumps(plan_run_output, indent=2))
        try:
            trending_topic=plan_run_output['outputs']['final_output']['summary']
            print(trending_topic)
        except:
            trending_topic='Summary not found'

        if trending_topic=='Summary not found':
            return jsonify({"error": "Data not enough to summarize trending topic.."}), 500
        else:
            if base_prompt=='':
                return jsonify({"error": "Need base prompt from user"}), 500
            print('base_prompt:',base_prompt)

            # Generate images using the prompt
            final_prompt=trending_topic+str(base_prompt)
            print('final_prompt=======================',final_prompt)

            # =================================================================================
            # Text to image generation
            images = generation_model.generate_images(
                prompt=final_prompt,
                number_of_images=1,  # Only generate one image for simplicity
                aspect_ratio="1:1",
                negative_prompt="",
                person_generation="",
                safety_filter_level="",
                add_watermark=True,
            )

            encoded_image=generate(image_data_1,image_data_2,final_prompt)

            # =========================================================
            # print(f"Generated images: {images}") 
            # # Get the generated image
            # if not images:
            #     return jsonify({"error": "Image generation failed or returned no results."}), 500
            # generated_image = images[0]._pil_image  # Assuming the image is returned as a PIL image

            # # Save the image to a file
            # file_path = 'generated_meme_image.png'
            # save_image(generated_image, file_path)

            # # Convert the image to bytes for API response
            # image_bytes = image_to_bytes(generated_image)

            # encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            if encoded_image=='no image':
                return jsonify({"message":'Updated!' }), 200
            else:
                return jsonify({"image_data": encoded_image}), 500

            # Return the image as a response
            # return send_file(BytesIO(image_bytes), mimetype='image/png', as_attachment=True, download_name='generated_meme_image.png')


    
# =============================================== Endpoint to generate meme image based on prompt =======================
@app.route('/base_trend', methods=['GET'])
def base_trend():
    global base_prompt
    try:
        # Get JSON data from the request
        prompt = request.args.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        else:
            base_prompt=prompt
            return jsonify({"message":'Updated!' }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =============================================== Endpoint to generate meme image based on prompt =======================

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True)

