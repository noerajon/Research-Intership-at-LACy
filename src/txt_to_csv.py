### Library

from pathlib import Path
import pandas as pd

### Définition fonction pour traitement de fichier

def txt_to_csv(nom_fichier,type_src,interest):
    tableau=[]
    file=open(nom_fichier,"r",encoding="utf8")
    i=0
    for line in file :
        if i<=5:
            ''
        elif i==6 : 
            nom_colonne=line.split(",")
        else :
            tableau.append(line.split(","))
        i+=1
    file.close()
    
    ### Création Data Frame
    
    columns_to_remove=nom_colonne[:]
    columns_to_keep=['Date(dd:mm:yyyy)','Time(hh:mm:ss)',*interest]
    for elem in columns_to_keep:
        while elem in columns_to_remove:
            columns_to_remove.remove(elem)
            
    data=pd.DataFrame(tableau,columns=nom_colonne)
    data=data.drop(columns_to_remove,axis=1)
    
    ### Paramétrisation des formats
    
    data2=pd.DataFrame(pd.to_numeric(data[interest[0]]))
    for i in range(1,len(interest)):
        data_i=pd.DataFrame(pd.to_numeric(data[interest[i]]))
        data2=data2.merge(data_i,left_index=True,right_index=True)
    data['Date(dd:mm:yyyy)']=data['Date(dd:mm:yyyy)']+' '+data['Time(hh:mm:ss)']
    data=data.drop(columns=['Time(hh:mm:ss)',*interest],axis=1)
    data=data.rename(columns={'Date(dd:mm:yyyy)':'Temps'})
    data['Temps']=pd.to_datetime(data['Temps'],format='%d:%m:%Y %H:%M:%S')
    data_process=data.merge(data2,left_index=True,right_index=True)
    data_process['Seconds'] = data_process['Temps'].apply(lambda x: pd.Timestamp(x).timestamp())
    data_process=data_process.set_index('Temps')
    nom_fichier=Path(nom_fichier)
    nom_fichier_only=nom_fichier.stem
    nom_fichier_csv='../data/PROCESS/'+type_src+nom_fichier_only+'.csv'
    data_process.to_csv(nom_fichier_csv,index='True')
    return(nom_fichier_csv)
