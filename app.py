import streamlit as st
import tempfile
import os
from pdf_parser import extract_text_from_bytes
from summarizer import summarize_resume_projects, get_available_models

st.set_page_config(
    page_title="Resume Project Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">📄 Resume Project Summarizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform technical projects into non-technical summaries in seconds!</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    
    available_models = get_available_models()
    selected_model = st.selectbox(
        "Select Groq Model",
        available_models,
        index=0,
        help="Different models offer varying speeds and quality"
    )
    
    st.divider()
    
    st.header("ℹ️ About")
    st.markdown("""
    This tool helps non-technical people understand technical projects on resumes.
    
    **How it works:**
    1. Upload a resume PDF
    2. AI extracts and analyzes projects
    3. Get simple, jargon-free summaries
    
    **Perfect for:**
    - HR managers
    - Non-technical recruiters
    - Hiring managers
    - Business stakeholders
    """)
    
    st.divider()
    
    st.header("📊 Benefits")
    st.markdown("""
    - ⏱️ **Saves 1+ hour** per resume
    - 🎯 **Accurate** project assessment
    - 💡 **Easy to understand** explanations
    - 📈 **Impact ratings** for each project
    """)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF resume",
        type=["pdf"],
        help="Upload a resume in PDF format"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.info(f"📊 File size: {uploaded_file.size / 1024:.2f} KB")

with col2:
    st.header("🎯 Actions")
    analyze_button = st.button(
        "🚀 Analyze Resume",
        type="primary",
        disabled=not uploaded_file,
        use_container_width=True
    )

if analyze_button and uploaded_file:
    
    with st.spinner("🔍 Extracting text from PDF..."):
        try:
            pdf_bytes = uploaded_file.read()
            resume_text = extract_text_from_bytes(pdf_bytes)
            
            if not resume_text or len(resume_text) < 50:
                st.error("❌ Could not extract sufficient text from PDF.")
                st.stop()
            
            st.success(f"✅ Extracted {len(resume_text)} characters from resume")
            
        except Exception as e:
            st.error(f"❌ Error extracting PDF: {str(e)}")
            st.stop()
    
    with st.spinner(f"🤖 Analyzing projects with {selected_model}..."):
        try:
            summary = summarize_resume_projects(resume_text, model=selected_model)
            
            st.success("✅ Analysis complete!")
            
            st.divider()
            st.header("📋 Project Summaries")
            
            with st.expander("📄 View Extracted Resume Text"):
                st.text_area("Raw Text", resume_text, height=200)
            
            st.markdown(summary)
            
            st.divider()
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                st.download_button(
                    label="📥 Download Summary (TXT)",
                    data=summary,
                    file_name=f"{uploaded_file.name.replace('.pdf', '')}_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_download2:
                markdown_content = f"# Resume Project Summary\n\n**File**: {uploaded_file.name}\n\n**Model Used**: {selected_model}\n\n---\n\n{summary}"
                st.download_button(
                    label="📥 Download Summary (MD)",
                    data=markdown_content,
                    file_name=f"{uploaded_file.name.replace('.pdf', '')}_summary.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
        except Exception as e:
            st.error(f"❌ Error generating summary: {str(e)}")
            st.info("💡 Please check your GROQ_API_KEY")

st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Built with Streamlit 🎈 | Powered by Groq ⚡ | PDF parsing with PyMuPDF 📄</p>
</div>
""", unsafe_allow_html=True)
