import requests
import json
import time
import urllib3
import os


def fetch_data(year, page, get_total_page=False, retry=10):

    if get_total_page is True:
        assert page == 1

    data = {
            "contentType": "periodicals",
            "tabId": "title",
            "ranges": ["{}_{}_Year".format(year, year)],
            "pageNumber": page
    }

    headers = {
        'Accept': 'application/json,text/plain,*/*',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '147',
        'Content-Type': 'application/json',
        'Referer': 'https://ieeexplore.ieee.org/browse/periodicals/title',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                        'Safari/537.36 Edg/108.0.1462.46',
    }

    url = 'https://ieeexplore.ieee.org/rest/publication'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    for attempt in range(retry): 
        try:
            res = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
            res.raise_for_status()

            try:
                dic_obj = res.json()
                if not get_total_page:
                    num_of_journal = dic_obj['totalRecords']
                    json_dir = f'./tmp/json_journal_year/{year}'
                    if not os.path.exists(json_dir):
                        os.system("mkdir -p {}".format(json_dir))
                    with open(os.path.join(json_dir, "{}.json".format(page)), 'w', encoding='utf-8') as f:
                        json.dump(dic_obj, f, ensure_ascii=False, indent=4)
                    print(f"Year {year} fetched successfully.")
                    return num_of_journal
                
                else:
                    num_of_page = dic_obj['totalPages']
                    return num_of_page


            except json.JSONDecodeError:
                print(f"JSON decode error on year {year}, attempt {attempt+1} of {retry}. Retrying...")
        
        except requests.RequestException as e:
            print(f"Request error on page {year}, attempt {attempt+1} of {retry}: {e}. Retrying...")

        
    print(f"Failed to fetch page {year} after {retry} attempts.")


if __name__ == "__main__":

    year_journal = []

    for year in range (1884, 2025):

        num_of_page_this_year = fetch_data(year, page=1, get_total_page=True)

        for page in range (1, num_of_page_this_year+1):
            num_of_journal = fetch_data(year, page=page, get_total_page=False)
            year_journal.append(num_of_journal)
            time.sleep(1)

    