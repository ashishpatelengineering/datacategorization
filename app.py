import streamlit as st
import pandas as pd
from io import StringIO
from google import genai
from dotenv import load_dotenv
from prompts import CATEGORY_SUGGESTION_PROMPT, CATEGORY_ASSIGNMENT_PROMPT  

# Load environment variables from .env file (like API keys)
try:
    load_dotenv()
except Exception as e:
    st.error(f"Error loading environment variables: {e}")

# Initialize the Gemini AI client
try:
    client = genai.Client()
except Exception as e:
    st.error(f"Error initializing Gemini AI client: {e}")
    client = None

# Configure Streamlit page layout
st.set_page_config(layout="wide")
st.title(":rainbow[AI-Assisted Data Categorization]")

# Utility functions
def call_gemini(contents, model="gemini-2.5-flash"):
    """
    Call the Gemini AI model with the given contents.
    """
    try:
        if client is None:
            return "Error: Gemini client not initialized."
        response = client.models.generate_content(model=model, contents=contents)
        return response.text.strip()
    except Exception as e:
        return f"Error calling Gemini AI: {e}"

def generate_suggested_categories(df: pd.DataFrame) -> str:
    """
    Generate 6 broad categories based on the CSV DataFrame content.
    """
    try:
        csv_text = df.to_csv(index=False)
        contents = CATEGORY_SUGGESTION_PROMPT.format(csv_text=csv_text)
        return call_gemini(contents)
    except Exception as e:
        return f"Error generating suggested categories: {e}"

def assign_categories(df: pd.DataFrame, categories: list) -> str:
    """
    Assign categories to each row of the DataFrame using AI.
    """
    try:
        csv_text = df.to_csv(index=False)
        contents = CATEGORY_ASSIGNMENT_PROMPT.format(
            categories=", ".join(categories),
            csv_text=csv_text
        )
        return call_gemini(contents)
    except Exception as e:
        return f"Error assigning categories: {e}"

# Streamlit User Interface

st.write(
    """
Efficiently categorize your CSV data with AI.
Upload your file, review the suggested categories,
adjust them as needed, and let the system assign categories to each row.
"""
)

# File uploader widget for CSV
uploaded_file = st.sidebar.file_uploader("Choose a CSV file to categorize", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("Uploaded Data", divider='rainbow')
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading uploaded CSV: {e}")
        df = None

    if df is not None:
        # Generate suggested categories only once per session
        if "suggested_categories" not in st.session_state:
            with st.spinner("Analyzing data to suggest categories..."):
                st.session_state["suggested_categories"] = generate_suggested_categories(df)

        st.subheader("Suggested Categories", divider='rainbow')
        # Text area for users to edit the AI-suggested categories
        categories_input = st.text_area(
            "Edit the suggested categories if needed:",
            value=st.session_state.get("suggested_categories", ""),
            height=200,
        )
        # Convert user input into a list of categories
        categories = [cat.strip() for cat in categories_input.split("\n") if cat.strip()]

        # Initialize session state for categorized CSV text
        if "categorized_csv_text" not in st.session_state:
            st.session_state["categorized_csv_text"] = None

        # Button to assign categories using AI
        if st.button("Assign Categories"):
            with st.spinner("Categorizing data..."):
                try:
                    st.session_state["categorized_csv_text"] = assign_categories(df, categories)
                except Exception as e:
                    st.error(f"Error during categorization: {e}")
                    st.session_state["categorized_csv_text"] = None

        # Display the categorized data if available
        if st.session_state["categorized_csv_text"]:
            try:
                categorized_df = pd.read_csv(StringIO(st.session_state["categorized_csv_text"]))
                st.subheader("Categorized Data", divider='rainbow')
                # Allow editing of categories in the data editor
                edited_df = st.data_editor(
                    categorized_df,
                    num_rows="dynamic",
                    disabled=[col for col in categorized_df.columns if col != "Category"],
                )
                # Provide a download button for the categorized CSV
                st.download_button(
                    label="Download Categorized Data",
                    data=edited_df.to_csv(index=False),
                    file_name=f"categorized_{uploaded_file.name}",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Error displaying categorized CSV: {e}")

