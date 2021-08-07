# Visualisation des données sur les accidents de la route

Ce projet consiste en une visualisation grâce à Dash et Plotly de la base de données des accidents de la route ayant causés des dommages corporels en France entre 2005 et 2018. Plusieurs représentations sont proposées, permettant de cerner l'ensemble des problématiques concernées.

## Bien démarrer

Cette section décrit tout ce qui est nécessaire afin que vous puissiez éxécuter le projet par vous même.

### Prérequis

Tout d'abord, clonez ou téléchargez le projet en local et placez vous à la racine du projet.
Une fois fait, certains package sont nécessaire pour faire fonctionner le projet. Pour les installer, il existe deux méthodes.

#### Avec Anaconda :
Pour mettre à jour un evironnement existant (ou envname est le nom de l'environnement à mettre à jour) :
```
conda update --name envname --file environment.yml
```
Pour créer un nouvel environnement dédié :
```
conda env create -f environment.yml

conda activate projet_accidents
```

#### Avec pip : 

```
pip install -r requirements.txt
```

### Installation

Aucune étape supplémentaire n'est nécessaire. Toutes les données sont téléchargées lors du premier démarrage de l'application.

Toutefois si vous souhaitez re-télécharger les données ultérieurement, il suffit d'éxécuter le module data.telechargement
```
python -m data.telechargement
```

## Usage

Afin de démarrer la webapp Dash, il suffit d'éxécuter "index.py".

```
python index.py
```

Ensuite, afin d'accéder à l'interface, il faut se connecter à l'aide d'un navigateur web à l'adresse : http://127.0.0.1:8050/

## License
[MIT](https://choosealicense.com/licenses/mit/)

