import pandas as pd
from src.data.database_loader import DatabaseLoader

def extract_job_postings(database_loader : DatabaseLoader) -> pd.DataFrame:

    final : pd.DataFrame = database_loader.get_job_postings()[['job_id', 'title', 'company_id', 'description']]

    final = pd.merge(final, __get_skills_table(database_loader), on='job_id', how='left')
    final = pd.merge(final, __get_industry_table(database_loader), on='company_id', how='left')
    final = pd.merge(final, __get_job_industry_table(database_loader), on='job_id', how='left')
    final = pd.merge(final, __get_company_table(database_loader), on='company_id', how='left')

    final = __fillna(data_frame = final, column = 'skill_name', value = 'Other')
    final = __fillna(data_frame = final, column = 'description', value = 'No description')
    final = __fillna(data_frame = final, column = 'industry', value = '')
    final = __fillna(data_frame = final, column = 'industry_name', value = '')
    final = __fillna(data_frame = final, column = 'company_name', value='No company')

    final['industries'] = __get_industries(final)
    final = final.drop(['industry', 'industry_name'], axis=1)

    final = final.rename(columns={'skill_name': 'skills'})

    job_postings : dict = final[['job_id', 'title', 'skills', 'industries', 'description', 'company_name']].to_dict('records')
    for job in job_postings: job['id'] = job.pop('job_id')

    return job_postings

def __get_job_industry_table(database_loader : DatabaseLoader):

    merged_job_industry = pd.merge(database_loader.get_job_industries(), database_loader.get_industries(), on='industry_id', how="left")
    merged_job_industry["industry_name"] = merged_job_industry["industry_name"].fillna("")
    df_grouped_job_industry = merged_job_industry.groupby('job_id')['industry_name'].apply(' '.join).reset_index()

    return df_grouped_job_industry

def __get_industry_table(database_loader : DatabaseLoader):

    df_grouped_industry = database_loader.get_company_industry().groupby('company_id')['industry'].apply(' '.join).reset_index()

    return df_grouped_industry

def __get_company_table(database_loader : DatabaseLoader):

    df_grouped_company = database_loader.get_company()
    df_grouped_company['name'] = df_grouped_company['name'].fillna('')
    df_grouped_company = df_grouped_company.groupby('company_id')['name'].apply(' '.join).reset_index()
    df_grouped_company = df_grouped_company.rename(columns={'name': 'company_name'})

    return df_grouped_company

def __get_skills_table(database_loader : DatabaseLoader):

    df_skills_merged = pd.merge(database_loader.get_job_skills(), database_loader.get_skill(), on='skill_abr')
    df_skills_grouped = df_skills_merged.groupby('job_id')['skill_name'].apply(' '.join).reset_index()

    return df_skills_grouped

def __get_industries(df_final : pd.DataFrame):

    industries_list : list = []
    for _ , row in df_final.iterrows():

        industry : set = set(row['industry'].split(' ')) if row['industry'] else set()
        industry_name : set = set(row['industry_name'].split(' ')) if row['industry_name'] else set()

        if not industry and not industry_name: merged_industries = 'Other'
        else: merged_industries = ' '.join(sorted(industry | industry_name))

        industries_list.append(merged_industries)

    return industries_list

def __fillna(data_frame : pd.DataFrame, column : str, value) -> pd.DataFrame:
    data_frame[column] = data_frame[column].fillna(value)
    return data_frame

"""
# ------------------------------------------
# Testing the extract_job_posting functiun
# ------------------------------------------

if __name__ == '__main__':

    database_loader : DatabaseLoader = DatabaseLoader()
    database_loader.load_data()

    job_postings = extract_job_postings(database_loader)[:5]
    for i in range(5): print(job_postings[i])
"""

