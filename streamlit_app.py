import streamlit as st
import requests
import json
from time import sleep
import openai
from typing import List
from pydantic import BaseModel

st.title('🎈Allia health')

# WARNING: Storing API keys directly in your code is not recommended for security reasons.
# In a production environment, use environment variables or secure secret management.
OPENAI_API_KEY = "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"  # Replace with your actual OpenAI API key

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Define Pydantic models
class Summary(BaseModel):
    session_focus: str
    chief_complaint: str

class Challenge(BaseModel):
    challenge_heading: str
    challenge_description: str

class Challenges(BaseModel):
    challenges: List[Challenge]

class Symptom(BaseModel):
    symptom_heading: str
    symptom_frequency: str
    symptom_description: str

class Symptoms(BaseModel):
    symptoms: List[Symptom]

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
            {"role": "system", "content": "You are a helpful psychologist who is expert at creating progress notes from sessions. Use the transcript provided to answer the questions. The transcript is a list of important sentences with the behavioural traits identified by a trait classification model. The traits are for your context. Do not mention the traits in any way"},
            {"role": "user", "content": prompt + " ".join(sentences)}
        ],
        response_format={"type": "json_object"}
    )
    return response_format.parse_raw(completion.choices[0].message.content)

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

if st.button("Analyze"):
    if transcript:
        with st.spinner("Analyzing transcript..."):
            result = call_api(transcript)
        
        # Display results
        st.subheader("Summary")
        st.write(f"Session Focus: {result['summary'].session_focus}")
        st.write(f"Chief Complaint: {result['summary'].chief_complaint}")

        st.subheader("Challenges")
        for challenge in result['challenges'].challenges:
            st.write(f"- {challenge.challenge_heading}: {challenge.challenge_description}")

        st.subheader("Symptoms")
        for symptom in result['symptoms'].symptoms:
            st.write(f"- {symptom.symptom_heading}")
            st.write(f"  Frequency: {symptom.symptom_frequency}")
            st.write(f"  Description: {symptom.symptom_description}")

        st.subheader("Assessment")
        st.write(f"Risks or Safety Concerns: {result['assessment'].risks_or_safety_concerns}")
        st.write(f"Therapeutic Approach: {result['assessment'].therapeutic_approach}")
        st.write(f"Psychological Interventions: {result['assessment'].psychological_interventions}")

        st.subheader("Plan")
        st.write(f"Follow-up Actions: {result['plan'].follow_up_actions}")
        st.write(f"Homework: {result['plan'].homework}")
        st.write(f"Additional Notes: {result['plan'].additional_notes}")
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
