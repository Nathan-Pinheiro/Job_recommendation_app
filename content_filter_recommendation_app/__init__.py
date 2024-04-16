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

        if 'num_jobs' not in st.session_state:
            st.session_state.num_jobs = 10

        st.write("Jobs :")
        recommended_jobs = get_recommended_jobs(job_postings, resume, 100)

        for i, job in enumerate(recommended_jobs[:st.session_state.num_jobs]):
            with st.expander(job['title']):
                st.write('**Company:**', job['company'])
                st.write('**Location:**', job['location'])
                st.write('**Description:**', job['description'])

        if st.session_state.num_jobs < len(recommended_jobs):
            if st.button("Show more jobs"):
                st.session_state.num_jobs += 10

if __name__ == '__main__':
    main()
