# 1) Create an AI agent and link to the backend
from langchain_core.tools import tool
from tools import query_medgemma, emergency_call
from config import GEMINI_API_KEY

@tool
def ask_mental_health_professional(query: str) -> str:
    """Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone"""
    return query_medgemma(query)


@tool
def emergency_tool_calling(phone: str):
    """Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help."""
    return emergency_call(phone)

@tool
def find_therapists_locationwise(location: str):
    """
    Finds and returns a list of licensed therapists near the specified location.
    Args:
        location(str): Name of the city or area where user is asking for therapy.
    Returns:
        str: Therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )

# create an ai agent and link it to the backend 
# from google import genai
# from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

tools = [ask_mental_health_professional, emergency_tool_calling, find_therapists_locationwise]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2, api_key=GEMINI_API_KEY)
graph = create_agent(llm, tools=tools)

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `locate_therapist_tool`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""

def parse_response(stream):
    final_response = None
    for s in stream:
        agent_data = s.get("agent")
        if agent_data:
            messages = agent_data.get("messages")
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response = msg.content
    return final_response

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        print("Received user input", {user_input[:200]})
        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
        stream = graph.stream(inputs, stream_mode="updates")
        final_response = parse_response(stream)
        print("answer:", final_response)