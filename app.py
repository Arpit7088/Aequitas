import streamlit as st
import pdfminer
from pdfminer.high_level import extract_text
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="Aequitas | AI Resume Screener",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SKILL DATABASE (Is list ko aap aur bada kar sakte ho) ---
SKILL_DB = [
    # Programming Languages
    "python", "java", "c++", "c", "javascript", "typescript", "php", "ruby", "swift", "kotlin", "go", "rust", "sql", "r", "matlab",
    # Web Development
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "bootstrap", "tailwind", "jquery",
    # Data Science & ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "nltk", "spacy", "matplotlib", "seaborn", "tableau", "power bi", "excel",
    # Cloud & DevOps
    "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", "git", "github", "gitlab", "linux", "unix", "bash", "terraform",
    # Databases
    "mysql", "postgresql", "mongodb", "oracle", "sqlite", "redis", "cassandra",
    # Soft Skills & Others
    "communication", "leadership", "problem solving", "agile", "scrum", "project management", "critical thinking"
]

# --- 3. CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    .main-title {
        font-size: 3rem;
        color: #2C3E50;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 30px;
    }
    .skill-tag {
        display: inline-block;
        padding: 5px 10px;
        margin: 5px;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .match-tag {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .missing-tag {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. HELPER FUNCTIONS ---
def get_text_from_pdf(file):
    return extract_text(file)

def get_text_from_docx(file):
    return docx2txt.process(file)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', text) # Punctuation hatao
    return text

def extract_skills(text):
    """Text me se skills dhundh kar set return karega"""
    found_skills = set()
    cleaned_text = clean_text(text)
    words = set(cleaned_text.split()) # Text ko words me todo
    
    for skill in SKILL_DB:
        # Check agar skill as a word exist karta hai (e.g. "java")
        if skill in words:
            found_skills.add(skill)
        # Check for multi-word skills (e.g. "power bi")
        elif " " in skill and skill in cleaned_text:
            found_skills.add(skill)
            
    return found_skills

# --- 5. SIDEBAR INTERFACE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("📂 Control Panel")
    st.markdown("Upload documents to check compatibility.")
    st.markdown("---")
    uploaded_jd = st.file_uploader("1️⃣ Upload Job Description (JD)", type=["pdf", "docx"])
    uploaded_resume = st.file_uploader("2️⃣ Upload Candidate Resume", type=["pdf", "docx"])
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Arpit Upadhyay**")

# --- 6. MAIN PAGE LOGIC ---
st.markdown('<div class="main-title">⚖️ Aequitas AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligent & Fair Resume Screening System</div>', unsafe_allow_html=True)

if uploaded_jd and uploaded_resume:
    with st.spinner('⚙️ Analyzing Skills & Compatibility...'):
        try:
            # 1. Text Extraction
            if uploaded_jd.type == "application/pdf":
                jd_text = get_text_from_pdf(uploaded_jd)
            else:
                jd_text = get_text_from_docx(uploaded_jd)

            if uploaded_resume.type == "application/pdf":
                resume_text = get_text_from_pdf(uploaded_resume)
            else:
                resume_text = get_text_from_docx(uploaded_resume)

            # 2. Skill Extraction Logic
            jd_skills = extract_skills(jd_text)
            resume_skills = extract_skills(resume_text)

            matched_skills = jd_skills.intersection(resume_skills)
            missing_skills = jd_skills.difference(resume_skills)

            # 3. Match Score Calculation (Cosine Similarity)
            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)
            text_list = [jd_clean, resume_clean]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(text_list)
            match_percentage = cosine_similarity(count_matrix)[0][1] * 100
            match_percentage = round(match_percentage, 2)

            # --- DISPLAY RESULTS ---
            st.markdown("---")
            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.subheader("🎯 Match Score")
                st.markdown(f"<h1 style='color: #2980b9;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                st.progress(int(match_percentage))
                
                if match_percentage >= 75:
                    st.success("✅ Strong Match!")
                elif match_percentage >= 50:
                    st.warning("⚠️ Average Match")
                else:
                    st.error("❌ Weak Match")

            with col2:
                st.subheader("🛠️ Skill Analysis")
                
                # Matched Skills
                st.write("**✅ Matched Skills (Present in both):**")
                if matched_skills:
                    match_html = "".join([f'<span class="skill-tag match-tag">{skill.upper()}</span>' for skill in matched_skills])
                    st.markdown(match_html, unsafe_allow_html=True)
                else:
                    st.info("No direct skill matches found.")

                st.write("") # Spacer

                # Missing Skills
                st.write("**❌ Missing Skills (Required by JD):**")
                if missing_skills:
                    missing_html = "".join([f'<span class="skill-tag missing-tag">{skill.upper()}</span>' for skill in missing_skills])
                    st.markdown(missing_html, unsafe_allow_html=True)
                else:
                    st.success("No critical skills missing!")

            # Raw Data Preview
            with st.expander("📄 View Extracted Text"):
                st.write("**Resume Content Snippet:**")
                st.caption(resume_clean[:500] + "...")

        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info("👈 Please upload both JD and Resume from the sidebar.")
    # use_column_width is the fix for the error you saw earlier
    st.image("https://img.freepik.com/free-vector/hiring-agency-candidates-job-interview_1262-18968.jpg", use_column_width=True)


