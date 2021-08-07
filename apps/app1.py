"""
Définit la page de l'application qui affiche les accidents en fonction du mois pour toutes les années du dataset
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps.app import app
from datavisualization.affichage import Viewer

vis = Viewer()

layout = html.Div([
    html.H3('Histogramme des accidents en fonction du mois',style={'margin-top':'30px'}),
    dcc.Graph(id='graph'),
    html.Div(style={'margin-left':'30px','margin-right':'30px'},children=dcc.Slider(id='year-slider',min=2005,max=2018,value=2005,marks={year:str(year) for year in range(2005,2019)})) #slider de sélection de l'année, entre 2005 et 2018 inclus
])


@app.callback (
    Output('graph','figure'),
    [Input('year-slider','value')] #on met à jour le graph sur modification du slider
)
def update_figure(selected_year):
    return vis.plot_mois_accident(selected_year)
