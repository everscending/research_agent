from agents import Agent, ModelSettings

def initAgent(name: str, instructions: str, tools=[], model_settings=ModelSettings(), output_type=None):
    agent_args = {
        "name": name,
        "instructions": instructions,
        "model": "gpt-4o-mini",
        "tools": tools,
        "model_settings": model_settings,
        # "output_type": output_type,
    }

    # if tools is not None:
    #     agent_args["tools"] = tools

    # if model_settings is not None:
    #     agent_args["model_settings"] = model_settings

    if output_type is not None:
        agent_args["output_type"] = output_type

    return Agent(**agent_args)