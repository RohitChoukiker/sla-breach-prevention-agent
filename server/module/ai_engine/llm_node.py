import vertexai
from vertexai.generative_models import GenerativeModel
import json
import os

vertexai.init(
    project=os.getenv("GCP_PROJECT"),
    location="us-central1"
)

model = GenerativeModel("gemini-1.5-flash")

def llm_reasoning(state):

    prompt = f"""
    Ticket: {state['description']}
    Urgency: {state['urgency']}
    Similar count: {state['similar_count']}

    Predict breach_probability (0-1) and confidence (0-1).
    Return JSON.
    """

    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text)

        state["breach_probability"] = float(result["breach_probability"])
        state["confidence_score"] = float(result["confidence"])

    except Exception as e:
        print("[LLM ERROR]", e)
        state["breach_probability"] = 0.4
        state["confidence_score"] = 0.7

    return state
