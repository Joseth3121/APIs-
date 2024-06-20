import json
import requests
import os
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def formar_json():
    dict_data = {
        'switches': [
            {"model1": 'CAT3750', "model2": 'CAT3760'}
        ],
        'routers': {
            'name': 'CSR100V',
            'vendor': 'cisco',
            'type': 'hardware'
        }
    }

    # Imprimir JSON en formato legible
    print(json.dumps(dict_data, indent=4, sort_keys=True))

    # Guardar el JSON en un archivo
    with open("./Data/switches.json", 'w') as file:
        json.dump(dict_data, file, indent=4, sort_keys=True)

def infraestructura_json():
    network_dict = {
        'servers': [
            {"server1": {'name': 'srv1', 'os': 'manjaro', 'services': ['ftp', 'ssh']}},
            {"server2": {'name': 'srv2', 'os': 'manjaro', 'services': ['http', 'sftp']}}
        ]
    }

    # Imprimir JSON en formato legible
    print(json.dumps(network_dict, indent=4, sort_keys=True))

    # Guardar el JSON en un archivo
    with open("./Data/intraestructura.json", 'w') as file:
        json.dump(network_dict, file, indent=4, sort_keys=True)

def get_api_ips():
    urls = [
        'http://ip-api.com/json/8.8.8.8',
        'http://ip-api.com/json/24.48.0.1?fields=message,timezone,isp',
        'http://ip-api.com/json/1.1.1.1?fields=status,country,regionName,lat,as'
    ]

    responses = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            responses.append(response.json())
        else:
            print(f"Failed to get data from {url}")

    # Imprimir respuestas en formato legible
    for response in responses:
        print(json.dumps(response, indent=4, sort_keys=True))

    # Guardar respuestas en un archivo JSON
    with open("./Data/api_responses.json", 'w') as file:
        json.dump(responses, file, indent=4, sort_keys=True)

def get_meraki_network_devices(api_key):
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Imprimir la respuesta en formato legible
        response_json = response.json()
        print(json.dumps(response_json, indent=4, sort_keys=True))

        # Guardar la respuesta en un archivo JSON
        with open("./Data/meraki_devices.json", 'w') as file:
            json.dump(response_json, file, indent=4, sort_keys=True)
        print("Data saved to ./Data/meraki_devices.json")
    else:
        print(f"Failed to get Meraki data, status code {response.status_code}")

if __name__ == '__main__':
    formar_json()
    infraestructura_json()
    get_api_ips()

    #API key de Meraki desde devnet , reemplaza con tu propia API key
    meraki_api_key = "75dd5334bef4d2bc96f26138c163c0a3fa0b5ca6"
    get_meraki_network_devices(meraki_api_key)
