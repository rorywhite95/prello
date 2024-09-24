# Implementing Linear Regression to predict null values for Housing Stress KPI

import pandas as pd

df = pd.read_csv("/content/prello_x_total_data.csv")      # uploading transformed data from BigQuery



# Selecting relevant columns for Linear Regression. Municipality code is for reference. Target is "intensite_tension_immo" or housing stress level.
# Four features are average sale price, max price, min price and number of sales recorded.

df_ML = df[["municipality_code", "avg_sales_amount", "max_sales_amount", "min_sales_amount", "nb_sales_recorded", "intensite_tension_immo"]]

df_ML.set_index("municipality_code", inplace=True)     # setting municipality code as the index



# separating dataframe into a) the non null target values, to be used to train and test the model...
# and b) the null values, to be predicted later with the model

df_ML_non_null = df_ML[df_ML["intensite_tension_immo"].notnull()]

df_ML_null = df_ML[df_ML["intensite_tension_immo"].isnull()]



X = df_ML_non_null.iloc[:,:4]     # selecting the four feature columns as X

y = df_ML_non_null["intensite_tension_immo"]     # selecting the target column as y



from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)     # setting train, test, split data



from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)     # scaling data
X_test_scaled = scaler.transform(X_test)



from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train_scaled, y_train)     # fitting Linear Regression model



# testing model (low-scoring, but will only apply to 539 municipalities, none of which are likely to appear near the top of the ranking)

model.score(X_test_scaled, y_test)



X_null = df_ML_null.iloc[:,:4]     # separating the features columns for the dataset with the null values to be predicted


X_null_scaled = scaler.fit_transform(X_null)     # scaling data


predicted_nulls = model.predict(X_null_scaled)     # predicting nulls


df_ML_null["intensite_tension_immo"] = predicted_nulls     # adding predicted values to the separated dataframe


df.loc[df["intensite_tension_immo"].isnull(), "intensite_tension_immo"] = predicted_nulls  # updating original dataframe nulls with new predicted values
