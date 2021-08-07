import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps.app import app
from datavisualization.traitement import Data
from datavisualization.affichage import Viewer
from data.transcription import categories, columns, transcription

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

vis = Viewer()
data = Data()

layout = html.Div([
    html.H3('Diagramme des accidents par année en fonction du temps'),
    dcc.Link("Retourner à l'index",href='/'),
    html.Br(),

        html.Div([
    
            html.Div([
                html.Label('Catégorie abscisses'),
                dcc.Dropdown(
                    id='categories',
                    options=[{'label': i, 'value': i.lower()} for i in categories],
                    value='caracteristiques'
                )], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '20%'} ),
    
            html.Div([
                html.Label('Nom de la colonne abscisses'),
                dcc.Dropdown(id='column_name1')
             ], style={'width': '30%', 'display': 'inline-block'}) ]),
        html.Br(),

        html.Div([
                
            html.Div([
                html.Label('Nom de la colonne ordonnées'),
            dcc.Dropdown(id='column_name2')
             ], style={'width': '30%', 'display': 'inline-block', 'marginLeft' : '50%'}) ]),
        html.Br(),
                
        html.Div([
        
            html.Div([        
                dcc.Graph(id = 'dispersion')], style={'width': '35%', 'display': 'inline-block', 'marginLeft': '5%'}),
 
         dcc.Slider(
                    id='year-slider',
                    min=2005,
                    max=2018,
                    value=2018,
                    marks={str(year): str(year) for year in range(2005,2019)},
                    step=None)
                     
         ],   style={'width': '50%', 'display': 'inline-block', 'marginLeft': '25%'}
     
        ) ])
    
@app.callback(
        Output('column_name1', 'options'),
        [Input('categories', 'value')]
        )
def update_column_names(selected_category):
    return columns[selected_category]

@app.callback(
    Output('column_name1', 'value'),
    [Input('column_name1', 'options')])
def set_column_name_value(available_options):
    return available_options[0]['value']

@app.callback(
        Output('column_name2', 'options'),
        [Input('categories', 'value')]
        )
def update_column_names(selected_category):
    return columns[selected_category]

@app.callback(
    Output('column_name2', 'value'),
    [Input('column_name2', 'options')])
def set_column_name_value(available_options):
    return available_options[1]['value']

@app.callback(
    Output('dispersion', 'figure'),
    [Input('column_name1', 'value'),
    Input('column_name2', 'value'),
    Input('year-slider', 'value'),
    Input('categories', 'value')]
)
def update_dispersion(column_abs, column_ord, year, category):
    return vis.graphique_2D(column_abs, column_ord, year, category, category)
