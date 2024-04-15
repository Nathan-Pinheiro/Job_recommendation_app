import io
from src.data.resume_extractor import ResumeExtractor
from src.data.job_extractor import extract_job_postings
from src.recommendar_system import get_recommended_jobs
from src.data.database_loader import DatabaseLoader
from src.model.resume import Resume
import streamlit as st

def main():

    database_loader : DatabaseLoader = DatabaseLoader()
    resume_extractor : ResumeExtractor = ResumeExtractor()

    database_loader.load_data()
    resume_extractor.load_matchers(database_loader)

    job_postings = extract_job_postings(database_loader)

    st.set_page_config(layout="wide")
    st.title("Job Recommendation App")
    st.write("Upload your resume in PDF format")

    uploaded_file = st.file_uploader("Choose a file", type=['pdf'])

    if uploaded_file is not None:

        st.write("Resume informations :")
        file_content = io.BytesIO(uploaded_file.read())
        resume : Resume = resume_extractor.get_resume_data(file_content)
        st.write(resume)

        st.write("Jobs :")
        recommended_jobs = get_recommended_jobs(job_postings, resume, 50)
        st.write(recommended_jobs)

if __name__ == '__main__':
    main()
