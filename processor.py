from docx import Document
from io import BytesIO

def process_document(uploaded_file, style):
    # 1. Load the raw document just to READ it
    raw_doc = Document(uploaded_file)
    
    # 2. Create a BRAND NEW document (this guarantees standard styles exist!)
    new_doc = Document()
    
    # Add a Heading 1 (level=1 is much safer than level=0) to prove it worked
    new_doc.add_heading(f'Formatted for: {style}', level=1)
    new_doc.add_paragraph('This document was cleaned and rebuilt by the AI formatting tool.\n')
    
    # 3. Extract text from the old document and move it to the new one
    for para in raw_doc.paragraphs:
        # We only want to copy paragraphs that actually have text in them
        if para.text.strip() != "": 
            new_doc.add_paragraph(para.text)
    
    # 4. Save the new clean document to our BytesIO stream
    output = BytesIO()
    new_doc.save(output)
    output.seek(0)
    
    return output