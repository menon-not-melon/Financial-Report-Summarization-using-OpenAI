import os
import re
import sys
import string
import nltk
import fitz
import tiktoken
import openai
from PyPDF2 import PdfReader
from docx import Document
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from langchain.llms import OpenAI
from langchain import PromptTemplate

# Downloading NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Defining prompts for creating summaries for the chunks
chunks_prompt = """
I want the detailed information on this
1. Business Overview – Include information such as the company's formation/incorporation date, headquarters location, business description, employee count, latest revenues, stock exchange listing and market capitalization, number of offices and locations, and details on their clients/customers. 2. Business Segment Overview. i. Extract the revenue percentage of each component (verticals, products, segments, and sections) as a part of the total revenue. ii. Performance: Evaluate the performance of each component by comparing the current year's sales/revenue and market share with the previous year's numbers.  iii. Sales Increase/Decrease explanation: Explain the causes of the increase or decrease in the performance of each component.  4. Breakdown of sales and revenue by geography, specifying the percentage contribution of each region to the total sales. 5. Summarize geographical data, such as workforce, clients, and offices, and outline the company's regional plans for expansion or reduction. 6. Analyze and explain regional sales fluctuations, including a geographical sales breakdown to identify sales trends. 7. Year-over-year sales increase or decline and reasons for the change. 8. Summary of rationale & considerations (risks & mitigating factors). 9. SWOT Analysis which elaborates to Strenths, weaknesses, opportunities and Threats a company. 10. Information about credit rating/credit rating change/change in the rating outlook 

Document:`{text}'
Summary:
"""
custom_prompt = PromptTemplate(template=chunks_prompt,input_variables=["text"])

# Defining prompt for creating a 2 page-summary with all our objectives. Prompt can be edited to suit the input cases
final_combine_prompt = """
Create a concise summary of the financial position of the company based on the provided speech. The summary should be strictly 2 pages long, covering the following key points and information about the mentioned points only and should be under the heading:

Business Overview:

Formation and Incorporation date, headquarters location, business description, employee count, latest revenues, stock exchange listing and market capitalization, number of offices, and key clients/customers.
The business overview should be in a paragraph and not in bullet points containing all the above points.
Business Segment Overview:

Extract the revenue percentage of each component (verticals, products, segments, sections) as part of total revenue in bullet points.
Evaluate performance of each component by comparing current year's sales/revenue and market share with previous year's numbers.
Explain reasons for any increase or decrease in performance in brief.
Geographical Sales Breakdown:

Summarize sales and revenue breakdown by geography, specifying percentage contribution of each region to total sales in bullet points.
Provide insights into workforce, client distribution, office locations, and outline regional expansion or reduction plans briefly.
Year-over-Year Sales Analysis:

Analyze year-over-year sales fluctuations and provide reasons for changes.
Rationale & Considerations:

Include SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) where each of the components are under subheadings.
Discuss key considerations, risks, and mitigating factors impacting the company's financial outlook.
Credit Rating and Outlook:

Provide information about current credit rating, any changes, and outlook briefly.

"""
final_summary_prompt = PromptTemplate(template=final_combine_prompt,input_variables=['text'])

# Defining prompt for generating 1-page summary. Prompt can be edited to suit the input cases
final_combine_prompt_1_pager = f"""
1-page summary should be summary of the given text including the numbers from Business segment overview & geographical segment overview with all the important points in just 1 page. The businesss overview should not be more than 4 lines.
The entire summary should not exceed 320 words.
"""
final_summary_prompt_one_pager = PromptTemplate(template=final_combine_prompt_1_pager,input_variables = ['text'])

# Initializing OpenAI client and input of open ai key
key = str(input("Enter your Open AI API key: "))
openai.api_key = key

# Function to extract text from PDF files
def extract_text_from_pdf(file_paths):
    text = "" # Initializing an empty string to store the extracted text
    for file_path in file_paths: # Iterating through each file path
        try:
            with fitz.open(file_path) as pdf_document:
                # Iterate through each page in the PDF document
                for page_num in range(len(pdf_document)):
                    # Get a page object
                    page = pdf_document.load_page(page_num)
                    
                    # Extract text from the page
                    page_text = page.get_text()
                    
                    # Append extracted text to the 'text' variable
                    text += page_text or "" or "" # Appending the text string if found
        # Handling Exceptions that might occur during PDF processing
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
    return text

# Function to preprocess text
def preprocess_text(text):
    try:
        # Tokenizing the text into words
        tokens = word_tokenize(text)
        # Converting each word into lower-case
        tokens = [word.lower() for word in tokens]
        # Removing punctuation 
        table = str.maketrans('', '', string.punctuation)
        stripped = [word.translate(table) for word in tokens]

        # Stopwords removal
        stop_words = set(stopwords.words('english'))
        words = [word for word in stripped if word not in stop_words]
        # Joining the words into a single string
        processed_text = ' '.join(words)

        # Counting the number of tokens after processing using tiktoken
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(processed_text))

        return processed_text, num_tokens

    # Handling exceptions that might occur during text preprocessing
    except Exception as e:
        print(f"Error in text preprocessing: {e}")
        return "", 0

# Function to split text into chunks
def split_text(text, chunk_size=20000, chunk_overlap=20):
    try:
        text_length = len(text) # Calculating the length of the entire text
        chunks = [] 
        start = 0
        # Iterating till the entire text is processed
        while start < text_length:
            end = start + chunk_size # Calculating the end index of the chunk
            chunks.append(text[start:end]) # Appending the chunk to the chunk list
            start += chunk_size - chunk_overlap # Calculating the beginning index of the next chunk
        return chunks
    # Handling exceptions that might happen while creating the chunks
    except Exception as e:
        print(f"Error splitting text into chunks: {e}")
        return []

# Function to generate a summary using OpenAI API
def generate_summary(text,prompt):
    try:
        MODEL = "gpt-4o-mini" # Specifying the model we want to use
        # Calling OpenAI API key for generating the summary by specifying the role message, text and prompt
        response = openai.chat.completions.create(
            model = MODEL,
            messages = [
                {"role": "system", "content": "You are a helpful and expert financial advisor"},
                {"role": "user", "content": text},
                {"role": "user", "content": prompt},
            ])
        return response.choices[0].message.content
    # Handling exceptions that might occur while generating the summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""

# Function to format the summary
def format_summary(input):
    # To remove #
    cleaned_input = input.replace('#','')
    # TO remove *
    cleaned_input = cleaned_input.replace('*','')
    return cleaned_input

# Function to write text to a Word document
def write_to_docx(text, filename):
    try:
        # Creating a Document object
        doc = Document() 
        # Adding text to the document
        doc.add_paragraph(text)
        # Saving the document with the filename provided
        doc.save(filename)
    # Handling exceptions that might come while writing into the .docx file    
    except Exception as e:
        print(f"Error writing to DOCX file: {e}")

if __name__ == "__main__":
    try:
        # Here we are taking multiple pdf files as input which are separated using ','
        # eg "Apple 10K.pdf","Apple 10Q.pdf","Apple_Deutsche_Jun23.pdf"
        input_paths =input("Enter the file paths")  
        # Splitting the input_paths string by ',' to create a list of file paths
        pdf_file_paths=[path.strip() for path in input_paths.split(',')]

        # Handling the exception if no file is provided as the input
        if not pdf_file_paths:
            raise ValueError("Please provide at least one PDF file path.")
        
        # Extracting text from PDFs
        text = extract_text_from_pdf(pdf_file_paths)
        
        # Preprocessing text and here num_tokens is the total input tokens
        text, num_tokens = preprocess_text(text)
            
        # Splitting text into chunks
        text_chunks = split_text(text)

        # Generating summaries for text chunks
        chunk_summaries = []
        for chunk in text_chunks:
            chunk_summary = generate_summary(chunk,chunks_prompt)
            chunk_summaries.append(chunk_summary)
        
        # Combining chunk summaries into one text
        combined_summary_text = " ".join(chunk_summaries)
        
        # Generate final summary
        final_summary = generate_summary(combined_summary_text,final_combine_prompt)
        
        # Generating 1-page summary        
        final_summary_one_page = generate_summary(final_summary,final_combine_prompt_1_pager)

        # Writing summaries to DOCX files
        if final_summary:
            final_summary=format_summary(final_summary)
            write_to_docx(final_summary, "final_summary_two_page.docx")
            print("2 page summary generated and saved successfully.")
        if final_summary_one_page:
            final_summary_one_page=format_summary(final_summary_one_page)
            write_to_docx(final_summary_one_page, "final_summary_one_page.docx")
            print("1 page summary generated and saved successfully.")
        

    except Exception as e:
        print(f"An error occurred: {e}")
