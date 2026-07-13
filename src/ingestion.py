import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import os

# Define the data lake storage path
STORAGE_DIR = "../data_lake/silver/"

def fetch_weather_data(latitude, longitude):
    """Extracts live weather data from an external REST API."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    print(f"📡 Requesting data from API: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Request Failed: Status Code {response.status_code}")

def transform_to_dataframe(raw_json, location_name):
    """Transforms raw nested JSON into a structured Pandas DataFrame."""
    current = raw_json.get('current_weather', {})
    
    # Flatten the JSON payload
    structured_data = {
        'location': [location_name],
        'temperature_celsius': [current.get('temperature')],
        'windspeed_kmh': [current.get('windspeed')],
        'winddirection': [current.get('winddirection')],
        'is_day': [current.get('is_day')],
        'extraction_timestamp': [datetime.now()]
    }
    
    return pd.DataFrame(structured_data)

def load_to_parquet(df, location_name):
    """Loads the dataframe into a columnar Parquet file (Data Lake simulation)."""
    # Ensure the directory exists
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    # Create a dynamic filename based on timestamp
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{STORAGE_DIR}{location_name}_{timestamp_str}.parquet"
    
    # Convert Pandas DataFrame to PyArrow Table and write to Parquet
    table = pa.Table.from_pandas(df)
    pq.write_table(table, filename)
    
    print(f"💾 Successfully wrote partitioned Parquet file to: {filename}")

if __name__ == "__main__":
    # Target coordinates: Jabalpur, MP (23.1815° N, 79.9864° E)
    TARGET_LAT = 23.1815
    TARGET_LONG = 79.9864
    LOCATION = "Jabalpur"
    
    print("🚀 Initializing ELT API Ingestion Pipeline...")
    
    # 1. Extract
    raw_api_data = fetch_weather_data(TARGET_LAT, TARGET_LONG)
    
    # 2. Transform
    clean_df = transform_to_dataframe(raw_api_data, LOCATION)
    print("\nData Preview:")
    print(clean_df.to_string())
    print("\n")
    
    # 3. Load
    load_to_parquet(clean_df, LOCATION)
