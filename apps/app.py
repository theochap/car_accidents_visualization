"""
Module qui crée l'application web

Il est indispensable que cette déclaration soit séparée des autres fichiers afin de ne pas avoir de problème lors des callbacks
"""
import dash_bootstrap_components as dbc
import dash
external_stylesheets = [dbc.themes.BOOTSTRAP] #stylesheet générique
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

