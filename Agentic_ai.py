import requests 
import os
from dotenv import load_dotenv

load_dotenv()

# groq_api_key = requests.get("Groq_api")
groq_api_key = os.getenv("GROQ_API_KEY")
# chatgpt_api_key = requests.get("Chatgpt_api")
chatgpt_api_key = os.getenv("CHATGPT_API_KEY")
# taveliy_api_key = requests.get("tavely_api")
tavily_api_key = os.getenv("TAVILY_API_KEY")

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_tavily import TavilySearchResults
# from langchain_community.tools.tavily_search import TavilySearch
from langchain_tavily import TavilySearch

open_ai = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=chatgpt_api_key)
groq_ai = ChatGroq(model="llama-3.3-70b-versatile",temperature=0.1, api_key=groq_api_key)

search_tool = TavilySearch(max_results=2)

from langgraph.prebuilt import create_react_agent 
from langchain_core.messages import HumanMessage, AIMessage

# system_prompt = "Act as an friendly ai agent"

def get_response_from_ai(llm_id, query, allow_search, model_provider,system_prompt):
    """
    Function to get response from AI based on the provided parameters.
    """
    if model_provider == "groq":
        llm = ChatGroq(model=llm_id, temperature=0.1, api_key=groq_api_key)
    elif model_provider == "openai":
        llm = ChatOpenAI(model=llm_id, temperature=0.1, api_key=chatgpt_api_key)
    else:
        raise ValueError("Unsupported model provider")

    tools = [TavilySearch(max_results=2)] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=tools,
        # state_modifier=system_prompt
    )

    # query = "Road map of becoming an ai engineer in 2025"
    state = {
        "messages":[
            {"role": "system", "content": system_prompt or "You are a helpful AI assistant."},
            *query
        ]
    }
    response = agent.invoke(state)
    message = response.get("messages")
    ai_message = [message.content for message in message if isinstance(message, AIMessage)]
    return ai_message[-1]
