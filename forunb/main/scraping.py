""" Obtendo os dados das disciplinas da UnB. """

from typing import List, Optional
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
from .sessions import URL, HEADERS, create_request_session, get_session_cookie, get_response

def get_list_of_departments(response=get_response(create_request_session())) -> Optional[List]:
    """ Obtem a lista de departamentos da UnB."""
    soup = BeautifulSoup(response.content, "html.parser")
    departments = soup.find("select", attrs={"id": "formTurma:inputDepto"})

    if departments is None:
        return None

    options_tag = departments.find_all("option")
    department_ids = [option["value"] for option in options_tag if option["value"] != "0"]

    return department_ids

class DisciplineWebScraper:
    """ Classe para raspar dados das disciplinas do site Sigaa da UnB. """
    def __init__(self, department: str, year: str, period: str, url=URL, session=None, cookie=None):
        self.disciplines: defaultdict[str, List[str]] = defaultdict(list)
        self.department = department
        self.period = period
        self.year = year
        self.url = url
        self.data = {
            "formTurma": "formTurma",
            "formTurma:inputNivel": "",
            "formTurma:inputDepto": self.department,
            "formTurma:inputAno": self.year,
            "formTurma:inputPeriodo": self.period,
            "formTurma:j_id_jsp_1370969402_11": "Buscar",
            "javax.faces.ViewState": "j_id1"
        }

        self.session = session if session is not None else create_request_session()
        self.cookie = cookie if cookie is not None else get_session_cookie(self.session)
        self.response = None

    def get_response_from_disciplines_post_request(self) -> requests.Response:
        """ Realiza um post request para obter a resposta com as disciplas. """
        self.response = self.session.post(
            self.url,
            headers=HEADERS,
            cookies=self.cookie,
            data=self.data
        )

    def make_disciplines(self, rows: str) -> None:
        """ Cria um dicionário com as disciplinas. """
        if rows is None or not len(rows):
            return None

        aux_title_and_code = ""

        for discipline in rows:
            if discipline.find("span", attrs={"class": "tituloDisciplina"}) is not None:
                title = discipline.find("span", attrs={"class": "tituloDisciplina"})
                aux_title_and_code = title.get_text().strip('-')

            elif "linhaPar" in discipline.get("class", []) or "linhaImpar" in discipline.get("class", []):
                code, name = aux_title_and_code.split(' - ', 1)
                self.disciplines[code].append(name)

    def retrieve_classes_tables(self, response):
        """ Obtém as tabelas com as disciplinas. """
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find("table", attrs={"class": "listagem"})

        if tables is None:
            return None

        return tables

    def make_web_scraping_of_disciplines(self, response) -> None:
        """ Realiza a raspagem de dados das disciplas. """
        tables = self.retrieve_classes_tables(response)

        if not tables:
            return None

        table_rows = tables.find_all("tr")
        self.make_disciplines(table_rows)

    def get_disciplines(self) -> defaultdict[str, List[str]]:
        """ Retorna um dicionário com as disciplinas. """
        if not self.response:
            self.get_response_from_disciplines_post_request()
        self.make_web_scraping_of_disciplines(self.response)

        return self.disciplines
