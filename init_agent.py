import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, ModelSettings, OpenAIChatCompletionsModel

load_dotenv(override=True)

defaultModel = "gpt-4o-mini"

def setModel(model: str):
    global defaultModel
    defaultModel = model
    print(f"Model set to {model}")

MODELS = {
    "gpt-4o-mini": {
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }, 
    "deepseek-chat": {
        "base_url": "https://api.deepseek.com/v1",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
    },
}

def initAgent(name: str, instructions: str, tools=[], model_settings=ModelSettings(), output_type=None):
    
    base_url = MODELS[defaultModel]["base_url"]
    api_key = MODELS[defaultModel]["api_key"]

    print(f"initAgent: {name}, {defaultModel}")

    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    model = OpenAIChatCompletionsModel(model=defaultModel, openai_client=client)


    agent_args = {
        "name": name,
        "instructions": instructions,
        "model": defaultModel,
        "tools": tools,
        "model_settings": model_settings,
        "model": model,
    }

    if output_type is not None:
        agent_args["output_type"] = output_type

    return Agent(**agent_args)