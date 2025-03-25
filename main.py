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

def calc_prediction(lat_deg,lon_deg,coordinates_lat,coordinates_lon,ground_speed,altitude):
    Radius = float(6371000)
    dlat = math.radians(coordinates_lat - lat_deg)
    dlon = math.radians(coordinates_lon - lon_deg)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat_deg)) * math.cos(math.radians(coordinates_lat)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = (Radius * c)/1000  # Distance in kilometers

    # Convert ground speed from knots (nautical miles per hour) to kilometers per hour
    ground_speed = ground_speed * 1.852
    ground_speed = (ground_speed + 220)/2 
    return distancia/ground_speed * 3600 
    

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

        columns = ['icao24','datetime','lat_deg','lon_deg','altitude','groundspeed']
        data = data[columns]
        data['groundspeed'] = data['groundspeed'].interpolate(method='linear')
        data['altitude'] = data['altitude'].interpolate(method= 'linear')        
        # Get the last data
        data = data[data["datetime"] == data["datetime"].max()]

        # Get the coordinates of the aircraft
        lat_deg = data.iloc[0].lat_deg
        long_deg = data.iloc[0].lon_deg

        #Get the speed of the aircraft
        ground_speed = data.iloc[0].groundspeed

        #Get the last altitude
        altitude = data.iloc[0].altitude

        #Get the coordinates of the runway
        runway_data = thresholds[thresholds['runway'] == RUNWAY]
        coordinates = runway_data.iloc[0].geometry.coords[0]
        runway_lon = coordinates[0]
        runway_lat = coordinates[1]

        
        #Calculate the time in seconds
        print (lat_deg, long_deg, runway_lat,runway_lon,ground_speed,altitude)
        prediction = calc_prediction(lat_deg, long_deg, runway_lat, runway_lon,ground_speed,altitude) 
        # Write the results
        write_results(prediction, ID_SCENARIO, ICAO, RUNWAY)






if __name__ == "__main__":
    main()