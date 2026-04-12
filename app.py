import streamlit as st
import database as db
import processor as proc

st.set_page_config(page_title="Manuscript Automator", layout="centered")

# --- Session State for Login ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# --- Login / Signup Page ---
if not st.session_state['logged_in']:
    st.title("Welcome to Manuscript Automator")
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
    st.sidebar.title(f"Welcome, {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.rerun()

    st.title("Raw DOCX to Publication-Ready")
    
    # 1. Upload
    st.subheader("1. Upload Manuscript")
    uploaded_file = st.file_uploader("Choose a raw .docx file", type=["docx"])
    
    # 2. Selection
    st.subheader("2. Select Target Journal Style")
    journal_style = st.selectbox(
        "Available Templates",
        ("IEEE Format", "Nature Format", "KPRIET Thesis Style")
    )
    
    # 3. Process & 4. Download
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner('AI is analyzing and formatting your document...'):
                
                # Run the logic from processor.py
                processed_file = proc.process_document(uploaded_file, journal_style)
                
                st.success("Document formatting complete!")
                
                # 4. Download
                st.download_button(
                    label="Download Publication-Ready Manuscript",
                    data=processed_file,
                    file_name=f"Formatted_{uploaded_file.name}",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )