import pandas as pd 
# crie um dataframe usando o arquivo movies.csv 
df = pd.read_csv('movies.csv') 
# classificação de dataframe: em relação à coluna weighted_rating em ordem crescente 
df = df.sort_values('weighted_rating' , ascending = False) 
# dataframe final 
output = df[['original_title' , 'runtime', 'release_date' , 'weighted_rating' ]].head(20)