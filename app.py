import streamlit as st
import pdfminer
from pdfminer.high_level import extract_text
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="Aequitas | Smart Resume Screening",
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

# --- 3. ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    /* Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Shining Gradient Title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #1A2980, #26D0CE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #57606f;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 400;
    }

    /* Developers Card in Sidebar */
    .dev-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .dev-header {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .dev-names {
        font-size: 1.1rem;
        font-weight: 600;
        line-height: 1.4;
    }

    /* Score Card Styling */
    .score-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #e1e1e1;
    }
    
    /* Tags */
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
        if skill in words:
            found_skills.add(skill)
        elif " " in skill and skill in cleaned_text:
            found_skills.add(skill)
    return found_skills

# --- 5. SIDEBAR (Updated with Developers at TOP) ---
with st.sidebar:
    # App Logo
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620986.png", width=70)
    
    # Developers Section (Top & Fascinating)
    st.markdown("""
        <div class="dev-card">
            <div class="dev-header">🚀 Built By Team Aequitas</div>
            <div class="dev-names">
                Arpit Upadhyay<br>
                Devansh Thakur<br>
                Arjun Kumar
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("📂 Upload Documents")
    uploaded_jd = st.file_uploader("1️⃣ Job Description (JD)", type=["pdf", "docx"])
    uploaded_resume = st.file_uploader("2️⃣ Candidate Resume", type=["pdf", "docx"])
    
    st.markdown("---")
    st.info("💡 **Note:** Works best with standard PDF/DOCX formats.")

# --- 6. MAIN PAGE ---
# Gradient Title
st.markdown('<div class="main-title">Aequitas AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligent & Fair Resume Screening System</div>', unsafe_allow_html=True)

if uploaded_jd and uploaded_resume:
    with st.spinner('⚡ AI is processing your documents...'):
        try:
            # Extraction
            if uploaded_jd.type == "application/pdf": jd_text = get_text_from_pdf(uploaded_jd)
            else: jd_text = get_text_from_docx(uploaded_jd)
            
            if uploaded_resume.type == "application/pdf": resume_text = get_text_from_pdf(uploaded_resume)
            else: resume_text = get_text_from_docx(uploaded_resume)

            # Analysis
            jd_skills = extract_skills(jd_text)
            resume_skills = extract_skills(resume_text)
            matched_skills = jd_skills.intersection(resume_skills)
            missing_skills = jd_skills.difference(resume_skills)

            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)
            cv = CountVectorizer()
            count_matrix = cv.fit_transform([jd_clean, resume_clean])
            match_percentage = round(cosine_similarity(count_matrix)[0][1] * 100, 2)

            # Results
            st.markdown("---")
            col1, col2 = st.columns([1, 1.5])

            with col1:
                st.markdown('<div class="score-card">', unsafe_allow_html=True)
                st.write("### 🎯 Match Score")
                if match_percentage >= 75:
                    st.markdown(f"<h1 style='color: #198754; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.success("✅ Excellent Match!")
                    st.balloons()
                elif match_percentage >= 50:
                    st.markdown(f"<h1 style='color: #fd7e14; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.warning("⚠️ Good Match")
                else:
                    st.markdown(f"<h1 style='color: #dc3545; font-size: 3.5rem;'>{match_percentage}%</h1>", unsafe_allow_html=True)
                    st.error("❌ Low Match")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("### 🧬 Skill DNA Analysis")
                
                st.write("**✅ Skills Matched:**")
                if matched_skills:
                    st.markdown("".join([f'<span class="skill-tag match-tag">{s.upper()}</span>' for s in matched_skills]), unsafe_allow_html=True)
                else:
                    st.warning("No skills matched directly.")
                
                st.write("---")
                
                st.write("**⚠️ Skills Missing:**")
                if missing_skills:
                    st.markdown("".join([f'<span class="skill-tag missing-tag">{s.upper()}</span>' for s in missing_skills]), unsafe_allow_html=True)
                else:
                    st.success("All required skills are present!")

            with st.expander("📄 View Resume Snippet"):
                st.info(resume_text[:600] + "...")

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    # --- LANDING PAGE (UPDATED IMAGE) ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # PROFESSIONAL HIGH-QUALITY VECTOR IMAGE
        st.image("https://img.freepik.com/free-vector/human-resources-management-concept-illustration_114360-8423.jpg", use_column_width=True)
    
    with col2:
        st.markdown("""
        <div style="padding-top: 20px;">
            <h3>👋 Welcome to the Future of Hiring</h3>
            <p style="font-size: 1.1rem; color: #555;">
                <b>Aequitas AI</b> eliminates bias and saves time by using advanced NLP to match resumes with job descriptions accurately.
            </p>
            <ul style="font-size: 1rem; line-height: 2;">
                <li>🚀 <b>Instant Compatibility Scores</b></li>
                <li>🧠 <b>Deep Skill Analysis (Matched vs Missing)</b></li>
                <li>⚖️ <b>Unbiased & Fair Screening</b></li>
            </ul>
            <br>
            <div style="background-color: #e8f0fe; padding: 15px; border-radius: 10px; border-left: 5px solid #4285f4;">
                <small>👈 <b>Start Now:</b> Upload JD & Resume from the Sidebar!</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
