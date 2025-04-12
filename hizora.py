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

# Create a default Portia config with LLM provider set to Google GenAI and model set to Gemini 2.0 Flash
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE_GENERATIVE_AI,
    llm_model_name=LLMModel.GEMINI_2_0_FLASH,
    google_api_key=GOOGLE_API_KEY
)
# Instantiate a Portia instance. Load it with the config and with the example tools.
portia = Portia(config=google_config, tools=example_tool_registry)

# Improved structured prompt
prompt = '''
You are a social media AI assistant.

--
hello from the future, things are better than you could have ever imagined

 2025-04-11T20:53:21.000Z
 intention &gt;&gt; reality; what we think, we become

 2025-04-11T18:45:13.000Z
 fucking the earth is the key to saving it

 2025-04-11T16:37:15.000Z
 i had a weird feeling the other day, i was at the park and i saw a guy playing fetch with his dog. but when the dog brought the ball back, instead of giving it back to the owner, it ran up to me and dropped it at my feet. i was taken aback, but i picked it up and threw it for the     

 2025-04-11T14:29:24.000Z
 (￣▽￣)

 ---
Return the output in this format:
- tweet trend (only one)
- meaning of the trend (only one)

'''


# Run the test query and print the output!
plan_run = portia.run(prompt)
print(plan_run.model_dump_json(indent=2))