import pyodbc, sqlparse, chardet, zipfile, os, ftplib, time, shutil, string
from datetime import datetime
from collections import Counter


class MyCsvWriter:
    def __init__(self, csv_file, delimiter='|'):
        self.csv_file = csv_file
        self.delimiter = delimiter

    def format_value(self, value):
        if value is None:
            return 'null'
        elif isinstance(value, datetime):
            formatted_value = value.strftime('%Y-%m-%d %H:%M:%S')
            microsecond = value.microsecond
            if microsecond:
                formatted_value += f'.{microsecond:06d}'.rstrip('0')
            else:
                formatted_value += '.0'
            return formatted_value
        elif isinstance(value, str):
            # Replace double backslashes with a placeholder
            value = value.replace('\\\\', '<DOUBLE_BACKSLASH_PLACEHOLDER>')

            # Replace single backslashes with a different placeholder
            value = value.replace('\\', '<SINGLE_BACKSLASH_PLACEHOLDER>')

            # Replace the placeholders back
            value = value.replace('<DOUBLE_BACKSLASH_PLACEHOLDER>', '\\\\').replace('<SINGLE_BACKSLASH_PLACEHOLDER>', '\\')

            return value
        else:
            return str(value).replace('"""', '"')

    def writerow(self, row):
        row_str = self.delimiter.join([self.format_value(value) for value in row])
        self.csv_file.write(row_str + '\n')

# ... (rest of your code remains unchanged)

def main():
    start_time = datetime.now()
    backup_response = backup(output_directory, arc_dir)
    if backup_response:
        print(backup_response)
        return
    execute_sql_scripts_in_order(driver, server, database, username, password, list_file_path, sql_dir,
                                  local_output_directory, output_directory, special_char)
    send_ftp(path_sqllog=output_directory)
    clean_files(arc_dir, ".zip", 30)
    print("total time required to run:", datetime.now() - start_time)

if __name__ == "__main__":
    main()
