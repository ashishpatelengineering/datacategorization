import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import os
from io import StringIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Gemini AI client
client = genai.Client()

# Streamlit App
st.title(":red[Data Categorization using AI]")

# Description
st.write("""
        Easily categorize your CSV data using AI.
        Upload your CSV, define the categories you want, and let the AI assign each row to a category.
        You can then download the categorized CSV.
""")

# Upload CSV
st.subheader(":orange[Upload your CSV]")
uploaded_file = st.file_uploader("Choose a CSV file to categorize", type=["csv"])

if uploaded_file:
    # Read uploaded CSV
    df = pd.read_csv(uploaded_file)
    st.subheader(":orange[Uploaded CSV]")
    st.dataframe(df)

    # Enter categories
    st.subheader(":orange[Enter Categories]")
    categories_input = st.text_area(
        "Enter categories (one per line). Each row in your CSV will be assigned one of these categories.",
        value="Category #1\nCategory #2\nCategory #3\nCategory #4 ... \nUnknown",
        height=150
    )
    categories = [c.strip() for c in categories_input.split("\n") if c.strip()]

    # Initialize session state for categorized CSV
    if "categorized_csv_text" not in st.session_state:
        st.session_state["categorized_csv_text"] = None

    # Assign categories
    if st.button("Assign Categories"):
        csv_text = df.to_csv(index=False)
        prompt = (
            "Analyze this CSV and add a new column called 'Category' as the last column. "
            f"Assign only one of the following categories to each row: {', '.join(categories)}. "
            "Do NOT use or invent any other categories. If you do not know just use the unknown category."
            "Return only the CSV text with the new column. No markdown, explanations, or extra text."
        )

        with st.spinner("Categorizing CSV..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[csv_text, prompt]
            )

            # Store categorized CSV in session state
            st.session_state["categorized_csv_text"] = response.text

    # Display categorized CSV if available
    if st.session_state["categorized_csv_text"]:
        categorized_df = pd.read_csv(StringIO(st.session_state["categorized_csv_text"]))
        st.subheader(":orange[Categorized CSV Result]")
        st.dataframe(categorized_df)
        
        # Editable category column
        st.subheader(":orange[Review & Refine Your Categorized Data]")
        edited_df = st.data_editor(
            categorized_df,
            num_rows="dynamic",
            disabled=[col for col in categorized_df.columns if col != "Category"]
        )

        # Dynamic download filename
        download_filename = f"categorized_{uploaded_file.name}"

        st.download_button(
            label="Download Categorized CSV",
            data=edited_df.to_csv(index=False),
            # data=st.session_state["categorized_csv_text"],
            file_name=download_filename,
            mime="text/csv"
        )
