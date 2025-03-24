import pandas as pd
import geopandas as gpd
import folium
from pyproj import Geod


    

def main():
    # Load the data
    predictions = pd.read_csv('samples/sample_predictions_empty.csv')
    
    predictions_vector = []

    for _, linea in predictions.iterrows():
        predictions_vector.append(linea.tolist())
        
        ID_SCENARIO = predictions_vector[0]
        ICAO = predictions_vector[1]
        RUNWAY = predictions_vector[2]






if __name__ == "__main__":
    main()