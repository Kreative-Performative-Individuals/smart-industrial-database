import os 
import sys 
import requests

new_datapoint = {'time': '2026-09-17 00:00:00+00:00',  
                 'asset_id': 'ast-sfio4727eub0',  
                 'name': 'Assembly Machine 3',  
                 'kpi': 'cost',  
                 'operation': 'independent',  
                 'sum': 1100.0, 'avg': 0.0, 'min': 0.0, 'max': 0.0, 'var': 1, 'status': 'normal'} 
 
 
def store_datapoint(new_datapoint):

    url_db = "http://localhost:8002/"
    try:
        response = requests.post(f"{url_db}store_datapoint", json=new_datapoint)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return JSON response from the server
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to store data point: {e}"}

#print(store_datapoint(new_datapoint))


#TODO fix 422
def get_historical_data(machine_name, asset_id, kpi, operation, timestap_start, timestamp_end): 
     # In some manner receives data frame filtered from the database in format dataframe 
     #Maybe we can define that if we give timestap_start = None, timestamp_end = None, 
     #they have to return us x values in the past starting from the last stored point 
     
     
     url_db = "http://localhost:8002/" 
      
     params = { 
     "start_date": timestap_start, 
     "end_date": timestamp_end, 
     "kpi_name": kpi, 
     "column_name": "",
     "machines": machine_name, 
     "operations": operation, 
     "asset_id": asset_id 
    } 
 
     # Send the GET request 
     response = requests.get(url_db + "get_real_time_data", json=params) 
 
     return response.json()["data"]
print(get_historical_data("Laser Welding Machine 2,Laser Welding Machine 1","ast-206phi0b9v6p","good_cycles","working,s","2024-10-19 00:00:00","2024-10-19 00:00:00"))

