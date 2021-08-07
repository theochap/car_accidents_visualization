"""
Module éxécuté dè l'import qui vérifie la présence des données et le télécharge si elles sont absente
"""
import os

from data.telechargement import fetch_data

def check_data():
    if not os.path.exists('data/data'): #si les données n'ont pas encore été téléchargées:
        fetch_data()

check_data()
