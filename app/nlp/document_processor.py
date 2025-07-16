import pdfplumber
import io
import re

def extract_text(file_obj):
    try:

        if isinstance(file_obj, io.BytesIO):
            content = file_obj.read()
            ext = file_obj.name.lower() if hasattr(file_obj, 'name') else ''
            if ext.endswith('.pdf'):
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    text = ''.join(page.extract_text() or '' for page in pdf.pages)
            elif ext.endswith('.txt'):
                text = content.decode('utf-8')
            else:
                raise ValueError("Unsupported file type or missing extension")
        else:
            file_path = str(file_obj)
            if file_path.endswith('.pdf'):
                with pdfplumber.open(file_path) as pdf:
                    text = ''.join(page.extract_text() or '' for page in pdf.pages)
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            else:
                raise ValueError("Unsupported file type")


        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{2,}', '\n\n', text)
        text = re.sub(r'(?<=[.,!?])(?=[^\s])', r' ', text)
        text = re.sub(r'[^\w\s.,!?()\-:;%]', '', text)

        text = fix_spacing(text)


        return text.strip()



    except Exception as e:
        raise ValueError(f"Error extracting text: {str(e)}")


def fix_spacing(text):

    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)


    text = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', text)


    text = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', text)


    text = re.sub(r'(?<=[.,!?])(?=[^\s])', r' ', text)

    return text

