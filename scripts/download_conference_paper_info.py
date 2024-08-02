import json
import os
import urllib3
import requests
import logging

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG) 
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('download_conference.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)



def process_conference_page(pub_number, page, get_page_number=False, retry=10):
    logger.info("Process Pubnumber {} page {} getnumber {}".format(pub_number, page, get_page_number))
    if get_page_number:
        assert page == 1
    
    data = {
            "newsearch": 'true',
            "highlight": 'true',
            'matchBoolean': 'true',
            'matchPubs': 'true',
            'action': 'search',
            "queryText": "(\"Publication Number\":{})".format(pub_number),
            "pageNumber": str(page),
            "rowsPerPage": 100,
    }

    headers = {
    'Accept': 'application/json,text/plain,*/*',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '147',
    'Content-Type': 'application/json',
    'Referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                    'Safari/537.36 Edg/108.0.1462.46',
    }

    url = 'https://ieeexplore.ieee.org/rest/search'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    for attempt in range(retry): 
        try:
            res = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False)
            res.raise_for_status()

            try:
                dic_obj = res.json()

                if get_page_number:
                    num_of_pages = dic_obj['totalPages']
                    return num_of_pages
                
                else:
                    if 'records' not in dic_obj:
                        logger.error("no records in publicationnumber {} page {}".format(pub_number, page))
                        return
                    if len(dic_obj['records']) != 0:
                        year = dic_obj['records'][0]['publicationYear']
                    else:
                        logger.error("empty record in publicationnumber {} page {}".format(pub_number, page))

                    path = os.path.join('./tmp/download_source_json_conference', str(pub_number), str(year))
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(os.path.join(path, '{}.json'.format(page)), 'w', encoding='utf-8') as f:
                        json.dump(dic_obj, f, ensure_ascii=False, indent=4)
                    logger.info(f"Pubnumber {pub_number} Year {year} Page {page} fetched successfully.")
                    return

            except json.JSONDecodeError:
                logger.warning(f"JSON decode error on Pubnumber {pub_number} page {page}, attempt {attempt+1} of {retry}. Retrying...")
                
        
        except requests.RequestException as e:
            logger.warning(f"Request error on Pubnumber {pub_number} page {page}, attempt {attempt+1} of {retry}: {e}. Retrying...")

    
    logger.error(f"Failed to fetch Pubnumber {pub_number}  page {page} after {retry} attempts.")

    

 
with open ('./tmp/all_conferences.json', 'r', encoding='utf-8') as fr:    
    all_conferences = json.load(fr)
    for pub_number, entry in all_conferences.items():
        num_of_page = process_conference_page(pub_number, page=1, get_page_number=True)
        for page in range (1, num_of_page+1):
            process_conference_page(pub_number, page=page, get_page_number=False)
