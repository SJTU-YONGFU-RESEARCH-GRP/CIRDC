# Comprehensive IEEE Research Data Collections (CIRDC)

This repository provides detailed information on all articles available through IEEE Xplore up to July 2024, organized for easy access and use by researchers. The repository also includes the necessary code for data collecting, facilitating further updates to the database. For an in-depth explanation of the dataset, please refer to the following publication: Y. Zhang, Y. Li, S. Makonin, and R. Kumar. Descriptor: Comprehensive IEEE Research Data Collections (CIRDC). IEEE Data Description.

## Database Structure

The database is in `CIRDC` folder. Each directory in `CIRDC` represents the publication number of a journal or conference, named by `publication number`. Each sub-directory in `publication number` directory contains multiple JSON files named by `year.json`. Each JSON file includes the information of all the papers for that journal/conference and for that year. An example is shown as follows, where 10 and 100 indicate `publication number`. 1964 and 1965 indicate `year`.

```
CIRDC/
├── 10
│   ├── 1964.json
│   ├── 1965.json
│   ├── ...
├── 100
    ├── ...
├── ...
```

## Data File Structure

Each JSON file contains a list, and each entity in the list corresponds to the metadata of a paper. The paper metadata is structured as follows:

| Name                | Description                                                                 | Type   |
|---------------------|-----------------------------------------------------------------------------|--------|
| publicationNumber   | Identifier for the journal/conference                                        | String |
| doi                 | Digital Object Identifier of the paper                                       | String |
| publicationYear     | Year the paper was published                                                 | String |
| publicationDate     | Full date of publication                                                     | String |
| articleNumber       | A unique number assigned to the paper                                        | String |
| articleTitle        | Title of the paper                                                           | String |
| volume              | Volume number                                                               | String |
| issue               | Issue number                                                                | String |
| startPage           | Starting page number                                                        | String |
| endPage             | Ending page number                                                          | String |
| publisher           | Name of the publisher                                                       | String |
| articleContentType  | Type of the paper (journal, conference, magazine, or early access article)    | String |
| publicationTitle    | Name of journal/conference                                                   | String |
| authors             | A list of authors                                                           | List   |

Each author entry in the `authors` field contains the following data:

| Name            | Description                                 | Type   |
|-----------------|---------------------------------------------|--------|
| id              | ID number of the author in IEEE system       | Int    |
| preferredName   | Full name of the author                      | String |
| firstName       | First name of the author                     | String |
| lastName        | Last name of the author                      | String |

## Publication Number Index

The `publication_number_index.csv` file provides an easy-to-navigate index of publication numbers, allowing users to quickly look up and cross-reference the corresponding publication number for specific journals and conferences by their names.

## Scripts for Data Collection

The scripts for collecting CIRDC are in the `scripts` folder. As the maximum number of entries returned in a single query is restricted to 10,000 in IEEE Xplore, the collection involves a two-stage process. The first stage is to collect the `publication number` of all the journals and conferences. The second stage is to collect the data based on the `publication number` on a year-by-year process. As the search results are returned on multiple pages, we handle each page sequentially. 

Follow the steps below to collect the data:
1. Run `mkdir tmp`.
2. Run `get_journal_info.py` and `get_conference_info.py`.
These scripts are to download all journal and conference information. This will generate temporary folders `json_conference_year` and `json_journal_year`. 
3. Run `get_all_publication_pubnumber.py`. This will process the downloaded conference and journal information to collect all publication numbers in temporary files `all_journals.json` and `all_conferences.json`. 
4. Run `download_journal_paper_info.py` and `download_conference_paper_info.py`. This will download the data of IEEE Xplore papers based on the publication numbers to `download_source_json` folder.
5. Run `post_process.py`. This will conduct post-processing for the downloaded json files.

The intermediate files generated during the process are saved in the `tmp` folder. The final output will be saved in `processed_json` folder.

## Dependencies

The scripts are tested using Python3.6. The following libraries are used. `requests (2.27.1)` library is required. Other versions could also work but haven't been tested. 

## License

This repository is licensed under the terms of the [Creative Commons Attribution 4.0 International License](LICENSE).
