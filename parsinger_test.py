import webapp.parsinger as p

import requests

import json

def test_find_address():
    test_addresses = [
    "Je veux savoir où est l'adresse de la tour eiffel ",
    "Salut Grand py bot, peux tu me dire où se trouve le palais de l'Elysée ? Merci ",
    "Où puis-je trouver un starbucks à paris ?",
    "Bonjour. Je cherche la place Bellecour. Peux tu me dire où elle se trouve ? ",
    "Quel est l'emplacement du stade de gerland ?",
    "Hello ! Je cherche l'adresse de la taverne du perroquet bourré",
    "Cette phrase a pour but de ne renvoyer aucune adresse"
    ]
    assert p.find_address(test_addresses[0]) == "tour+eiffel"
    assert p.find_address(test_addresses[1]) == "palais+de+l'Elysée"
    assert p.find_address(test_addresses[2]) == "starbucks+à+paris"
    assert p.find_address(test_addresses[3]) == "place+Bellecour"
    assert p.find_address(test_addresses[4]) == "stade+de+gerland"
    assert p.find_address(test_addresses[5]) == "taverne+du+perroquet+bourré"
    assert p.find_address(test_addresses[6]) == "end process"


def test_map_request(monkeypatch):   

    class Mockrequest():
            def __init__(self, url):
                self.mockresult = {
                    "results": [{
                        "formatted_address": "testaddress",
                        "geometry": {
                            "location": {
                                "lat": 48.85837009999999,
                                "lng": 2.2944813
                            }
                        }
                    }]
                }

            def json(self):
                return self.mockresult


    monkeypatch.setattr(requests, 'get', Mockrequest)
    assert p.map_request("test_query") == ("testaddress", 48.85837009999999, 2.2944813)


def test_wiki_title_request(monkeypatch):

    class Mockrequest():
            def __init__(self, url):
                self.mockresult = {
                    "query": {
                        "geosearch": [{
                            "title": "testtitle"
                            }
                        ]
                    }
                }

            def json(self):
                return self.mockresult

    monkeypatch.setattr(requests, 'get', Mockrequest)
    assert p.wiki_title_request(48, 2) == ("testtitle")


def test_wiki_content_request(monkeypatch):
        
    class Mockrequest():
        def __init__(self, url):
                self.mockresult = {
                    "query": {
                        "pages": [{
                            "extract": "testextract",
                            "fullurl": "testurl"
                            }
                        ]
                    }
                }

        def json(self):
            return self.mockresult

    monkeypatch.setattr(requests, 'get', Mockrequest)
    assert p.wiki_content_request("testtitle") == ("testextract", "testurl")
