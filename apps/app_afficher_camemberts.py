"""
Définit la page web qui affiche des diagrammes circulaires portant sur l'ensemble des données présentes dans la base de données
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from apps.app import app
from datavisualization.affichage import Viewer
from data.transcription import categories, columns, transcription



vis = Viewer()
data = vis.data
#On récupère la liste des catégories


layout = html.Div([
        
    html.Br(),

        html.Div([
    
            html.Div([
                html.Label('Catégorie'),
                dcc.Dropdown( #menu de la catégorie de fichier csv à charger (lieux, caracteristiques etc.)
                    id='categories',
                    options=[{'label': i, 'value': i.lower()} for i in categories],
                    value='caracteristiques'
                )], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '20%'} ),
    
            html.Div([ #nom de la colonne à représenter du fichier chargé
                html.Label('Nom de la colonne'),
            dcc.Dropdown(id='column_name')
             ], style={'width': '30%', 'display': 'inline-block'}) ]),
        html.Br(),
            
    
    html.Div([
        
        html.Div([
                
            dcc.Graph(id='pie-graph'), #camembert

            dcc.Slider( #slider des années couvertes par le dataset
            id='year-slider',
            min=2005,
            max=2018,
            value=2018,
            marks={str(year): str(year) for year in range(2005,2019)},
            step=None)], style={'marginLeft' :'5%', 'display': 'inline-block'}
            ) ], 
            
            style = {'width': '40%', 'display': 'inline-block'} ),
    
    html.Div([dcc.Graph(id = 'timelapse')], style = {'width': '40%', 'display' : 'inline-block', 'marginLeft': '10%'}) #timelapse des données
    
    ])
        
    




@app.callback( #change le nom des colonnes que l'on peut choisir en fonction du fichier sélectionné
        Output('column_name', 'options'),
        [Input('categories', 'value')]
        )
def update_column_names(selected_category):
    return columns[selected_category]

@app.callback( #change les valeurs des colonnes que l'on peut choisir lorsque l'on met à jour le nom avec le callback ci-dessus
    Output('column_name', 'value'),
    [Input('column_name', 'options')])
def set_column_name_value(available_options):
    return available_options[0]['value']

@app.callback( #met à jour le camembert en fonction des 2 dropdown et du slider
    Output('pie-graph', 'figure'),
    [Input('column_name', 'value'),
     Input('year-slider', 'value'),
     Input('categories', 'value')])
     
def update_pie(selected_column, selected_year, selected_category):
    return vis.plot_camembert(selected_column,selected_year,selected_category)
        
@app.callback(
        Output('timelapse', 'figure'), #met à jour le time lapse en fonction des dropdown
        [Input('column_name', 'value'),
         Input('categories', 'value')])
def update_timelapse(selected_column, selected_category):
    return vis.timelapse_category_column(selected_column,selected_category)
