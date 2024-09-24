# building municipality ranking model


# Selecting columns to be used in algorithm. Municipality code and city name for reference
# Average sales amount, housing stress level, and tourism "score" will be the three attributes used to calculate the ranking

df_algorithm = df[["municipality_code", "city_name", "avg_sales_amount", "intensite_tension_immo", "sum_tourist_sites"]]



df_algorithm.set_index("municipality_code", inplace=True)     # setting municipality code as index



# Replacing all null tourism "scores" with 0, since there are no recorded tourist sites for these municipalities in the data

df_algorithm["sum_tourist_sites"].fillna(value=0, inplace=True)



# The KPIs or features of the ranking algorithm are:
# - Average Sale Price (i.e. municipalities with higher profit possibilities - important, since Prello takes a percentage of the sale fee)
# - Tourism "score" (i.e. municipalities with significant tourism sites - higher value areas since they will be in demand from tourists to rent)
# - Housing stress level (i.e. areas where rent is less affordable, greater risks of mortgage default etc. - unattractive for investors)

# These KPIs will be scaled to a relative score, and then given a suitable weight, and then combined to give an overall ranking for each municipality



import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import QuantileTransformer     # importing scalers to be used for calculating the ranking



#establish weights for the three features in the algorithm - can be altered depending on which KPIs are more important
# 3,2,3 gives a good picture of top locations for typical high-end second homes, particularly coastal and ski resort locations

price_weight = 3
tourism_weight = 2
stress_weight = 3



#set scaler ranges - to give each feature a "score", relative to their value, in order to be combined in the algorithm

scaler_price = MinMaxScaler(feature_range=(0.5,9.999)) # house sale prices range from $50,000 to over $32 million
scaler_stress = MinMaxScaler(feature_range=(1.2903,9.999)) # housing stress indices range from 4 to 31, 1.2903 - 10 is an attempt to reflect this
scaler_tourism = QuantileTransformer(output_distribution='normal') # since a few outliers with lots of tourist sites, use quantile distribution scaler



# turning features into arrays, with column shape, to be scaled

price = df_algorithm["avg_sales_amount"].values.reshape(-1,1)
tourism = df_algorithm["sum_tourist_sites"].values.reshape(-1,1)
stress = df_algorithm["intensite_tension_immo"].values.reshape(-1,1)



# scaling arrays

price_scaled = scaler_price.fit_transform(price)
stress_scaled = scaler_stress.fit_transform(stress)
tourism_scaled = scaler_tourism.fit_transform(tourism)



# flattening data to form dataframe

price_scaled = price_scaled.flatten()
tourism_scaled = tourism_scaled.flatten()
stress_scaled = stress_scaled.flatten()



# putting scaled data back into dataframe to calculate ranking

df_calculation = pd.DataFrame({'price': price_scaled, 'tourism': tourism_scaled, 'stress': stress_scaled}, index=df_algorithm.index)



# weighting features and combining to calculate score

df_calculation["calculation"] = (df_calculation["price"]*price_weight) + (df_calculation["tourism"]*tourism_weight) - (df_calculation["stress"]*stress_weight)



df_calculation.sort_values(by="calculation", ascending=False, inplace=True)     # ordering by calculated score descending


df_calculation["ranking"] = df_calculation.reset_index().index + 1     # temporarily resetting index to add ranking column based on calculated score


df_ranking = pd.DataFrame(df_calculation, columns=["ranking", "calculation"])     # separating out ranking + municipality code to be joined back to original table


pd.set_option('display.float_format', '{:.2f}'.format)     # disables scientific notation, puts values into floats


df_prello_ranking = pd.merge(df_algorithm, df_ranking, on=["municipality_code"]).sort_values(by=["ranking"])     # merging ranking with original dataframe


df_prello_ranking.head(15)     # displaying top 15 municipalities


df_prello_ranking.to_csv("prello_ranking_calculation.csv")     # exporting results to be visualized 
