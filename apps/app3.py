"""
Définit page de l'appliation web qui affiche une carte des accidents, qu'on peut filtrer selon les conditions de lumière et les conditions atmosphériques
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps.app import app
from datavisualization.affichage import Viewer
from data.transcription import transcription

vis = Viewer()
lum_dropdown = [{'label':i,'value':transcription['lum'].index(i)+1} for i in transcription['lum']]
lum_dropdown.insert(0,{'label':'Aucun','value':0})

atm_dropdown = [{'label':i,'value':transcription['atm'].index(i)+1} for i in transcription['atm']]
atm_dropdown.insert(0,{'label':'Aucun','value':0})

layout = html.Div([
    html.H3('Carte des accidents en 2018',style={'margin-top':'30px'}),
    html.Div([
        html.Div([
            html.Label("Année"),
            dcc.Dropdown(
                id='dropdown_carte',
                options=[{'label':year,'value':year} for year in range(2005,2019)],
                value=2018
            )
        ]),
        html.Div([    
            html.Label("Luminosité"),
            dcc.Dropdown(id='lum_name',options=lum_dropdown,value=0),
        ]),
        html.Div([
            html.Label("Conditions atmosphériques"),
            dcc.Dropdown(id='atm_name',options=atm_dropdown,value=0)
        ])
    ]),
    dcc.Graph(id='carte_accidents')
])

@app.callback(
    Output("carte_accidents","figure"),
    [Input("dropdown_carte","value"),Input("lum_name","value"),Input('atm_name','value')])
def update_carte(year,filtre_lum,filtre_atm):
    return vis.carte_accidents(year,{'atm':filtre_atm,'lum':filtre_lum})