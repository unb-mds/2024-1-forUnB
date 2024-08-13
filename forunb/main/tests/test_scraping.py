import unittest
from unittest.mock import patch, MagicMock
from main.scraping import get_list_of_departments, DisciplineWebScraper, defaultdict, BeautifulSoup
from main.sessions import create_request_session

class TestScraping(unittest.TestCase):

    @patch('main.scraping.get_response')
    def test_get_list_of_departments_success(self, mock_get_response):
        # Testa a função get_list_of_departments para garantir que ela extrai corretamente
        # os IDs dos departamentos a partir de uma resposta HTML simulada que contém 
        # um elemento <select> com opções de departamentos.
        html_content = '''
        <html>
        <body>
            <select id="formTurma:inputDepto">
                <option value="0">Selecione</option>
                <option value="1">Departamento 1</option>
                <option value="2">Departamento 2</option>
                <option value="640">Departamento X</option>
            </select>
        </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.content = html_content.encode('utf-8')
        mock_get_response.return_value = mock_response

        departments = get_list_of_departments()
        self.assertIn('978', departments)
        self.assertIn('314', departments)

    @patch('main.scraping.create_request_session')
    @patch('main.scraping.get_session_cookie')
    def test_discipline_web_scraper_initialization(self, mock_get_session_cookie, mock_create_request_session):
        # Testa a inicialização da classe DisciplineWebScraper para garantir que 
        # a sessão e os cookies sejam configurados corretamente usando mocks.
        # Verifica se os atributos department, year, period, session e cookie 
        # são definidos como esperado e se a resposta inicial é None.
        mock_session = MagicMock()
        mock_create_request_session.return_value = mock_session
        
        mock_cookie = MagicMock()
        mock_get_session_cookie.return_value = mock_cookie

        scraper = DisciplineWebScraper(department='1', year='2024', period='1')
        
        mock_create_request_session.assert_called_once()  # Garante que a sessão foi criada uma vez
        self.assertEqual(scraper.department, '1')
        self.assertEqual(scraper.year, '2024')
        self.assertEqual(scraper.period, '1')
        self.assertIs(scraper.session, mock_session)  # Verifica se a sessão foi definida para a sessão simulada
        self.assertEqual(scraper.cookie, mock_cookie)
        self.assertIsNone(scraper.response)

    @patch('main.scraping.DisciplineWebScraper.get_response_from_disciplines_post_request')
    @patch('main.scraping.DisciplineWebScraper.retrieve_classes_tables')
    def test_make_web_scraping_of_disciplines_success(self, mock_retrieve_classes_tables, mock_get_response_from_disciplines_post_request):
        # Testa o processo de web scraping para garantir que as disciplinas sejam
        # extraídas corretamente de uma resposta HTML simulada que contém uma tabela 
        # com dados de disciplinas. Verifica se as disciplinas são adicionadas 
        # corretamente ao dicionário disciplines da classe.
        html_content = '''
        <html>
        <body>
            <table class="listagem">
                <tr>
                    <td><span class="tituloDisciplina">Code 1 - Discipline 1</span></td>
                </tr>
                <tr class="linhaPar"><td></td></tr>
                <tr class="linhaImpar"><td></td></tr>
            </table>
        </body>
        </html>
        '''
        mock_response = MagicMock()
        mock_response.content = html_content.encode('utf-8')
        mock_retrieve_classes_tables.return_value = BeautifulSoup(html_content, "html.parser").find("table")
        mock_get_response_from_disciplines_post_request.return_value = mock_response

        scraper = DisciplineWebScraper(department='1', year='2024', period='1')
        scraper.response = mock_response
        scraper.make_web_scraping_of_disciplines(mock_response)
        
        # Verificar se a disciplina foi adicionada corretamente
        self.assertIn('Code 1', scraper.disciplines)
        self.assertIn('Discipline 1', scraper.disciplines['Code 1'])

if __name__ == '__main__':
    unittest.main()
