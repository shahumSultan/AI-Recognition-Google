import streamlit as st
import os
from functions import full_address, analyze_images_with_openai, fetch_street_view_image

st.set_page_config(page_title='AI Recognition',
                   layout='centered', initial_sidebar_state='expanded')

OUTPUT_DIR = "images"

# Initialize session state
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None

# Sidebar for buttons
st.sidebar.title("Options")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file:
    st.session_state.file_uploaded = True
    st.sidebar.success("File uploaded successfully!")
    dataframe = full_address(uploaded_file)
    prompt_template = st.text_area("Enter a custom prompt for the AI model",
                                   placeholder="Using roof, siding, landscaping, driveway and windows as the key factors. Grade this home from 0-10, 10 being perfect.")

    prompt = None if not prompt_template.strip() else prompt_template

# Complete Analysis Button
# if st.sidebar.button("Complete Analysis", disabled=not st.session_state.file_uploaded):
#     if st.session_state.file_uploaded:
#         st.write("Starting analysis...")
#         progress_text = "Operation in progress. Please wait."
#         my_bar = st.progress(0, text=f"{progress_text} 0%")

#         total_rows = len(dataframe)
#         completed_rows = 0

#         for index, row in dataframe.iterrows():
#             try:
#                 image_path = fetch_street_view_image(row['combined_address'], OUTPUT_DIR)
#                 analysis = analyze_images_with_openai(image_path, prompt)
#                 dataframe.at[index, "OpenAI_Analysis"] = analysis
#             except Exception as e:
#                 st.error(f"Error processing the reques: {e}")
#                 dataframe.at[index, "OpenAI_Analysis"] = f"{str(e)}"

#             completed_rows += 1
#             progress_percentage = int((completed_rows / total_rows) * 100)
#             my_bar.progress(completed_rows / total_rows,
#                             text=f"{progress_text} {progress_percentage}%")

#         # Save analysis data for download
#         st.session_state.csv_data = dataframe.to_csv(
#             index=False).encode('utf-8')
#         st.session_state.analysis_done = True
#         st.success("Analysis completed!")

# # Download Button
# st.sidebar.download_button(
#     label="Download Button",
#     data=st.session_state.csv_data if st.session_state.analysis_done else b"",
#     file_name="analysis_result.csv",
#     mime="text/csv",
#     disabled=not st.session_state.analysis_done
# )

# Main Page with Dropdown
st.title("AI Recognition")
if uploaded_file:
    selected_option = st.selectbox(
        "Choose an option", options=dataframe["combined_address"], index=None)
    st.write("here")
    google_image = fetch_street_view_image(selected_option, OUTPUT_DIR)
    bot_response = analyze_images_with_openai(google_image, prompt)
    st.image(google_image)
    st.write(bot_response)
