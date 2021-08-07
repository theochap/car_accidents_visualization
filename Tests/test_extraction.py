"""
Module qui teste les fonctions du module extraction
"""

import datavisualization.extraction as ext
import pytest
import os

#unit tests:
def test_get_csv():
    assert ext.get_csv_list() == ['Base de données agrégée des accidents corporels de la circulation de 2005 à 2010 pour France Métropolitaine.csv', 'Base de données agrégée des accidents corporels de la circulation de 2005 à 2010 pour les DOM.csv', 'Base de données agrégée des accidents corporels de la circulation sur 6 années de 2006 à 2011.csv', 'Base de données agrégée des véhicules impliqués de 2006 à 2011.csv', 'caracteristiques-2017.csv', 'caracteristiques-2018.csv', 'caracteristiques_2005.csv', 'caracteristiques_2006.csv', 'caracteristiques_2007.csv', 'caracteristiques_2008.csv', 'caracteristiques_2009.csv', 'caracteristiques_2010.csv', 'caracteristiques_2011.csv', 'caracteristiques_2012.csv', 'caracteristiques_2013.csv', 'caracteristiques_2014.csv', 'caracteristiques_2015.csv', 'caracteristiques_2016.csv', 'lieux-2017.csv', 'lieux-2018.csv', 'lieux_2005.csv', 'lieux_2006.csv', 'lieux_2007.csv', 'lieux_2008.csv', 'lieux_2009.csv', 'lieux_2010.csv', 'lieux_2011.csv', 'lieux_2012.csv', 'lieux_2013.csv', 'lieux_2014.csv', 'lieux_2015.csv', 'lieux_2016.csv', 'usagers-2017.csv', 'usagers-2018.csv', 'usagers_2005.csv', 'usagers_2006.csv', 'usagers_2007.csv', 'usagers_2008.csv', 'usagers_2009.csv', 'usagers_2010.csv', 'usagers_2011.csv', 'usagers_2012.csv', 'usagers_2013.csv', 'usagers_2014.csv', 'usagers_2015.csv', 'usagers_2016.csv', 'vehicules-2017.csv', 'vehicules-2018.csv', 'vehicules_2005.csv', 'vehicules_2006.csv', 'vehicules_2007.csv', 'vehicules_2008.csv', 'vehicules_2009.csv', 'vehicules_2010.csv', 'vehicules_2011.csv', 'vehicules_2012.csv', 'vehicules_2013.csv', 'vehicules_2014.csv', 'vehicules_2015.csv', 'vehicules_2016.csv']

def test_csv_sep():
    """Teste la détection automatique de séparateur.
    On crée des csv de chaque sorte possible de séparateur et on vérifie qu'ils sont bien détectés"""
    sep_list = [',','\t',';']
    sep_out=[]
    for sep in sep_list:
        file = open('csv.csv','w')
        file.write("test"+sep+"test2"+sep+"test3")
        file.close()
        sep_out.append(ext.detect_csv_separator('csv.csv'))
    os.remove('csv.csv')
    assert sep_list==sep_out
        
#integration tests
def test_import_csv():
    """teste la fonction d'import des fichiers csv, à la fois directement et à l'aide du fichier pickle créé"""
    #reset
    os.remove('./data/data.p')
    #sans pickle
    ext.import_all_csv_in_dataframe()
    #avec pickle
    ext.import_all_csv_in_dataframe()

