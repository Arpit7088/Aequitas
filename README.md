# Aequitas: An Intelligent and Fair AI System for Resume Screening ⚖️🤖

## Introduction
**Aequitas** (meaning Fairness) is a web application designed to evaluate the compatibility of a resume with a job description. Utilizing Natural Language Processing (NLP) techniques, the app extracts and compares key skills from both documents to provide a compatibility score. 

The goal of Aequitas is to make recruitment **unbiased** and efficient by focusing purely on skills and compatibility scores using machine learning models.


## Features
- **File Upload:** Users can upload job descriptions and resumes in PDF or DOCX format.
- **Text Extraction:** Extracts text from uploaded documents using `pdfminer` and `docx2txt`.
- **Skill Extraction:** Identifies and extracts relevant skills from the text using a predefined skill set.
- **Compatibility Score:** Calculates a similarity score between the resume and the job description.
- **Skills Comparison:** Displays matching and missing skills based on the extracted data.
  
## Technical Details
1. **Text Extraction:**
   - PDF text extraction is performed using `pdfminer`.
   - DOCX text extraction is done using `docx2txt`.

2. **Skill Extraction:**
   - Skills are matched against a predefined list using regular expressions.

3. **Similarity Calculation:**
   - Utilizes `CountVectorizer` and `cosine_similarity` from `sklearn` to compute the compatibility score.

4. **Streamlit WebApp:**
   - Provides an interactive interface for users to upload files and view results.
   - Displays the compatibility score and skill comparison using custom styling.

## Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/Arpit7088/Aequitas.git](https://github.com/Arpit7088/Aequitas.git)
   cd Aequitas
