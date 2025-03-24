import pandas as pd
import geopandas as gpd
import folium
from pyproj import Geod
import os, math

def write_results(prediccion, ID_SCENARIO, ICAO, RUNWAY):
    # Crea un DataFrame con los resultados
    results = pd.DataFrame([{
        'id_scenario': ID_SCENARIO,
        'icao24': ICAO,
        'runway': RUNWAY,
        'seconds_to_threshold': prediccion
    }])

    # Ruta del archivo
    file_path = 'results/predictions.csv'

    # Verifica si el archivo ya existe
    if not os.path.exists(file_path):
        # Si el archivo no existe, escribe con encabezados
        results.to_csv(file_path, index=False)
    else:
        # Si el archivo existe, agrega los datos sin sobrescribir encabezados
        results.to_csv(file_path, mode='a', index=False, header=False)

def calc_prediction(lat_deg,lon_deg,coordinates_lat,coordinates_lon,air_speed):
    Radius = float(6371000)
    dlat = math.radians(coordinates_lat - lat_deg)
    dlon = math.radians(coordinates_lon - lon_deg)
    a = math.sin(dlat/2)^2 + math.cos(math.radians(lat_deg)) * math.cos(math.radians(coordinates_lat)) * math.sin(dlon/2)^2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    s = Radius * c / 1000;
    return s/air_speed*3600  #Convert distance to kilometers
    

def main():

    #! Elimina el archivo de resultados si ya existe
    if os.path.exists('results/predictions.csv'):
        os.remove('results/predictions.csv')

    # Load the data
    predictions = pd.read_csv('samples/sample_predictions_empty.csv')
    
    # Load the thresholds
    thresholds = gpd.read_file('thresholds.geojson')

    for _, line in predictions.iterrows():
        
        ID_SCENARIO = line['id_scenario']
        ICAO = line['icao24']
        RUNWAY = line['runway']
        
        data = pd.read_parquet('samples/' + ID_SCENARIO + '.parquet')
        data = data[data['icao24'] == ICAO]
        data["datetime"] = pd.to_datetime(data["ts"], unit="ms")

        columns = ['icao24','datetime','lat_deg','lon_deg','bds60_IAS']
        data = data[columns]
        data = data.ffill()
        
        
        # Get the last data
        data = data[data["datetime"] == data["datetime"].max()]

        # Get the coordinates of the aircraft
        lat_deg = data.iloc[0].lat_deg
        long_deg = data.iloc[0].lon_deg

        #Get the speed of the aircraft
        air_speed = data.iloc[0].bds60_IAS


        #Get the coordinates of the runway
        runway_data = thresholds[thresholds['runway'] == RUNWAY]
        coordinates = runway_data.iloc[0].geometry.coords[0]
        runway_lat = coordinates[0]
        runway_lon = coordinates[1]

        
        #Calculate the time in seconds
        print (lat_deg, long_deg, runway_lat, runway_lon,air_speed)
        prediction = calc_prediction(lat_deg, long_deg, runway_lat, runway_lon,air_speed) 
        # Write the results
        write_results(prediction, ID_SCENARIO, ICAO, RUNWAY)






if __name__ == "__main__":
    main()