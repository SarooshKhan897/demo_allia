import streamlit as st
import requests
import json
from time import sleep
import openai
from typing import List
from pydantic import BaseModel
from openai import OpenAI
import streamlit as st
import openai
from typing import List
from typing import Dict
from typing import Optional
from pydantic import BaseModel

st.title('Allia health')

# Initialize OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()

# Define Pydantic models
class Summary(BaseModel):
    session_focus: str
    chief_complaint: str

class Challenge(BaseModel):
    challenge: str

class Challenges(BaseModel):
    challenges: List[Challenge]

class Symptoms(BaseModel):
    symptoms: Dict[str, Optional[str]]

class Assessment(BaseModel):
    risks_or_safety_concerns: str
    therapeutic_approach: str
    psychological_interventions: str

class Plan(BaseModel):
    follow_up_actions: str
    homework: str
    additional_notes: str

def remove_timestamps(transcript: str) -> str:
    lines = transcript.split('\n')
    cleaned_lines = [line.split(']')[1].strip() if ']' in line else line for line in lines]
    return '\n'.join(cleaned_lines)

def fetch_completion(response_format, prompt, sentences):
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        temperature=0.7,
        top_p=0.67,
        frequency_penalty=0.5,
        messages=[
            {"role": "system", "content": "You are a helpful psychologist who is expert at creating progress notes from sessions. Use the transcript provided to answer the questions in json. The transcript is a list of important sentences with the behavioural traits identified by a trait classification model. The traits are for your context. Do not mention the traits in any way"},
            {"role": "user", "content": prompt + " ".join(sentences)}
        ],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content

def call_api(transcript):
    # Process the transcript
    cleaned_transcript = remove_timestamps(transcript)
    sentences = cleaned_transcript.split('.')

    # Define tasks
    tasks = {
        "summary": {
            "format": Summary,
            "prompt": "Use the information shared to create a brief description of what was the focus of the session and a summary of the chief complaint as described by them. Ensure the response is clinical with a 60-70 on the Flesch-Kincaid reading scale. Avoid fancy adjectives."
        },
        "challenges": {
            "format": Challenges,
            "prompt": "Find three key challenges that the patient shared in the meeting. Mention specific statements that validate the challenges."
        },
        "symptoms": {
            "format": Symptoms,
            "prompt": "Can you extract important symptoms the patient has shared alongside specific information for each, broken down into sub-bullets. Only report what the patient has shared."
        },
        "assessment": {
            "format": Assessment,
            "prompt": "Add specific information regarding any risks or safety concerns, therapeutic approaches utilized, and psychological intervention techniques used during the meeting."
        },
        "plan": {
            "format": Plan,
            "prompt": "Explain if any follow-up actions or homework were discussed during the meeting. Feel free to mention any additional notes."
        }
    }

    # Process each task
    results = {}
    for task_name, task_info in tasks.items():
        results[task_name] = fetch_completion(task_info["format"], task_info["prompt"], sentences)

    return results

st.title("Therapy Session Analysis")

# Text area for transcript input
transcript = st.text_area("Enter the therapy session transcript:", height=200)

import json
def pretty_print_json(data, key, heading):
    st.subheader(heading)
    if isinstance(data, list):
        for i, item in enumerate(data):
            st.markdown(f"**{key} {i + 1}:**")
            for sub_key, sub_value in item.items():
                st.markdown(f"- **{sub_key}:** {sub_value}")
            st.markdown("---")
    elif isinstance(data, dict):
        for sub_key, sub_value in data.items():
            st.markdown(f"**{sub_key}:** {sub_value}")
    else:
        st.text(data)
    st.markdown("\n")
    


st.title("Progress Note")

st.title("Session Report Analysis")

if st.button("Analyze"):
    transcript = "Some transcript text here"  # Placeholder for transcript input
    if transcript:
        with st.spinner("Analyzing transcript..."):
            result = call_api(transcript)
        
        # Ensure result is a dictionary after parsing
        if isinstance(result, str):
            result = json.loads(result)
        
        # Display results
        if "summary" in result:
            pretty_print_json(result["summary"], key="summary", heading="Session Summary")

        if "challenges" in result and isinstance(result["challenges"], dict):
            challenges = result["challenges"].get("challenges", [])
            pretty_print_json(challenges, key="Challenge", heading="Client Challenges")

        if "symptoms" in result and isinstance(result["symptoms"], dict):
            symptoms = result["symptoms"].get("symptoms", [])
            pretty_print_json(symptoms, key="Symptom", heading="Reported Symptoms")

        if "assessment" in result and isinstance(result["assessment"], dict):
            pretty_print_json(result["assessment"], key="Assessment", heading="Assessment Details")

        if "plan" in result and isinstance(result["plan"], dict):
            pretty_print_json(result["plan"], key="Plan", heading="Follow-up Plan")
    else:
        st.warning("Please enter a transcript to analyze.")

# Instructions for GitHub deployment
st.sidebar.title("Deployment Instructions")
st.sidebar.write("""
1. Create a GitHub repository for your app.
2. Add this script as `app.py` in your repository.
3. Create a `requirements.txt` file with:
   ```
   streamlit
   openai
   pydantic
   ```
4. Add a `README.md` file with app description and setup instructions.
5. Replace 'your-api-key-here' in the OPENAI_API_KEY variable with your actual OpenAI API key.
6. Push your code to GitHub.
7. Set up GitHub Actions for automatic deployment or use a platform like Streamlit Sharing.

Note: Storing API keys directly in your code is not recommended for security reasons. 
In a production environment, consider using environment variables or secure secret management.
""")
