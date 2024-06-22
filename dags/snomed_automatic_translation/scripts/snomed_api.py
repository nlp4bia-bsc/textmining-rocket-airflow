from urllib.request import urlopen, Request
from urllib.parse import quote
import json

baseUrl = 'https://browser.ihtsdotools.org/snowstorm/snomed-ct'

def urlopen_with_header(url, language):
    req = Request(url)
    req.add_header('User-Agent', 'PostmanRuntime/7.29.0')
    req.add_header('Accept-Language', language)
    return urlopen(req)

def getConceptById(id, language, edition, version):
    url = baseUrl + '/browser/' + edition + '/' + version + '/concepts?size=1&conceptIds=' + id
    response = urlopen_with_header(url, language).read()
    data = json.loads(response.decode('utf-8'))

    if data['total'] == 0:
        print(f"ID: {id}, language: {language}, Concept: None, Complete result: There's not results, URL: {url}")
        return None
    
    result = data['items'][0]['pt']['term'] if data['items'][0]['pt']['lang'] == language else None
    print(f"ID: {id}, language: {language}, Concept: {result}, Complete result: {data['items'][0]['pt']}, URL: {url}")
    
    return result