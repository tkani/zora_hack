
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps
import base64
from io import BytesIO
from google.genai import types
from google import genai

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
    
    
    