# Comprehensive IEEE Research Data Collections (CIRDC)

This repository provides detailed information on all articles available through IEEE Xplore up to July 2024, organized for easy access and use by researchers. The repository also includes the necessary code for data collecting, facilitating further updates to the database. For an in-depth explanation of the dataset, please refer to the following publication: Y. Zhang, Y. Li, S. Makonin, and R. Kumar. Descriptor: Comprehensive IEEE Research Data Collections (CIRDC). IEEE Data Description.

## Database Structure

The database is in `CIRDC` folder. Each directory in `CIRDC` represents the publication number of a journal or conference, named by `publication number`. Each sub-directory in `publication number` directory contains multiple JSON files named by `year.json'. Each JSON file includes the information of all the papers for that journal/conference and for that year. An example is shown as follows, where 10 and 100 indicate `publication number`. 1964 and 1965 indicate `year`.

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

## Publication Number Index

The `publication_number_index.csv` file provides an easy-to-navigate index of publication numbers, allowing users to quickly look up and cross-reference the corresponding publication number for specific journals and conferences by their names.

## Scripts for Data Collection

The scripts for crawling the database are located in the `scripts` folder. As the maximum number of entries returned in a single query is restricted to 10,000 in IEEE Xplore, the collection involves a two-stage process. The first stage is to collect the `publication number` of all the journals and conferences. The second stage is to collect the data based on the `publication number` on a year-by-year process. As the search results are returned on multiple pages, we handle each page sequentially. 

Follow the steps below to collect the data:

1. Run `get_journal_info.py` and `get_conference_info.py` to retrieve all journal and conference publication numbers.
2. Run `get_all_publication_pubnumber.py` to gather all publication numbers.
3. Use `download_journal_paper_info.py` and `download_conference_paper_info.py` to download the article information.
4. Finally, execute `post_process.py` for data post-processing. The intermediate files generated during the process are saved in the `tmp` folder.

## License

This repository is licensed under the terms of the [Creative Commons Attribution 4.0 International License](LICENSE).
