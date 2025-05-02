import streamlit as st
import os
from streamlit_pdf_viewer import pdf_viewer
from models import AVAILABLE_MODELS
from prompts import PROMPT_TEMPLATES
from extractor import gemini_extract_pdf

st.set_page_config(
    page_title="PDF Extractor with Gemini",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Extractor with Gemini")
st.markdown("---")

# --- Gemini Config Sidebar ---
st.sidebar.subheader("--- Gemini Config ---")
api_key_env = os.getenv("GOOGLE_API_KEY")
api_key = st.sidebar.text_input(
    "Enter your Google AI API Key:",
    type="password",
    value=api_key_env if api_key_env else "",
)

default_index = 0
selected_model = st.sidebar.selectbox(
    "Select Gemini Model:",
    options=AVAILABLE_MODELS,
    index=default_index,
)

# --- File Updater and Prompt ---
col1, col2 = st.columns([1, 5])

with col1:
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        key="pdf_uploader"
    )

with col2:
    # --- Prompt Template Selection ---
    template_options = list(PROMPT_TEMPLATES.keys())
    default_template_index = template_options.index("Custom")
    selected_template_name = st.selectbox(
        "Choose a prompt template (optional):",
        options=template_options,
        index=default_template_index,
        key="template_selector"
    )
    
    initial_prompt_text = PROMPT_TEMPLATES[selected_template_name] #Connect selector to text area
    
    # --- Text Area ---
    extraction_prompt = st.text_area(
        "Specify what information Gemini should extract (edit template below if needed):",
        value=initial_prompt_text,
        height=150,
        key="extraction_prompt_area"
    )

# --- Process & Display --
if uploaded_file is not None:
    try:
        pdf_bytes = uploaded_file.getvalue()
        pdf_mime_type = uploaded_file.type # Get MIME type (e.g., 'application/pdf')
        if not pdf_mime_type: # Fallback if type isn't detected by Streamlit
            pdf_mime_type = 'application/pdf'
            
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}", icon="❌")
        st.stop()
    
    col3, col4 = st.columns([3, 2])
    
    # --- Col3: PDF Viewer ---
    with col3:
        if uploaded_file:
            st.subheader(f"Source PDF: :orange[{uploaded_file.name}]")
            st.markdown("---")
            with st.spinner("Loading PDF viewer..."):
                try:
                    pdf_viewer(input=pdf_bytes, width="100%", height=1100)
                except Exception as e:
                    st.error(f"Error loading PDF viewer: {e}", icon="👁️‍🗨️")
                    
    # --- Col4: Gemini Extraction & Results ---
    if 'output_data' not in st.session_state:
        st.session_state.output_data = None
    
    with col4:
        st.subheader("Gemini Extraction")
        
        if not api_key:
            st.warning("Please enter your Google AI API Key in the sidebar¥")
            st.stop()
        if st.button(f"Extract with {selected_model}", key="analyze_button", use_container_width=True):
            with st.spinner(f"Processing PDF..."):
                extracted_text = gemini_extract_pdf(api_key, pdf_bytes, pdf_mime_type, extraction_prompt, selected_model)
                st.session_state.output_data = extracted_text
                if not st.session_state.output_data:
                    st.error("Extraction failed or returned no content.")
        if st.session_state.output_data:
            st.download_button(
                label="Download JSON",
                data=st.session_state.output_data,
                file_name=f"{uploaded_file.name}.json",
                mime="application/json"
            )
            st.code(st.session_state.output_data, language="json", height=1050)