import requests
from bs4 import BeautifulSoup
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

def scrape_doctor_details(session, nmc_no):
    start_time = time.time()  # Record start time
    url = f'https://www.nmc.org.np/searchPractitioner?name=&nmc_no={nmc_no}&degree='
    response = session.get(url)
    
    if response.status_code != 200:
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    details = {}
    try:
        table = soup.find('table', {'class': 'table table-bordered table-result'})
        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    key = columns[0].text.replace(':', '').strip().lower().replace(' ', '_')
                    value = columns[1].text.strip()
                    if key in ['full_name', 'nmc_no', 'address', 'gender', 'degree', 'remarks']:
                        details[key] = value
    except AttributeError:
        return None, None
    
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    return details, elapsed_time

def main():
    doctors_list = Queue()
    total_start_time = time.time()  # Record overall start time

    def worker(session, nmc_no):
        try:
            details, elapsed_time = scrape_doctor_details(session, nmc_no)
            if details:
                # Commented out the print statement
                # print(f'NMC No: {details.get("nmc_no")}, Details: {details}, Time Taken: {elapsed_time:.2f} seconds')
                doctors_list.put(details)
            else:
                # Commented out the print statement
                # print(f'NMC No: {nmc_no}, No Details Found, Time Taken: {elapsed_time:.2f} seconds')
                pass
        except Exception as e:
            # Commented out the print statement
            # print(f'Error with NMC No: {nmc_no}, {str(e)}')
            pass

    with ThreadPoolExecutor(max_workers=12) as executor, requests.Session() as session:
        futures = [executor.submit(worker, session, nmc_no) for nmc_no in range(1, 36362)]
        for future in as_completed(futures):
            future.result()  # Wait for the thread to complete

    # Collect all items from the queue
    results = []
    while not doctors_list.empty():
        results.append(doctors_list.get())

    # Sort the list by nmc_no
    results.sort(key=lambda x: int(x['nmc_no']))

    os.makedirs('../data', exist_ok=True)
    with open('../data/doctors_details.json', 'w') as f:
        json.dump(results, f, indent=4)

    total_end_time = time.time()  # Record overall end time
    total_elapsed_time = total_end_time - total_start_time  # Calculate overall elapsed time

    # Commented out the print statement
    print('Scraping completed and data saved to data/doctors_details.json')
    print(f'Overall Time Taken: {total_elapsed_time:.2f} seconds')

if __name__ == "__main__":
    main()
