import streamlit as st
import requests
import time

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
            headers = {'Content-Type': 'application/json'}
            try:
                post_response = requests.post("https://api-stage.allia.health/api/clinician/note/process-temp", headers=headers, json=data)
                post_response.raise_for_status()
                post_result = post_response.json()
                st.subheader("Generated Progress Note")
                st.markdown(post_result.get("progress_note", "No response available"))
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed: {e}")
            except ValueError:
                st.error("Invalid JSON response from server")
                
            # Keep trying to get the processed notes via GET request until a valid response is received
            get_success = False
            while not get_success:
                try:
                    get_response = requests.get("https://api-stage.allia.health/api/clinician/note/process-temp", headers=headers)
                    get_response.raise_for_status()
                    get_result = get_response.json()
                    if get_result.get("progress_note"):
                        get_success = True
                        st.subheader("Retrieved Progress Note")
                        st.markdown(get_result.get("progress_note", "No response available"))
                    else:
                        time.sleep(2)  # Wait for 2 seconds before trying again
                except requests.exceptions.RequestException as e:
                    st.error(f"API request failed: {e}")
                    time.sleep(2)  # Wait for 2 seconds before trying again
                except ValueError:
                    st.error("Invalid JSON response from server")
                    time.sleep(2)  # Wait for 2 seconds before trying again

elif selected_option == "Treatment Plan":
    st.header("Treatment Plan - Demo")
    st.markdown("Upload a transcript from a therapy session and paste patient's EHR to process it into a detailed note")
    st.markdown("Note: The treatment plan does not include the context from behavioral markers and clinical assessments. These features require active patient input")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])
    ehr_data = st.text_area("Enter EHR Data (if available)")

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        data = {"transcript": transcript_content, "ehr_data": ehr_data}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post("http://example.com/treatment_plan", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            st.subheader("Generated Treatment Plan")
            st.text(result.get("treatment_plan", "No response available"))
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
        except ValueError:
            st.error("Invalid JSON response from server")

elif selected_option == "Copilot":
    st.header("Allia Copilot")
    st.markdown("This model is powered by Allia's proprietary language model. It responds with references to accurate academic literature spanning over 1M documents. It is still a work in progress and will be launched in January 2025")
    llm_option = st.selectbox("Choose LLM", ["OpenAI", "Claude", "Llama", "Allia"])
    chat_history = st.session_state.get("chat_history", [])

    user_input = st.text_input("You: ")
    if st.button("Send"):
        if user_input:
            chat_history.append(f"You: {user_input}")
            data = {"user_input": user_input}
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.post(f"http://example.com/copilot/{llm_option.lower()}", headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                reply = result.get("reply", "No response available")
            except requests.exceptions.RequestException as e:
                reply = f"API request failed: {e}"
            except ValueError:
                reply = "Invalid JSON response from server"
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
        data = {"transcript": transcript_content}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post("http://example.com/language_analysis", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            st.subheader("Sentence Analysis")
            sentences = result.get("sentences", [])
            for sentence, label in sentences:
                st.write(f"{sentence} - **{label}**")
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
        except ValueError:
            st.error("Invalid JSON response from server")
else:
    st.write("Please select a valid option from the sidebar.")
