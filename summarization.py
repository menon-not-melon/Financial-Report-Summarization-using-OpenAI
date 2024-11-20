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
chunks_prompt="""
i want all the detailed information on this
1. Business Overview – Include information such as the company's formation/incorporation date, headquarters location, business description, employee count, latest revenues, stock exchange listing and market capitalization, number of offices and locations, and details on their clients/customers. 2. Business Segment Overview. i. Extract the revenue percentage of each component (verticals, products, segments, and sections) as a part of the total revenue. ii. Performance: Evaluate the performance of each component by comparing the current year's sales/revenue and market share with the previous year's numbers.  iii. Sales Increase/Decrease explanation: Explain the causes of the increase or decrease in the performance of each component.  4. Breakdown of sales and revenue by geography, specifying the percentage contribution of each region to the total sales. 5. Summarize geographical data, such as workforce, clients, and offices, and outline the company's regional plans for expansion or reduction. 6. Analyze and explain regional sales fluctuations, including a geographical sales breakdown to identify sales trends. 7. Year-over-year sales increase or decline and reasons for the change. 8. Summary of rationale & considerations (risks & mitigating factors). 9. SWOT Analysis which elaborates to Strenths, weaknesses, opportunities and Threats a company. 10. Information about credit rating/credit rating change/change in the rating outlook 

Document:`{text}'
Summary:
"""
custom_prompt = PromptTemplate(template=chunks_prompt,input_variables=["text"])
