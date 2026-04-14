import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from io import BytesIO
import time

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def hex_to_rgb(hex_code):
    """Converts a web hex color (#FF0000) to Word RGBColor."""
    hex_code = hex_code.lstrip('#')
    return RGBColor(*tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)))

def classify_text(text):
    # (Keep your existing classify_text function exactly the same here)
    prompt = f"""
    Analyze this text from a raw manuscript and classify it into exactly ONE of these categories:
    - Title
    - Heading 1
    - Heading 2
    - Paragraph
    - Figure Caption
    - Table Caption

    Text to analyze: "{text}"
    
    Respond with ONLY the exact category name and nothing else.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip().replace(".", "")
    except Exception:
        return "Paragraph"

def apply_custom_formatting(paragraph, classification, settings):
    """Applies dynamic rules chosen by the user in the UI."""
    
    # Apply user's line spacing
    paragraph.paragraph_format.line_spacing = settings["line_spacing"]
    paragraph.paragraph_format.space_before = Pt(12)
    paragraph.paragraph_format.space_after = Pt(0)
    
    # Default parameters based on user settings
    align = WD_ALIGN_PARAGRAPH.LEFT
    font_size = Pt(settings["body_size"])
    bold = False
    italic = False
    color = RGBColor(0, 0, 0) # Default black

    # Apply specific rules based on classification and user settings
    if classification == "Title":
        align = WD_ALIGN_PARAGRAPH.CENTER
        font_size = Pt(settings["title_size"]) 
        bold = True
    
    elif classification == "Heading 1":
        font_size = Pt(settings["h1_size"]) 
        bold = True
        color = hex_to_rgb(settings["h1_color"])
    
    elif classification == "Heading 2":
        font_size = Pt(settings["h2_size"]) 
        bold = True
        color = hex_to_rgb(settings["h2_color"])
        
    elif classification == "Paragraph":
        align = WD_ALIGN_PARAGRAPH.JUSTIFY 
        
    elif classification in ["Figure Caption", "Table Caption"]:
        align = WD_ALIGN_PARAGRAPH.CENTER 
        font_size = Pt(11)
        italic = True 

    paragraph.alignment = align

    for run in paragraph.runs:
        run.font.name = settings["font"]
        run.font.size = font_size
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color

def get_word_count(uploaded_file):
    # (Keep your existing get_word_count function here)
    doc = Document(uploaded_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return len(" ".join(full_text).split())

def process_document(uploaded_file, settings):
    """Now accepts the settings dictionary from the UI"""
    doc = Document(uploaded_file)
    
    progress_text = "AI is analyzing and applying your custom rules..."
    progress_bar = st.progress(0, text=progress_text)
    
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

    total_paras = len(doc.paragraphs)
    
    for i, para in enumerate(doc.paragraphs):
        if 'graphicData' in para._p.xml:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            continue
            
        text = para.text.strip()
        if text != "":
            classification = classify_text(text)
            # Pass the settings into the formatter
            apply_custom_formatting(para, classification, settings)
            time.sleep(2) 
            
        progress_bar.progress((i + 1) / total_paras, text=f"Processed paragraph {i+1} of {total_paras}")
        
    progress_bar.empty()
    
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    
    return output