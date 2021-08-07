"""
Module définissant la classe viewer, qui contient toutes les fonctions d'affichage
"""
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from data.transcription import transcription
from datavisualization.traitement import Data

class Viewer:
    """Classe viewer, utilisée pour l'affichage des données
    Il faut faire bien attention à pas mélanger Viewer et Data, ces deux classes doivent rester clairement séparée
    (ex : ne pas faire de traitements stats dans Viewer)"""

    liste_mois=["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Decembre"]
    data=Data() #permet d'alléger la syntaxe lors d'appels de Viewer, et on peut créer plusieurs instanes de viewer sans temps de chargement

    def __init__(self):
        return

    def plot_mois_accident(self,year):
        """Représente sur un histogramme les accidents en fonction du mois"""
        file_dict = self.data.filter_data(year=year,category="caracteristiques")
        df = [file_dict[elt] for elt in file_dict][0] #façon alambiquée de récupérer le seul dataframe dans file_dict
        fig= px.histogram(df,x='mois')
        tick = [x for x in range(1,13)]
        fig.update_layout(xaxis={"ticktext":self.liste_mois,"tickvals":tick,"tickmode":'array'})
        return fig

    def plot_accidents_annees(self,minYear,maxYear):
        """représente le total des accidents par année au cours du temps"""
        #dictionnaire contenant pour chaque année le nombre d'accidents
        total_acc_dict={year:len(list(self.data.filter_data(year=year,category='caracteristiques').values())[0]) for year in range(minYear,maxYear+1)}
        df = pd.DataFrame.from_dict({'total des accidents':total_acc_dict})
        df=df.reset_index()
        df=df.rename(columns={'index':'années'})
        fig = px.bar(df,x="années",y='total des accidents')
        return fig

    def carte_accidents(self,year,filtre):
        """représente la carte des accidents pour l'année year"""
        df = self.data.clean_gps_coord_acc(year,filtre=filtre)

        fig = go.Figure(go.Scattermapbox(
            lat=df.lat, #colonne des latitudes
            lon=df.long, #colonne des longitudes
            mode='markers',
            text=pd.DataFrame({'lum':df.lum_txt,'atm':df.atm_txt}), #données représentées lorsqu'on met sa souris sur un point
            marker=go.scattermapbox.Marker(
                size=14, #taille du marker
                color=df['lum'], #données à partir de laquelle on échelonne les couleurs, ici la luminosité
                colorscale=[[0,"yellow"],[0.25,"orange"],[0.5,"black"],[1,"blue"]], #échelle de couleurs, réglée à la main pour être représentative
            ),
            ))
        fig.update_layout(
            hovermode='closest',
            height=700, #hauteur de la fenêtre
            mapbox=go.layout.Mapbox(
                style="carto-positron", #clé d'api lien sur mapbox liée au compte de gauvain
                bearing=0,
                center=go.layout.mapbox.Center( #point sur lequel est centré la carte
                    lat=46.7,
                    lon=1.7 #centre de la france
                ),
                pitch=0,
                zoom=4.7,
            )
        )
        return fig

    def graphique_2D(self, column_abs, column_ord, year, category_abs, category_ord):
        df = self.data.dataframe_2D(column_abs, column_ord, year, category_abs, category_ord)
        S = [pow(x, 1/3) for x in df["Num_Acc"].values.tolist()]
        df = df.reset_index()
        df = df[[column_abs, column_ord]]
        fig = px.scatter(df, x = column_abs, y = column_ord, size = S)
        fig.update_layout(width = 800, height = 800)
        
        if column_abs in transcription:
            x = transcription[column_abs]
            X = [i for i in range(1, len(x) + 1)]
        else:
            x = None
            X = None
            
        if column_ord in transcription:
            y = transcription[column_ord]
            Y = [i for i in range(1, len(y) + 1)]
        else :
            y = None
            Y = None
        fig.update_layout(
        xaxis = dict(tickmode = 'array', tickvals = X, ticktext = x),
        yaxis = dict(tickmode = 'array', tickvals = Y, ticktext = y))
        return fig


    def plot_camembert(self, selected_column, selected_year, selected_category):
        """renvoie un camembert de la colonne sélectionnée du fichier sélectionné pour l'année sélectionnée"""
        data_filtered = self.data.valeurs_pourcentages(column_name = selected_column, category = selected_category, years = (selected_year)) #on filtre les données nécessaires
    
        if selected_column in transcription:
            labels = transcription[selected_column][0:min(len(data_filtered.keys()), 10)] #si il y a plus de 10 possibilités, on garde les 10 plus courantes
            
        else:    
            labels = list(data_filtered.keys())[0: min(len(data_filtered.keys())-1, 10)] #si on ne trouve pas la transcription des colonnes en bon français
        values = [data_filtered[value][0] for value in data_filtered.keys()][0:len(labels)] #idem pour les valeurs
        
        return {
            "data": [go.Pie(labels= labels, values= values, #on envoie le magnifique pie chart
                            textinfo='label')],
            "layout": go.Layout(title= "Categorie : {}, colonne : {}, année : {}".format(selected_category, selected_column, selected_year),
                                legend={"x": 1, "y": 0.7} )
            }
        
    def timelapse_category_column(self,selected_column,selected_category):
        """renvoie l'évolution au fil du temps d'une colonne selected_column de la caegorie selected_category"""
        data_list = []
        for i in range(2005, 2019): #on boucle sur les années
            selected_data = [self.data.data_dict[file] for file in self.data.data_dict if (selected_category in file) and (str(i) in file)][0] #façon alambiquée de récupérer ce que l'on veut
            
            data_list.append(selected_data[selected_column].value_counts().reset_index()) #on compte les occurences de chaque valeur
            
            data_list[i - 2005] = data_list[i - 2005].reindex(columns=list(data_list[i - 2005].columns) + ['Year']) # on s'arrange avec l'index pour que ça rende bien
            data_list[i - 2005].loc[:, 'Year'] = i
        
        datapx = pd.concat(data_list) #on concatène la liste pour l'affichage
        
        if selected_column in transcription:
            for i in range(0, len(transcription[selected_column])): #on remet l'index en français
                datapx.loc[datapx['index']==i +1, 'index'] = transcription[selected_column][i]

        
        fig = px.line(datapx, x='Year', y = selected_column, color = 'index') # affichage de la figure
        #fig.update_layout(width = 600, height = 600)            
        return fig
    
