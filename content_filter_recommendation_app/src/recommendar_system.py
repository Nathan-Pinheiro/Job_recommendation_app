import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.model.resume import Resume

SKILLS_WEIGHT = 0.3
TITLES_WEIGHT = 0.4
INDUSTRIES_WEIGHT = 0.3

def get_recommended_jobs(job_postings : pd.DataFrame, resume_data : Resume, jobs_amount : int = 10) -> pd.DataFrame:

    tfidf = TfidfVectorizer(stop_words="english")

    df_skills_similarity = __get_skills_similarity_score(job_postings, resume_data.get_skills(), tfidf)
    df_titles_similarity = __get_titles_similarity_score(job_postings, resume_data.get_titles(), tfidf)
    df_industries_similarity = __get_industries_similarity_score(job_postings, resume_data.get_industries(), tfidf)

    df_similarities = pd.DataFrame()
    df_similarities["similarity_percentage"] = __get_similarity_percentage(df_skills_similarity, df_titles_similarity, df_industries_similarity)
    df_similarities["job_title"] = [job["title"] for job in job_postings]
    df_similarities["skills"] = [job["skills"] for job in job_postings]
    df_similarities["company_name"] = [job["company_name"] for job in job_postings]
    df_similarities["description"] = [job["description"] for job in job_postings]

    sorted_similarity_df = df_similarities.sort_values("similarity_percentage", ascending=False)

    recommended_jobs = sorted_similarity_df.head(jobs_amount)

    return recommended_jobs

def __get_similarity_percentage(df_skills_similarity : pd.DataFrame, df_titles_similarity : pd.DataFrame, df_industries_similarity : pd.DataFrame):

    skills_similarity_score = SKILLS_WEIGHT * df_skills_similarity["similarity_score"]
    titles_similarity_score = TITLES_WEIGHT * df_titles_similarity["similarity_score"]
    df_industries_similarity = INDUSTRIES_WEIGHT * df_industries_similarity["similarity_score"]
    coef_sum = TITLES_WEIGHT + SKILLS_WEIGHT + INDUSTRIES_WEIGHT

    similarity_score = ( titles_similarity_score + skills_similarity_score + df_industries_similarity)  / coef_sum

    return round(similarity_score * 100, 2)

def __get_skills_similarity_score(job_postings, resume_skills_flatten : str, tfidf : TfidfVectorizer):

    job_skills = [job["skills"] for job in job_postings]
    resume_skills = [resume_skills_flatten]

    return __get_similarity_score(job_skills, resume_skills, tfidf)

def __get_titles_similarity_score(job_postings, resume_titles_flatten : str, tfidf : TfidfVectorizer):

    jobs_title = [job["title"] for job in job_postings]
    resume_titles = [resume_titles_flatten]

    return __get_similarity_score(jobs_title, resume_titles, tfidf)

def __get_industries_similarity_score(job_postings, resume_industries_flatten : str, tfidf : TfidfVectorizer):

    jobs_industries = [job["industries"] for job in job_postings]
    resume_industries = [resume_industries_flatten]

    return __get_similarity_score(jobs_industries, resume_industries, tfidf)

def __get_similarity_score(first_flatten_list : list, second_flatten_list : list, tfidf : TfidfVectorizer):

    job_tfidf_matrix = tfidf.fit_transform(first_flatten_list)
    resume_tfidf_matrix = tfidf.transform(second_flatten_list)

    similarity_scores = cosine_similarity(job_tfidf_matrix, resume_tfidf_matrix).flatten()

    return pd.DataFrame(similarity_scores, columns=["similarity_score"])