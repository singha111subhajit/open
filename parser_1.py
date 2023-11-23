import pyodbc
import csv
import sqlparse
import chardet
from datetime import datetime
import zipfile
import os

def execute_sql_scripts_in_order(server, database, username, password, list_file_path, sql_dir, output_directory):
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

        # Read the list of SQL scripts from the file
        with open(list_file_path, 'r') as list_file:
            sql_scripts = list_file.read().splitlines()

        # Get the current date and time for creating unique ZIP file names
        current_datetime = datetime.now()
        date_string = current_datetime.strftime('%Y%m%d')
        time_string = current_datetime.strftime('%H%M%S')

        # Execute each script in the specified order
        for script_name in sql_scripts:
            # Build the full path to the SQL script
            script_path = os.path.join(sql_dir, script_name)

            # Get the base name of the SQL file without extension
            sql_file_name = os.path.splitext(script_name)[0]

            # Generate the CSV file name with the specified format
            csv_file_name = f'{sql_file_name}-{date_string}-{time_string}.csv'
            csv_file_path = os.path.join(output_directory, csv_file_name)

            # Open a CSV file for writing
            with open(csv_file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                # Detect encoding of the SQL script
                with open(script_path, 'rb') as script_file:
                    result = chardet.detect(script_file.read())
                    encoding = result['encoding']

                # Read the SQL script from the file with detected encoding
                with open(script_path, 'r', encoding=encoding) as script_file:
                    sql_script = script_file.read()

                # Use sqlparse to split the script into individual statements
                parsed_script = sqlparse.split(sql_script)

                # Execute each statement in the script
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

                        # Write column names to CSV (only for the first script)
                        if not csv_writer:
                            csv_writer.writerow(column_names)

                        # Fetch all rows and write to CSV
                        rows = cursor.fetchall()
                        for row in rows:
                            csv_writer.writerow(row)

            print(f"SQL script '{sql_file_name}' executed successfully! Results written to {csv_file_path}")

            # Create a ZIP file with the same base name as the CSV file
            zip_file_name = f'{output_directory}/{sql_file_name}-{date_string}-{time_string}.zip'
            with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
                # Add the CSV file to the ZIP file
                zip_file.write(csv_file_path, arcname=f'{sql_file_name}-{date_string}-{time_string}.csv')

            print(f"CSV file '{csv_file_name}' compressed to {zip_file_name}")

            # Remove the original CSV file after compressing to ZIP
            os.remove(csv_file_path)

    except pyodbc.Error as e:
        print(f"Error executing SQL scripts: {e}")

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
list_file_path = '/home/subhajit/Desktop/open/list_sql.txt'
sql_dir = '/home/subhajit/Desktop/open/sql_files'
output_directory = '/home/subhajit/Desktop/open/output'
execute_sql_scripts_in_order(server, database, username, password, list_file_path, sql_dir, output_directory)
