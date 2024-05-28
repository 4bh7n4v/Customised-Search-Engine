import os
import getpass
from googleapiclient.discovery import build
from cryptography.fernet import Fernet

def generate_encryption_key():
    return Fernet.generate_key()

def encrypt_message(message, encryption_key):
    fernet = Fernet(encryption_key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, encryption_key):
    fernet = Fernet(encryption_key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

def store_credentials(api_key, search_engine_id, encryption_key):
    encrypted_api_key = encrypt_message(api_key, encryption_key)
    encrypted_search_engine_id = encrypt_message(search_engine_id, encryption_key)
    with open('encrypted_credentials.txt', 'wb') as file:
        file.write(encryption_key + b'\n')
        file.write(encrypted_api_key + b'\n')
        file.write(encrypted_search_engine_id + b'\n')

def read_encrypted_credentials():
    with open('encrypted_credentials.txt', 'rb') as file:
        encryption_key = file.readline().strip()
        encrypted_api_key = file.readline().strip()
        encrypted_search_engine_id = file.readline().strip()
    return encryption_key, encrypted_api_key, encrypted_search_engine_id

def Search(search_query, api_key, search_engine_id):
    service = build("customsearch", "v1", developerKey=api_key)
    search_results = service.cse().list(q=search_query, cx=search_engine_id).execute()
    return search_results

def main():
    if not os.path.exists('encrypted_credentials.txt'):
        print("enter your API key and search engine ID.")
        api_key = getpass.getpass('Enter Your API Key: ')
        search_engine_id = getpass.getpass('Enter Your Search Engine ID: ')
        encryption_key = generate_encryption_key()
        store_credentials(api_key, search_engine_id, encryption_key)

    encryption_key, encrypted_api_key, encrypted_search_engine_id = read_encrypted_credentials()

    api_key = decrypt_message(encrypted_api_key, encryption_key)
    search_engine_id = decrypt_message(encrypted_search_engine_id, encryption_key)

    search_query = input("Enter the choice you want Search")
    search_results = Search(search_query, api_key, search_engine_id)

    if 'items' in search_results:
        for item in search_results['items']:
            print(f"Title: {item.get('title')}")
            print(f"Link: {item.get('link')}")
            print(f"Snippet: {item.get('snippet')}\n")
    else:
        print("No results found.")

    with open('search_results.txt', 'w', encoding='utf-8') as file:
        if 'items' in search_results:
            for item in search_results['items']:
                file.write(f"Title: {item.get('title')}\n")
                file.write(f"Link: {item.get('link')}\n")
                file.write(f"Snippet: {item.get('snippet')}\n\n")
        else:
            file.write("No results found.\n")

if __name__ == "__main__":
    main()
