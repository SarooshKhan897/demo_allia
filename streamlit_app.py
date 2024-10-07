import streamlit as st

st.title('🎈Allia health')

st.write('This app demonstrate's Allia's core capabilities!')

import streamlit as st
import requests
import json
from time import sleep

def call_api(transcript):
    # Simulate API call with a delay
    sleep(3)
    # Replace this with your actual API call
    response = {
        "summary": "This is a summary of the therapy session.",
        "key_points": [
            "Patient expressed anxiety about work",
            "Discussed coping mechanisms",
            "Set goals for next week"
        ],
        "sentiment": "Generally positive"
    }
    return response

st.title("Therapy Session Analysis")

# Text area for transcript input
transcript = st.text_area("Enter the therapy session transcript:", height=200)

if st.button("Analyze"):
    if transcript:
        with st.spinner("Analyzing transcript..."):
            # Call API (simulated)
            result = call_api(transcript)
        
        # Pretty print the result
        st.subheader("Analysis Results:")
        st.json(result)
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
   requests
   ```
4. Add a `README.md` file with app description and setup instructions.
5. Push your code to GitHub.
6. Set up GitHub Actions for automatic deployment or use a platform like Streamlit Sharing.
""")
