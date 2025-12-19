import streamlit as st
import pdfminer
from pdfminer.high_level import extract_text
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="Aequitas: AI Resume Auditor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SKILL DATABASE ---
SKILL_DB = [
    "python", "java", "c++", "c", "javascript", "typescript", "php", "ruby", "swift", "kotlin", "go", "rust", "sql", "r", "matlab",
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "bootstrap", "tailwind", "jquery",
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "nltk", "spacy", "matplotlib", "seaborn", "tableau", "power bi", "excel",
    "aws", "azure", "google cloud", "docker", "kubernetes", "jenkins", "git", "github", "gitlab", "linux", "unix", "bash", "terraform",
    "mysql", "postgresql", "mongodb", "oracle", "sqlite", "redis", "cassandra",
    "communication", "leadership", "problem solving", "agile", "scrum", "project management", "critical thinking"
]

# --- 3. INJECT FONT AWESOME & CUSTOM CSS ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Dark Header Strip */
    .header-strip {
        background-color: #0f172a; /* Dark Blue-Black Theme */
        padding: 20px;
        border-radius: 10px;
        color: white;
        display: flex;
        align-items: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-logo {
        font-size: 40px;
        color: #0078D4; /* The exact blue color you wanted */
        margin-right: 20px;
    }
    .header-text h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
    }
    .header-text p {
        margin: 0;
        font-size: 1rem;
        color: #94a3b8;
    }

    /* Developer Card (Accurate Middle Position) */
    .dev-card-simple {
        background-color: #ffffff;
        border-left: 5px solid #0078D4;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .dev-title {
        font-size: 0.85rem;
        font-weight: bold;
        color: #555;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .dev-list {
        font-size: 1rem;
        color: #222;
        font-weight: 600;
        line-height: 1.6;
    }

    /* Score Card & Tags */
    .score-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #e1e1e1;
    }
    .skill-tag {
        display: inline-block;
        padding: 6px 12px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .match-tag { background-color: #d1e7dd; color: #0f5132; border: 1px solid #badbcc; }
    .missing-tag { background-color: #f8d7da; color: #842029; border: 1px solid #f5c2c7; }
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
    text = re.sub(r'[^\w\s]', ' ', text)
    return text
def extract_skills(text):
    found_skills = set()
    cleaned_text = clean_text(text)
    words = set(cleaned_text.split())
    for skill in SKILL_DB:
        if skill in words: found_skills.add(skill)
        elif " " in skill and skill in cleaned_text: found_skills.add(skill)
    return found_skills

# --- 5. SIDEBAR (Correct Order & Position) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("Control Panel")
    
    # 1. Upload Section
    st.markdown("### 1. Upload Documents")
    uploaded_jd = st.file_uploader("Job Description (JD)", type=["pdf", "docx"])
    uploaded_resume = st.file_uploader("Candidate Resume", type=["pdf", "docx"])
    
    st.markdown("---")

    # 2. Developers Section (Accurate Middle Position)
    # Order: Devansh -> Arpit -> Arjun
    st.markdown("""
        <div class="dev-card-simple">
            <div class="dev-title">🚀 Developed By</div>
            <div class="dev-list">
                1. Devansh Thakur<br>
                2. Arpit Upadhyay<br>
                3. Arjun Kumar
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Aequitas v1.0 | Final Year Project")

# --- 6. MAIN PAGE HEADER ---
# Using FontAwesome Icon as requested in screenshot
st.markdown("""
    <div class="header-strip">
        <i class="fas fa-balance-scale header-logo"></i>
        <div class="header-text">
            <h1>Aequitas: AI Resume Auditor</h1>
            <p>Intelligent & Fair Resume Screening System</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 7. LOGIC & DASHBOARD ---
if uploaded_jd and uploaded_resume:
    with st.spinner('⚡ AI is auditing the resume...'):
        try:
            if uploaded_jd.type == "application/pdf": jd_text = get_text_from_pdf(uploaded_jd)
            else: jd_text = get_text_from_docx(uploaded_jd)
            if uploaded_resume.type == "application/pdf": resume_text = get_text_from_pdf(uploaded_resume)
            else: resume_text = get_text_from_docx(uploaded_resume)

            jd_skills = extract_skills(jd_text)
            resume_skills = extract_skills(resume_text)
            matched_skills = jd_skills.intersection(resume_skills)
            missing_skills = jd_skills.difference(resume_skills)

            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)
            cv = CountVectorizer()
            count_matrix = cv.fit_transform([jd_clean, resume_clean])
            match_percentage = round(cosine_similarity(count_matrix)[0][1] * 100, 2)

            # --- RESULT SECTION ---
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)
                st.write("### 🎯 Match Score")
                if match_percentage >= 75:
                    st.markdown(f"<h1 style='color: #198754; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.success("✅ Excellent Match")
                    st.balloons()
                elif match_percentage >= 50:
                    st.markdown(f"<h1 style='color: #fd7e14; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.warning("⚠️ Average Match")
                else:
                    st.markdown(f"<h1 style='color: #dc3545; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.error("❌ Low Match")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.write("### 🧬 Skill Audit")
                st.write("**✅ Matched Skills:**")
                if matched_skills: st.markdown("".join([f'<span class="skill-tag match-tag">{s.upper()}</span>' for s in matched_skills]), unsafe_allow_html=True)
                else: st.warning("No skills matched directly.")
                
                st.write("---")
                
                st.write("**❌ Missing Skills:**")
                if missing_skills: st.markdown("".join([f'<span class="skill-tag missing-tag">{s.upper()}</span>' for s in missing_skills]), unsafe_allow_html=True)
                else: st.success("No key skills missing!")

            with st.expander("📄 View Resume Snippet"):
                st.info(resume_text[:600] + "...")

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    # --- LANDING PAGE (UPDATED WITH YOUR S3 IMAGE) ---
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # Using the exact S3 link you provided
        st.image("https://website-artificio.s3.us-west-2.amazonaws.com/Resume_Parsing_a180290fcd.jpg", use_column_width=True)
    
    with col2:
        st.markdown("""
        <div style="padding-top: 20px; padding-left: 10px;">
            <h2 style="color: #2c3e50;">Automated Resume Parsing</h2>
            <p style="font-size: 1.1rem; color: #555; line-height: 1.6;">
                <b>Aequitas AI</b> is a powerful tool designed to help recruiters and candidates by providing an unbiased, automated analysis of resumes against job descriptions.
            </p>
            <ul style="font-size: 1rem; line-height: 1.8; color: #444;">
                <li>🚀 <b>Instant Match Calculation</b></li>
                <li>⚖️ <b>Fair & Unbiased Screening</b></li>
                <li>🔍 <b>Detailed Skill Gap Analysis</b></li>
            </ul>
            <br>
            <div style="background-color: #f1f5f9; padding: 15px; border-radius: 8px; border-left: 5px solid #0078D4;">
                <small>👈 <b>Start Audit:</b> Upload JD & Resume from the Sidebar.</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

