import os
import requests
import streamlit as st
import re
import fitz  # PyMuPDF
from docx import Document

APP_KEY = os.getenv("APP_KEY")

BASE_URL = "https://api.dify.ai/v1"

def analyze_news(news_text):
    url = f"{BASE_URL}/workflows/run"
    headers = {
        "Authorization": f"Bearer {APP_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {
            "news": news_text,
        },
        "user": "abc-123"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get analysis"}

def parse_response(response_text):
    classification_match = re.search(r'<Classification>(\d)</Classification>', response_text)
    reason_match = re.search(r'<Reason>(.*?)</Reason>', response_text, re.DOTALL)
    sentiment_match = re.search(r'<Sentiment>(.*?)</Sentiment>', response_text, re.DOTALL)
    subject_category_match = re.search(r'<Category>(.*?)</Category>', response_text, re.DOTALL)
    keywords_match = re.search(r'<Keywords>(.*?)</Keywords>', response_text, re.DOTALL)
    
    if classification_match and reason_match:
        classification = classification_match.group(1)
        reason = reason_match.group(1).strip()
        sentiment = sentiment_match.group(1).strip() if sentiment_match else None
        subject_category = subject_category_match.group(1).strip() if subject_category_match else None
        keywords = keywords_match.group(1).strip() if keywords_match else None
        return classification, reason, sentiment, subject_category, keywords
    else:
        return None, None, None, None, None

def extract_text_from_pdf(file):
    document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in document:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    document = Document(file)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

st.set_page_config(page_title="News Xenophobia Analysis", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.big-font {
    font-size: 24px !important;
}
.sidebar .sidebar-content {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.main .block-container {
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.result-box {
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.result-box h3 {
    margin-top: 0;
}
.green {
    background-color: #d4edda;
    color: #155724;
}
.yellow {
    background-color: #fff3cd;
    color: #856404;
}
.red {
    background-color: #f8d7da;
    color: #721c24;
}
.dark-red {
    background-color: #f5c6cb;
    color: #721c24;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.title('News Xenophobia Analysis')
    st.write("Please enter the news content or upload a PDF/Word file to analyze its level of xenophobia.")
    
    news_input = st.text_area("News Content:", height=150, key="news_input")
    
    uploaded_file = st.file_uploader("Upload a PDF or Word file", type=["pdf", "docx"])
    
    if st.button('Analyze'):
        if not news_input.strip() and not uploaded_file:
            st.error("Please enter valid news content or upload a file!")
        else:
            with st.spinner('Analyzing...'):
                if uploaded_file:
                    if uploaded_file.type == "application/pdf":
                        news_input = extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        news_input = extract_text_from_docx(uploaded_file)
                
                result = analyze_news(news_input)
                print('result', result)
            
            if 'error' in result:
                st.error(result['error'])
            else:
                result_json = result['data']['outputs']['text']
                print('result_json', result_json)
                
                if result_json:
                    classification, reason, sentiment, subject_category, keywords = parse_response(result_json)
                    if classification and reason:
                        with col2:
                            st.write(f"### Analysis Result:")
                            if classification == '1':
                                color_class = 'green'
                            elif classification == '2':
                                color_class = 'yellow'
                            elif classification == '3':
                                color_class = 'red'
                            elif classification == '4':
                                color_class = 'dark-red'
                            
                            result_html = f"""
                            <div class='result-box {color_class}'>
                                <h3>Classification: {classification}</h3>
                                <p>{reason}</p>
                            """
                            if sentiment:
                                result_html += f"<p><strong>Sentiment:</strong> {sentiment}</p>"
                            if subject_category:
                                result_html += f"<p><strong>Subject Category:</strong> {subject_category}</p>"
                            if keywords:
                                result_html += f"<p><strong>Keywords:</strong> {keywords}</p>"
                            result_html += "</div>"
                            
                            st.markdown(result_html, unsafe_allow_html=True)
                    else:
                        st.error("Invalid response format. Please check the API.")
                else:
                    st.error("Invalid response format. Please check the API.")

