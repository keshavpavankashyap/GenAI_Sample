# -*- coding: utf-8 -*-
"""Text_Generation_Facebook

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LeAnp0QU1Zr4BeVP0rYmY7NImXp612tl
"""



import streamlit as st
from transformers import pipeline
import pdfplumber
from docx import Document

# Load NLP pipelines from Hugging Face
content_analysis_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")
summarization_pipeline = pipeline("summarization")
grammar_correction_pipeline = pipeline("text2text-generation", model="facebook/bart-large-cnn")
text_generation_pipeline = pipeline("text-generation", model="gpt2")

# Helper functions to read documents
def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

def read_word(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Streamlit interface
st.title("Document Analyzer & Text Generator")

# File uploader
file = st.file_uploader("Upload a PDF or Word document", type=['pdf', 'docx'])

# Text area for user input
user_input = st.text_input("Enter a sentence (type 'exit' to terminate):")

if file:
    # Detect file type and extract content
    if file.type == "application/pdf":
        doc_text = read_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc_text = read_word(file)

    # Display document content
    st.write("Document Content:")
    st.write(doc_text)

    # Test Case 1: Check content, accuracy, readability, and understandability
    if st.button("Check Document"):
        st.write("Analyzing document for content, accuracy, readability, and understandability...")
        # Simulate the check (in reality, you would build a custom model or use an existing NLP model for this)
        analysis = content_analysis_pipeline(doc_text)
        st.write(f"Analysis Results: {analysis}")

    # Test Case 2: Provide a summary of the document
    if st.button("Summarize Document"):
        st.write("Summarizing document...")
        summary = summarization_pipeline(doc_text, max_length=100, min_length=30, do_sample=False)
        st.write(f"Summary: {summary[0]['summary_text']}")

    # Test Case 3: Correct grammatical mistakes
    if st.button("Correct Grammar"):
        st.write("Correcting grammar...")
        corrected_text = grammar_correction_pipeline(doc_text)[0]['generated_text']
        st.write(f"Corrected Text: {corrected_text}")

    # Test Case 4: Interactive text generation
    if user_input:
        if user_input.lower() == 'exit':
            st.stop()  # Stop the execution
        else:
            generated_text = text_generation_pipeline(user_input, max_length=50)[0]['generated_text']
            st.write(f"Generated Text: {generated_text}")
