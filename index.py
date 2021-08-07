"""
index de l'application web

Ce fichier est éxécuté lorsqu'on se trouve à la racine du site.
Il sert également à démarrer la web app dash
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import data.check_data #télécharge les données si elles n'existent pas afin de garantir l'intégrité des imports suivants
from apps.app import app #on importe l'objet app principal de dash qu'on a créé
from apps import app1,app2,app3,app_afficher_camemberts, applum_atm #on ouvre les différentes pages pour récupérer leurs layouts.

#représente le contenu de la page web actuellement consultée
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), #dcc.location permet de récupérer la position relative actuelle, on lui donne l'id url
    html.Div(id='page-content') #représente le contenu de la page, mis à jour grâce au callback définit plus bas
])

#définit la barre de navigation utile au travers de l'application
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Index", href="/")),
        dbc.DropdownMenu(
            right=True,
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Histogramme du nombre d'accidents selon les années",href='/accidents-annees'),
                dbc.DropdownMenuItem("Histogramme du nombre d'accidents selon le mois de l'année",href='/accidents-mois'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Carte interactive des accidents en France",href='/accidents-carte'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Diagramme de dispersion des accidents en fonction de la luminosité et de la météo",href='/accidents-dispersion'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Diagrammes circulaires et temporels sur l'ensemble des données",href="/accidents-stats")
            ],
            
        ),
    ],
    brand="Visualisation des données sur les accidents de la route",
    brand_href="/",
    sticky="top",
    color="primary"
)



#définit le contenu de la page index. Cette variable est renvoyée par le callback lorsqu'on se trouve en "/" (racine)

body_index = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                html.H1("Visualisation des données sur les accidents de la route"),
                html.H4("Une application simple, ludique, et intelligente pour comprendre les enjeux de la sécurité routière",style={'margin-top':'60px'})
            ])
        ],
        style={'margin-top':'70px','text-align':'center'},
        ),
        dbc.Row(
            style={'margin-top':'70px'},
            children=[
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src='https://sd-md-03.hostedseedbox.com:10362/share/downloads/ann-acc.png')
                ]),
                dbc.CardBody([
                    html.H4("Nombre d'accidents par an", className="card-title"),
                    html.P(
                    "Grâce à un histogramme représentant le nombre d'accidents par an, prenez toute la mesure du problème de la sécurité routière.",
                        className="card-text",
                    ),
                    html.A(dbc.Button("Voir l'histogramme", color="primary"),href='/accidents-annees'),
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src='https://sd-md-03.hostedseedbox.com:10362/share/downloads/cam.png')
                ]),
                dbc.CardBody([
                    html.H4("Diagramme général sur la base de données", className="card-title"),
                    html.P(
                    "Grâce à une astucieuse représentation en diagramme circulaire et temporel, visualisez l'ensemble des données contenues dans la base.",
                        className="card-text",
                    ),
                    html.A(dbc.Button("Voir le diagramme", color="primary"),href='/accidents-stats'),
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src='https://sd-md-03.hostedseedbox.com:10362/share/downloads/carte.png')
                ]),
                dbc.CardBody([
                    html.H4("Carte de France des accidents", className="card-title"),
                    html.P(
                        "Visualisez de manière interactive les accidents, avec la possibilité de trier par année, par météo et par luminosité.",
                        className="card-text",
                    ),
                    html.A(dbc.Button("Voir la carte", color="primary"),href='/accidents-carte'),
                ])
            ]),

        ]),
        dbc.Row(
            style={'margin-top':'70px'},
            children=[
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src='https://sd-md-03.hostedseedbox.com:10362/share/downloads/disp.png')
                ]),
                dbc.CardBody([
                    html.H4("Diagramme de dispersion", className="card-title"),
                    html.P(
                    "Grâce à un diagramme de dispersion, visualisez les relations entre plusieurs séries de données.",
                        className="card-text",
                    ),
                    html.A(dbc.Button("Voir le diagramme", color="primary"),href='/accidents-dispersion'),
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src='https://sd-md-03.hostedseedbox.com:10362/share/downloads/ann-acc.png')
                ]),
                dbc.CardBody([
                    html.H4("Nombre d'accidents selon le mois", className="card-title"),
                    html.P(
                    "Visualisez le nombre d'accidents chaque mois selon les années grâce à un histogramme.",
                        className="card-text",
                    ),
                    html.A(dbc.Button("Voir l'histogramme", color="primary"),href='/accidents-mois'),
                ])
            ]),

        ]),
        

    ])
layout_404 = html.Div([
    html.H1("Erreur 404 : page non trouvée"),
    dcc.Link("Retourner à l'index",href="/")
])

#callback qui modifie le contenu de la page actuelle en fonction de l'url que l'on visite
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/accidents-mois':
        return [navbar,app1.layout]
    elif pathname == '/accidents-annees':
        return [navbar,app2.layout]
    elif pathname == "/accidents-carte":
        return [navbar,app3.layout]
    elif pathname == "/accidents-dispersion":
        return [navbar,applum_atm.layout]
    elif pathname == "/accidents-stats":
        return [navbar,app_afficher_camemberts.layout]
    elif pathname == '/':
        return [navbar,body_index]
    else:
        return [navbar,layout_404]

if __name__ == '__main__':
    app.run_server(debug=True)