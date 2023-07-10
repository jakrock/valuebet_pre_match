from sqlite_utils import Database
import pandas as pd
from pprint import pprint
import numpy as np


#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#recupere les donner de la database 
#donner a recuperer : les cote domicile , exterieur, draw de betkenn et 1xbet et le noms des macth des 2 cote 
#creation de linstance de la base de donnee
db=Database("database.db")

resultat = db.query('''
    SELECT t1.events_1xbet, t1.events_betkeen, t2.domicile AS xbet_domicile,
           t2.exterieur AS xbet_exterieur, t2.draw AS xbet_draw,
           t3.domicile AS betkeen_domicile, t3.exterieur AS betkeen_exterieur,
           t3.draw AS betkeen_draw
    FROM id_1x2general_pre_match AS t1
    INNER JOIN odd_1x2_1xbet AS t2 ON t1.id = t2.id_pre_match
    INNER JOIN odd_1x2_betkeen AS t3 ON t2.id_pre_match = t3.id_pre_match
''')
#on cree un dataframe 
df=pd.DataFrame(list(resultat))
# la fonction tutu  sert a supprimer les colonne 
print(df)
# créer des masques booléens pour les valeurs qui doivent être remplacées par None
mask1 = df['betkeen_domicile'] < df['xbet_domicile']
mask2 = df['betkeen_exterieur'] < df['xbet_exterieur']
mask3 = df['betkeen_draw'] < df['xbet_draw']

# remplacer les valeurs selon les masques
df.loc[mask1, 'betkeen_domicile'] = None
df.loc[~mask1, 'xbet_domicile'] = None

df.loc[mask2, 'betkeen_exterieur'] = None
df.loc[~mask2, 'xbet_exterieur'] = None

df.loc[mask3, 'betkeen_draw'] = None
df.loc[~mask3, 'xbet_draw'] = None

print(df)

# Sélectionner les colonnes numériques uniquement
numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(1000000000000000)
df['inverse_sum'] = df[numeric_cols].apply(lambda x: sum(1/x), axis=1)

df = df[df['inverse_sum'] < 1]


print(df)
data_dict=df.to_dict("records")



# Transformer le DataFrame en dictionnaire de dictionnaires avec l'option 'record'
data_dict = df.to_dict(orient='records')

# Supprimer les entrées correspondantes aux NaN
data_dict_no_nan = [{k: v for k, v in d.items() if pd.notnull(v)} for d in data_dict]

#pprint(data_dict_no_nan)



