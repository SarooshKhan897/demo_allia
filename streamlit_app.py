import streamlit as st
import requests

# Function to call an API for processing

def call_api(endpoint, data):
    # Replace with your actual API endpoint and handle the response appropriately
    response = requests.post(endpoint, json=data)
    return response.json()

# Streamlit app
st.title("Allia Health - Demo")

# Sidebar Navigation
options = ["Notes", "Treatment Plan", "Copilot", "Language"]
selected_option = st.sidebar.selectbox("Select an Option", options)

if selected_option == "Notes":
    st.header("Upload Therapy Transcript for Progress Notes")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])

    if transcript_file is not None:
        # Read file content and convert to appropriate format if needed
        transcript_content = transcript_file.read().decode("utf-8")
        response = call_api("http://example.com/notes", {"transcript": transcript_content})
        
        # Display the progress note neatly
        st.subheader("Generated Progress Note")
        st.text(response.get("progress_note", "No response available"))

elif selected_option == "Treatment Plan":
    st.header("Upload Therapy Transcript and EHR Data for Treatment Plan")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])
    ehr_data = st.text_area("Enter EHR Data (if available)")

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        response = call_api("http://example.com/treatment_plan", {"transcript": transcript_content, "ehr_data": ehr_data})
        
        # Display the treatment plan neatly
        st.subheader("Generated Treatment Plan")
        st.text(response.get("treatment_plan", "No response available"))

elif selected_option == "Copilot":
    st.header("Chat Copilot")
    user_input = st.text_input("Enter your query")
    if st.button("Ask Copilot"):
        response = call_api("http://example.com/copilot", {"user_input": user_input})
        
        # Display the response from Copilot
        st.subheader("Copilot Response")
        st.text(response.get("reply", "No response available"))

elif selected_option == "Language":
    st.header("Upload Therapy Transcript for Sentence Analysis")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        response = call_api("http://example.com/language_analysis", {"transcript": transcript_content})
        
        # Display the sentences and their labels
        st.subheader("Sentence Analysis")
        sentences = response.get("sentences", [])
        for sentence, label in sentences:
            st.write(f"{sentence} - **{label}**")

else:
    st.write("Please select a valid option from the sidebar.")
