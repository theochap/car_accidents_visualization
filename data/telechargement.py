"""
Ce module permet de télécharger la "Base de données accidents corporels de la circulation" à partir de l'API de data.gouv.fr
"""

import requests
import os,os.path

def fetch_data():
    """télécharge la "Base de données accidents corporels de la circulation" à partir de l'API de data.gouv.fr
    
    les fichiers sont placés dans le dossier data/data
    """
    r = requests.get("https://www.data.gouv.fr/api/1/datasets/base-de-donnees-accidents-corporels-de-la-circulation/") #requete sur la page de l'api avec requests
    
    my_path = os.path.abspath(os.path.dirname(__file__)) #tour de magie pour travailler avec le bon path relatif peu import depuis quel working directory le module est éxécuté

    #si le sous-répertoire data n'existe pas, on le crée
    if not os.path.exists(os.path.join(my_path,"../data/data")):
        os.mkdir(os.path.join(my_path,"../data/data"))
    
    for resource in r.json()['resources']: #à l'aide du décodage json de la requête, on boucle sur les ressource présentent dans la page
        url = resource['url']
        title = resource['title']
        if title[-4]!=".": #si l'extension est absente (concerne quelques fichiers)
            title += url[-4:] #alors on la rajoute
        path = os.path.join(my_path, "../data/data/"+title.replace('\"','')) #certains fichiers ont des "", ce qui fait planter os.path, on le retire
        with open(path,'wb') as file: #wb : write,binary
            download_request = requests.get(url)
            file.write(download_request.content) #on écrite le contenu binaire de la requete dans le fichier

def check_data():
    if not os.path.exists('data'): #si les données n'ont pas encore été téléchargées:
        fetch_data()

if __name__ == '__main__':
    fetch_data()
    