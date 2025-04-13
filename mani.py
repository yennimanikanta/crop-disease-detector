from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io
import base64
import time

# Load environment variables
load_dotenv()

# Configure dark theme with animations
def set_dark_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        background-image: radial-gradient(circle at 10% 20%, rgba(56, 182, 255, 0.1) 0%, transparent 20%);
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #38b6ff;
        text-shadow: 0 2px 4px rgba(56, 182, 255, 0.3);
    }
    .stButton>button {
        background-color: #38b6ff;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(56, 182, 255, 0.4);
    }
    .stImage>img {
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(56, 182, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stImage>img:hover {
        transform: scale(1.02);
    }
    .diagnosis-box {
        background-color: #1e2130;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        border-left: 4px solid #38b6ff;
        animation: fadeIn 0.8s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .star-rating {
        color: #FFD700;
        font-size: 24px;
        letter-spacing: 3px;
    }
    .section-header {
        background: linear-gradient(90deg, #38b6ff, transparent);
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

set_dark_theme()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

def analyze_plant_image(image_bytes):
    """Analyze plant image using Gemini 1.5 Flash"""
    try:
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        prompt = """**As an expert plant pathologist, provide a comprehensive analysis with these sections:**
        
        🌟 **Health Rating**: (1-5 stars based on severity)
        
        🌿 **Plant Identification**: 
        - Common name
        - Scientific name (if identifiable)
        
        🔍 **Health Assessment**:
        - Overall health status (Healthy/At Risk/Diseased)
        - Confidence level (High/Medium/Low)
        
        🦠 **Disease Analysis** (if any):
        - Disease name (common + scientific)
        - Key visual symptoms
        - Likely causes
        
        💊 **Treatment Plan**:
        - Immediate actions
        - Chemical treatments (with active ingredients)
        - Organic alternatives
        - Application instructions
        
        🛡️ **Prevention Strategies**:
        - Cultural practices
        - Environmental adjustments
        - Monitoring schedule
        
        📸 **Image Quality Note**:
        - Assessment of image usefulness
        - Suggestions for better images (if needed)"""
        
        img = Image.open(io.BytesIO(image_bytes))
        response = model.generate_content([prompt, img])
        return response.text
        
    except Exception as e:
        st.error(f"Error analyzing image: {str(e)}")
        return None

# Star rating component
def star_rating(rating):
    stars = ""
    full_star = "★"
    empty_star = "☆"
    for i in range(5):
        if i < rating:
            stars += full_star
        else:
            stars += empty_star
    return f'<div class="star-rating">{stars}</div>'

# Custom animated header
def animated_header():
    st.markdown("""
    <div class="pulse" style="text-align:center;margin-bottom:2rem;">
        <h1 style="color:#38b6ff;font-size:2.5rem;">🌿 Advanced Crop Doctor Pro</h1>
        <p style="color:#aaa;">AI-Powered Plant Health Diagnosis System</p>
    </div>
    """, unsafe_allow_html=True)

# Streamlit UI
animated_header()

# Image upload section with custom animation
with st.container():
    col1, col2 = st.columns([3,1])
    with col1:
        uploaded_file = st.file_uploader(
            "Drag & drop plant image or click to browse", 
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("🚀 Launch Analysis", use_container_width=True):
            st.session_state.analyze = True

if uploaded_file is not None:
    try:
        # Display the uploaded image with animation
        image = Image.open(uploaded_file)
        
        st.markdown("---")
        with st.container():
            st.subheader("📸 Submitted Plant Sample")
            st.image(image, use_column_width=True)
        
        if st.session_state.get('analyze', False):
            with st.spinner("🧪 Analyzing with AI..."):
                # Add artificial loading animation
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(percent_complete + 1)
                
                # Get image bytes
                img_bytes = uploaded_file.getvalue()
                
                # Analyze the image
                analysis = analyze_plant_image(img_bytes)
                
                if analysis:
                    # Display results with animations
                    st.markdown("---")
                    st.subheader("🔬 Comprehensive Diagnosis Report")
                    
                    # Add star rating
                    st.markdown("""
                    <div class="section-header">
                        <h4>🌟 Health Rating</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(star_rating(3), unsafe_allow_html=True)  # Default rating
                    
                    # Display diagnosis in beautiful card
                    st.markdown(f"""
                    <div class="diagnosis-box">
                        {analysis.replace('\n', '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add image again below diagnosis
                    st.image(image, caption="Reference Image", use_column_width=True)
                    
                    # Add download button with animation
                    st.download_button(
                        label="📥 Download Full Report",
                        data=analysis,
                        file_name="plant_diagnosis_report.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Analysis failed. Please try again with a clearer image.")
                    
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

# Sidebar with additional features
with st.sidebar:
    st.markdown("""
    <div style="border-bottom:1px solid #38b6ff;padding-bottom:1rem;margin-bottom:1rem;">
        <h3 style="color:#38b6ff;">📸 Imaging Guide</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - 🎯 **Focus**: Clear shots of affected areas
    - 🌞 **Lighting**: Natural light preferred
    - 📐 **Angles**: Multiple perspectives
    - 🖼️ **Background**: Simple, contrasting
    """)
    
    st.markdown("""
    <div style="border-bottom:1px solid #38b6ff;padding-bottom:1rem;margin-bottom:1rem;">
        <h3 style="color:#38b6ff;">⚠️ Common Issues</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - 🍄 Fungal infections
    - 🦠 Bacterial diseases
    - 🐛 Pest infestations
    - 🌱 Nutrient deficiencies
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;font-size:0.8rem;padding:1rem;">
    <p>🌱 Powered by DeepLearning(CNN)• plant Pathology Analysis System v3.0</p>
</div>
""", unsafe_allow_html=True)