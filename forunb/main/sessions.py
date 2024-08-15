""" Sessions module for the ForUnB webscraping. """
import requests

URL = "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", # pylint: disable=C0301
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers",
}


def create_request_session():
    """ Creates a request session with headers. """
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def get_session_cookie(session):
    """ Gets the session cookie. """
    response = session.get(URL)
    return response.cookies


def get_response(session=None):
    """ Gets the response from the URL. """
    if session is None:
        session = create_request_session()
    response = session.get(URL)
    return response
