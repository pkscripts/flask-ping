import subprocess
import json
from datetime import datetime


def ping_ip(ip_address):
    try:
        response = subprocess.run(["ping", "-n", "2", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)       
        if "100% loss" in str(response.stdout):
            return "Failed"
        elif "100% loss" not in str(response.stdout):
            return "Success"
        else:
            return "Failed"
    except Exception as err: 
        print(ip_address + ": " + str(err))
        return "Failed"


def update_json(ip_address, status, timestamp):
    try:
        with open('ping_results.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
        with open('ping_results.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    if ip_address in data.keys() and data[ip_address]['status'] == status:
       timestamp = data[ip_address]['timestamp']
       
    try:
        data[ip_address] = {'status': status, 'timestamp': timestamp}
        with open('ping_results.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except:
        pass

def main():
    with open('ip_list.json', 'r') as json_file:
        data = json.load(json_file)

    ip_addresses = [ip for ip in data]
    for ip_address in ip_addresses:
        timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        status = ping_ip(ip_address)
        update_json(ip_address, status, timestamp)


if __name__ == '__main__':
   main()
