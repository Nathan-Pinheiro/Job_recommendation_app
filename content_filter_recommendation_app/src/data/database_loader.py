import pandas as pd
import os
from spacy.matcher import Matcher

DATA_DIR : str = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'resources', 'dataset')

JOB_POSTING_URL : str = os.path.join(DATA_DIR, 'job_postings.csv')
JOB_SKILLS_URL : str = os.path.join(DATA_DIR, 'job_details', 'job_skills.csv')
JOB_INDUSTRY_URL : str = os.path.join(DATA_DIR, 'job_details', 'job_industries.csv')
COMPANY_INDUSTRY_URL : str = os.path.join(DATA_DIR, 'company_details', 'company_industries.csv')
COMPANIES_URL : str = os.path.join(DATA_DIR, 'company_details', 'companies.csv')
INDUSTRIES_URL : str = os.path.join(DATA_DIR, 'maps', 'industries.csv')
SKILLS_URL : str = os.path.join(DATA_DIR, 'maps', 'skills.csv')

class DatabaseLoader:

    job_postings : pd.DataFrame
    industries : pd.DataFrame
    company_industry : pd.DataFrame
    job_skills : pd.DataFrame
    skill : pd.DataFrame
    company : pd.DataFrame

    skills_matcher : Matcher
    titles_matcher : Matcher

    def load_data(self) -> None:

        self.job_postings = pd.read_csv(JOB_POSTING_URL)
        self.job_industries = pd.read_csv(JOB_INDUSTRY_URL)
        self.industries = pd.read_csv(INDUSTRIES_URL)
        self.company_industry = pd.read_csv(COMPANY_INDUSTRY_URL)
        self.job_skills = pd.read_csv(JOB_SKILLS_URL)
        self.skill = pd.read_csv(SKILLS_URL)
        self.company = pd.read_csv(COMPANIES_URL)

        #companies : pd.DataFrame = pd.read_csv(COMPANIES_URL)

    def get_job_postings(self) -> pd.DataFrame:
        return self.job_postings

    def get_job_industries(self) -> pd.DataFrame:
        return self.job_industries

    def get_industries(self) -> pd.DataFrame:
        return self.industries

    def get_company_industry(self) -> pd.DataFrame:
        return self.company_industry

    def get_job_skills(self) -> pd.DataFrame:
        return self.job_skills

    def get_skill(self) -> pd.DataFrame:
        return self.skill

    def get_company(self) -> pd.DataFrame:
        return self.company