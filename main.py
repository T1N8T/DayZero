import pandas as pd
import geopandas as gpd
import folium
from pyproj import Geod
import os

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

def calc_prediction():

    return None
    

def main():

    #! Elimina el archivo de resultados si ya existe
    if os.path.exists('results/predictions.csv'):
        os.remove('results/predictions.csv')

    # Load the data
    predictions = pd.read_csv('samples/sample_predictions_empty.csv')
    

    for _, line in predictions.iterrows():
        
        ID_SCENARIO = line['id_scenario']
        ICAO = line['icao24']
        RUNWAY = line['runway']
        
        data = pd.read_parquet('samples/' + ID_SCENARIO + '.parquet')
        data = data[data['icao24'] == ICAO]
        data["datetime"] = pd.to_datetime(data["ts"], unit="ms")

        columns = ['icao24','datetime']
        data = data[columns]

        # Calculate the time in seconds
        prediction = calc_prediction()

        # Write the results
        write_results(prediction, ID_SCENARIO, ICAO, RUNWAY)






if __name__ == "__main__":
    main()