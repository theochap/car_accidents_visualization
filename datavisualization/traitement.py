"""
Module définissant la classe data, qui gère le traitement des données
"""
import pandas as pd

from datavisualization.extraction import import_all_csv_in_dataframe

class Data:
    """Classe Data, qui sert à traiter les données
    Cette classe effectue l'extraction et d'eventuels traitements statistiques en vue de faire une visualisation.
    Il faut faire bien attention à pas mélanger Viewer et Data, ces deux classes doivent rester clairement séparée
    (ex : ne pas faire de traitements stats dans Viewer)"""
    
    data_dict = import_all_csv_in_dataframe() # on définit data_dict comme class atribute comme ça on peut créer plusieurs objets data
    #sans re-importer à chaque fois.
    lum_alias = {
        1:"Plein jour",
        2:"Crépuscule ou aube",
        3:"Nuit sans éclairage public",
        4:"Nuit avec éclairage public non allumé",
        5:"Nuit avec éclairage public allumé",
    } #constante qui peut servir

    atm_alias = {
        1:"Normale",
        2:"Pluie légère",
        3:"Pluie forte",
        4:"Neige - grêle",
        5:"Brouillard - fumée",
        6:"Vent fort - tempête",
        7:"Temps éblouissant",
        8:"Temps couvert",
        9:"Autre"
    }


    def __init__(self):
        return

        
    def filter_data(self,year=None,category=None):
        """filtre les données du dictionnaire selon l'année et la catégorie"""
        out={}
        if year:
            year = str(year)
        if year and category:
            for file in self.data_dict:
                if (category in file) and (year in file):
                    out[file]=self.data_dict[file]
        elif year and not category: #si on veut filtrer une année sans distinction de catégorie
            for file in self.data_dict:
                if year in file:
                    out[file]=self.data_dict[file]
        elif category and not year: #si on veut filtrer une catégorie sans distinction d'année
            for file in self.data_dict:
                
                if category in file:
                    out[file]=self.data_dict[file]
        return out

    def year_in_file(self,year_range:list,file:str):
        """fonction auxiliaire qui renvoie true si il existe au moins un élément de year_range dans file"""
        for year in year_range:
            year=str(year)
            if year in file:
                return True
        return False

    def merge_data(self,category:str,year_range:list):
        """fusionne les fichiers category pour les annees dans year_range
        renvoie un dataframe qui contient les données de category des années year_range"""
        df_list = [self.data_dict[file] for file in self.data_dict if (category in file) and self.year_in_file(year_range,file)]
        return pd.concat(df_list)

    def valeurs_pourcentages(self, column_name, category, years = range(2005,2019) ):
        """Retourne les valeurs, leur nombre d'occurences et le pourcentage de présence (par rapport à l'ensemble des valeurs de la colonne)
        d'une colonne (column_name) d'un objet Data, pour les clés de 
        data_dict qui appartiennent à category pendant les années years
        par défaut, la fonction agit sur les fichiers de la catégorie "category" de 2005 à 2018)"""
        
        valeurs = {}
        
        total = 0
        
        if type(years)==int:
            years = [years]
        
        df = self.merge_data(category, years)
        
        val_distinctes = df[column_name].value_counts().reset_index().to_numpy()
            
        for (valeur, occurrences) in val_distinctes:
            valeurs[valeur] = [occurrences]
            total += occurrences

        for valeur in valeurs.keys():
            valeurs[valeur].append(valeurs[valeur][0]/total *100)
            
        return valeurs

    def clean_gps_coord_acc(self,year,filtre={}):
        """Renvoie un dataframe nettoyé afin d'afficher une carte des accidents pour l'année year"""
        year = str(year)
        df = list(self.filter_data(year=year,category="caracteristiques").values())[0] #on récupère le bon fichier

        df = df[['lat','long','lum','atm']].copy() #on filtre les colonnes que l'on souhaite. Copy car on souhaite le modifier (sinon message d'erreur comme quoi on risquerait de modifier les données originelles)

        #filtrage

        if filtre.get('lum'):
            f = filtre.get('lum')
            df.loc[df['lum']!=f,'lat']=float('nan')
        
        if filtre.get('atm'):
            f = filtre.get('atm')
            df.loc[df['atm']!=f,'lat']=float('nan')

        L=[]
        for val in df['lum']:
            L.append(self.lum_alias[val]) #afin de faire la color scale ET d'afficher les infos, on doit garder les chiffres dans le dataframe, donc on passe par une colonne supplémentaire
        df.insert(0,"lum_txt",L)

        L=[]
        for val in df['atm']:
            if val in range(9):L.append(self.atm_alias[val]) #afin de faire la color scale ET d'afficher les infos, on doit garder les chiffres dans le dataframe, donc on passe par une colonne supplémentaire
            else:L.append(float('nan'))
        df.insert(0,"atm_txt",L)

        df.lat/=100000
        df.long/=100000
        return df

    def dataframe_2D(self,column_abs, column_ord, year, category_abs, category_ord):
        if category_abs == category_ord:
            file = self.filter_data(category = category_abs, year = year)
            data_filtered = [file[elt] for elt in file][0]
            data_filtered = data_filtered[["Num_Acc", column_abs, column_ord]]
            data_filtered = data_filtered.groupby([column_abs, column_ord]).count()
    
        else :
            file1 = self.filter_data(category = category_abs, year = year)
            df1 = [file1[elt] for elt in file1][0]
            file2 = self.filter_data(category = category_ord, year = year)
            df2 = [file2[elt] for elt in file2][0]
            data_filtered = df1.merge(df2, on = 'Num_acc')
            data_filtered = data_filtered[["Num_Acc", column_abs, column_ord]]
            data_filtered = data_filtered.groupby([column_abs, column_ord]).count()

        return(data_filtered)



