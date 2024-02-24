import requests

# Set the server's address and port
server_address = 'http://192.168.0.104:8080'

# Ask the user what operation they want to perform
print("Do you want to download or upload a file?")
operation = input("Enter 'download' or 'upload': ").strip().lower()

if operation == 'download':
    # Specify the file you want to download
    file_name = input("Enter the name of the file you want to download: ")
    # Send a GET request to the server to download the file
    response = requests.get(f'{server_address}/{file_name}')
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File {file_name} downloaded successfully.")
    else:
        print(f"Failed to download file {file_name}. Status code: {response.status_code}")

elif operation == 'upload':
    # Specify the file you want to upload
    file_name = input("Enter the name of the file you want to upload: ")
    # Open the file in binary mode
    with open(file_name, 'rb') as file:
        file_content = file.read()
        # Prepare the headers with the file name
        headers = {'Filename': file_name}
        # Send a POST request to the server to upload the file
        # The file's binary content is sent directly in the data parameter
        response = requests.post(server_address, data=file_content, headers=headers)
    if response.status_code == 200:
        print(f"File {file_name} uploaded successfully.")
    else:
        print(f"Failed to upload file {file_name}. Status code: {response.status_code}")
else:
    print("Invalid operation. Please enter 'download' or 'upload'.")