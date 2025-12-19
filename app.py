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

# --- 2. CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    /* Background styling */
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    
    /* Main Title Styling */
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
    
    /* Card Styling for Results */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Metrics Styling */
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2980b9;
    }
    
    /* Sidebar styling */
    .sidebar-text {
        font-size: 1.1rem;
        color: #ecf0f1;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def get_text_from_pdf(file):
    return extract_text(file)

def get_text_from_docx(file):
    return docx2txt.process(file)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

# --- 4. SIDEBAR INTERFACE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.title("📂 Control Panel")
    st.markdown("Upload documents to check compatibility.")
    
    st.markdown("---")
    
    # File Uploaders
    uploaded_jd = st.file_uploader("1️⃣ Upload Job Description (JD)", type=["pdf", "docx"], help="Upload the JD file here")
    uploaded_resume = st.file_uploader("2️⃣ Upload Candidate Resume", type=["pdf", "docx"], help="Upload the Resume file here")
    
    st.markdown("---")
    st.info("💡 **Tip:** Use clear PDF or DOCX files for best results.")
    
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Arpit Upadhyay**")
    st.caption("© 2025 Aequitas AI Systems")

# --- 5. MAIN PAGE LOGIC ---

# Header Section
st.markdown('<div class="main-title">⚖️ Aequitas AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligent & Fair Resume Screening System</div>', unsafe_allow_html=True)

# Logic
if uploaded_jd and uploaded_resume:
    
    with st.spinner('⚙️ AI is analyzing the resume... Please wait...'):
        try:
            # Extract Text from JD
            if uploaded_jd.type == "application/pdf":
                jd_text = get_text_from_pdf(uploaded_jd)
            else:
                jd_text = get_text_from_docx(uploaded_jd)

            # Extract Text from Resume
            if uploaded_resume.type == "application/pdf":
                resume_text = get_text_from_pdf(uploaded_resume)
            else:
                resume_text = get_text_from_docx(uploaded_resume)

            # Clean and Calculate Match
            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)
            
            text_list = [jd_clean, resume_clean]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(text_list)
            match_percentage = cosine_similarity(count_matrix)[0][1] * 100
            match_percentage = round(match_percentage, 2)

            # --- RESULT DASHBOARD ---
            st.markdown("---")
            
            # Columns for layout
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.write("### 🎯 Compatibility Score")
                
                # Dynamic Color based on score
                if match_percentage >= 75:
                    st.markdown(f'<p class="metric-value" style="color: #27ae60;">{match_percentage}%</p>', unsafe_allow_html=True)
                    st.success("🌟 **Excellent Match!** This candidate is highly recommended.")
                    st.balloons()
                elif match_percentage >= 50:
                    st.markdown(f'<p class="metric-value" style="color: #f39c12;">{match_percentage}%</p>', unsafe_allow_html=True)
                    st.warning("⚠️ **Good Match.** Review skills manually.")
                else:
                    st.markdown(f'<p class="metric-value" style="color: #c0392b;">{match_percentage}%</p>', unsafe_allow_html=True)
                    st.error("❌ **Low Match.** Profile does not fit well.")
                
                st.progress(int(match_percentage))
                st.markdown('</div>', unsafe_allow_html=True)

            # Extra Details Section
            st.markdown("### 📝 Analysis Details")
            
            tab1, tab2 = st.tabs(["📄 Resume Preview", "🔍 Match Insights"])
            
            with tab1:
                st.text_area("Extracted Resume Text (Snippet):", resume_clean[:1000] + "...", height=200)
            
            with tab2:
                st.write("### Missing Keywords:")
                st.write("*(Feature coming soon in Aequitas v2.0)*")
                st.info(f"Resume Length: {len(resume_clean)} characters | JD Length: {len(jd_clean)} characters")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

else:
    # Default Landing Page (Jab file upload na ho)
    st.container()
    col1, col2 = st.columns(2)
    
    with col1:
        # FIX IS HERE: use_column_width instead of use_container_width
        st.image("https://img.freepik.com/free-vector/hiring-agency-candidates-job-interview_1262-18968.jpg", use_column_width=True)
    
    with col2:
        st.markdown("""
        ### 👋 Welcome to Aequitas!
        
        This tool uses advanced **Natural Language Processing (NLP)** to screen resumes fairly.
        
        **How to use:**
        1. Open the **Sidebar** (Left Panel).
        2. Upload the **Job Description (JD)**.
        3. Upload the **Resume**.
        4. Get an instant **AI Match Score**.
        
        *Built for unbiased recruitment.*
        """)

