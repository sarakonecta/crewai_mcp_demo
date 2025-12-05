import streamlit as st
import requests
import time


# Tech Stack Validator - CrewAI Integration
# This Streamlit app interfaces with a deployed CrewAI crew to analyze 
# and provide technology adoption recommendations.


# Configuration from Streamlit secrets
CREW_URL = st.secrets["CREW_URL"]
BEARER_TOKEN = st.secrets["BEARER_TOKEN"]

st.set_page_config(page_title="Tech Stack Validator")

st.title("Tech Stack Validator")
st.write("Enter a technology name to get an adoption recommendation.")

technology = st.text_input("Technology name:", placeholder="e.g., CrewAI, Next.js, FastAPI")

if st.button("Analyze", type="primary"):
    if not technology.strip():
        st.warning("Please enter a technology name.")
        st.stop()
    
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Step 1: Kickoff the CrewAI execution
    with st.spinner(f"Starting analysis for {technology}..."):
        response = requests.post(
            f"{CREW_URL}/kickoff",
            headers=headers,
            json={"inputs": {"technology": technology}}
        )
        kickoff_id = response.json().get("kickoff_id")
    
    # Step 2: Poll for execution results
    status_url = f"{CREW_URL}/status/{kickoff_id}"
    
    with st.spinner(f"Analyzing {technology}..."):
        for i in range(120):  # 10 min max (120 * 5 seconds)
            time.sleep(5)
            
            response = requests.get(status_url, headers=headers)
            if response.status_code != 200:
                continue
                
            data = response.json()
            if not data:
                continue
            
            # Check if completed
            state = str(data.get("state", "")).upper()
            
            if state == "SUCCESS":
                st.success("Analysis completed successfully!")
                
                # Extract the output from the "result" field
                output = data.get("result", "No output available")
                
                # Clean up markdown code blocks if present
                if output.startswith("```markdown"):
                    output = output.replace("```markdown\n", "").replace("```", "")
                elif output.startswith("```"):
                    output = output.replace("```\n", "").replace("```", "")
                
                st.markdown(output)
                break
        else:
            # Timeout reached without completion
            st.warning("Analysis is taking longer than expected. Please check the CrewAI dashboard for status.")