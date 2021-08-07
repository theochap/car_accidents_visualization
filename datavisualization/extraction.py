"""
Module qui gère l'extraction des données à partir des csv téléchargés.
"""

import os
import pandas as pd
import pickle

from data.telechargement import fetch_data

def get_csv_list():
    """renvoie la liste des fichiers csv dans ./data/data"""

    file_list = [file[2] for file in os.walk('./data/data')] #liste contenant une liste des fichiers dans ./data/data
    csv_list = [file for file in file_list[0] if file[-4:]=='.csv'] #on ne garde que les csv
    return csv_list

def detect_csv_separator(csv_path):
    """renvoie le séparateur du fichier csv en csv_path"""

    valid_separator_list = [',','\t',';'] #liste des séparateurs valides
    d={}
    with open(csv_path,'r',encoding="ISO-8859-1") as file:
        txt = file.read()
        for separator in valid_separator_list: #pour chaque séparateur
            sep_count = len(txt.split("\n")[0].split(separator)) #on compte le nombre de colonnes qu'on obtient avec le header
            d[separator]=sep_count
    return max(d,key=d.get) #on garde le séparateur qui transforme en le plus de colonnes

def import_all_csv_in_dataframe():
    """importe dans des dataframe tous les csv dans data/data
    renvoie un dictionnaire avec :
    clé : nom du fichier csv
    valeur = dataframe du fichier csv"""

    if os.path.exists('./data/data.p'):
        with open('./data/data.p','rb') as f:
            print("chargement avec pickle")
            d=pickle.load(f) #si on a déjà extrait une fois, on charge le fichier à partir du dump pickle
        return d
    else:
        d={}
        csv_list = get_csv_list() #on récupère la liste des csv dans data/data
        for csv in csv_list:
            print(csv) #on affiche le nom du csv en cours de traitement dans la console
            csv_path = './data/data/'+csv
            sep = detect_csv_separator(csv_path) #on récupère le séparateur du csv
            d[csv]=pd.read_csv(csv_path,encoding="ISO-8859-1",sep=sep,error_bad_lines=False) #on l'importe dans un df. error_bad_lines=False car dans certains fichiers pandas détecte de façon étrange une colonne de trop pourtant inexistante. Cela concerne un nombre très faible de lignes au sein de ces fichiers
        with open("./data/data.p","wb") as f:
            pickle.dump(d,f) #si on a jamais extrait on crée le dump pickle pour un futur chargement plus rapide
        return d