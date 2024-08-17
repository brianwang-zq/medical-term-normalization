#package imports
from nltk import *
from nltk.corpus import *
import umls_api
import requests
from math import sqrt, pow, exp
import numpy as np
import argparse

#presetting variables
version = "current"
identifier = "C1262477"

uri = 'https://uts-ws.nlm.nih.gov'

parser = argparse.ArgumentParser()
parser.add_argument("api_key", help="User API Key", type=str)
parser.add_argument("notepath", help="PATH of patient note", type=str)
parser.add_argument("reference_phrase", help="Reference phrase", type=str)
args = parser.parse_args()
check = (args.notepath)

file = open(check,"r")
fun = file.read()
file.close() 
fun = fun.lower()

reference_phrase = args.reference_phrase
apikey = args.api_key

#extract concepts from reference phrase
def results_list(string, returntype):
    resultlist = []
    cuiresultlist = []
    content_endpoint = "/rest/search/"+version
    full_url = uri+content_endpoint
    page = 0
    
    try:
        while True:
            page += 1
            query = {'string':string,'apiKey':apikey, 'pageNumber':page}
            r = requests.get(full_url,params=query)
            r.raise_for_status()
            r.encoding = 'utf-8'
            outputs  = r.json()
        
            items = (([outputs['result']])[0])['results']
            
            if len(items) == 0:
                if page == 1:
                    print('No results found.'+'\n')
                    break
                else:
                    break
            for result in items:
                resultlist.append(result['name'])
                cuiresultlist.append(result['ui'])#
    except Exception as except_error:
        print(except_error)
    if returntype == "string":
        return resultlist
    elif returntype == "CUI":
        return cuiresultlist


resultlist = results_list(reference_phrase, "CUI")

#UMLS atom extraction
def atom_extraction(cuilist):
    finallist = []

    for cuiidentifier in cuilist:
        content_endpoint = '/rest/content/'+str(version)+'/CUI/'+str(cuiidentifier)
        page = 0
        query = {'apiKey':apikey}
        r = requests.get(uri+content_endpoint, params=query)
        r.encoding = 'utf-8'
                    
        if r.status_code != 200:
            raise Exception('Search term ' + "'" + str(identifier) + "'" + ' not found')
                    
        items  = r.json()
        jsonData = items['result']
        Atoms = jsonData['atoms']
        namelist = []
        try:   
            while True:
                page += 1
                atom_query = {'apiKey':apikey, 'pageNumber':page}
                a = requests.get(Atoms, params=atom_query)
                a.encoding = 'utf-8'
                
                if a.status_code != 200:
                    break
                all_atoms = a.json()
                jsonAtoms = all_atoms['result']
            
                for atom in jsonAtoms:
                    namelist.append(atom['name'])
        except Exception as except_error:
            print(except_error)
        finallist.append(namelist)
    return finallist

extractedlist = (atom_extraction(resultlist))

#flatten atom list into 1 dimensional list
def flatten_list(nested_list):
   
    finalreturn = [item for sublist in nested_list for item in sublist]
    finalreturn = [x.lower() for x in finalreturn]
    return finalreturn

extractedlist = flatten_list(extractedlist)
extractedfinal = list(set(extractedlist))


#searching for atoms in text, return indices
def words_in_string(word_list, a_string, returntype):
    filtered = {}
    filteredind = []
    for word in word_list:
        filteredindex = []
        start = 0
        while start < len(a_string):
            index = a_string.find(word, start)
            if index == -1:
                break
            filteredindex.append([index,index+len(word),len(word)])
            start = index + 1
        filtered[word] = filteredindex
    tbd = []
    for i in filtered:  
        if filtered[i] == []:
            tbd.append(i)
    for i in tbd:
        del filtered[i]
    if returntype == "all": #return all atoms and their locations
        return filtered
    elif returntype == "instances": #return only locations without atoms
        for i in filtered:
            for x in filtered[i]:
                filteredind.append(x)
        return filteredind


indexloc = words_in_string(extractedfinal, fun, "instances")

#normalize text by replacing atom locations
def normalize(ptnote, locations):
    normalizedtext = "normalized " + reference_phrase
    locations_sorted = sorted(locations, key=lambda x: x[0], reverse=True)

    
    for i in locations_sorted:
        startingindex = i[0]
        endingindex = i[1]
        ptnote = (f"{ptnote[:startingindex]}{normalizedtext}{ptnote[endingindex:]}")
    return ptnote


#output
print(normalize(fun, indexloc))



#FUTURE WORK, SIMILARITY CHECK FOR FALSE POSITIVES / TYPOS

#from sklearn.metrics.pairwise import cosine_similarity
##import spacy
#nlp = spacy.load("en_core_web_md")

#def get_phrase_vector(phrase):
#    doc = nlp(phrase)
#    return doc.vector

#def cosine_similarity(v1, v2):
#    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

#def is_similar(reference, phrase):
#    ref_vector = get_phrase_vector(reference)
#    phrase_vector = get_phrase_vector(phrase)
#    return cosine_similarity(ref_vector, phrase_vector)


#def check_similarity(a_string):
#    normalizedsent = sent_tokenize(a_string)
#    filteredsentences = words_in_string_sent(extractedfinal, fun, "instances")
#    for i in filteredsentences:
#        print(is_similar("weight loss",normalizedsent[i-1]))
        


#print(normalize(fun))
#print(check_similarity(fun))




