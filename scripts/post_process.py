import json
import os
import logging



logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG) 
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('process.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)




def list_second_level_folders_with_parents(root_dir):
    second_level_folders_with_parents = []
    for root, dirs, files in os.walk(root_dir):
        if root == root_dir:
            for dir_name in dirs:
                first_level_folder = dir_name
                subdir_path = os.path.join(root, dir_name)
                for subroot, subdirs, subfiles in os.walk(subdir_path):
                    if subroot == subdir_path:
                        for subdir_name in subdirs:
                            second_level_folders_with_parents.append((first_level_folder, subdir_name))
            break

    return second_level_folders_with_parents


def process_source_json(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    folders_with_parents = list_second_level_folders_with_parents(src_dir)
    cnt = 0
    for parent, folder in folders_with_parents:
        cnt += 1
        print ('{}/{}'.format(cnt, len(folders_with_parents)))
        folder_to_be_processed = os.path.join(src_dir, parent, folder)
        dst_json_folder = os.path.join(dst_dir, parent)
        if not os.path.exists(dst_json_folder):
            os.makedirs(dst_json_folder)
        dst_json = os.path.join(dst_dir, parent, "{}.json".format(folder))
        if os.path.exists(dst_json):
            continue
        process_function(folder_to_be_processed, dst_json)
                


def process_function(folder_to_be_processed, dst_json):
    processed_list = []
    for root, dirs, files in os.walk(folder_to_be_processed):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)    
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    if 'records' in data:
                        records = data['records']
                    else:
                        records = []
                        logger.warning('No records found in file: {}'.format(file_path))

                    for record_cnt, record in enumerate(records):

                        _this_processed_record = {}
                        _this_processed_record['publicationNumber'] = record['publicationNumber'] if 'publicationNumber' in record else None
                        _this_processed_record['doi'] = record['doi'] if 'doi' in record else None
                        _this_processed_record['publicationYear'] = record['publicationYear'] if 'publicationYear' in record else None
                        _this_processed_record['publicationDate'] = record['publicationDate'] if 'publicationDate' in record else None
                        _this_processed_record['articleNumber'] = record['articleNumber'] if 'articleNumber' in record else None
                        _this_processed_record['articleTitle'] = record['articleTitle'] if 'articleTitle' in record else None
                        _this_processed_record['volume'] = record['volume'] if 'volume' in record else None
                        _this_processed_record['issue'] = record['issue'] if 'issue' in record else None
                        _this_processed_record['startPage'] = record['startPage'] if 'startPage' in record else None
                        _this_processed_record['endPage'] = record['endPage'] if 'endPage' in record else None
                        _this_processed_record['publisher'] = record['publisher'] if 'publisher' in record else None
                        _this_processed_record['contentType'] = record['contentType'] if 'contentType' in record else None
                        _this_processed_record['articleContentType'] = record['articleContentType'] if 'articleContentType' in record else None
                        _this_processed_record['publicationTitle'] = record['publicationTitle'] if 'publicationTitle' in record else None
                        _this_processed_record['highlightedTitle'] = record['highlightedTitle'] if 'highlightedTitle' in record else None

                        _this_processed_record['authors'] = []
                        
                        if 'authors' in record:
                            for each_author in record['authors']:
                                _this_author= {}

                                _this_author['id'] = each_author['id'] if 'id' in each_author else None
                                _this_author['preferredName'] = each_author['preferredName'] if 'preferredName' in each_author else None
                                _this_author['firstName'] = each_author['firstName'] if 'firstName' in each_author else None
                                _this_author['lastName'] = each_author['lastName'] if 'lastName' in each_author else None
                                _this_processed_record['authors'].append(_this_author)

                        processed_list.append(_this_processed_record)

    with open(dst_json, 'w') as dst_file:
        json.dump(processed_list, dst_file, indent=4)

    return





if __name__ == '__main__':

    source_path = './tmp/download_source_json'
    target_path = './tmp/processed_json'


    process_source_json(source_path, target_path)
    
    