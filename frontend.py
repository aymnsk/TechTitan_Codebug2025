import streamlit as st
import cv2
from PIL import Image
import numpy as np
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="CAMCOM",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the futuristic cyberpunk style
st.markdown("""
<style>
    body {
        background-color: #000000;
        color: #00ffcc;
        font-family: Arial, sans-serif;
    }
    .stApp {
        background-color: #000000;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
        text-shadow: 0px 0px 10px #00ffcc;
    }
    .stButton>button {
        border: 2px solid #00ffcc;
        background-color: transparent;
        color: #00ffcc;
        border-radius: 8px;
        font-size: 0.9em;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        box-shadow: 0px 0px 15px #00ffcc;
        padding: 10px 15px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00ffcc;
        color: black;
        transform: scale(1.05);
        box-shadow: 0px 0px 25px #00ffcc;
    }
    .project-name {
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 0px 0px 10px #00ffcc;
        color: #00ffcc;
        text-align: right;
        padding-right: 20px;
        margin-bottom: 20px;
    }
    .system-status {
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        border-radius: 5px;
        padding: 5px 10px;
        background-color: rgba(0, 255, 204, 0.1);
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .timestamp {
        font-family: 'Courier New', monospace;
        font-size: 1em;
        color: #00ffcc;
        margin-top: 10px;
        text-align: center;
    }
    .camera-placeholder {
        width: 100%;
        height: 330px;
        background: rgba(0, 30, 20, 0.5);
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid rgba(0, 255, 204, 0.3);
    }
    .output-display {
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 10px;
        padding: 10px;
        background: rgba(0, 30, 20, 0.5);
        height: 400px;  /* Increased height */
        overflow-y: auto;
    }
    .output-title {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 10px;
        text-shadow: 0px 0px 5px #00ffcc;
    }
    .output-content {
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: #00ffcc;
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
    # Display camera status
    status = "ACTIVE" if st.session_state.camera_on else "INACTIVE"
    st.markdown(f'<div class="system-status">CAMERA STATUS: {status}</div>', unsafe_allow_html=True)
    
    # Camera display logic
    if st.session_state.camera_on and not st.session_state.image_captured:
        camera_image = st.camera_input("", key="camera", label_visibility="collapsed")
        if camera_image is not None:
            st.session_state.captured_image = camera_image
    elif st.session_state.image_captured and st.session_state.captured_image is not None:
        st.image(st.session_state.captured_image, use_column_width=True)
    else:
        st.markdown(
            """
            <div class="camera-placeholder">
                <p style="color:#00ffcc;">CAMERA OFFLINE</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Display timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f'<div class="timestamp">{current_time}</div>', unsafe_allow_html=True)

# Output display (now in its own column, to the right of camera)
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

# System log section below the camera feed
st.markdown("<h3>SYSTEM LOG</h3>", unsafe_allow_html=True)
# Display log entries (most recent first)
for entry in reversed(st.session_state.system_log[-8:]):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"<p style='font-family: monospace; margin: 5px 0; font-size: 0.9em;'>[{timestamp}] {entry}</p>", unsafe_allow_html=True)

# Control panel (now spanning all columns)
st.markdown("### CONTROL PANEL")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("ON/OFF"):
        toggle_camera()
with c2:
    if st.button("VIDEO"):
        st.session_state.system_log.append("Video mode selected")
        st.session_state.output_text = "VIDEO MODE ENABLED\nRECORDING READY"
with c3:
    if st.button("CAPTURE"):
        capture_image()
with c4:
    if st.button("AUDIO"):
        st.session_state.system_log.append("Audio recording unavailable")
        st.session_state.output_text = "AUDIO MODULE\nCURRENTLY OFFLINE\nMAINTENANCE REQUIRED"
with c5:
    if st.button("SETTINGS"):
        st.session_state.system_log.append("Settings accessed")
        st.session_state.output_text = "SETTINGS PANEL\n\nRESOLUTION: 1080p\nFRAME RATE: 30fps\nNIGHT MODE: ENABLED\nAI ASSIST: ACTIVE"

# System footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 10px; color: #00ffcc; font-size: 0.8em; font-family: monospace;">
        CAMCOM SYSTEM v1.0 | SECURE CONNECTION ESTABLISHED
    </div>
    """, 
    unsafe_allow_html=True
)