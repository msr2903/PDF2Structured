import os
import google.generativeai as genai
import tempfile
import re

def gemini_extract_pdf(api_key, pdf_bytes, mime_type, prompt, model_name):
    """Uploads PDF, sends to Gemini, cleans response, returns text/error."""
    if not api_key: return "Error: API key not provided."
    temp_file_path, pdf_file_resource, cleaned_result = None, None, None
    try:
        genai.configure(api_key=api_key)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
            tf.write(pdf_bytes); temp_file_path = tf.name
        pdf_file_resource = genai.upload_file(path=temp_file_path, mime_type=mime_type)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content([prompt, pdf_file_resource], request_options={"timeout": 600})

        if hasattr(response, 'text'):
            raw_text = response.text
            if isinstance(raw_text, str):
                match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text, re.DOTALL)
                cleaned_result = match.group(1).strip() if match else raw_text.strip()
            else: cleaned_result = "Error: Gemini returned non-text content."
        return cleaned_result
    
    except Exception as e:
        return f"Error during processing: {str(e)}"
    finally:
        if pdf_file_resource:
            genai.delete_file(pdf_file_resource.name)
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)