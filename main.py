import streamlit as st
import os
from functions import full_address, fetch_street_view_image, analyze_images_with_openai
from dotenv import load_dotenv

st.set_page_config(page_title='AI Recognition', layout='centered', initial_sidebar_state='expanded')
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OUTPUT_DIR = "images"

st.title("AI Recongition")



with st.sidebar:
    uploaded_file = st.file_uploader(label="Upload CSV", type=['csv'], accept_multiple_files=False)

if uploaded_file:
    st.success("File Uploaded")
    dataframe = full_address(uploaded_file)
    analysis_btn = st.button(label="Complete Analysis")
    # if analysis_btn:
    #     progress_text = "Operation in progress. Please wait."
    #     my_bar = st.progress(0, text=f"{progress_text} 0%")

    #     total_rows = len(dataframe)  # Total number of rows in the dataframe
    #     completed_rows = 0

    #     for index, row in dataframe.iterrows():
    #         try:
    #             image_paths = fetch_street_view_image(
    #                 row, GOOGLE_API_KEY, OUTPUT_DIR)
    #             analysis = analyze_images_with_openai(image_paths)
    #             dataframe.at[index, "OpenAI_Analysis"] = analysis
    #         except Exception as e:
    #             st.error(f"Error processing the request: {e}")
    #             dataframe.at[index, "OpenAI_Analysis"] = f"Error: {str(e)}"

    #         # Update the progress bar
    #         completed_rows += 1
    #         progress_percentage = int((completed_rows / total_rows) * 100)
    #         my_bar.progress(completed_rows / total_rows,
    #                         text=f"{progress_text} {progress_percentage}%")

    #     # Save the output CSV file
    #     output_csv = os.path.join(OUTPUT_DIR, 'analysis_result.csv')
    #     dataframe.to_csv(output_csv, index=False)
    #     st.success("Analysis Complete")

    #     csv_data = dataframe.to_csv(index=False).encode('utf-8')
    #     st.download_button(
    #         label="Download CSV",
    #         data=csv_data,
    #         file_name='analysis_result.csv',
    #         mime='text/csv'
    #     )

if uploaded_file:
    selection = st.selectbox(label='Select Address', options=dataframe['combined_address'], index=None)
    if selection:
        st.write(f"You selected : {selection}")
        # google_image = fetch_street_view_image(selection, GOOGLE_API_KEY, OUTPUT_DIR)
        # st.image(google_image)
        # bot_response = analyze_images_with_openai(google_image)
        # st.write(bot_response)