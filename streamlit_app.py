import streamlit as st
import requests

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
        transcript_content = transcript_file.read().decode("utf-8")
        
        # Prepare data for POST request
        data = {
            "transcript": transcript_content
        }
        
        # Send POST request to process the note
        if st.button("Process Transcript"):
            response = call_post_api("https://api-stage.allia.health/api/clinician/note/process-temp", data)
            
            # Display the progress note neatly
            st.subheader("Generated Progress Note")
            st.markdown(response.get("progress_note", "No response available"))
        
        # Automatically get the processed notes via GET request
        response = call_get_api("https://api-stage.allia.health/api/clinician/note/process-temp")
        
        # Display the retrieved note
        st.subheader("Retrieved Progress Note")
        st.markdown(response.get("progress_note", "No response available"))

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
