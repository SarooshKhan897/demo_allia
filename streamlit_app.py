import streamlit as st
from typing import List
from pydantic import BaseModel

# Define all models
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

# Function to handle completions
def fetch_completion(response_format, prompt, sentences):
    # Mockup of processing function - Replace with actual logic as required
    return response_format(**{"session_focus": "Sample focus", "chief_complaint": "Sample complaint"})

# Dictionary to map response formats with respective prompts
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

# Streamlit app
st.title("Allia Health Demo")

# Sidebar Navigation
options = ["Notes", "Treatment Plan", "Copilot", "Language"]
selected_option = st.sidebar.selectbox("Select an Option", options)

if selected_option == "Notes":
    st.header("Progress Notes")
    st.markdown("Upload a transcript from a therapy session and Allia's models will automatically process it into a thorough progress note")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])

    if transcript_file is not None:
        # Read file content and convert to appropriate format if needed
        transcript_content = transcript_file.read().decode("utf-8")
        sentences = transcript_content.split('.')  # Example of splitting transcript into sentences

        # Loop through the tasks and fetch the corresponding completion
        for task_name, task_info in tasks.items():
            if task_name == "summary":
                summary = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.subheader("Session Summary")
                st.text(summary)
            elif task_name == "challenges":
                challenges = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.subheader("Challenges")
                st.text(challenges)
            elif task_name == "symptoms":
                symptoms = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.subheader("Symptoms")
                st.text(symptoms)
            elif task_name == "assessment":
                assessment = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.subheader("Assessment")
                st.text(assessment)
            elif task_name == "plan":
                plan = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.subheader("Plan")
                st.text(plan)

elif selected_option == "Treatment Plan":
    st.header("Treatment Plan - Demo")
    st.markdown("Upload a transcript from a therapy session and paste patient's EHR to process it into a detailed note")
    st.markdown("Note: The treatment plan does not include the context from behavioral markers and clinical assessments. These features require active patient input")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])
    ehr_data = st.text_area("Enter EHR Data (if available)")

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        st.subheader("Generated Treatment Plan")
        st.text("Treatment plan generation logic here...")

elif selected_option == "Copilot":
    st.header("Allia Copilot")
    st.markdown("This model is powered by Allia's proprietary language model. It responds with references to accurate academic literature spanning over 1M documents. It is still a work in progress and will be launched in January 2025")
    llm_option = st.selectbox("Choose LLM", ["OpenAI", "Claude", "Llama", "Allia"])
    chat_history = st.session_state.get("chat_history", [])

    user_input = st.text_input("You: ")
    if st.button("Send"):
        if user_input:
            chat_history.append(f"You: {user_input}")
            reply = "Generated response from copilot model..."  # Placeholder response
            chat_history.append(f"{llm_option}: {reply}")
            st.session_state["chat_history"] = chat_history

    st.subheader("Chat History")
    for message in chat_history:
        st.write(message)

elif selected_option == "Language":
    st.header("Language demo")
    st.markdown("Upload a therapy transcript and Allia's proprietary models will identify the key psychiatric traits and dimensional analysis of the patient. This exactly emulates the way a clinician thinks")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        st.subheader("Sentence Analysis")
        st.text("Language analysis logic here...")
else:
    st.write("Please select a valid option from the sidebar.")
