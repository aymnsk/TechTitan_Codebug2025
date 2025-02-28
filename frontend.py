import streamlit as st
import cv2
from PIL import Image
import numpy as np
from datetime import datetime
import base64

def load_font(font_path):
    with open(font_path, "rb") as f:
        font_data = f.read()
    return base64.b64encode(font_data).decode()

font_base64 = load_font("MinecraftTen-VGORe.ttf")

# Set page config
st.set_page_config(
    page_title="CAMCOM",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with linear gradient background & enhanced button styles
st.markdown("""
<style>
            
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

    body {
        background-color:#08090A;
        color: #F4FAFF;
        font-family: "Inter","MinecraftTen-VGORe",Arial, sans-serif;
    }
    .stApp {
    background-color:#08090A;   }
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #F4FAFF !important;
        text-shadow: 0px 0px 10px #F4FAFF;
        transistion:all 0.4s ease-in-out;
    }
    
    .stButton>button {
        background: #7CC6FE;
        color: black;
        border: none;
        border-radius: 8px;
        font-size: 1em;
        font-weight: bold;
        padding: 12px 20px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0px 4px 8px rgba(124, 198, 254, 0.4),
                    0px 4px 16px rgba(124,198,254,0.4);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(to right,#F4FAFF,#2d87adb3);
        color: black;
        transform: scale(1.05);
        box-shadow: 0px 8px 16px rgba(93, 253, 203, 0.6);
    }
    .project-name {
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 0px 0px 15px #7CC6FE;
        color: #F4FAFF;
        text-align: center;
        padding-bottom: 20px;
    }
    .system-status {
        font-family: 'Courier New', monospace;
        font-size: 1em;
        color: #F4FAFF;
        border-radius: 5px;
        padding: 8px 15px;
        background: #7CC6FE;
        margin: 10px 0;
    }
    .timestamp {
        font-family: 'Courier New', monospace;
        font-size: 1em;
        color: #5DFDCB;
        margin-top: 10px;
        text-align: center;
    }
    .output-display {
        background: #7CC6FE;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(124, 198, 254, 0.3);
        color: #F4FAFF;
        font-size: 1.1em;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Project title
st.markdown('<div class="project-name">CAMCOM</div>', unsafe_allow_html=True)

# Initialize session state variables
if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False
if 'image_captured' not in st.session_state:
    st.session_state.image_captured = False
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'system_log' not in st.session_state:
    st.session_state.system_log = ["System initialized"]
if 'output_text' not in st.session_state:
    st.session_state.output_text = "READY FOR ANALYSIS"

# Functions for camera controls
def toggle_camera():
    st.session_state.camera_on = not st.session_state.camera_on
    st.session_state.image_captured = False
    status = "activated" if st.session_state.camera_on else "deactivated"
    st.session_state.system_log.append(f"Camera {status}")
    if st.session_state.camera_on:
        st.session_state.output_text = "CAMERA ACTIVE\nAWAITING INPUT"
    else:
        st.session_state.output_text = "CAMERA OFFLINE\nSYSTEM STANDBY"

def capture_image():
    if st.session_state.camera_on:
        st.session_state.image_captured = True
        st.session_state.system_log.append("Image captured")
        st.session_state.output_text = "IMAGE ANALYSIS IN PROGRESS...\n\nPROCESSING...\n\nDETECTING OBJECTS...\n\nANALYSIS COMPLETE."

# Main layout with two columns (camera and output)
col1, col2 = st.columns([2, 1])

# Camera section
with col1:
    status = "ACTIVE" if st.session_state.camera_on else "INACTIVE"
    st.markdown(f'<div class="system-status">CAMERA STATUS: {status}</div>', unsafe_allow_html=True)
    if st.session_state.camera_on and not st.session_state.image_captured:
        camera_image = st.camera_input("", key="camera", label_visibility="collapsed")
        if camera_image is not None:
            st.session_state.captured_image = camera_image
    elif st.session_state.image_captured and st.session_state.captured_image is not None:
        st.image(st.session_state.captured_image, use_column_width=True)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f'<div class="timestamp">{current_time}</div>', unsafe_allow_html=True)

# Output display
with col2:
    st.markdown(
        f"""
        <div class="output-display">
            <div class="output-title">OUTPUT</div>
            <div class="output-content">{st.session_state.output_text.replace('\n', '<br>')}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# System log
st.markdown("<h3>SYSTEM LOG</h3>", unsafe_allow_html=True)
for entry in reversed(st.session_state.system_log[-8:]):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"<p style='font-family: monospace; margin: 5px 0; font-size: 0.9em;'>[{timestamp}] {entry}</p>", unsafe_allow_html=True)

# Control panel
st.markdown("### CONTROL PANEL")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("ON/OFF"):
        toggle_camera()
with c2:
    if st.button("Air Paint"):
        st.session_state.system_log.append("Video mode selected")
        st.session_state.output_text = "VIDEO MODE ENABLED\nRECORDING READY"
with c3:
    if st.button("Gesture Ai"):
        capture_image()
with c4:
    if st.button("Hand Sign"):
        st.session_state.system_log.append("Audio recording unavailable")
        st.session_state.output_text = "AUDIO MODULE\nCURRENTLY OFFLINE\nMAINTENANCE REQUIRED"

st.markdown("<div style='text-align: center; color: #F4FAFF; font-size: 0.8em;'>CAMCOM SYSTEM v1.0 | SECURE CONNECTION ESTABLISHED</div>", unsafe_allow_html=True)
