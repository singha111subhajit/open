import pyodbc
import csv
import sqlparse
import chardet
from datetime import datetime
import zipfile
import os

class NoQuoteCsvWriter:
    def __init__(self, csv_file, delimiter='|'):
        self.csv_file = csv_file
        self.delimiter = delimiter

    def writerow(self, row):
        row_str = self.delimiter.join([str(value) for value in row])
        self.csv_file.write(row_str + '\n')

def clean_files(dir):
    # delete all files from the specific dir
    print("*"*76)
    for file in [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]:
        os.remove(file)
        print("delete file: ", file)
    print("*"*76)

def execute_sql_scripts_in_order(driver, server, database, username, password, list_file_path, sql_dir, output_directory):
    # executing sql statements and copy the output if available and write in a .csv file with the right format
    # and then create a .zip of that .csv file
    print("*"*76)
    conn = None
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        cursor = conn.cursor()
        with open(list_file_path, 'r') as list_file:
            sql_scripts = list_file.read().splitlines()
        current_datetime = datetime.now()
        date_string = current_datetime.strftime('%Y%m%d')
        time_string = current_datetime.strftime('%H%M%S')
        for script_name in sql_scripts:
            script_path = os.path.join(sql_dir, script_name)
            sql_file_name = os.path.splitext(script_name)[0]
            csv_file_name = f'{sql_file_name}{date_string}{time_string}.csv'
            csv_file_path = os.path.join(output_directory, csv_file_name)

            with open(csv_file_path, 'w', newline='') as csv_file:
                csv_writer = None
                with open(script_path, 'rb') as script_file:
                    result = chardet.detect(script_file.read())
                    encoding = result['encoding']
                with open(script_path, 'r', encoding=encoding) as script_file:
                    sql_script = script_file.read()
                parsed_script = sqlparse.split(sql_script)
                for statement in parsed_script:
                    if not statement.strip():
                        continue
                    cursor.execute(statement)
                    if cursor.description is not None:
                        column_names = [column[0] for column in cursor.description]
                        if not csv_writer:
                            csv_writer = NoQuoteCsvWriter(csv_file, delimiter='|')
                            csv_writer.writerow(column_names)
                        rows = cursor.fetchall()
                        for row in rows:
                            formatted_row = [value.strftime('%Y-%m-%d %H:%M:%S.%f').rstrip('0').rstrip('.')
                                             if isinstance(value, datetime) else value for value in row]
                            csv_writer.writerow(formatted_row)

            print(f"SQL Script '{sql_file_name}' Executed Successfully! Results Written To {csv_file_path}")
            zip_file_name = f'{output_directory}\{sql_file_name}{date_string}{time_string}.zip'
            with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(csv_file_path, arcname=f'{sql_file_name}{date_string}{time_string}.csv')
            print(f"CSV file '{csv_file_name}' Compressed To {zip_file_name}")
            os.remove(csv_file_path)
    except pyodbc.Error as e:
        print(f"Error Executing SQL Scripts: {e}")
    except Exception as ex:
        print(f"An Unexpected Error Occurred: {ex}")
    finally:
        if conn:
            conn.close()
    print("*"*76)