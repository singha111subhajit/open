import pyodbc
import csv
import sqlparse
import chardet

def execute_sql_script(server, database, username, password, script_path, output_csv_path):
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

        # Create a cursor
        cursor = conn.cursor()

        # Detect encoding of the SQL script
        with open(script_path, 'rb') as script_file:
            result = chardet.detect(script_file.read())
            encoding = result['encoding']

        # Read the SQL script from the file with detected encoding
        with open(script_path, 'r', encoding=encoding) as script_file:
            sql_script = script_file.read()

        # Use sqlparse to split the script into individual statements
        parsed_script = sqlparse.split(sql_script)

        # Open a CSV file for writing
        with open(output_csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Execute each statement
            for statement in parsed_script:
                # Skip empty statements
                if not statement.strip():
                    continue
                
                # Execute the statement
                cursor.execute(statement)

                # Check if the statement is a SELECT query
                if cursor.description is not None:
                    # Fetch column names
                    column_names = [column[0] for column in cursor.description]

                    # Write column names to CSV
                    csv_writer.writerow(column_names)

                    # Fetch all rows and write to CSV
                    rows = cursor.fetchall()
                    for row in rows:
                        csv_writer.writerow(row)

        print(f"SQL script executed successfully! Results written to {output_csv_path}")

    except pyodbc.Error as e:
        print(f"Error executing SQL script: {e}")

    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

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
output_csv_path = '/home/subhajit/Desktop/open/sql_output.csv'

execute_sql_script(server, database, username, password, script_path, output_csv_path)
