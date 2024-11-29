import streamlit as st
from PIL import Image
import pyttsx3
import os
import pytesseract
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# Initialize Google Generative AI with API Key
GEMINI_API_KEY = "AIzaSyD1uX9EStt8b7w7wlkM66v9j0DdGUPzS0o"  # Replace with your valid API key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Styling and Page Layout
st.markdown(
    """
    <style>
     .main-title {
        font-size: 48px;
         font-weight: bold;
         text-align: center;
         color: #0662f6;
         margin-top: -20px;
     }
    .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-header {
        font-size: 24px;
        color: #333;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">SmartVisionAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle"> Empowering Vision with AI 🗣️</div>', unsafe_allow_html=True)

# Sidebar Features
st.sidebar.image(
    r"C:\Users\HP\OneDrive\Pictures\logo.jpg", width=250
)

st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
     **SmartvisionAI**
     
     **🌟 Key Capabilities**
     
    - 🔍 **Visual Insights**: Receive AI-generated observations about the image, including objects and actionable insights.
    - 📝 **Text Extraction**: Retrieve any visible text from the image using advanced OCR technology.
    - 🔊 **Listen Aloud**: Transform extracted text into clear, audible speech

    💡 **Why It’s Beneficial**: This tool empowers visually impaired individuals by providing detailed visual explanations, text recognition, and audio assistance. 

    🤖 **Technology Behind the Magic**:  

    - **Google Gemini API**: For intelligent scene interpretation and descriptions.  
    - **Tesseract OCR**: For accurate text recognition from images.  
    - **pyttsx3**: For seamless text-to-speech conversion.
    """
)

st.sidebar.text_area(
    "📜 Instructions", 
    "Upload an image to start. Choose a feature to interact with:\n1. Get visual insights\n2. Text extraction\n3. Listen it out"
)

# Functions
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech using pyttsx3."""
    if text.strip():
        try:
            engine = pyttsx3.init(driverName='sapi5')  # Reinitialize engine every call
            engine.setProperty('rate', 150)  # Set speech rate
            engine.setProperty('volume', 1.0)  # Set volume
            engine.say(text)
            engine.runAndWait()
            engine.stop()  # Stop to avoid loop issues
        except Exception as e:
            raise RuntimeError(f"Text-to-Speech conversion failed: {e}")
    else:
        raise ValueError("No text provided for Text-to-Speech.")

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Upload Image Section
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Buttons Section
st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
col2,col1, col3 = st.columns(3)

ocr_button = col2.button("📝 Extract Text")
scene_button = col1.button("🔍 Describe Scene")
tts_button = col3.button("🔊 Text-to-Speech")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

# Process user interactions
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Getting visual insights..."):
            response = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='feature-header'>🔍 Visual Insight</h3>", unsafe_allow_html=True)
            st.write(response)

    if ocr_button:
        with st.spinner("Text Extraction from the image..."):
            text = extract_text_from_image(image)
            st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", text, height=150)

    if tts_button:
        with st.spinner("Getting out the speech..."):
            try:
                text = extract_text_from_image(image)
                text_to_speech(text)
                st.success("✅ Text-to-Speech Conversion Completed!")
            except ValueError as e:
                st.warning(str(e))
            except RuntimeError as e:
                st.error(f"❌ {e}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")

# Footer
st.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Google Gemini API</strong> | Built using Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Google Gemini API</strong> | Built using Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
