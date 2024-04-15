class Resume :

    __skills : str
    __titles : str
    __indutries : str

    def __init__(self, skills, titles, industries) -> None:
        self.__skills = skills
        self.__titles = titles
        self.__indutries = industries

    def __str__(self) -> str:
        return f"Skills: {self.__skills}\nTitles: {self.__titles}\nIndutries: {self.__indutries}"

    def get_skills(self) -> str:
        return self.__skills

    def get_titles(self) -> str:
        return self.__titles

    def get_industries(self) -> str:
        return self.__indutries