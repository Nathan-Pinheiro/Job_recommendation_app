import spacy
from spacy.matcher import Matcher
import PyPDF2
from src.data.database_loader import DatabaseLoader
from src.model.resume import Resume
import os

class ResumeExtractor:

    nlp = spacy.load('en_core_web_sm')
    skills_matcher : Matcher
    titles_matcher : Matcher
    industries_matcher : Matcher

    def get_resume_data(self, file_content) -> Resume :

        resume_text = self.__extract_text_from_pdf(file_content)

        skills = self.__extract_skills_from_text(resume_text)
        titles = self.__extract_titles_from_text(resume_text)
        industries = self.__extract_industries_from_text(resume_text)

        return Resume(" ".join(skills), " ".join(titles),  " ".join(industries))

    def load_matchers(self, database_loader: DatabaseLoader) -> None :

        self.skills_matcher = Matcher(self.nlp.vocab)
        self.titles_matcher = Matcher(self.nlp.vocab)
        self.industries_matcher = Matcher(self.nlp.vocab)

        skills = database_loader.get_skill()['skill_name'].str.lower().tolist()
        titles = database_loader.get_job_postings()['title'].str.lower().tolist()
        industries = database_loader.get_industries()['industry_name'].fillna("").str.lower().tolist()

        skill_patterns = [[{'LOWER': skill}] for skill in skills]
        for pattern in skill_patterns:
            self.skills_matcher.add('Skills', [pattern])

        title_patterns = [[{'LOWER': title}] for title in titles]
        for pattern in title_patterns:
            self.titles_matcher.add('Titles', [pattern])

        industries_pattern = [[{'LOWER': industry}] for industry in industries]
        for pattern in industries_pattern:
            self.industries_matcher.add('Industries', [pattern])

    def __extract_skills_from_text(self, text : str):

        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        matched_skills = set()

        for sentence in sentences:

            doc = self.nlp(sentence)
            matches = self.skills_matcher(doc)
            matched_skills |= set([doc[start:end].text for _ , start, end in matches])

        return matched_skills

    def __extract_titles_from_text(self, text : str):

        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        matched_titles = set()

        for sentence in sentences:

            doc = self.nlp(sentence)
            matches = self.titles_matcher(doc)
            matched_titles |= set([doc[start:end].text for _ , start, end in matches])

        return matched_titles

    def __extract_industries_from_text(self, text : str):

        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        matched_titles = set()

        for sentence in sentences:

            doc = self.nlp(sentence)
            matches = self.industries_matcher(doc)
            matched_titles |= set([doc[start:end].text for _ , start, end in matches])

        return matched_titles

    def __extract_text_from_pdf(self, file_content):

        pdf_reader = PyPDF2.PdfReader(file_content)
        text = ''

        for page in pdf_reader.pages:
            text += page.extract_text().lower()

        return text

"""
# ------------------------------------------
# Testing the ResumeExtractor object
# ------------------------------------------

if __name__ == '__main__':

    database_loader : DatabaseLoader = DatabaseLoader()
    database_loader.load_data()

    resumeExtractor : ResumeExtractor = ResumeExtractor()
    resumeExtractor.load_matchers(database_loader)

    print(resumeExtractor.get_resume_data())
"""