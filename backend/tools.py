# 1) Setup Ollama with MedGemma tool
import ollama
def query_medgemma(prompt: str):
    """Calls MedGemma model with a therapist personality.
    Return the response as a mental health professional."""

    system_prompt = """You are Dr. Emily Hartman, a compassionate and experienced clinical psychologist
    Respond to patients with:
    1) Emotional attunement("I can sense how difficult this must be for you...")
    2) Gentle Normalization("Many people feel this way when...")
    3) Practical Guidance("What sometimes helps is...")
    4) Strengths-focused support("I notice how you are...")
    
    Key princeples:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """
    
    try:
        response = ollama.chat(
            model='alibayram/medgemma:4b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                'num_predict': 350,  # Slightly higher for structured responses
                'temperature': 0.7,  # Balanced creativity/accuracy
                'top_p': 0.9        # For diverse but relevant responses
            }
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"I'm having technical difficulties currently. Please try again shortly."

# print(query_medgemma(prompt = "What is the difference between depression and anxiety ?"))
    
# 2) Setup Twillio calling API tool
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

def emergency_call():
    """Initiate an emergency call to the user's number"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
        to=EMERGENCY_CONTACT,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"  # Can customize message
    )
        return f"Emergency call initiated"
    except Exception as e:
        return f"Failed to initiate emergency call: {str(e)}"

emergency_call()
# 3) Setup Location tool