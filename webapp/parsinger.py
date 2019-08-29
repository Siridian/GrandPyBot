#! /usr/bin/env python3
# coding: utf-8


'''This is the main module. The parsinger handles the entire backend part
of the project, by processing user's queries and returning the various
informations to be displayed by the frontend.
'''


import re

from flask import jsonify

import requests


def parse(user_input):
    '''Main function. This will call successive functions on a given string
    to extract an address, find its coordinates on google maps, get the name
    of the related location according to wikipedia, and return its address,
    trivia and link.
    Any error during the process will return a status message that will be
    understood by the frontend, before ending the research.
    '''

    address = find_address(user_input.lower())
    if address == "end process":
        print("=======UNREADABLE======")
        dic = {"status": "unreadable"}
    else:
        trueadr, lat, lon = map_request(address)
        if trueadr == "error":
            print("======NOT FOUND======")
            dic = {"status": "not found"}
        else:
            title = wiki_title_request(lat, lon)
            if title == "Unknown":
                print("======UNKNOWN======")
                dic = {
                    "status": "unknown",
                    "name": address,
                    "address": trueadr,
                    "latitude": lat,
                    "longitude": lon
                }
            else:
                content, url = wiki_content_request(title)
                dic = {
                    "status": "ok",
                    "name": address,
                    "address": trueadr,
                    "latitude": lat,
                    "longitude": lon,
                    "trivia": content,
                    "link": url
                }
    return jsonify(dic)


def find_address(user_sentence):
    '''This function uses regex to extract the name of the location we're
    looking for in a given string.
    '''

    r_list = [
        r'adresse d[ue]s?(?: l[a\'-])?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
        r'trouver? l?[ae\']?s?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
        r'cherche l?[ae\']?s?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
        r'où est(?: située?)? l?[ae\']?s?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
        r'emplacement d[ue]s?(?: l[a\'-])?(?: ?une?)? ?((?:[\w\']+\s?){1,4})'
    ]
    result_list = []

    for r in r_list:
        regex = re.compile(r)
        result = regex.search(user_sentence)
        if result:
            result_list.append(_format_string(result.groups(1)[0]))

    if result_list:
        selected_result = max(result_list, key=len)
        return(selected_result)

    else:
        return("end process")

def _format_string(string):
    '''_format_string is used to clean the strings handled by the parser
    and is not meant to be called manually.
    '''

    string = string.replace('adresse d', '')
    string = string.replace('emplacement d', '')
    string = string.replace(" ", "+")
    if string[len(string)-1] == '+':
        string = string[:-1]
    return string


def map_request(query):
    '''This function requests the google maps api to find the coordinates
    and address corresponding to a given string. Such string is usually
    extracted from user input by the find_address function.
    '''

    r_maps = requests.get(
        'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + query + '&key=AIzaSyCY8uAiaK0_0WecT1Xg405iPOv4aNLmHN0').json()

    try:
        adresse = r_maps['results'][0]["formatted_address"]
        latitude = r_maps['results'][0]["geometry"]["location"]["lat"]
        longitude = r_maps['results'][0]["geometry"]["location"]["lng"]

    except:

        if '+' in query:
            cut_index = query.rfind('+')
            new_query = query[:cut_index]
            return map_request(new_query)

        else:
            return("error", "not", "found")

    print(adresse, latitude, longitude)
    return (adresse, latitude, longitude)


def wiki_title_request(lat, lon):
    '''This function takes two integers (latitude and longitude) and returns
    the name of the closest location known to the wikipedia api.
    '''

    r_wiki_loc = requests.get(
        'http://fr.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={}|{}&gsradius=100&gslimit=1&format=json'.format(lat, lon)).json()

    try:
        title = r_wiki_loc["query"]["geosearch"][0]["title"]
        return(title)
    except:
        return("Unknown")


def wiki_content_request(title):
    '''This function returns trivia information and link to the wikipedia page
    of a given location name. The string containing said name is usually
    obtained using the wiki_title_request function.
    '''

    r_wiki_text = requests.get(
        'http://fr.wikipedia.org/w/api.php?action=query&prop=extracts|info&exsentences=3&inprop=url&explaintext=&titles={}&format=json&formatversion=2'.format(title)).json()

    content = r_wiki_text["query"]["pages"][0]["extract"]
    url = r_wiki_text["query"]["pages"][0]["fullurl"]

    return (content, url)
