import os
from flask import Flask, request, jsonify, send_file

from io import BytesIO
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
import typing
import IPython.display
import os
import json
from google.genai import types
from google import genai
import requests
from packages.config import portia
from packages.twitter import hash_trend
from packages.gen_ai import image_to_bytes, save_image, generate

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

            if encoded_image=='no image':
                return jsonify({"message":'Updated!' }), 200
            else:
                return jsonify({"image_data": encoded_image}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True)

