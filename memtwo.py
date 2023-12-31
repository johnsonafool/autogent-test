"""Example of how to add MemGPT into an AutoGen groupchat

Based on the official AutoGen example here: https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb

Begin by doing:
  pip install "pyautogen[teachable]"
  pip install pymemgpt
  or
  pip install -e . (inside the MemGPT home directory)
"""

import os
import autogen
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

config_list = [
    {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
]

# If USE_MEMGPT is False, then this example will be the same as the official AutoGen repo (https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb)
# If USE_MEMGPT is True, then we swap out the "coder" agent with a MemGPT agent
USE_MEMGPT = False
# If DEBUG is False, a lot of MemGPT's inner workings output is suppressed and only the final send_message is displayed.
# If DEBUG is True, then all of MemGPT's inner workings (function calls, etc.) will be output.
DEBUG = False

llm_config = {"config_list": config_list, "seed": 42}

# The user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE",  # needed?
)

# The agent playing the role of the product manager (PM)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)

if not USE_MEMGPT:
    # In the AutoGen example, we create an AssistantAgent to play the role of the coder
    coder = autogen.AssistantAgent(
        name="Coder",
        llm_config=llm_config,
    )

else:
    # In our example, we swap this AutoGen agent with a MemGPT agent
    # This MemGPT agent will have all the benefits of MemGPT, ie persistent memory, etc.
    coder = create_autogen_memgpt_agent(
        "MemGPT_coder",
        persona_description="I am a 10x engineer, trained in Python. I was the first engineer at Uber (which I make sure to tell everyone I work with).",
        user_description=f"You are participating in a group chat with a user ({user_proxy.name}) and a product manager ({pm.name}).",
        interface_kwargs={"debug": DEBUG},
    )

# Initialize the group chat between the user and two LLM agents (PM and coder)
groupchat = autogen.GroupChat(agents=[user_proxy, pm, coder], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Begin the group chat with a message from the user
user_proxy.initiate_chat(
    manager,
    message="I want to design an app to make me one million dollars in one month. Yes, your heard that right.",
)
