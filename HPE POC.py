pip install requests

# COMMAND ----------

# Add databses to config file

# COMMAND ----------

import json
import requests
import base64

def prompt_user_for_database():
    db_name = input("Enter the name of the new database: ").strip()
    url = input("Enter the URL of the new database: ").strip()
    format_type = input("Enter the format (json/csv) of the new database: ").strip().lower()

    if format_type not in ["json", "csv"]:
        print("Invalid format type. Please choose 'json' or 'csv'.")
        return None

    return db_name, url, format_type

def update_config_file(repo_url, file_path, new_database_info, github_token):
    try:
        raw_url = f"{repo_url}/contents/{file_path}"

        response = requests.get(raw_url, headers={"Authorization": f"token {github_token}"})
        response.raise_for_status() 
        config = json.loads(base64.b64decode(response.json()["content"]).decode("utf-8"))

        db_name, url, format_type = new_database_info
        config["databases"][db_name] = {"url": url, "format": format_type}

        updated_config_content = json.dumps(config, indent=4)

        update_url = f"{repo_url}/contents/{file_path}"

        payload = {
            "message": "Update configuration file",
            "content": base64.b64encode(updated_config_content.encode("utf-8")).decode("utf-8"),
            "sha": response.json()["sha"]  
        }

        response = requests.put(update_url, headers={"Authorization": f"token {github_token}"}, json=payload)
        response.raise_for_status()
        print(f"Configuration file updated successfully with the new database: {db_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

def main():
    github_repo_url = #insert configuration file link- i was using my own github kindly create and host a new file
    config_file_path = "Configurationfile.json"
    github_token = #generate and paste token string for accessing the github hosted file publicly
    new_database_info = prompt_user_for_database()
    if new_database_info is None:
        return

    #https://github.com/CVEProject/cvelistV5/archive/refs/heads/main.zip
    update_config_file(github_repo_url, config_file_path, new_database_info, github_token)

if __name__ == "__main__":
    main()


# COMMAND ----------

#  Access databases from config file

# COMMAND ----------

import requests
import json
import csv
import gzip
import io
from io import StringIO

def load_configuration_from_github(repo_url, file_path):
    try:
        raw_url = f"{repo_url.rstrip('/')}/raw/main/{file_path.lstrip('/')}"
        response = requests.get(raw_url)
        response.raise_for_status()
        config = json.loads(response.text)
        return config
    except requests.exceptions.RequestException as e:
        print(f"Error accessing configuration file: {e}")
        return None

def fetch_nvd_data(url_template):
    try:
        year = input("Enter the year (e.g., 2022) for NVD data: ").strip()
        url = url_template.format(year=year)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gzip_file:
            json_data = json.load(gzip_file)
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def fetch_cve_data(url_template):
    try:
        url = url_template
        response = requests.get(url)
        response.raise_for_status()  
        csv_data = response.text
        return csv_data

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def main():
    github_repo_url = #insert your own config file link access
    config_file_path = "Configurationfile.json"
    config = load_configuration_from_github(github_repo_url, config_file_path)

    if config is not None:
        databases = config.get('databases', {})
        print("Available Databases:")
        for db_name in databases:
            print(f"- {db_name}")
        
        selected_db = input("Enter the name of the database to fetch data from: ").strip()
        if selected_db in databases:
            db_info = databases[selected_db]
            url_template = db_info['url']
            format_type = db_info['format']
            #print(url_template)
            if format_type == "json":
                if selected_db == "NVD":
                    data = fetch_nvd_data(url_template)
                else:
                    data = fetch_cve_data(url_template)
            elif format_type == "csv":
                data = fetch_cve_data(url_template)

            if data is not None:
                if format_type == "json":
                    if selected_db == "NVD":
                        num_entries = len(data['CVE_Items'])
                        print(f"Total number of entries for {selected_db} in {year}: {num_entries}")
                        for i, vulnerability in enumerate(data.get('CVE_Items', []), start=1):
                            cve_id = vulnerability['cve']['CVE_data_meta']['ID']
                            description = vulnerability['cve']['description']['description_data'][0]['value']
                            print(f"\nVulnerability {i} (CVE-ID: {cve_id}):")
                            print(f"Description: {description}")
                elif format_type == "csv":
                    reader = csv.reader(StringIO(data))
                    next(reader)  
                    for i, row in enumerate(reader, start=1):
                        cve_id = row[0]  
                        description = row[2]
                        print(f"\nVulnerability {i} (CVE-ID: {cve_id}):")
                        print(f"Description: {description}")
            else:
                print(f"No data fetched for {selected_db}")
        else:
            print("Invalid database selected. Please choose from the available options.")
    else:
        print("Failed to load configuration from GitHub.")

if __name__ == "__main__":
    main()


# COMMAND ----------

# The GHSA Databse code

# COMMAND ----------

import requests
import json
import csv
import gzip
import io
from io import StringIO

def load_configuration_from_github(repo_url, file_path):
    try:
        raw_url = f"{repo_url.rstrip('/')}/raw/main/{file_path.lstrip('/')}"
        response = requests.get(raw_url)
        response.raise_for_status()
        config = json.loads(response.text)
        return config
    except requests.exceptions.RequestException as e:
        print(f"Error accessing configuration file: {e}")
        return None

def fetch_vulners_data(vulnerability_id):
    url = f"https://vulners.com/api/v3/search/id/?id={vulnerability_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()  
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
def extract_vulnerability_info(data, vulnerability_id ):
    if data is not None and data.get('result') == 'OK':
        v1 = data.get('data', [])
        v2=v1.get('documents', [])
        v3=v2.get(vulnerability_id, [])
        print(f"ID: {v3.get('id', [])}")
        print(f"Type: {v3.get('type', [])}")
        print(f"BulletinFamily: {v3.get('bulletinFamily', [])}")
        print(f"Title: {v3.get('title', [])}")
        print(f"Description: {v3.get('description', [])}")
           
    else:
        print("No valid data or unsuccessful API response.")
def fetch_json_data(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gzip_file:
            json_data = json.load(gzip_file)
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def fetch_csv_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        csv_data = response.text
        return csv_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def main():
    github_repo_url = #insert configuration file link- i was using my own github kindly create and host a new file
    config_file_path = "Configurationfile.json"
    config = load_configuration_from_github(github_repo_url, config_file_path)

    if config is not None:
        databases = config.get('databases', {})
        print("Available Databases:")
        for db_name in databases:
            print(f"- {db_name}")
        
        selected_db = input("Enter the name of the database to fetch data from: ").strip()
        if selected_db in databases:
            db_info = databases[selected_db]
            url = db_info['url']
            print(url)
            format_type = db_info['format']
            
            if format_type == "json" and selected_db == "NVD":
                data = fetch_json_data(url)
            elif format_type == "csv":
                data = fetch_csv_data(url)
            if selected_db == "Vulners": 
                vulnerability_id = input("Enter the vulnerability ID (e.g., WOLFI:GHSA-JQ35-85CJ-FJ4P): ").strip()
                url = f"https://vulners.com/api/v3/search/id/?id={vulnerability_id}"
                data = fetch_vulners_data(vulnerability_id)
                extract_vulnerability_info(data, vulnerability_id)
            

            elif data is not None:
                
                if format_type == "json":
                    num_entries = len(data['CVE_Items'])
                    print(f"Processing {selected_db} JSON data...")
                    print(f"Total number of entries for {selected_db} in 2023 : {num_entries}")
                    for i, vulnerability in enumerate(data.get('CVE_Items', []), start=1):
                        cve_id = vulnerability['cve']['CVE_data_meta']['ID']
                        description = vulnerability['cve']['description']['description_data'][0]['value']
                        print(f"\nVulnerability {i} (CVE-ID: {cve_id}):")
                        print(f"Description: {description}")
                elif format_type == "csv":
                    
                    print(f"Processing {selected_db} CSV data...")
                    
                    reader = csv.reader(StringIO(data))
                    next(reader)  
                    for i, row in enumerate(reader, start=1):
                        cve_id = row[0]  
                        description = row[2]
                        print(f"\nVulnerability {i} (CVE-ID: {cve_id}):")
                        print(f"Description: {description}")
                    
            else:
                print(f"No data fetched for {selected_db}")
        else:
            print("Invalid database selected. Please choose from the available options.")
    else:
        print("Failed to load configuration ")

if __name__ == "__main__":
    main()
    #WOLFI:GHSA-2C7C-3MJ9-8FQH
    #WOLFI:GHSA-JQ35-85CJ-FJ4P


# COMMAND ----------


