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
    time: datetime
    isset_id: str
    name: str
    kpi: str
    operation: str
    sum: float
    avg: float
    min: float
    max: float
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

class SingleMachineDetail(BaseModel):
    machineId: str
    machineName: str
    machineStatus: str
    dataRange: list[datetime]
    totalPower: float
    totalConsumption: float
    totalCost: float

class Production(BaseModel):
    totalPower: float
    totalConsumption: float
    totalCost: float
    energyContributions: float
    machines: list

class SingleProduction(BaseModel):
    machine_id: str
    machine_name: str
    machine_status: str
    data_range: list[datetime]
    total_cycles: int
    good_cycles: int
    bad_cycles: int
    average_cycle_time: float


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
                print(data.time, data.isset_id, data.name, data.kpi, data.operation,
                      data.sum, data.avg, data.min, data.max, data.anomaly)

                query = """
                    INSERT INTO real_time_data (
                        time, asset_id, name, kpi, operation, sum, avg, min, max, anomaly
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """
                cursor.execute(query, (data.time, data.isset_id, data.name, data.kpi,
                                       data.operation, data.sum, data.avg, data.min,
                                       data.max, data.anomaly))

                logs = cursor.fetchall()
        return {"data": logs}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


# FILTERED GET HISTORICAL DATA
@app.get("/filtered_historical_data")
def filtered_get_historical_data(name: str, asset_id: str, kpi: str, operation: str, timestamp_start: datetime, timestamp_end: datetime):
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

                if name:
                    conditions.append("name = %s")
                    params.append(name)

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

                dashboard = DashboardObj(total_machines=total_machines,totalConsumptionPerDay=consumption_sum,totalCostPerDay=cost_sum,totalAlarm=random.randint(0,3),costAnalysis={}
                                         )

        return {"data":dashboard}
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
                single_machine_detail = SingleMachineDetail(
                    machineId=machine_id,
                    machineName=machineName,
                    machineStatus=machineStatus,
                    dataRange=datarange,
                    totalPower=total_power,
                    totalConsumption=consumption_sum,
                    totalCost=cost_sum
                )

            return {"data":single_machine_detail}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}

<<<<<<< HEAD
# Base endpoint for accessing database

import pandas as pd

@app.get("/get_aggregated_kpi")
def get_aggregated_kpi(time_start: datetime, time_end: datetime):
    """
    Retrieves data from the `aggregated_kpi` table for a specified time range
    and returns it in JSON format.

    The time range is matched against rows with overlapping `begin_datetime` and `end_datetime`.

    Args:
        time_start (datetime): The start of the time range for the query.
        time_end (datetime): The end of the time range for the query.

    Returns:
        str: A JSON-formatted string containing the filtered data.
    """
    # SQL query to retrieve data based on the time range
    # The condition checks for any overlap between the input range and the row's datetime range
    query = """
        SELECT * 
        FROM aggregated_kpi
        WHERE begin_datetime <= %s AND end_datetime >= %s;
    """
    
    try:
        # Establish a connection to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            # Execute the SQL query and read the result into a DataFrame
            df = pd.read_sql_query(query, conn, params=(time_end, time_start))
        
        # Convert the DataFrame to JSON format with "records" orientation
        return df.to_json(orient="records")
    except Exception as e:
        # Handle any errors that occur during the process and return an error message in JSON format
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while executing the query"}'

@app.get("/get_machines")
def get_machines(asset_id=None):
    """
    Retrieves machine information from the `machines` table.
    If `asset_id` is provided, filters the table by `asset_id`.
    Otherwise, returns the entire table.

    Args:
        asset_id (str, optional): The ID of the machine to filter by. Defaults to None.

    Returns:
        str: A JSON-formatted string containing the machine data.
    """
    # SQL query to retrieve all machines or filter by asset_id
    query = """
        SELECT * 
        FROM machines
        WHERE (%s IS NULL OR asset_id = %s);
    """
    
    try:
        # Establish a connection to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            # Execute the query and read the result into a DataFrame
            df = pd.read_sql_query(query, conn, params=(asset_id, asset_id))
        
        # Convert the DataFrame to JSON format with "records" orientation
        return df.to_json(orient="records")
    except Exception as e:
        # Handle any errors that occur during the process and return an error message in JSON format
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while executing the query"}'

@app.get("/get_maintenance_records")
def get_maintenance_records(time_start: datetime, time_end: datetime):
    """
    Retrieves maintenance records from the `maintenance_records` table
    for records that overlap with the specified time range.

    Args:
        time_start (datetime): Start of the time range.
        time_end (datetime): End of the time range.

    Returns:
        str: A JSON-formatted string containing the maintenance records.
    """
    # SQL query to retrieve records where the time ranges overlap
    query = """
        SELECT * 
        FROM maintenance_records
        WHERE start_time <= %s AND end_time >= %s;
    """
    
    try:
        # Establish a connection to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            # Execute the query and read the result into a DataFrame
            df = pd.read_sql_query(query, conn, params=(time_end, time_start))
        
        # Convert the DataFrame to JSON format with "records" orientation
        return df.to_json(orient="records")
    except Exception as e:
        # Handle any errors that occur during the process and return an error message in JSON format
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while executing the query"}'

@app.get("/get_personal_data")
def get_personal_data(name=None, surname=None, operator_id=None):
    """
    Retrieves personal data based on the given parameters from the `personal_data` table.
    
    Args:
        name (str, optional): First name of the person.
        surname (str, optional): Surname of the person.
        operator_id (int, optional): Unique identifier for the operator.
    
    Returns:
        str: JSON-formatted string containing the results.
    """
    # Base query
    query = "SELECT * FROM personal_data"
    conditions = []
    params = []

    # Determine conditions based on input parameters
    if operator_id:
        conditions.append("operator_id = %s")
        params.append(operator_id)
    elif name and surname:
        conditions.append("name = %s AND surname = %s")
        params.extend([name, surname])
    elif name:
        conditions.append("name = %s")
        params.append(name)
    elif surname:
        conditions.append("surname = %s")
        params.append(surname)

    # Add conditions to query if any
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    try:
        # Establish database connection
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            # Execute query and load results into DataFrame
            df = pd.read_sql_query(query, conn, params=params)
        
        # Return results as JSON
        return df.to_json(orient="records")
    except Exception as e:
        # Handle any errors during execution
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while retrieving personal data"}'



# API prototype for the energy dashboard
=======
'''
input: init_date, end_date
log_id: int
start_time: str
end_time: str
responsible_operator_id: int
operation_description: str
result_summary: str
asset_id: int
'''
@app.get("/production")
async def get_production_logs(init_date, end_date):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Query to fetch production logs
                query = """
                    SELECT *
                    FROM public.production_logs where start_time >= %s and end_time <= %s
                """
                cursor.execute(query,(init_date,end_date))
                logs = cursor.fetchall()
        return logs

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}

'''
input: asset_id
'''
@app.get("/production_detail")
async def get_production_detail(asset_id):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Query to fetch production logs
                query = """
                    SELECT *
                    FROM public.production_logs where asset_id = %s
                """
                cursor.execute(query, (asset_id,))
                logs = cursor.fetchall()
        return logs

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


'''// Production
input: init_date, end_date
const production = {
    totalPower: "",
    totalConsumption: "",
    totalCost: "",
    energyContributions: "",
    machines: [
        {
            machineId: "",
            machineName: "",
            machineStatus: "",
            averageCycleTime: "",
            cycleCount: "",
            badCycles: "",
            goodCycles: "",
            efficiency: "",
            density: "",
            failureRate: "",
            successRate: "",
        },
    ]
}'''

@app.get("/production_dashboard")
async def get_production_dashboard(init_date, end_date):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Query to fetch production logs
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

                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s
                """
                cursor.execute(query,(init_date,end_date,"power"))

                logs = cursor.fetchall()
                total_power = 0
                for log in logs:
                    total_power += log[0]


                query = """
                        select * from real_time_data where time >= %s and time <= %s 
                """
                cursor.execute(query,(init_date,end_date))
                logs = cursor.fetchall()
                energy_Contribution = 0
                running = 0
                idle = 0
                for log in logs:
                    if log[-1].lower() == "running":
                        running+=1
                    else:
                        idle+=1
                if (idle > 0 ) and (running > 0):
                    energy_Contribution = (running/(idle+running)) * 100

                
                query = """
                    select m.*
                    FROM public.machines as m inner join public.real_time_data as r on m.asset_id = r.asset_id where r.time >= %s and r.time <= %s
                """
                cursor.execute(query,(init_date,end_date))

                total_machines = cursor.fetchall()
            
                consumption_sum = 0 if math.isnan(consumption_sum) else consumption_sum
                cost_sum = 0 if math.isnan(cost_sum) else cost_sum
                total_power = 0 if math.isnan(total_power) else total_power


                returnValue = Production(totalConsumption=consumption_sum,totalCost=cost_sum,energyContributions=energy_Contribution,machines=total_machines,totalPower=total_power)
                
        return {"data":returnValue}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}

'''// Single Production Detail
input: init_date, end_date, asset_id
const singleProduction = {
    machineId: "",
    machineName: "",
    machineStatus: "",
    dataRange: "",
    totalCycles: "",
    goodCycles: "",
    badCycles: "",
    averageCycleTime: "",
}
'''
@app.get("/single_production")
async def get_single_production(init_date, end_date,asset_id):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Query to fetch production logs
                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query,(init_date,end_date,"goodCycles",asset_id))

                logs = cursor.fetchall()
                good_cycles = 0
                for log in logs:
                    good_cycles += log[0]
                
                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query,(init_date,end_date,"badCycles",asset_id))

                logs = cursor.fetchall()
                bad_cycles = 0
                for log in logs:
                    bad_cycles += log[0]

                query = """
                    Select avg from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query,(init_date,end_date,"CycleTime",asset_id))

                logs = cursor.fetchall()
                average_cycle_time = 0
                for log in logs:
                    average_cycle_time += log[0]
                query = """
                    select * from machines where machine_id = %s
                    """
                cursor.execute(query,(asset_id,))
            
                logs = cursor.fetchall()
                machine = logs[0]

            returnValue = SingleProduction(machine_id=asset_id,machine_name=machine[1],machine_status=machine[6],
                                           data_range=[init_date,end_date],total_cycles=good_cycles+bad_cycles,good_cycles=good_cycles,average_cycle_time=average_cycle_time)
                
        return {"data":returnValue}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}





>>>>>>> 8df213afe05ab4165ca04557f150faf8bd251133

"""
// Machine Usage
input: init_date, end_date
// Energy

const energy = {
    totalPower: "",
    totalConsumption: "",
    totalCost: "",
    energy Contributions: "", // Cosa vuol dire?
    machines: [
        {
            machineId: "",
            machineName: "",
            machineStatus: "",
            consumption: {
                total: "",
                working: "",
                idle: ""
            },

            efficiency: {
                energyEfficiencyRatio: "",  // Cosa vuol dire?
                energyConsumptionPerUnit: ""  // Cosa vuol dire?
            },

            sustainability: { // Non ne teniamo conto
                renewableEnergyUsagePercentage: "", // Cosa vuol dire?
                carbonFootPrint: "" // Cosa vuol dire?
            }
        },
    ]
}

"""


@app.get("/energy")
def get_energy(init_date, end_date):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                init_date = datetime.fromisoformat(init_date)
                end_date = datetime.fromisoformat(end_date)
                query = query = """
                WITH aggregated_data AS (
                SELECT
                    rtd.asset_id,
                    SUM(CASE WHEN rtd.kpi = 'power' THEN rtd.sum ELSE 0 END) AS total_power,
                    SUM(CASE WHEN rtd.kpi = 'consumption' THEN rtd.sum ELSE 0 END) AS total_consumption,
                    SUM(CASE WHEN rtd.kpi = 'cost' THEN rtd.sum ELSE 0 END) AS total_cost,
                    SUM(CASE WHEN rtd.operation = 'working' THEN rtd.sum ELSE 0 END) AS working_consumption,
                    SUM(CASE WHEN rtd.operation = 'idle' THEN rtd.sum ELSE 0 END) AS idle_consumption
                FROM
                    real_time_data rtd
                WHERE
                    rtd.time BETWEEN %s AND %s
                GROUP BY
                    rtd.asset_id
            ),
            machine_details AS (
                SELECT
                    m.asset_id,
                    m.name AS machine_name,
                    m.status AS machine_status
                FROM
                    machines m
                WHERE
                    m.status = 'active'
            )
            SELECT
                COALESCE(SUM(ad.total_power), 0) AS total_power,
                COALESCE(SUM(ad.total_consumption), 0) AS total_consumption,
                COALESCE(SUM(ad.total_cost), 0) AS total_cost,
                JSON_AGG(
                    JSON_BUILD_OBJECT(
                        'machineId', md.asset_id,
                        'machineName', md.machine_name,
                        'machineStatus', md.machine_status,
                        'consumption', JSON_BUILD_OBJECT(
                            'total', COALESCE(ad.total_consumption, 0),
                            'working', COALESCE(ad.working_consumption, 0),
                            'idle', COALESCE(ad.idle_consumption, 0)
                        )
                    )
                ) AS machines
            FROM
                machine_details md
            LEFT JOIN
                aggregated_data ad
            ON
                md.asset_id = ad.asset_id;
                """
                params = {
                    'start_time': init_date,
                    'end_time': end_date
                }

                cursor.execute(query, params)

                result = cursor.fetchone()
                if result:
                    energy = {
                        "totalPower": result[0],
                        "totalConsumption": result[1],
                        "totalCost": result[2],
                        "energyContributions": result[3],
                        "machines": json.loads(result[4])  # Decodifica il JSON restituito
                    }
                    return energy
                else:
                    return {"message": "No data found for the given range."}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}


"""
// Single Energy Detail
input : machine_id, init_date, end_date
const singleEnergy = {
    machineId: "",
    machineName: "",
    machineStatus: "",
    dataRange: "",
    totalPower: "",
    totalConsumption: "",
    totalCost: "",
    energyContributions: "", // Cosa vuol dire?
    workingConsumption: "", 
    idleConsumption: "",
    energyEfficiencyRatio: "", // Cosa vuol dire?
    energyConsumptionPerUnit: "", // Cosa vuol dire?
    renewableEnergyUsagePercentage: "", // Cosa vuol dire?
    carbonFootprint: "", // Cosa vuol dire?
"""

@app.get("/single_energy_detail")
def single_energy_detail(machine_id, time_start, time_end):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                query = """
                WITH MachineSummary AS (
                    SELECT 
                        machine_id AS machineId,
                        machine_name AS machineName,
                        machine_status AS machineStatus,
                        %(time_start)s || ' to ' || %(time_end)s AS dataRange,
                        SUM(power) AS totalPower,
                        SUM(consumption) AS totalConsumption,
                        SUM(cost) AS totalCost,
                        SUM(renewable_energy) / NULLIF(SUM(consumption), 0) * 100 AS energyContributions,
                        SUM(CASE WHEN machine_status = 'working' THEN consumption ELSE 0 END) AS workingConsumption,
                        SUM(CASE WHEN machine_status = 'idle' THEN consumption ELSE 0 END) AS idleConsumption,
                        AVG(energy_efficiency_ratio) AS energyEfficiencyRatio,
                        AVG(energy_consumption_per_unit) AS energyConsumptionPerUnit,
                        SUM(renewable_energy) / NULLIF(SUM(consumption), 0) * 100 AS renewableEnergyUsagePercentage,
                        SUM(carbon_footprint) AS carbonFootprint
                    FROM historical_data
                    WHERE machine_id = %(machine_id)s
                      AND timestamp BETWEEN %(time_start)s AND %(time_end)s
                    GROUP BY machine_id, machine_name, machine_status
                ),
                MachineChart AS (
                    SELECT 
                        DATE(timestamp) AS date,
                        SUM(consumption) AS totalConsumption,
                        SUM(CASE WHEN machine_status = 'working' THEN consumption ELSE 0 END) AS workingConsumption,
                        SUM(CASE WHEN machine_status = 'idle' THEN consumption ELSE 0 END) AS idleConsumption
                    FROM historical_data
                    WHERE machine_id = %(machine_id)s
                      AND timestamp BETWEEN %(time_start)s AND %(time_end)s
                    GROUP BY DATE(timestamp)
                )
                SELECT 
                    ms.machineId,
                    ms.machineName,
                    ms.machineStatus,
                    ms.dataRange,
                    ms.totalPower,
                    ms.totalConsumption,
                    ms.totalCost,
                    ms.energyContributions,
                    ms.workingConsumption,
                    ms.idleConsumption,
                    ms.energyEfficiencyRatio,
                    ms.energyConsumptionPerUnit,
                    ms.renewableEnergyUsagePercentage,
                    ms.carbonFootprint,
                    'line' AS chartType,
                    json_agg(
                        json_build_object(
                            'date', mc.date,
                            'totalConsumption', mc.totalConsumption,
                            'workingConsumption', mc.workingConsumption,
                            'idleConsumption', mc.idleConsumption
                        )
                    ) AS chart
                FROM MachineSummary ms, MachineChart mc;
                """
                
                params = {
                    "machine_id": machine_id,
                    "time_start": time_start,
                    "time_end": time_end
                }
                
                cursor.execute(query, params)
                
                result = cursor.fetchone()
                if result:
                    singleEnergy = {
                        "machineId": result[0],
                        "machineName": result[1],
                        "machineStatus": result[2],
                        "dataRange": result[3],
                        "totalPower": result[4],
                        "totalConsumption": result[5],
                        "totalCost": result[6],
                        "energyContributions": result[7],
                        "workingConsumption": result[8],
                        "idleConsumption": result[9],
                        "energyEfficiencyRatio": result[10],
                        "energyConsumptionPerUnit": result[11],
                        "renewableEnergyUsagePercentage": result[12],
                        "carbonFootprint": result[13],
                        "chartType": result[14],
                        "Chart": json.loads(result[15])  
                    }
                    return singleEnergy
                else:
                    return {"message": "No data found for the given range."}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
                

"""
// Financial Report
const Financial = {
    dataRange: "",
    grossMargin: "",
    roi: "",
    revenuePerEmployee: "", // Finto fisso
    salesGrowthRate: "", 
    totalOperationalCost: "",
    costPerUnit: "",
    costPerCycle: "", 
    totalEnergyCost: "",
    chartType: "",
    Chart: [
        {
            date: "",
            operationalCost: "",
        },
    ]
}
"""




