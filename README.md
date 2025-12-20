# ⚖️ Aequitas: AI Resume Auditor

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B)
![Status](https://img.shields.io/badge/Status-Live-success)

> **Intelligent & Fair Resume Screening System using NLP.** > *Analyzes Resumes against Job Descriptions to provide Match Scores & Skill Gap Analysis.*

---

## 🚀 Live Demo
Check out the live application here:  
👉 **[Launch Aequitas AI App](https://aequitas-arpit7088.streamlit.app/)** *(Note: If the link doesn't open, please check the repository description)*

---

## 🧐 About The Project

**Aequitas AI** is a Resume Parsing and Screening tool designed to help recruiters and candidates by automating the initial screening process. Unlike traditional keyword matching, this tool uses **Cosine Similarity** and **Natural Language Processing (NLP)** to calculate the match percentage accurately.

### Key Features:
* **📄 Multi-Format Support:** Accepts PDF and DOCX files for both Resumes and JDs.
* **🧠 Intelligent Parsing:** Extracts text and cleans it using NLP techniques (Regex & Tokenization).
* **📊 Compatibility Score:** Calculates a match percentage (0-100%) based on vector similarity.
* **🧬 Skill DNA Analysis:**
    * ✅ **Matched Skills:** Shows skills present in both documents.
    * ❌ **Missing Skills:** Highlights critical skills missing from the resume.
* **⚖️ Bias Reduction:** Focuses purely on technical skills and content.

---

## 📸 Screenshots

| **Dashboard Interface** | **Analysis Result** |
|:---:|:---:|
| <img src="https://website-artificio.s3.us-west-2.amazonaws.com/Resume_Parsing_a180290fcd.jpg" width="400"> | *Add your result screenshot here* |

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend:** Python 3.10
* **NLP & ML:** Scikit-Learn (Cosine Similarity, CountVectorizer)
* **Text Processing:** `pdfminer.six` (PDF), `docx2txt` (DOCX), `re` (Regex)

---

## ⚙️ How to Run Locally

If you want to run this project on your local machine, follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Arpit7088/Aequitas.git](https://github.com/Arpit7088/Aequitas.git)
    cd Aequitas
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

---

## 👨‍💻 By

**Arpit Upadhyay** *B.Tech AI/ML Student* GitHub: [@Arpit7088](https://github.com/Arpit7088)

---

<p align="center">
  <i>Built with ❤️ using Python & Streamlit</i>
</p>
