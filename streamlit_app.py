import streamlit as st
import requests
from PyPDF2 import PdfReader

# Function to call the POST API for processing notes
def call_post_api(endpoint, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(endpoint, headers=headers, json=data)
    return response.json()

# Function to call the GET API for retrieving processed notes
def call_get_api(endpoint):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(endpoint, headers=headers)
    return response.json()

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
        if transcript_file.type == "application/pdf":
            pdf_reader = PdfReader(transcript_file)
            transcript_content = "\n".join(page.extract_text() for page in pdf_reader.pages)
        else:
            transcript_content = transcript_file.read().decode("utf-8")

        sentences = transcript_content
        from typing import List, Union
        from pydantic import BaseModel
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
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                temperature=0.7,
                top_p = 0.67,
                frequency_penalty=0.5,
                messages=[
                    {"role": "system", "content": "You are a helpful psychologist who is expert at creating progress notes from sessions. Use the transcript provided to answer the questions. The transcript is a list of important sentences with the behavioural traits identified by a trait classification model. The traits are for your context. Do not mention the traits in any way"},
                    {"role": "user", "content": prompt + " ".join(sentences)}
                ],
                response_format=response_format,
            )
            return completion.choices[0].message.parsed

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

        # Loop through the tasks and fetch the corresponding completion
        for task_name, task_info in tasks.items():
            if task_name == "summary":
                summary = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.markdown(summary)
            elif task_name == "challenges":
                challenges = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.markdown(challenges)
            elif task_name == "symptoms":
                symptoms = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.markdown(symptoms)
            elif task_name == "assessment":
                assessment = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.markdown(assessment)
            elif task_name == "plan":
                plan = fetch_completion(task_info["format"], task_info["prompt"], sentences)
                st.markdown(plan) 

        

elif selected_option == "Treatment Plan":
    st.header("Treatment Plan - Demo")
    st.markdown("Upload a transcript from a therapy session and paste patient's EHR to process it into a detailed note")
    st.markdown("Note: The treatment plan does not include the context from behavioral markers and clinical assessments. These features require active patient input")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])
    ehr_data = st.text_area("Enter EHR Data (if available)")

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        response = call_post_api("http://example.com/treatment_plan", {"transcript": transcript_content, "ehr_data": ehr_data})
        
        # Display the treatment plan neatly
        st.subheader("Generated Treatment Plan")
        st.text(response.get("treatment_plan", "No response available"))

elif selected_option == "Copilot":
    st.header("Allia Copilot")
    st.markdown("This model is powered by Allia's proprietary language model. It responds with references to accurate academic literature spanning over 1M documents. It is still a work in progress and will be launched in January 2025")
    llm_option = st.selectbox("Choose LLM", ["OpenAI", "Claude", "Llama", "Allia"])
    chat_history = st.session_state.get("chat_history", [])

    user_input = st.text_input("You: ")
    if st.button("Send"):
        if user_input:
            chat_history.append(f"You: {user_input}")
            response = call_post_api(f"http://example.com/copilot/{llm_option.lower()}", {"user_input": user_input})
            reply = response.get("reply", "No response available")
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
        response = call_post_api("http://example.com/language_analysis", {"transcript": transcript_content})
        
        # Display the sentences and their labels
        st.subheader("Sentence Analysis")
        sentences = response.get("sentences", [])
        for sentence, label in sentences:
            st.write(f"{sentence} - **{label}**")

else:
    st.write("Please select a valid option from the sidebar.")
