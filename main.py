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
st.title("AI Recognition")
selected_option = st.text_input("Enter an address to search for")
bot_analysis_btn = st.button("Analyze")
if selected_option and bot_analysis_btn:
    prompt = (
        "You are an expert in property insurance evaluation. Analyze the given images of a home using key factors: "
        "roof, siding, landscaping, driveway, and windows. Compare both images to assess the overall condition, "
        "potential risks, and insurability of the property. \n\n"

        "🏡 **Evaluation Criteria:** \n"
        "1 **Roof (2 points)** - Check for visible wear, missing shingles, or damage that may lead to leaks or structural issues. \n"
        "2 **Siding (2 points)** - Assess the condition of the exterior walls for cracks, moisture damage, or peeling paint. \n"
        "3 **Landscaping (2 points)** - Determine if overgrown trees, poor drainage, or uneven terrain could increase risks. \n"
        "4 **Driveway (2 points)** - Look for cracks, potholes, or other hazards that could affect safety and liability coverage. \n"
        "5 **Windows (2 points)** - Inspect for broken, outdated, or poorly sealed windows that might impact energy efficiency or security. \n\n"

        "📝 **Final Report:** \n"
        "✅ Compare the two images and highlight any differences in condition. \n"
        "✅ Identify any visible risk factors that could affect home insurance premiums. \n"
        "✅ Provide a final **Home Insurance Score (0-10)**, summarizing how insurable the home is. \n"
        "✅ Suggest possible improvements to increase the property's insurability and lower insurance costs. \n\n"

        "**Example Response:** \n"
        "🏡 **Final Home Insurance Score: 7/10** \n"
        "🔹 The roof appears well-maintained, but minor wear is visible. (1.5/2) \n"
        "🔹 Siding is in good condition, but slight discoloration is noticeable. (1.5/2) \n"
        "🔹 Landscaping shows potential drainage issues near the foundation. (1/2) \n"
        "🔹 The driveway has a few cracks that may pose minor risks. (1/2) \n"
        "🔹 Windows seem intact but could be upgraded for better insulation. (1/2) \n"
        "💡 Suggested Improvements: Seal driveway cracks, improve drainage near the foundation, and consider energy-efficient windows."
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