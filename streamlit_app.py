import streamlit as st
import requests

# Function to call an API for processing
def call_api(endpoint, data):
    # Replace with your actual API endpoint and handle the response appropriately
    response = requests.post(endpoint, json=data)
    return response.json()
sample = "<h1>Session Overview</h1><p>The session focused on exploring the patient's current emotional state and identifying any stressors contributing to their anxiety levels. The therapist aimed to understand the root causes of the patient's discomfort and discuss potential coping strategies.</p><h2>Chief Complaint</h2><p>The patient expressed feelings of persistent anxiety and occasional panic attacks. They reported difficulty concentrating at work, leading to decreased productivity. The patient also mentioned experiencing trouble sleeping, often waking up in the middle of the night with racing thoughts.</p><h2>Key Challenges</h2><ol>  <li><strong>Managing Medication Side Effects</strong>  <p>The patient expressed difficulty in dealing with the side effects of their medication. They mentioned, \"I've been feeling constantly nauseous and dizzy since I started this new medication.\" This indicates a significant challenge in managing their treatment plan effectively.</p>  </li>  <li><strong>Difficulty in Maintaining a Healthy Diet</strong>  <p>During the meeting, the patient shared concerns about their diet, stating, \"I find it hard to stick to a healthy eating plan with my busy schedule.\" This highlights a struggle to maintain nutritional goals amidst daily life demands.</p>  </li>  <li><strong>Emotional Strain and Stress Management</strong>  <p>The patient discussed feelings of stress and emotional strain, saying, \"I often feel overwhelmed and anxious about my health condition.\" This statement reflects the mental health challenges they are facing alongside their physical health issues.</p>  </li></ol><h2>Risks or Safety Concerns</h2><ol>  <li><strong>Confidentiality Breach</strong>    <ul>      <li>Risk of sensitive information being shared outside the meeting.</li>      <li>Ensure all participants understand and commit to confidentiality agreements.</li>    </ul>  </li>  <li><strong>Emotional Distress</strong>    <ul>      <li>Discussions may trigger emotional responses in some individuals.</li>      <li>Have a mental health professional available for immediate support if needed.</li>    </ul>  </li>  <li><strong>Miscommunication</strong>    <ul>      <li>Risk of misunderstandings leading to misinterpretation of discussed topics.</li>      <li>Encourage open communication and provide summaries or minutes post-meeting to clarify points discussed.</li>    </ul>  </li></ol><h2>Therapeutic Approach</h2><ol>  <li><strong>Cognitive Behavioral Therapy (CBT)</strong>  <p>Utilized to help participants recognize and alter negative thought patterns that may arise during discussions.</p>  </li>  <li><strong>Mindfulness-Based Stress Reduction (MBSR)</strong>  <p>Implemented to help individuals remain present, reducing anxiety about past or future topics discussed in the meeting.</p>  </li>  <li><strong>Solution-Focused Brief Therapy (SFBT)</strong>  <p>Focused on identifying solutions rather than dwelling on problems, fostering a positive outcome-oriented mindset among participants.</p>  </li></ol><h2>Psychological Interventions</h2><ol>  <li><strong>Active Listening Techniques</strong>  <p>Encouraging all participants to engage in active listening, ensuring everyone feels heard and understood, which can prevent misunderstandings and foster a supportive environment.</p>  </li>  <li><strong>Guided Imagery</strong>  <p>Used as a relaxation technique during breaks or when tension arises, helping participants visualize calming scenarios to reduce stress levels.</p>  </li>  <li><strong>Role-Playing Exercises</strong>  <p>Participants may engage in role-playing scenarios to practice responses to potential real-life situations discussed during the meeting, enhancing preparedness and confidence.</p>  </li></ol><h2>Plan</h2><h3>Follow-Up Actions</h3><p>Based on the provided transcript, it appears that no specific follow-up actions were discussed during the meeting. It is important to review any meeting notes or recordings to ensure that nothing was overlooked.</p><h4>Suggested Follow-Up Actions:</h4><ol>  <li>Review Meeting Minutes: Ensure all participants have access to the meeting minutes for reference.</li>  <li>Assign Tasks: If there were topics that required further action, assign tasks to relevant team members.</li>  <li>Schedule Next Meeting: Determine if a follow-up meeting is necessary and schedule accordingly.</li>  <li>Feedback Collection: Gather feedback from attendees on the meeting's effectiveness and areas for improvement.</li></ol><h3>Homework</h3><p>The transcript does not explicitly mention any homework assignments or tasks given to attendees post-meeting. However, it's good practice to:</p><ol>  <li>Reflect on Discussion Points: Attendees should review their notes and reflect on any topics discussed that require individual attention or research.</li>  <li>Prepare for Next Steps: Depending on their role in the project or discussion, participants might need to prepare materials or reports for future meetings.</li>  <li>Share Insights: Encourage team members to share insights or findings related to the meeting topics with their peers.</li></ol><h3>Additional Notes</h3><p>While the transcript only indicates that the meeting ended, here are some additional considerations:</p><ul>  <li>Meeting Summary: If not already done, summarize key points discussed during the meeting for clarity and record-keeping.</li>  <li>Clarification Requests: Encourage attendees who may have questions about what was discussed to reach out for clarification.</li>  <li>Open Communication Channels: Ensure open lines of communication among team members so they can discuss any arising issues related to the meeting topics.</li></ul>"
# Streamlit app
st.title("Allia health demo")


# Sidebar Navigation
options = ["Notes", "Treatment Plan", "Copilot", "Language"]
selected_option = st.sidebar.selectbox("Select an Option", options)

if selected_option == "Notes":
    st.header("Progress Notes")
    st.markdown("Upload a transcript from a therapy session and Allia's models with automatically process it into a thorough progress note")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])

    if transcript_file is not None:
        # Read file content and convert to appropriate format if needed
        transcript_content = transcript_file.read().decode("utf-8")
        response = call_api("http://example.com/notes", {"transcript": transcript_content})
        
        # Display the progress note neatly
        st.subheader("Generated Progress Note")
        st.markdown(response.get("progress_note", "No response available"))

elif selected_option == "Treatment Plan":
    st.header("Treatment Plan - Demo")
    st.markdown("Upload a transcript from a therapy session and paste patient's EHR to process it into a detailed note")
    st.markdown("Note: The treatment plan does not include the context from behavioural markers and clinical assessments. These features require an active patient input")
    transcript_file = st.file_uploader("Upload a Transcript File (txt/pdf)", type=["txt", "pdf"])
    ehr_data = st.text_area("Enter EHR Data (if available)")

    if transcript_file is not None:
        transcript_content = transcript_file.read().decode("utf-8")
        response = call_api("http://example.com/treatment_plan", {"transcript": transcript_content, "ehr_data": ehr_data})
        
        # Display the treatment plan neatly
        st.subheader("Generated Treatment Plan")
        st.text(response.get("treatment_plan", "No response available"))

elif selected_option == "Copilot":
    st.header("Allia Copilot")
    st.markdown("This model is powered by Allia's proprietary language model. It responsds with references accurate academic literature spanning over 1M documents. It is still a work in progress and will be launched in January 2025")
    llm_option = st.selectbox("Choose LLM", ["OpenAI", "Claude", "Llama", "Allia"])
    chat_history = st.session_state.get("chat_history", [])

    user_input = st.text_input("You: ")
    if st.button("Send"):
        if user_input:
            chat_history.append(f"You: {user_input}")
            response = call_api(f"http://example.com/copilot/{llm_option.lower()}", {"user_input": user_input})
            reply = response.get("reply", "No response available")
            chat_history.append(f"{llm_option}: {reply}")
            st.session_state["chat_history"] = chat_history

    st.subheader("Chat History")
    for message in chat_history:
        st.write(message)

elif selected_option == "Language":
    st.header("Language demo")
    st.markdown("Upload a therapy transcript and Allia's proprietory models will identify the key psychiatric traits and dimensional anaysis of the patient. This exactly emulates the way a clinician  thinks")
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
