import streamlit as st
import database as db
import processor as proc

# 1. Page Configuration
st.set_page_config(page_title="Manuscript Automator", page_icon="📝", layout="centered", initial_sidebar_state="collapsed")

# 2. Inject Dark Theme Custom CSS
custom_css = """
<style>
    /* Hide Streamlit Default Menu & Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main App Background (Deep Slate) & Text */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Standard Button Styling (Vibrant Blue for visibility) */
    .stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #3b82f6;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        border-color: #2563eb;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        color: #ffffff;
    }

    /* Make the Download Button POP (Neon Purple/Pink Gradient) */
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
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
        box-shadow: 0 8px 15px rgba(236, 72, 153, 0.4);
        color: white;
    }

    /* Style the File Uploader for Dark Mode */
    [data-testid="stFileUploadDropzone"] {
        background-color: #1e293b;
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 20px;
        color: #f8fafc;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #8b5cf6;
        background-color: #283548;
    }
    
    /* Clean up input fields for Dark Mode */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f8fafc;
        border-radius: 8px;
        border: 1px solid #334155;
        padding: 10px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 1px #8b5cf6;
    }

    /* Override markdown text colors to ensure visibility */
    .stMarkdown p, .stMarkdown li {
        color: #cbd5e1 !important;
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
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Changed text colors to white and light gray for dark mode
        st.write("<h1 style='text-align: center; color: #ffffff;'>Manuscript AI</h1>", unsafe_allow_html=True)
        st.write("<p style='text-align: center; color: #94a3b8;'>Automated publication formatting.</p>", unsafe_allow_html=True)
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
    with st.sidebar:
        st.title(f"👋 Hi, {st.session_state['username']}")
        st.write("Welcome to your dashboard.")
        st.write("---")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.rerun()

    # Changed header to pure white
    st.write("<h2 style='color: #ffffff;'>Format Your Manuscript</h2>", unsafe_allow_html=True)
    st.info("✨ AI will enforce: Times New Roman, Justified text, 1.5 spacing, and custom headings.")
    
    st.write("### 1. Upload Raw Document")
    uploaded_file = st.file_uploader("", type=["docx"], help="Upload your raw .docx manuscript here.")
    
    if uploaded_file is not None:
        st.write("### 2. Process & Download")
        
        if st.button("🚀 Process Document"):
            
            # --- NEW LIMIT CHECK ---
            with st.spinner("Checking document length..."):
                word_count = proc.get_word_count(uploaded_file)
            
            if word_count > 2500:
                st.error(f"❌ Error: Document is too long ({word_count} words). The free tier is limited to 2,500 words (approx. 10 pages).")
            # -----------------------
            
            else:
                # If it passes the test, process it normally!
                with st.spinner(f"Processing {word_count} words..."):
                    processed_file = proc.process_document(uploaded_file, "Custom")
                
                st.success("✅ Formatting complete! Your document is ready.")
                
                st.download_button(
                    label="📥 Download Publication-Ready Manuscript",
                    data=processed_file,
                    file_name=f"Formatted_{uploaded_file.name}",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )