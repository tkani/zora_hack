
from dotenv import load_dotenv
import os
from portia import (
    Config,
    LLMModel,
    LLMProvider,
    Portia,
    example_tool_registry,
)

load_dotenv()

# =================================== Twitter api's ===========================
# Replace with your Bearer Token
bearer_token1 ='AAAAAAAAAAAAAAAAAAAAAAE10gEAAAAA3pMA2HfKbr7BTJbmy9ouVy0W6KY%3DsUH4wi1m01vRpn3MRsX7oVqvG1XuKCW2UFwkRMPKwvquAZaRHD'
bearer_token2 ='AAAAAAAAAAAAAAAAAAAAAMI20gEAAAAAysuDAw5CHj3IL5G5vU%2FYZb9keg8%3Daatt6jyjQngINMWKTzuFPzafb0pY5JBAmqjflYxOjOmkNv0cQu'
bearer_token3 ='AAAAAAAAAAAAAAAAAAAAANI20gEAAAAACgEEwK6BX8JO5BI3BWPCdy8e%2BGY%3DLLdIpm0pnxwpktKehi6owvkJTKcVN4mwHiYAY4LZsmTgE26Ob8'
bearer_token4 ='AAAAAAAAAAAAAAAAAAAAAE820gEAAAAA6Lu0XKbbaF%2BYWNJ72o0AGjnby8k%3DldwO3II4SDU6DWI7XLF1VMexlHv8Wx7ypdQdvx7pA1O6XVhaxh' 
max_result=5
base_prompt=''

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')



# =================================== Gen AI =========================
# Create a default Portia config with LLM provider set to Google GenAI and model set to Gemini 2.0 Flash
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
    llm_model_name=LLMModel.GEMINI_2_0_FLASH,
    google_api_key=GOOGLE_API_KEY
)

# Instantiate a Portia instance. Load it with the config and with the example tools.
portia = Portia(config=google_config, tools=example_tool_registry)
