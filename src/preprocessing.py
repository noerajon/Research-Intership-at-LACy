### Library

import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

### Import des modules

import txt_to_csv

### Choisir le type d'analyse à mener

# liste_Kaufmann=['AOD_870nm','AOD_675nm','AOD_440nm','440-675_Angstrom_Exponent','440-870_Angstrom_Exponent']
# liste_Toledano=['AOD_870nm','AOD_440nm','440-870_Angstrom_Exponent']
# AOD_data_analysis=['AOD_870nm','AOD_675nm','AOD_440nm']
# liste_verif_angstrom=['AOD_870nm','AOD_675nm','AOD_500nm','AOD_440nm','AOD_380nm','AOD_340nm','440-870_Angstrom_Exponent','380-500_Angstrom_Exponent','440-675_Angstrom_Exponent','500-870_Angstrom_Exponent','340-440_Angstrom_Exponent']
# liste_INTRO_evolution_AOD_AE=['AOD_440nm','AOD_500nm','440-870_Angstrom_Exponent']
# liste_INTRO_climato_AOD_AE=['AOD_440nm','440-870_Angstrom_Exponent']
# liste_INTRO_evolution_AOD_fire_season=['AOD_440nm','AOD_500nm']
# liste_INTRO_distribution_AOD_AE=['AOD_440nm','AOD_500nm','440-870_Angstrom_Exponent']
# liste_Salinas=['AOD_500nm','440-870_Angstrom_Exponent']
# liste_Kaskaoutis=['AOD_500nm','440-870_Angstrom_Exponent']
# liste_Pace=['AOD_500nm','440-870_Angstrom_Exponent']
# liste_Smirnov=['AOD_500nm','440-870_Angstrom_Exponent']
# liste_Jalal=['AOD_500nm','440-870_Angstrom_Exponent']
# liste_Filonchyk=['AOD_440nm','440-870_Angstrom_Exponent']
# liste_INTRO_lecture_SDA=['Fine_Mode_AOD_500nm[tau_f]','Coarse_Mode_AOD_500nm[tau_c]','FineModeFraction_500nm[eta]']
# liste_INTRO_lecture_DP=['Asymmetry_Factor-Total[440nm]']

# interest=liste_INTRO_climato_AOD_AE
    
### Réglage paramètre fichier


# type_src='AERONET/'
# nom_fichier="20200101_20241231_Maido_OPAR/20200101_20241231_Maido_OPAR.lev20"

def preprocessing(interest,type_src,nom_fichier):
    data_dir='../data/BRUT/'
    nom_dir=data_dir+type_src+nom_fichier
    nom_df=txt_to_csv.txt_to_csv(nom_dir, type_src, interest)
    
    ### Lecture fichier et réglage de l'index pour le time series
    
    data_process_0=pd.read_csv(nom_df)
    data_process_0['Temps'] = pd.to_datetime(data_process_0['Temps'])
    data_process_0.set_index('Temps',inplace=True)
    
    
    data_process_0['Date'] = pd.to_datetime(data_process_0['Seconds'], unit='s', origin='unix')
    data_process=data_process_0[data_process_0.index>'2004-01-01']
    
    ### Suppression des données inexistantes
    
    lower_quantile = 0
    upper_quantile = 100
    
    for i in range(len(interest)):
        data_process = data_process[(data_process[interest[i]] >= lower_quantile) & (data_process[interest[i]] <= upper_quantile)]
    
    ### Vérification des types de données présent dans le DataFrame
    
    verif_type=data_process.dtypes
    print(verif_type)
    return(data_process)
