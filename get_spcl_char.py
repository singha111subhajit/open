from collections import Counter
import string
import os

def most_used_special_character(file_path):
    try:
        with open(file_path, 'r') as file:
            file_names = file.readlines()
            all_file_names = ''.join(file_names)
            for name in file_names:
                _, ext = os.path.splitext(name.strip())
                if ext:
                    all_file_names = all_file_names.replace(ext, '')
            char_count = Counter(all_file_names)
            special_chars = [char for char in string.punctuation if char_count[char] > 0]
            if special_chars:
                most_used_char = max(special_chars, key=lambda char: char_count[char])
                return most_used_char
            else:
                print("No Special Characters Found In File Names.")
                return

    except FileNotFoundError:
        return "File Not Found."

# Example usage
file_path = 'sql.list'
result = most_used_special_character(file_path)
print(f"Most used special character: {result}")

