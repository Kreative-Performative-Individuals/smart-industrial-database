import math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from datetime import datetime
from pydantic import BaseModel
import psycopg2
import os
import json
from typing import Optional
from dotenv import load_dotenv
import hashlib
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SALT = os.getenv("SALT")
KEY_ENC = os.getenv("KEY")

app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    status: str
    var: float

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

class AggregatedKPI(BaseModel):
    name: str
    aggregated_value: float
    begin_datetime: str
    end_datetime: str
    kpi_list: list[str]
    operations: list[str]
    machines: list[str]
    step: int

class RealTimeData(BaseModel):
    start_date: str
    end_date: str 
    kpi_name: str
    asset_id: str
    machines: str
    operations: str
    column_name: str

#salva
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

#Salva
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

#Salva
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


"""@app.post("/insert_aggregated_kpi", summary="Insert aggregated KPI into the table")
async def insert_query(data: AggregatedKPI):
    try:
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            print(data)
            with conn.cursor() as cursor:
                # Prepare the SQL insert query
                query = "INSERT INTO aggregated_kpi (name, aggregated_value, begin_datetime, end_datetime, kpi_list, operations, machines, step) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

                # Execute the query with the provided data
                cursor.execute(query, (data.name, data.aggregated_value, data.begin_datetime, data.end_datetime, data.kpi_list, data.operations, data.machines, data.step))
                
                # Commit the transaction to save changes permanently
                conn.commit()

        return {"message": "Query inserted successfully"}

    except Exception as e:
        # Log the error and return an error message
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}
"""

"""
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
"""

"""@app.get("/real_time_data", summary="Fetch real-time data",
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
"""
"""
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

"""
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
        if math.isnan(val):
            return None  # Convert NaN values to None
    return val


def row_to_dict(columns, row):
    return {col: safe_float(value) for col, value in zip(columns, row)}


#Salva
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
    
"""
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
                      data.sum, data.avg, data.min, data.max, data.status, data.var)

                query = 
                    INSERT INTO real_time_data (
                        time, asset_id, name, kpi, operation, sum, avg, min, max, status, var
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                
                cursor.execute(query, (data.time, data.isset_id, data.name, data.kpi,
                                       data.operation, data.sum, data.avg, data.min,
                                       data.max, data.status, data.var))

                logs = cursor.fetchall()
        return {"data": logs}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}
"""
"""
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
                query = 
                    SELECT * FROM real_time_data
                
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

"""
#hash strings, such as password
def hash_string(in_string: str) -> str:
    hashed_string = hashlib.sha256(in_string.encode('utf-8')).hexdigest()
    return hashed_string

# Query endpoints for frontend
@app.post("/register")
async def register_user(user: UserRequest):
    """
    Endpoint to register a new user.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Debug: Print user details
                print(f"Registering user: {user}")

                # Check if the username or email already exists
                check_query = """
                    SELECT COUNT(*)
                    FROM users
                    WHERE username = %s OR email = %s
                """
                cursor.execute(check_query, (user.username, user.email))
                duplicate_count = cursor.fetchone()[0]

                if duplicate_count > 0:
                    return {"message": "Duplicate username or email"}

                # Insert the new user into the database
                insert_query = """
                    INSERT INTO users (username, password, email, role)
                    VALUES (%s,%s, pgp_sym_encrypt(%s,%s), pgp_sym_encrypt(%s,%s))
                    RETURNING userid;
                """
                hashed_password = hash_string(SALT + user.password)
                cursor.execute(insert_query, (user.username, hashed_password, user.email,KEY_ENC, user.role,KEY_ENC))
                
                # Fetch the newly created user ID
                user_id = cursor.fetchone()
                return {"data": {"userid": user_id}}

    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return {"message": "An error occurred", "error": str(e)}


@app.post("/login")
async def login(user: LoginRequest):
    """
    Endpoint to authenticate a user.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Debug: Print user details
                print(f"Attempting login for user: {user.username}")

                # Query to validate user credentials
                login_query = """
                    SELECT * 
                    FROM users 
                    WHERE username = %s AND  password = %s;
                """
                hashed_password = hash_string(SALT + user.password)
                cursor.execute(login_query, (user.username, hashed_password))

                # Check if any records are returned
                user_data = cursor.fetchone()
                if not user_data:
                    return {"message": "Login failed"}

                return {"message": "Login successful"}

    except Exception as e:
        print(f"An error occurred during login: {e}")
        return {"message": "An error occurred", "error": str(e)}


#Salva
@app.get("/get_machines")
async def get_machines(init_date, end_date):
    try:
        # Connect to the database
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Parse the input date to a timestamp
                timestamp = datetime.strptime(init_date, "%Y-%m-%d %H:%M:%S")

                # Query to get the total number of machines
                query = """
                        select Count(*) from machines 
                    """
                cursor.execute(query)
                total_machines = cursor.fetchall()[0][0]
                print(total_machines)

                # Query to calculate the total consumption within the given date range
                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s
                """
                cursor.execute(query, (init_date, end_date, "consumption"))
                logs = cursor.fetchall()
                consumption_sum = 0
                for log in logs:
                    consumption_sum += log[0]

                # Query to calculate the total cost within the given date range
                query = """
                    Select avg from real_time_data where time >= %s and time <= %s and kpi = %s
                """
                cursor.execute(query, (init_date, end_date, "cost"))
                logs = cursor.fetchall()
                cost_sum = 0
                for log in logs:
                    cost_sum += log[0]


                # Handle cases where the sums might be NaN
                consumption_sum = 0 if math.isnan(consumption_sum) else consumption_sum
                cost_sum = 0 if math.isnan(cost_sum) else cost_sum

                # Construct a dashboard response object
                dashboard = DashboardObj(
                    totalMachines=total_machines,
                    totalConsumptionPerDay=consumption_sum,
                    totalCostPerDay=cost_sum,
                )

        # Return the dashboard data
        return {"data": dashboard}

    except Exception as e:
        # Error handling
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}

#Salva        
# Single Machine Detail
@app.get("/single_machine_detail")
def single_machine_detail(machine_id, init_date, end_date):
    try:
        # Connect to the database
        with psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Query to get the machine name using its asset_id
                query = """
                    Select name from machines where asset_id = %s
                """
                cursor.execute(query, (machine_id,))
                logs = cursor.fetchall()
                machineName = logs[0][0]

                # Query to get the machine status based on its asset_id and the given date range
                query = """
                    Select operation from real_time_data where asset_id = %s and time >= %s and time <= %s
                """
                cursor.execute(query, (machine_id, init_date, end_date))
                logs = cursor.fetchall()
                machineStatus = logs[0][0]

                # Define the date range
                datarange = [init_date, end_date]

                # Query to calculate the total consumption for the machine
                query = """
                    Select sum from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query, (init_date, end_date, "consumption", machine_id))
                logs = cursor.fetchall()
                consumption_sum = 0
                for log in logs:
                    consumption_sum += log[0]

                # Query to calculate the total cost for the machine
                query = """
                    Select avg from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query, (init_date, end_date, "cost", machine_id))
                logs = cursor.fetchall()
                cost_sum = 0
                for log in logs:
                    cost_sum += log[0]

                # Query to calculate the total power for the machine
                query = """
                    Select avg from real_time_data where time >= %s and time <= %s and kpi = %s and asset_id = %s
                """
                cursor.execute(query, (init_date, end_date, "power", machine_id))
                logs = cursor.fetchall()
                total_power = 0
                for log in logs:
                    total_power += log[0]

                # Handle cases where the sums might be NaN
                consumption_sum = 0 if math.isnan(consumption_sum) else consumption_sum
                cost_sum = 0 if math.isnan(cost_sum) else cost_sum
                total_power = 0 if math.isnan(total_power) else total_power

                # Construct and return the final response object with all the data
                single_machine_detail = SingleMachineDetail(
                    machineId=machine_id,
                    machineName=machineName,
                    machineStatus=machineStatus,
                    dataRange=datarange,
                    totalPower=total_power,
                    totalConsumption=consumption_sum,
                    totalCost=cost_sum
                )

            # Return the data for the single machine
            return {"data": single_machine_detail}

    except Exception as e:
        # Error handling
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}

# Base endpoint for accessing database

@app.get("/get_aggregated_kpi_base")
def get_aggregated_kpi_base(time_start: Optional[datetime] = None, time_end: Optional[datetime] = None):
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
    query ="SELECT * FROM aggregated_kpi"
    conditions = []
    params = []

    if time_start and time_end:
        conditions.append("begin_datetime >= %s AND end_datetime <= %s")
        params.append(time_start)
        params.append(time_end)


    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    try:
        # Establish a connection to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:

                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Get column names from the cursor description
                col_names = [desc[0] for desc in cursor.description]

                # Convert rows to a list of dictionaries
                result = [dict(zip(col_names, row)) for row in rows]

                return result

    except Exception as e:
        # Handle any errors that occur during the process and return an error message in JSON format
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while executing the query"}'
    
# Helper function to replace NaN and Inf values
def handle_nan_inf(value):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None 
    return value


@app.get("/get_real_time_data")
def get_real_time_data(request:RealTimeData):
    # SQL query template with parameterized placeholders
    start_date = request.start_date
    end_date = request.end_date
    kpi_name = request.kpi_name
    asset_id = request.asset_id
    machines = request.machines
    operations = request.operations
    column_name = request.column_name

    base_query = """
    SELECT asset_id, operation, time, min,max,sum,avg,name
    FROM real_time_data
    WHERE kpi = %s
    """
    # Initialize parameters list with kpi_name
    params = [kpi_name]
    if machines and operations:
            machine_conditions = []
            for m, o in zip(machines.split(","), operations.split(",")):
                machine_conditions.append("(name = %s AND operation = %s)")
                params.extend([m, o])  # Add the machine and operation to params list
            machine_filter = " AND (" + " OR ".join(machine_conditions) + ")"
            base_query += machine_filter

    if machines and not operations:
        machine_conditions = []
        for m in zip(machines.split(",")):
            machine_conditions.append("(name = %s)")
            params.extend(m)  # Add the machine and operation to params list
        machine_filter = " AND (" + " OR ".join(machine_conditions) + ")"
        base_query += machine_filter

    if operations and not machines:
        machine_conditions = []
        for m in zip(operations.split(",")):
            machine_conditions.append("(operation = %s)")
            params.extend(m)  # Add the machine and operation to params list
        machine_filter = " AND (" + " OR ".join(machine_conditions) + ")"
        base_query += machine_filter


    # Add time filtering
    base_query += " AND time >= %s AND time <= %s"
    params.extend([start_date, end_date])

    #Add asset_id filtering
    if asset_id:
        base_query += " AND asset_id = %s"
        params.append(asset_id)

    # Output the final query
    print("Final SQL Query:", base_query)
    print("With parameters:", params)

    try:
        # Establish a connection to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Execute the query with parameters
                cursor.execute(base_query, params)
                results = cursor.fetchall()
                return_val = []
                index  = 0
                if column_name:
                    match column_name:
                        case "min":
                            index = 3
                        case "max":
                            index = 4
                        case "sum":
                            index = 5
                        case "avg":
                            index = 6
                    for elem in results:
                        return_val.append({"asset_id":elem[0],"operation":elem[1],"time":elem[2],column_name:elem[index]})
                else:
                    for elem in results:
                        return_val.append({"asset_id":elem[0],"operation":elem[1],"time":elem[2],"min":elem[3],"max":elem[4],"sum":elem[5],"avg":elem[6],"name":elem[7]})

        return {"data": return_val}   

    except Exception as e:
        # Handle any errors that occur during the process and return an error message in JSON format
        print(f"Error while executing the query: {e}")
        return {"error": "An error occurred while executing the query"}
    
@app.get("/get_machines_base")
def get_machines_base(asset_id: Optional[str]=None):
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
            with conn.cursor() as cursor:
                # Execute the query and read the result into a DataFrame
                # Execute query and load results into DataFrame
                # Execute the query
                cursor.execute(query, (asset_id, asset_id))
                rows = cursor.fetchall()

                # Get column names from the cursor description
                col_names = [desc[0] for desc in cursor.description]

                # Convert rows to a list of dictionaries
                result = [dict(zip(col_names, row)) for row in rows]

                return result

    except Exception as e:
        # Handle any errors that occur during the process and return an error message in JSON format
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while executing the query"}'


@app.get("/get_maintenance_records_base")
def get_maintenance_records_base(
    time_start: Optional[datetime] = None, 
    time_end: Optional[datetime] = None
):
    """
    Retrieves maintenance records from the `maintenance_records` table.
    If no parameters are provided, the entire table is returned.
    
    Args:
        time_start (Optional[datetime]): Start of the time range (inclusive).
        time_end (Optional[datetime]): End of the time range (inclusive).

    Returns:
        str: A JSON-formatted string containing the maintenance records.
    """
    # Base query
    query = "SELECT * FROM maintenance_records"
    params = []

    # Add filtering conditions if time range is specified
    if time_start and time_end:
        query += " WHERE start_time >= %s AND end_time <= %s"
        params.extend([time_start, time_end])

    try:
        # Establish a connection to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Execute the query and read the result into a DataFrame
                # Execute query and load results into DataFrame
                # Execute the query
                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Get column names from the cursor description
                col_names = [desc[0] for desc in cursor.description]

                # Convert rows to a list of dictionaries
                result = [dict(zip(col_names, row)) for row in rows]
                return result

    except Exception as e:
        # Handle any errors that occur during the process and return an error message in JSON format
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while executing the query"}'
    
@app.get("/get_personal_data_base")
def get_personal_data_base(name: Optional[str] = None,
                        surname: Optional[str] = None,
                        operator_id: Optional[int] = None):
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
            with conn.cursor() as cursor:
                # Execute the query
                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Get column names from the cursor description
                col_names = [desc[0] for desc in cursor.description]

                # Convert rows to a list of dictionaries
                result = [dict(zip(col_names, row)) for row in rows]
            
                return result
    except Exception as e:
        # Handle any errors during execution
        print(f"Error while executing the query: {e}")
        return '{"error": "An error occurred while retrieving personal data"}'


@app.get("/get_production_logs_base")
def get_production_logs_base(start_time: Optional[datetime] = None, 
                        end_time: Optional[datetime] = None, 
                        asset_id: Optional[str] = None):
    """
    Retrieve records from the `production_logs` table based on optional filters.
    
    Args:
        start_time (Optional[datetime]): The start of the datetime range.
        end_time (Optional[datetime]): The end of the datetime range.
        asset_id (Optional[str]): The identifier for the asset.

    Returns:
        list: A list of dictionaries containing the retrieved records.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                # Base query
                query = "SELECT * FROM production_logs"
                conditions = []
                params = []

                # Add conditions based on provided arguments
                if start_time and end_time:
                    conditions.append("start_time >= %s AND end_time <= %s")
                    params.extend([start_time, end_time])
                if asset_id:
                    conditions.append("asset_id = %s")
                    params.append(asset_id)

                # Append WHERE clause if there are conditions
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                # Execute the query
                cursor.execute(query, params)
                rows = cursor.fetchall()

                # Get column names from the cursor description
                col_names = [desc[0] for desc in cursor.description]

                # Convert rows to a list of dictionaries
                result = [dict(zip(col_names, row)) for row in rows]
                
                return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


@app.get("/get_real_time_data_base")
def get_real_time_data_base(start_time: Optional[datetime] = None, 
                            end_time: Optional[datetime] = None, 
                            kpi: Optional[str] = None,
                            asset_id: Optional[str] = None):
    """
    Retrieve records from the `real_time_data` table based on optional filters.
    """
    try:
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        ) as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM real_time_data"
                conditions = []
                params = []

                if start_time and end_time:
                    conditions.append("time >= %s AND time <= %s")
                    params.extend([start_time, end_time])
                if kpi:
                    conditions.append("kpi = %s")
                    params.append(kpi)
                if asset_id:
                    conditions.append("asset_id = %s")
                    params.append(asset_id)

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                cursor.execute(query, params)
                rows = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]
                result = [dict(zip(col_names, row)) for row in rows]

                # Normalizza i valori problematici
                for record in result:
                    for key, value in record.items():
                        if isinstance(value, float):
                            if math.isnan(value) or math.isinf(value):
                                record[key] = None  # Sostituisci con un valore neutrale

                return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": "An error occurred", "error": str(e)}


# API prototype for the energy dashboard

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
                query = query = 
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
                query =
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
