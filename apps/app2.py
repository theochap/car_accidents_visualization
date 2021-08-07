"""
Définit une page de l'app qui affiche les accidents en fonction du temps
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps.app import app
from datavisualization.affichage import Viewer

vis = Viewer()

layout = html.Div([
    html.H3('Diagramme des accidents par année en fonction du temps',style={'margin-top':'30px'}),
    dcc.Graph(figure=vis.plot_accidents_annees(2005,2018)) #graph simple des accidents en fonction du temps
])