import os
import requests
import time
import json
from colorama import init, Fore, Style
import random
from concurrent.futures import ThreadPoolExecutor, as_completed  # Add as_completed
from datetime import datetime, timedelta
import re  # Add this import

init(autoreset=True)

headers = {
    "Reqable-Id": "reqable-id-ea1b4318-bc3d-431e-9ef5-980b7da9e59d",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "accept-language": "en-US",
    "origin": "https://miniapp.yesco.in",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://miniapp.yesco.in/",
    "priority": "u=4, i"
}

def get_max_balance():
    while True:
        try:
            max_balance = float(input("Enter the maximum balance: "))
            return max_balance
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

max_balance = get_max_balance()

# Function to get random color
def get_random_color():
    colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return random.choice(colors)

# Read and parse the query.txt file
with open('query.txt', 'r') as file:
    lines = file.readlines()

authorizations = [line.strip() for line in lines]

def format_balance(balance):
    value = float(balance)
    formatted_value = "{:,.0f}".format(value).replace(",", ".")
    return formatted_value

def fetch_user_data(auth, index):
    url = 'https://clownfish-app-f7unk.ondigitalocean.app/v2/user/getInfo'
    headers['Launch-Params'] = auth
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()['payload']
        gold = format_balance(data['scoreData']['gold'])
        level = data['scoreData']['level']
        
        result = (
            f"{get_random_color()}YesWhite Akun-{index+1}{Style.RESET_ALL} | "
            f"Balance: {Fore.GREEN}{gold}{Style.RESET_ALL} | "
            f"Level: {get_random_color()}{str(level).upper()}{Style.RESET_ALL}"
        )
        
        return result
    return None

def claim_ads_reward(auth, times=10):
    url = 'https://clownfish-app-f7unk.ondigitalocean.app/v2/tasks/claimAdsgramAdReward'
    headers['Launch-Params'] = auth
    headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundaryw240bYQxKm9eX3FA'
    
    data = (
        '------WebKitFormBoundaryw240bYQxKm9eX3FA\r\n'
        'Content-Disposition: form-data; name="viewCompletedAt"\r\n\r\n'
        f'{int(time.time() * 1000)}\r\n'
        '------WebKitFormBoundaryw240bYQxKm9eX3FA\r\n'
        'Content-Disposition: form-data; name="reference"\r\n\r\n'
        '81\r\n'
        '------WebKitFormBoundaryw240bYQxKm9eX3FA--\r\n'
    )
    
    def send_request():
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'ok' and result['payload'].get('success'):
                return True
        return False

    with ThreadPoolExecutor(max_workers=times) as executor:
        futures = [executor.submit(send_request) for _ in range(times)]
        results = [future.result() for future in as_completed(futures)]
    
    return all(results)

def fetch_and_print_user_data(auth, index):
    while True:
        try:
            result = fetch_user_data(auth, index)
            if result:
                # Extract the balance from the result string
                balance_str = result.split("Balance: ")[1].split(" | ")[0].replace(Fore.GREEN, "").replace(Style.RESET_ALL, "")
                balance = float(balance_str.replace(".", "").replace(",", "."))

                if max_balance != 0 and balance >= max_balance:
                    print(Fore.YELLOW + f"Balance Akun {index + 1} {balance}, skipping inject coin.")
                    return result

                if claim_ads_reward(auth):
                    result = fetch_user_data(auth, index)
                    if result:
                        print(result)  # Print the updated balance
                return result
            else:
                return Fore.RED + f"Failed to fetch data for Akun {index + 1}"
        
        except Exception as e:
            return Fore.RED + f"Error fetching data for Akun {index + 1}: {e}"

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

print("Starting yescoin white..")  # Debug print
results_dict = {}  # Dictionary to store the latest result for each account

while True:
 
    # Use ThreadPoolExecutor to make requests concurrently
    with ThreadPoolExecutor(max_workers=len(authorizations)) as executor:
        futures = {executor.submit(fetch_and_print_user_data, auth, index): index for index, auth in enumerate(authorizations)}
        for future in as_completed(futures):
            index = futures[future]
            try:
                result = future.result()
                if result:
                    # Strip ANSI codes before extracting the account index
                    clean_result = strip_ansi_codes(result)
                    account_index = int(clean_result.split("YesWhite Akun-")[1].split(" | ")[0]) - 1
                    results_dict[account_index] = result  # Update the result for the account
            except Exception as e:
                print(Fore.RED + f"Error processing result for Akun {index + 1}: {e}")

    if results_dict:
        # Clear the previous output
        print("\033c", end="")  # ANSI escape code to clear the screen
        # Print all results at once
        for index in sorted(results_dict.keys()):
            print(results_dict[index])
    
    # time.sleep(1)  # Adjust sleep time as needed

# ... existing code ...