"""
Module qui teste les fonctions du module traitement
"""

from datavisualization.traitement import Data

data = Data()

def test_filter_data():
    """teste la fonction filter_data en vérifiant qu'on obtient bien la totalité des fichiers attendus"""
    year_list = [x for x in range(2005,2019)]
    category_list = ['caracteristiques','lieux','usagers','vehicules']

    for year in year_list:
        a=data.filter_data(year=year)
        assert (len(a)==4 or len(a)==6)
        for category in category_list:
            b=data.filter_data(year=year,category=category)
            assert len(b)==1
    for category in category_list:
        c=data.filter_data(category=category)
        assert len(c)==14

def test_year_in_file():
    assert data.year_in_file([x for x in range(2005,2019)],'caracteristiques-2018.csv')

def test_merge_data():
    """teste la fonction merge_data en vérifiant la longueur du fichier après concaténation"""
    assert len(data.merge_data('caracteristiques',[2006,2007]))==len(data.data_dict['caracteristiques_2006.csv'])+len(data.data_dict['caracteristiques_2007.csv'])

def test_val_pourc():
    data.valeurs_pourcentages('lum','caracteristiques')

def test_gps():
    data.clean_gps_coord_acc(2015,{'lum':3})
    data.clean_gps_coord_acc(2015,{'atm':3})
    data.clean_gps_coord_acc(2015,{'lum':3,'atm':3})

