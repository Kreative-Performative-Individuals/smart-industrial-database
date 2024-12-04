import math
from fastapi import FastAPI
import psycopg2
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime
import psycopg2
import os
import json
from fastapi.encoders import jsonable_encoder
from fastapi import Query
from typing import Optional
from math import isnan, isinf
from dotenv import load_dotenv
import hashlib
import random
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()


class AnomalyDataRequest(BaseModel):
    timestamp: datetime
    isset_id: str
    name: str
    kpi: str
    operation: str
    sum: float
    avg: float
    min: float
    max: float
    var: float
    anomaly: str

class UserRequest(BaseModel):
      email: str
      password: str
      username: str    
      role: str

class LoginRequest(BaseModel):
      username: str
      password: str

class DashboardObj(BaseModel):
    totalMachines: int
    totalConsumptionPerDay: float
    totalCostPerDay: float
    totalAlarm: float
    costAnalysis: float


@app.get("/machines", summary="Fetch machine records",
         description="This endpoint retrieves all records from the machines table in the database, displaying details about each machine.")
async def fetch_machines():
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                print("Connessione al database riuscita.")

                # Query the machines table to fetch all rows
                cursor.execute("SELECT * FROM machines;")
                machines = cursor.fetchall()

                # Print the results of the query
                print("\nRisultati della query:")
                for row in machines:
                    print(row)

        return {"message": "Machines fetched successfully", "data": machines}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


@app.get("/query", summary="Fetch query records", )
async def fetch_query(statement: str):
    print("Statement", statement)
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                print("Connessione al database riuscita.")

                # Query the machines table to fetch all rows
                cursor.execute(statement)
                result = cursor.fetchall()

        return {"message": "Query fetched successfully", "data": result}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


@app.post("/insert", summary="Insert records", )
async def insert_query(statement: str, data: dict):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Query the machines table to fetch all rows
                cursor.execute(statement, data)
                conn.commit()

        return {"message": "Query inserted successfully"}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


@app.get("/maintenance_records", summary="Fetch maintenance records",
         description="This endpoint retrieves all maintenance records from the database and displays them.")
async def fetch_maintenance_records():
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                print("Connessione al database riuscita.")
                cursor.execute("SELECT * FROM maintenance_records;")
                records = cursor.fetchall()
                print("\nRisultati della query:")
                for row in records:
                    print(row)
        return {"message": "Maintenance records fetched successfully", "data": records}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


@app.get("/real_time_data", summary="Fetch real-time data",
         description="This endpoint retrieves all real-time data related to KPIs from the database, enabling live performance tracking.")
async def fetch_personal_data():
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                print("Connessione al database riuscita.")
                cursor.execute("SELECT * FROM personal_data;")
                data = cursor.fetchall()
                print("\nRisultati della query:")
                for row in data:
                    print(row)
        return {"message": "Personal data fetched successfully", "data": data}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


@app.get("/production_logs", summary="Fetch production logs",
         description="This endpoint retrieves all production logs from the database, useful for monitoring and analytics purposes.")
async def fetch_production_logs():
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                print("Connessione al database riuscita.")
                cursor.execute("SELECT * FROM production_logs;")
                logs = cursor.fetchall()
                print("\nRisultati della query:")
                for row in logs:
                    print(row)
        return {"message": "Production logs fetched successfully", "data": logs}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


# TODO, implement a query to return requested data to allow group 3 to do their calculations.
# Please check the data format of the return. 
# The query should filter based on the parameters: 
#     machine_name, asset_id, kpi, operation, timestamp_start, timestamp_end
# and should return the records with the same information, 
# so a list of records like:
#     machine_name, asset_id, kpi, operation, timestamp_start, timestamp_end
# Test the endpoint before pushing so that we are sure that group 3 can use it.


def safe_float(val):
    if isinstance(val, float):
        if val == float('inf') or val == float('-inf'):
            return str(val)  # Convert infinite values to a string representation
        if isnan(val):
            return None  # Convert NaN values to None
    return val


def row_to_dict(columns, row):
    return {col: safe_float(value) for col, value in zip(columns, row)}


from math import isnan


@app.get("/historical_data")
async def get_historical_data():
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM real_time_data")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]  # This retrieves column names from cursor

                data = [row_to_dict(columns, row) for row in rows]

                if not data:
                    print("No data found.")
                return {"data": data}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}
    



# TODO, implement the query for the endpoint.
# This endpoint should allow group 3 to post data inside the database. 
# The data that should be stored is like this 
# datapoint = {
#     'timestamp': 'timepoint',
#     'isset_id': 'ast-yhccl1zjue2t',
#     'name': 'metal_cutting',
#     'kpi': 'time',
#     'operation': 'working',
#     'sum': float, 
#     'avg': float,
#     'min': float,
#     'max': float,
#     'var': float
# }

# And should go in the real-time data table. The AnomlayDataRequest object stores the informations that are needed to perform the query
# there is an extra field called anomaly, that can be ignored if we don't want to use that, but they can identify anomalies so it's 
# included. Test the endponits before pushing so that we are sure group 3 can use them.
@app.post("/store_datapoint")
async def post_data_point(data: AnomalyDataRequest):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                print("parameters")
                # Print to check if parameters are passed correctly.
                print(data.timestamp, data.isset_id, data.name, data.kpi, data.operation,
                      data.sum, data.avg, data.min, data.max, data.var, data.anomaly)

                # TODO implement the real query.
                
                query = """
                    INSERT INTO real_time_data (
                        timestamp, asset_id, name, kpi, operation, sum, avg, min, max, var, anomaly
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """

                cursor.execute(query, (data.timestamp, data.isset_id, data.name, data.kpi,
                                       data.operation, data.sum, data.avg, data.min,
                                       data.max, data.var, data.anomaly))

                logs = cursor.fetchall()
        return {"data": logs}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


# FILTERED GET HISTORICAL DATA
@app.get("/filtered_historical_data")
def filtered_get_historical_data(machine_name:str, asset_id:str, kpi:str, operation:str, timestamp_start:datetime, timestamp_end:datetime):
    try:
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
            
        ) as conn:
            with conn.cursor() as cursor:
                print("Connessione al database riuscita.")
                # AL POSTO DI real_time_data METTERE IL NOME DELLA TABELLA
                query = """
                    SELECT * FROM real_time_data
                """
                conditions = []
                params = []

                if machine_name:
                    conditions.append("name = %s")
                    params.append(machine_name)

                if asset_id:
                    conditions.append("asset_id = %s")
                    params.append(asset_id)

                if kpi:
                    conditions.append("kpi = %s")
                    params.append(kpi)

                if timestamp_start:
                    conditions.append("time >= %s")
                    params.append(timestamp_start)

                if timestamp_end:
                    conditions.append("time <= %s")
                    params.append(timestamp_end)

                # Aggiungi la clausola WHERE se ci sono condizioni
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                # Aggiungi l'ordinamento
                query += " ORDER BY time ASC;"

                # Esegui la query
                cursor.execute(query, params)
                data = cursor.fetchall()

                # Print the results of the query
                print("\nPrint the results of the query':")
                for row in data:
                    print(row)

    except Exception as e:
        print(f"Errore: {e}")
        return {"message": "An error occurred", "error": str(e)}
    
#hash strings, such as password
def hash_string(in_string: str) -> str:
    hashed_string = hashlib.sha256(in_string.encode('utf-8')).hexdigest()
    return hashed_string

# Query endpoints for frontend
'''
const user = {
    email: "String",
    password: "String",
    username: "String",
    role: "User Role (SMO / FFM)"
}'''
@app.post("/register")
async def register_user(user: UserRequest):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
               
                # Print to check if parameters are passed correctly.
                print(user)

                # TODO implement the real query.

                query = """
                    SELECT COUNT(*) 
                    FROM users 
                    WHERE username = %s OR email = %s
                """
                cursor.execute(query, (user.username, user.email))

                res = cursor.fetchall()
                if res[0][0] >= 1:
                    return {"message":"Duplicate username or email"}
                
                query = """
                    INSERT INTO users (
                        username, password, email, role
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING userid;
                """

                cursor.execute(query, (user.username,hash_string(user.password),user.email,user.role))

                logs = cursor.fetchall()
        return {"data": logs}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}
    
@app.post("/login")
async def login(user: LoginRequest):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
               
                # Print to check if parameters are passed correctly.
                print(user)

                # TODO implement the real query.
                
                query = """
                    Select * from users where username = %s and password = %s
                """

                cursor.execute(query, (user.username,hash_string(user.password)))

                logs = cursor.fetchall()
                print(len(logs))
                if len(logs) == 0:
                    return {"message":"login failed"}
                    
        return {"message":"login successful"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}

'''
const dashboard = {
    totalMachines: "",
    totalConsumptionPerDay: "",
    totalCostPerDay: "",
    totalAlarm: "",
    costAnalysis: {},
    recentlyViewed: {
        machineUsage: [{}],
        energy: [{}],
        production: [{}]
    }
}
'''
#dashboard = DashboardObj()
@app.get("/get_machines")
async def get_machines(init_date, end_date):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                timestamp = datetime.strptime(init_date, "%Y-%m-%d %H:%M:%S")

                init_date = datetime.fromisoformat(init_date)
                end_date = datetime.fromisoformat(end_date)
                # Print to check if parameters are passed correctly.
                # TODO implement the real query.
                

                query = """
                        select Count(*) from machines 
                    """
                cursor.execute(query)
                total_machines = cursor.fetchall()[0][0]
                print(total_machines)


                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s
                """
                cursor.execute(query,(init_date,end_date,"consumption"))

                logs = cursor.fetchall()
                consumption_sum = 0
                for log in logs:
                    consumption_sum += log[0]
                
                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s
                """
                cursor.execute(query,(init_date,end_date,"cost"))

                logs = cursor.fetchall()
                cost_sum = 0
                for log in logs:
                    cost_sum += log[0]                    


                # Create a sequence of integers representing the components of the timestamp
                timestamp_ints = [timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second]
                random.seed(sum(timestamp_ints))
                consumption_sum = 0 if math.isnan(consumption_sum) else consumption_sum
                cost_sum = 0 if math.isnan(cost_sum) else cost_sum

        return {"data":{"totalMachines":total_machines,"totalConsumptionPerDay":consumption_sum,"totalCostPerDay":cost_sum,"totalAlarm":random.randint(0,3)}}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}
    

'''// Single Machine Detail
const singleMachines = {
    machineId: "",
    machineName: "",
    machineStatus: "",
    dataRange: "",
    totalPower: "",
    totalConsumption: "",
    totalCost: "",
}'''
@app.get("/single_machine_detail")
def single_machine_detail(machine_id,init_date,end_date):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
               
                # Print to check if parameters are passed correctly

                # TODO implement the real query.
                
                print("hello")
                query = """
                    Select name from machines where asset_id = %s
                """

                cursor.execute(query, (machine_id,))
                logs = cursor.fetchall()
                machineName = logs[0][0]
                init_date = datetime.fromisoformat(init_date)
                end_date = datetime.fromisoformat(end_date)
                query = """
                    Select operations from real_time_data where asset_id = %s and time >= %s and time <= %s
                """

                cursor.execute(query, (machine_id,init_date,end_date))
                logs = cursor.fetchall()
                machineStatus = logs[0][0]
                datarange = [init_date,end_date]            
                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query,(init_date,end_date,"consumption",machine_id))

                logs = cursor.fetchall()
                consumption_sum = 0
                for log in logs:
                    consumption_sum += log[0]
                
                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query,(init_date,end_date,"cost",machine_id))

                logs = cursor.fetchall()
                cost_sum = 0
                for log in logs:
                    cost_sum += log[0]

                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query,(init_date,end_date,"power",machine_id))

                logs = cursor.fetchall()
                total_power = 0
                for log in logs:
                    total_power += log[0]

                consumption_sum = 0 if math.isnan(consumption_sum) else consumption_sum
                cost_sum = 0 if math.isnan(cost_sum) else cost_sum
                total_power = 0 if math.isnan(total_power) else total_power
                # Construct and return the final response object
                single_machine_detail = {
                    "machineId": machine_id,
                    "machineName": machineName,
                    "machineStatus": machineStatus,
                    "dataRange": datarange,
                    "totalPower": total_power,
                    "totalConsumption": consumption_sum,
                    "totalCost": cost_sum
                }

                print(single_machine_detail)
            return {"data":single_machine_detail}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}
