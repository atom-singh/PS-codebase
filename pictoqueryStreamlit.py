import streamlit as st
import base64
from openai import OpenAI

# Ensure you have set your OpenAI API key in the Streamlit secrets
# You can set it in the Streamlit Cloud or in a .streamlit/secrets.tom
api_key = st.secrets["OPENAI_API_KEY"]

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

st.title("PictoQuery Streamlit App")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    base64_image = encode_image(uploaded_file)
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    user_text_prompt = st.text_input("Enter your question:")
    
    if st.button("Submit"):
        if user_text_prompt:
            main_prompt = f"I have uploaded an image. Based on the image, give me the correct answer also taking '{user_text_prompt}' into consideration."
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": main_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }],
            )
            st.write(response.choices[0].message.content)
        else:
            st.warning("Please enter a question.")