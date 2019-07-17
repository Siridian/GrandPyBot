import re

from flask import jsonify

import requests

print("coucou")

def stpmarche(user_input):
    address = find_address(user_input)
    if address == "end process":
        dic = {"status": "unreadable"}
        #print("Je n'ai pas compris mon poussin, peux-tu me dire où tu veux aller ?")
    else:
        trueadr, lat, lon = map_request(address)
        if lat == "not":
            dic = {"status": "not found"}
            #print("Je suis désolé mon poussin, je ne connais pas cet endroit...")
        else:
            content, url = wiki_query(lat, lon)
            dic = {
            "status": "ok",
            "address": trueadr,
            "latitude": lat,
            "longitude": lon,
            "trivia": content,
            "link": url
            }
    return jsonify(dic)


def find_address(user_sentence):
    r_list = [
    r'adresse d[ue]s?(?: l[a\'-])?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
    r'trouver? l?[ae\']?s?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
    r'cherche l?[ae\']?s?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
    r'où est l?[ae\']?s?(?: ?une?)? ?((?:[\w\'-]+\s?){1,4})',
    r'emplacement d[ue]s?(?: l[a\'-])?(?: ?une?)? ?((?:[\w\']+\s?){1,4})'
    ]

    result_list = []

    for r in r_list:
        regex = re.compile(r)
        result = regex.search(user_sentence)
        if result:
            result_list.append(format_string(result.groups(1)[0]))

    if result_list:    
        selected_result = max(result_list, key=len)
        return(selected_result)

    else:
        return("end process")

def map_request(query):
    
    print("trying with : " + query)

    r_maps = requests.get(
            'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + query + '&key=AIzaSyCY8uAiaK0_0WecT1Xg405iPOv4aNLmHN0').json()
    
    try:
        adresse = r_maps['results'][0]["formatted_address"]
        latitude = r_maps['results'][0]["geometry"]["location"]["lat"]
        longitude = r_maps['results'][0]["geometry"]["location"]["lng"]

    
    except IndexError:

        if '+' in query:
            cut_index = query.rfind('+')
            new_query = query[:cut_index]
            return map_request(new_query)

        else:
            return("not", "found")

    return(adresse, latitude, longitude)


def wiki_query(lat, lon):

    r_wiki_loc = requests.get(
                'http://fr.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={}|{}&gsradius=100&gslimit=1&format=json'.format(lat, lon)).json()

    title = r_wiki_loc["query"]["geosearch"][0]["title"]

    print(title)

    r_wiki_text = requests.get(
                    'http://fr.wikipedia.org/w/api.php?action=query&prop=extracts|info&exsentences=3&inprop=url&explaintext=&titles={}&format=json&formatversion=2'.format(title)).json()

    
    content = r_wiki_text["query"]["pages"][0]["extract"]
    url = r_wiki_text["query"]["pages"][0]["fullurl"]
    print(clean_wiki(content))

    return(content, url)
    

def format_string(string):
    string = string.replace('adresse d','')
    string = string.replace('emplacement d','')
    string = string.replace(" ", "+")
    if string[len(string)-1] == '+':
        string = string[:-1]
    return string


def clean_wiki(string):
    cleaned_string = string.split("\n\n")[0]
    cleaned_string = re.sub(r'<.*?>', "", cleaned_string)
    cleaned_string = re.sub(r'{.*?}}', "", cleaned_string)
    return cleaned_string
