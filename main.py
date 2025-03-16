import streamlit as st
import os
from functions import analyze_images_with_openai, fetch_street_view_image, getLatLongGoogle, getGoogleSatImage

st.set_page_config(page_title='AI Recognition', layout='centered')

OUTPUT_DIR = "images"

# Check if a file is uploaded
# if uploaded_file:
#     st.session_state.file_uploaded = True
#     st.sidebar.success("File uploaded successfully!")
#     dataframe = full_address(uploaded_file)
#     prompt_template = st.text_area("Enter a custom prompt for the AI model",
#                                    placeholder="Using roof, siding, landscaping, driveway and windows as the key factors. Grade this home from 0-10, 10 being perfect.")

    # prompt = None if not prompt_template.strip() else prompt_template

# Main Page with Dropdown
st.title("House Insurance Evaluation")
selected_option = st.text_input("Enter an address to search for")
bot_analysis_btn = st.button("Analyze")
if selected_option and bot_analysis_btn:
    prompt = (
        "You are an expert in property insurance evaluation. Analyze the given images of a home based on key factors such as roof, siding, landscaping, driveway, and windows. "
        "Provide a final **Home Insurance Score (0-10)** based on the overall condition and potential risks affecting insurability."
    )
    google_image = fetch_street_view_image(selected_option, OUTPUT_DIR)
    lat, long = getLatLongGoogle(selected_option)["results"][0]["geometry"]["location"]["lat"], getLatLongGoogle(selected_option)["results"][0]["geometry"]["location"]["lng"]
    google_main_image = getGoogleSatImage(lat, long, OUTPUT_DIR)
    image_paths = ["images/front_view.jpeg", "images/top_view.jpeg"]
    bot_response = analyze_images_with_openai(image_paths, prompt)
    img1, img2 = st.columns(2)
    with img1:
        st.image(google_main_image)
    with img2:
        st.image(google_image)
    
    st.write(bot_response)

# 774 W BEVERLY DR, CLOVIS, 93612, CA
# 1332 ADLER DR, CLOVIS, 93612, CA
# 609 W INDIANAPOLIS AVE, CLOVIS, 93612, CA