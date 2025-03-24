import pandas as pd
import geopandas as gpd
import folium
from pyproj import Geod

def write_results(prediccion, ID_SCENARIO, ICAO, RUNWAY):

    return None

def calc_prediction():
    
    return None
    

def main():
    # Load the data
    predictions = pd.read_csv('samples/sample_predictions_empty.csv')
    
    predictions_vector = []

    for _, linea in predictions.iterrows():
        predictions_vector.append(linea.tolist())
        
        ID_SCENARIO = predictions_vector[0]
        ICAO = predictions_vector[1]
        RUNWAY = predictions_vector[2]
        
        data = pd.read_parquet('samples/' + ID_SCENARIO + '.parquet')
        data = data[data['ICAO'] == ICAO]
        data["datetime"] = pd.to_datetime(data["ts"], unit="ms")

        columns = ['ni idea todavia']
        data = data[columns]

        # Calculate the time in seconds
        prediction = calc_prediction()

        # Write the results
        write_results(prediction, ID_SCENARIO, ICAO, RUNWAY)






if __name__ == "__main__":
    main()