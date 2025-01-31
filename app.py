import streamlit as st
import pandas as pd
from google_drive import upload_file_to_drive
from data_handler import load_excel, clean_column_names, get_filtered_view

# Streamlit App Configuration
st.set_page_config(
    page_title="Customer Management Tool",
    layout="wide",
)

# File Upload Section
st.title("📊 Customer Management Tool")
st.subheader("Upload Your Excel File")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        # Load Excel File
        xl = load_excel(uploaded_file)
        sheet_names = xl.keys()
        selected_sheet = st.selectbox("Select a sheet", sheet_names)

        # Parse the selected sheet
        df = xl[selected_sheet]
        df = clean_column_names(df)
        st.dataframe(df)

        # Search Functionality
        search_term = st.text_input("🔍 Search:")
        if search_term:
            filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
            st.write(f"Results for: **{search_term}**")
            st.dataframe(filtered_df)

        # View Selection
        view_type = st.selectbox("Choose a View", ["Whole Sheet", "Action Items", "Knowledge", "Communication and Awareness", "Annual Goals"])
        filtered_view = get_filtered_view(df, view_type)
        st.dataframe(filtered_view)

        # File Upload to Google Drive
        st.subheader("📤 Upload to Google Drive")
        if st.button("Upload File"):
            folder_id = "1jJvNynJcPKn4bLFVP687ruRsPwvxy5b0"  # Google Drive Folder ID
            file_data = uploaded_file.getvalue()
            file_id = upload_file_to_drive(file_data, uploaded_file.name, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", folder_id)
            file_url = f"https://drive.google.com/file/d/{file_id}/view"
            st.success(f"File uploaded successfully! [View File]({file_url})")

    except Exception as e:
        st.error(f"Failed to process the file: {e}")
