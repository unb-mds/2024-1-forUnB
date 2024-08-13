import unittest
from unittest.mock import patch, MagicMock
from main.scraping import get_list_of_departments, DisciplineWebScraper
from main.sessions import create_request_session

class TestScraping(unittest.TestCase):

    @patch('main.scraping.get_response')
    def test_get_list_of_departments_success(self, mock_get_response):
        # Simula uma resposta HTTP com HTML contendo um select de departamentos
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


    

    

    

    

if __name__ == '__main__':
    unittest.main()
