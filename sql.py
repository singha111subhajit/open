import pyodbc

def execute_sql_script(server, database, username, password, script_path):
    conn = None
    try:
        # Connect to the SQL Server
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        cursor = conn.cursor()

        # Read the SQL script from the file
        with open(script_path, 'r') as script_file:
            sql_script = script_file.read()

        # Execute the SQL script
        cursor.execute(sql_script)

        # Commit the changes
        conn.commit()

        print("SQL script executed successfully!")

        # Select all values from TestTable
        select_query = "SELECT * FROM TestTable"
        cursor.execute(select_query)
        
        # Fetch all rows and print the results
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except pyodbc.Error as e:
        print(f"Error executing SQL script: {e}")

    finally:
        # Close the connection
        if conn:
            conn.close()

# Example usage
server = 'localhost,1433'
database = 'master'  # Replace with your actual database name
username = 'sa'
password = 'YourPassword123!'  # Replace with your actual password
script_path = '/home/subhajit/Desktop/paramount/test_script.sql'

execute_sql_script(server, database, username, password, script_path)
