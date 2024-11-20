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

