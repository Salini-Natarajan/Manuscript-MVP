import streamlit as st
import database as db
import processor as proc

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="Manuscript Automator", page_icon="📝", layout="centered", initial_sidebar_state="collapsed")

# 2. Inject Custom CSS for "SaaS Level" Look
custom_css = """
<style>
    /* Hide Streamlit Default Menu & Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main Background & Text */
    .stApp {
        background-color: #f8f9fa;
        color: #1e1e1e;
        font-family: 'Inter', sans-serif;
    }

    /* Standard Button Styling (Login, Sign Up, Process) */
    .stButton > button {
        width: 100%;
        background-color: #2b313e;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #434c5e;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: white;
    }

    /* Make the Download Button POP (Gradient) */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(118, 75, 162, 0.3);
        color: white;
    }

    /* Style the File Uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Clean up input fields */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Session State for Login ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# --- Login / Signup Landing Page ---
if not st.session_state['logged_in']:
    # Use columns to create a centered, narrow login card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("<h1 style='text-align: center; color: #2b313e;'>Manuscript AI</h1>", unsafe_allow_html=True)
        st.write("<p style='text-align: center; color: #64748b;'>Automated publication formatting.</p>", unsafe_allow_html=True)
        st.write("") # Spacer
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                if db.authenticate_user(login_user, login_pass):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = login_user
                    st.rerun()
                else:
                    st.error("Invalid username or password")
                    
        with tab2:
            new_user = st.text_input("New Username", key="reg_user")
            new_pass = st.text_input("New Password", type="password", key="reg_pass")
            if st.button("Sign Up"):
                if new_user and new_pass:
                    if db.create_user(new_user, new_pass):
                        st.success("Account created! Please log in.")
                    else:
                        st.error("Username already exists.")
                else:
                    st.warning("Please fill out all fields.")

# --- Main App Dashboard ---
else:
    # Sidebar for navigation/logout
    with st.sidebar:
        st.title(f"👋 Hi, {st.session_state['username']}")
        st.write("Welcome to your dashboard.")
        st.write("---")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.rerun()

    # Main UI
    st.write("<h2 style='color: #2b313e;'>Format Your Manuscript</h2>", unsafe_allow_html=True)
    st.info("✨ AI will enforce: Times New Roman, Justified text, 1.5 spacing, and custom headings.")
    
    st.write("### 1. Upload Raw Document")
    uploaded_file = st.file_uploader("", type=["docx"], help="Upload your raw .docx manuscript here.")
    
    if uploaded_file is not None:
        st.write("### 2. Process & Download")
        
        if st.button("🚀 Process Document"):
            
            # Run the logic from your upgraded processor.py
            processed_file = proc.process_document(uploaded_file, "Custom")
            
            st.success("✅ Formatting complete! Your document is ready.")
            
            # The CSS above targets this specific button to make it a purple gradient
            st.download_button(
                label="📥 Download Publication-Ready Manuscript",
                data=processed_file,
                file_name=f"Formatted_{uploaded_file.name}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )