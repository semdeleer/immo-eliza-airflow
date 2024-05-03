
import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures, Normalizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import BaggingRegressor
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score, r2_score
import pickle
import os

def make_model():
    url = os.path.join(".","dags", "immoweb", "data", "clean", "clean_house2.csv")
    house = pd.read_csv(url, sep=",")

    x = house.drop(["price", "locality_name", "latitude", "longitude", "furnished", "property_id", "number_of_rooms"], axis=1)
    y = house[["price"]]

    nfeatuers = ["living_area", "terrace_area", "garden_area", "surface_of_good"]
    cfeatures = ["postal_code", "property_type", "property_subtype", "type_of_sale", "kitchen_type", "fully_equipped_kitchen", "open_fire", "terrace", "garden", "number_of_facades", "swimming_pool", "state_of_building", "main_city", "province"]

    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=41)

    num_pipeline = make_pipeline(SimpleImputer(missing_values=np.nan), StandardScaler(), PolynomialFeatures(degree=3))
    cat_pipeline = make_pipeline(SimpleImputer(strategy="most_frequent", missing_values=np.nan),OneHotEncoder(handle_unknown='ignore'))

    preprocessor = make_column_transformer((num_pipeline, nfeatuers), (cat_pipeline, cfeatures))
    b = BaggingRegressor(n_estimators=150) 

    model = make_pipeline(preprocessor, b)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    directory = './dags/immoweb/model'

    # Ensure the directory exists, create it if necessary
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the full path to the pickle file
    file_path = os.path.join(directory, 'model_pickle_b2')

    # Write the pickled model to the file
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)


#print('Mean squared error : ' + str(mean_squared_error(y_test,y_pred)))
#print('Mean absolute error : ' + str(mean_absolute_error(y_test,y_pred)))
#print('Explained vaiance score : ' + str(explained_variance_score(y_test,y_pred)))
#print('r2 score : ' + str(r2_score(y_test,y_pred)))

#x_train.head()

if __name__ == "__main__":
    #house_data = {'postal_code' :[1060],'property_type' :["HOUSE"],'property_subtype' :["HOUSE"],'type_of_sale':["BUY_REGULAR"],'living_area':["220.0"],'kitchen_type':["SEMI_EQUIPPED"],'fully_equipped_kitchen':[1.0],'open_fire':[0],'terrace':[0],'terrace_area':[50.0],'garden':[1.0],'garden_area':[100.0],'surface_of_good':[218.0],'number_of_facades':[4],'swimming_pool':[1.0],'state_of_building':['GOOD'],'main_city':['wevelgem'], "province":["west-vlaanderen"]}
    #test_df = pd.DataFrame(house_data)
    #y_pred = model.predict(test_df)
    #print(y_pred)
    make_model()