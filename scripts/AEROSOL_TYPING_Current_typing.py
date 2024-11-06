# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:04:31 2024

@author: rajonn
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path
from shapely.geometry import Point, Polygon
from netCDF4 import Dataset
import os
import seaborn as sns
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from preprocessing import preprocessing

array_DZ = np.array([[0, 0], [0, 3], [0.02, 3], [0.02, 0]])
array_CM = np.array([[0.025, 0], [0.025, 0.75],[0.04, 0.75], [0.045, 0.5],[0.06, 0.25],[0.08, 0]])
array_CMwithPollution = np.array([[0.05, 0.7], [0.06, 1], [0.09, 1], [0.09, 0.5],[0.12, 0.2],[0.085, 0.1],[0.06,0.35]])
array_BB = np.array([[0.075, 1.25], [0.1, 2], [0.6, 2], [0.6, 1.2], [0.1, 1.2]])
array_CA = np.array([[0.02, 0.8], [0.02, 1.8], [0.04, 1.8], [0.04, 0.8]])

# Créer le polygone en utilisant les sommets
polygon_DZ = Polygon(array_DZ)
polygon_CM = Polygon(array_CM)
polygon_CMwithPollution = Polygon(array_CMwithPollution)
polygon_BB = Polygon(array_BB)
polygon_CA = Polygon(array_CA)

def find_timestamps(df, points):
    timestamps = []
    for point in points:
        mask = (df['AOD_440nm'] == point[0]) & (df['440-870_Angstrom_Exponent'] == point[1])
        timestamp = df.loc[mask, 'Date']
        if not timestamp.empty:
            timestamps.append(timestamp.values[0])
        else:
            timestamps.append(None)  # Si aucun timestamp n'est trouvé
    return pd.DataFrame(timestamps)

# Spécifie le chemin du dossier
folder_path = '../data/BRUT/AERONET/CURRENT'

# Récupérer la liste des fichiers
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

if len(files) > 1 : 
    print('Un seul fichier doit être présent dans le dossier CURRENT')
elif len(files) == 0 :
    print('Veuillez placer un fichier dans le dossier CURRENT')
elif len(files) == 1 :
    ### Récupération du DataFrame 
    
    liste_interest=['AOD_440nm','440-870_Angstrom_Exponent']
    
    type_src='AERONET/'
    nom_fichier=f"CURRENT/{files[0]}"
    interest=liste_interest
    
    from preprocessing import preprocessing
    
    data_process = preprocessing(interest,type_src,nom_fichier)
    
    # Ouvrir le fichier NetCDF
    with Dataset('../data/PROCESS/AERONET/contour_mathematique.nc', 'r') as nc_file:
        # Lire une variable, par exemple x_PM
        x_PM = nc_file.variables['x_PM'][:]
        x_CMP = nc_file.variables['x_MP'][:]
        x_BB = nc_file.variables['x_BB'][:]
        x_CA = nc_file.variables['x_CA'][:]
        y_PM = nc_file.variables['y_PM'][:]
        y_CMP = nc_file.variables['y_MP'][:]
        y_BB = nc_file.variables['y_BB'][:]
        y_CA = nc_file.variables['y_CA'][:]
    
        
    # Définition du contour pour chaque type
    contour_points_CM = np.column_stack((x_PM, y_PM))
    contour_points_CMP = np.column_stack((x_CMP, y_CMP))
    contour_points_BB = np.column_stack((x_BB, y_BB))
    contour_points_CA = np.column_stack((x_CA, y_CA))
    
    contour_path_CM = Path(contour_points_CM)
    contour_path_CMP = Path(contour_points_CMP)
    contour_path_BB = Path(contour_points_BB)
    contour_path_CA = Path(contour_points_CA)
    
    data_process_for_points = data_process.copy()
    data_process_for_points = data_process_for_points.drop(['Date','Seconds'],axis = 1)
    points = data_process_for_points.values

    
    # Définition du vecteur de sélection de type booléen pour chaque type
    inside_CM = contour_path_CM.contains_points(points)
    inside_CMP = contour_path_CMP.contains_points(points)
    inside_BB = contour_path_BB.contains_points(points)
    inside_CA = contour_path_CA.contains_points(points)

    # Sélection des points pour chaque type
    points_inside_CM = points[inside_CM]
    points_inside_CMP = points[inside_CMP]
    points_inside_BB = points[inside_BB]
    points_inside_CA = points[inside_CA]

    # Application de la fonction pour récupérer les timestamps 
    timestamps_CA = find_timestamps(data_process, points_inside_CA)
    timestamps_CM = find_timestamps(data_process, points_inside_CM)
    timestamps_CMP = find_timestamps(data_process, points_inside_CMP)
    timestamps_BB = find_timestamps(data_process, points_inside_BB)

    # Mise au format datetime
    timestamps_CM = pd.to_datetime(timestamps_CM[0])
    timestamps_CMP = pd.to_datetime(timestamps_CMP[0])
    timestamps_BB = pd.to_datetime(timestamps_BB[0])
    timestamps_CA = pd.to_datetime(timestamps_CA[0])

    # Création des DataFrame par type
    CM_vf_2 = data_process.loc[data_process['Date'].isin(timestamps_CM)]
    CMP_vf_2 = data_process.loc[data_process['Date'].isin(timestamps_CMP)]
    BB_vf_2 = data_process.loc[data_process['Date'].isin(timestamps_BB)]
    CA_vf_2 = data_process.loc[data_process['Date'].isin(timestamps_CA)]

    # Récupérationion du DataFrame de type MIX
    df_combine_v2 = pd.concat([CM_vf_2, CMP_vf_2, BB_vf_2,CA_vf_2], ignore_index=True)
    df_diff_2 = data_process.merge(df_combine_v2, how='outer', indicator=True)
    MIX_vf_2 = df_diff_2[df_diff_2['_merge'] == 'left_only'].drop(columns=['_merge'])
    MIX_vf_2.index = MIX_vf_2['Date']
    
    # Construction de la série de points sous forme de liste de tuples
    points_list = list(zip(data_process['AOD_440nm'], data_process['440-870_Angstrom_Exponent']))

    # Conversion en array NumPy
    points_array = np.array(points_list)

    # Identifier les points à l'intérieur du polygone
    points_inside_DZ = np.array([point for point in points_array if polygon_DZ.contains(Point(point))])
    points_inside_CM = np.array([point for point in points_array if polygon_CM.contains(Point(point))])
    points_inside_CMwithPollution = np.array([point for point in points_array if polygon_CMwithPollution.contains(Point(point))])
    points_inside_BB = np.array([point for point in points_array if polygon_BB.contains(Point(point))])
    points_inside_CA = np.array([point for point in points_array if polygon_CA.contains(Point(point))])

    # Nombre de points identifier par le filtre pour chaque type par rapport aux données totales
    recap_donnee=[[len(points_inside_DZ),len(points_array)],[len(points_inside_CM),len(points_array)],[len(points_inside_CMwithPollution),len(points_array)],[len(points_inside_BB),len(points_array)],[len(points_inside_CA),len(points_array)]]

    # Application de la fonction pour récupérer les timestamps 
    timestamps_DZ = find_timestamps(data_process, points_inside_DZ)
    timestamps_CM = find_timestamps(data_process, points_inside_CM)
    timestamps_CMwithPollution = find_timestamps(data_process, points_inside_CMwithPollution)
    timestamps_BB = find_timestamps(data_process, points_inside_BB)
    timestamps_CA = find_timestamps(data_process, points_inside_CA)

    # Mise au format datetime
    timestamps_CM = pd.to_datetime(timestamps_CM[0])
    timestamps_CMwithPollution = pd.to_datetime(timestamps_CMwithPollution[0])
    timestamps_BB = pd.to_datetime(timestamps_BB[0])
    timestamps_CA = pd.to_datetime(timestamps_CA[0])

    # Création des DataFrame par type
    CM_vf = data_process.loc[data_process['Date'].isin(timestamps_CM)]
    CMwithPollution_vf = data_process.loc[data_process['Date'].isin(timestamps_CMwithPollution)]
    BB_vf = data_process.loc[data_process['Date'].isin(timestamps_BB)]
    CA_vf = data_process.loc[data_process['Date'].isin(timestamps_CA)]

    # Récupérationion du DataFrame de type MIX
    df_combine = pd.concat([CM_vf, CMwithPollution_vf, BB_vf,CA_vf], ignore_index=True)
    df_diff = data_process.merge(df_combine, how='outer', indicator=True)
    MIX_vf = df_diff[df_diff['_merge'] == 'left_only'].drop(columns=['_merge'])
    MIX_vf.index = MIX_vf['Date']
    
    colonne_meth = ['emp','mat']
    colonne_type = ['PM','MP','BB','CA','MIX']
    colonnes_meth = colonne_meth + colonne_meth + colonne_meth + colonne_meth +colonne_meth
    colonne_type = ['PM','MP','BB','CA','MIX']
    colonnes_type = []
    for i in range(5):
        for j in range(2):
            colonnes_type.append(colonne_type[i])
            
    df_aerosol_typing = {
        'Type': colonnes_type,
        'Method': colonnes_meth,
        'Pourcentage': [0.0 for i in range(2*len(colonne_type))]

    }
    df_aerosol_typing = pd.DataFrame(df_aerosol_typing)
    
    # Nombre totale de données par mois
    N_tot = data_process.count().iloc[0]
    
    # Type Pure Marine (PM)
    N_type_pourcent = 100*CM_vf.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[0,2]=round(N_type_pourcent,1)
    
    # Type Marine + Pollution (MP)
    N_type_pourcent = 100*CMwithPollution_vf.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[2,2]=round(N_type_pourcent,1)
    
    # Type Biomass Burning (BB)
    N_type_pourcent = 100*BB_vf.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[4,2]=round(N_type_pourcent,1)
    
    # Type Clean Atmosphere (CA)
    N_type_pourcent = 100*CA_vf.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[6,2]=round(N_type_pourcent,1)
    
    # Type MIX (MIX)
    N_type_pourcent = 100*MIX_vf.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[8,2]=round(N_type_pourcent,1)
        
    
    # Nombre totale de données par mois
    N_tot = data_process.count().iloc[0]
    
    # Type Pure Marine (PM)
    N_type_pourcent = 100*CM_vf_2.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[1,2]=round(N_type_pourcent,1)
    
    # Type Marine + Pollution (MP)
    N_type_pourcent = 100*CMP_vf_2.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[3,2]=round(N_type_pourcent,1)
    
    # Type Biomass Burning (BB)
    N_type_pourcent = 100*BB_vf_2.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[5,2]=round(N_type_pourcent,1)
    
    # Type Clean Atmosphere (CA)
    N_type_pourcent = 100*CA_vf_2.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[7,2]=round(N_type_pourcent,1)
    
    # Type MIX (MIX)
    N_type_pourcent = 100*MIX_vf_2.count().iloc[0]/N_tot
    df_aerosol_typing.iloc[9,2]=round(N_type_pourcent,1)
    
    custom_palette = sns.color_palette(['royalblue', 'brown','red','green','grey'])    
    
    plt.figure(figsize=(13, 6))
    sns.barplot(x='Method', y='Pourcentage', hue='Type', data=df_aerosol_typing, palette=custom_palette)
    plt.xlabel('Method',fontsize=14)
    plt.ylabel('Percentage',fontsize=14)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    
    plt.legend(title='Type',fontsize=13,loc='upper left')
    plt.title(f'Period : from {str(data_process.index[0])[:10]} to {str(data_process.index[-1])[:10]}', fontsize = 14)
    plt.show()