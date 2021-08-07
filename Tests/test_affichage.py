"""
Module qui teste les fonctions du module affichage
"""

from datavisualization.affichage import Viewer

vis = Viewer()

def test_plot_mois_acc():
    vis.plot_mois_accident(2015)

def test_acc_ann():
    vis.plot_accidents_annees(2005,2017)

def test_carte():
    vis.carte_accidents(2015,{'lum':3,'atm':4})

