import os 
import json
import logging

def parse_years(years):
    if ' - ' in years:
        start_year, end_year = years.split(' - ')
        return start_year.strip(), end_year.strip()
    return years.strip(), 'Present'


JOURNAL = 0

if JOURNAL:
    #### Process Journals ####
    all_journals = {}
    for year in range (1884, 2025):
        print (year)
        for root, dirs, names in os.walk(os.path.join('./tmp/json_journal_year', '{}'.format(year))):
            for name in names:
                json_path = os.path.join(root, name)
                with open(json_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for record in data.get('records', []):
                        title = record.get('title')
                        all_years = record.get('allYears', '')
                        publication_number = record.get('publicationNumber')
                        
                        if publication_number and publication_number not in all_journals:
                            start_year, end_year = parse_years(all_years)
                            
                            all_journals[publication_number] = {
                                'title': title,
                                'start_year': start_year,
                                'end_year': end_year,
                                'publication_number': publication_number
                            }

                        # Process title history
                        for history in record.get('titleHistory', []):
                            history_title = history.get('displayTitle')
                            start_year = history.get('startYear')
                            end_year = history.get('endYear')
                            history_publication_number = history.get('publicationNumber')
                            if history_publication_number and history_publication_number not in all_journals:
                                all_journals[history_publication_number] = {
                                    'title': history_title,
                                    'start_year': start_year,
                                    'end_year': end_year,
                                    'publication_number': history_publication_number
                                }


    with open ("./tmp/all_journals.json", 'w') as f:
        json.dump(all_journals, f, indent=4)



else:

    all_conferences = {}
    #### Process Conference ####
    for year in range (1884, 2025):
        for root, dirs, names in os.walk(os.path.join('./tmp/json_conference_year', '{}'.format(year))):
            for name in names:
                json_path = os.path.join(root, name)
                with open(json_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for record in data.get('records', []):
                        if "titleHistory" in record:
                            for each_history in record["titleHistory"]:
                                _this_pub_number = each_history["publicationNumber"]
                                _this_pub_title = each_history["displayTitle"]
                                all_conferences[_this_pub_number] = _this_pub_title
                        else:
                            _this_pub_number = record["publicationNumber"]
                            _this_pub_title = record["title"]
                            all_conferences[_this_pub_number] = _this_pub_title


    with open ("./tmp/all_conferences.json", 'w') as f:
        json.dump(all_conferences, f, indent=4)    





