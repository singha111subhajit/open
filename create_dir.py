import os

def create_directory(directory_name):
    try:
        # Get the current working directory
        current_directory = os.getcwd()

        # Specify the full path of the directory
        full_path = os.path.join(current_directory, directory_name)

        # Check if the directory already exists
        if not os.path.exists(full_path):
            # Create the directory
            os.makedirs(full_path)
            print(f"Directory '{directory_name}' created successfully at: {full_path}")
        else:
            print(f"Directory '{directory_name}' already exists at: {full_path}")

        # Return the full path
        return full_path
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the directory name you want to create
directory_to_create = "SSTS-451"

# Call the function to create the directory and get the full path
directory_path = create_directory(directory_to_create)

# Print the full path
print("Full Path:", directory_path)
