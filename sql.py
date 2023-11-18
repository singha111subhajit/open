import pyodbc

def execute_sql_script(server, database, username, password, script_path, output_file_path):
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

        # Split the script into individual statements
        sql_statements = [statement.strip() for statement in sql_script.split(";")]

        for statement in sql_statements:
            if statement:
                # Execute each statement
                cursor.execute(statement)

                # Check if the statement is a SELECT query
                if cursor.description is not None:
                    # Fetch all rows and store the results in a list
                    rows = cursor.fetchall()

                    # Write the results to a text file
                    with open(output_file_path, 'a') as output_file:
                        for row in rows:
                            output_file.write(str(row) + '\n')

        print(f"SQL script executed successfully! Results written to: {output_file_path}")

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
script_path = '/home/subhajit/Desktop/open/sql_1.sql'
output_file_path = '/home/subhajit/Desktop/open/sql_script_results.txt'

execute_sql_script(server, database, username, password, script_path, output_file_path)
