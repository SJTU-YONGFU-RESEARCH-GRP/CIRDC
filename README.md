# Comprehensive IEEE Research Data Collections (CIRDC)

This repository contains detailed information on all articles available on IEEE Xplore. For a comprehensive description of the database, please refer to the article:
Y. Zhang, Y. Li, S. Makonin, and R. Kumar. Descriptor: Comprehensive IEEE Research Data Collections (CIRDC). IEEE Data Description.

## Database Structure

CIRDC is a database where each subdirectory represents the publication number of a journal or conference. Each subdirectory contains multiple JSON files named after the year. Each JSON file includes all the paper information for that journal/conference for that year.

## Publication Number Index

The `publication_number_index.csv` file contains the index of publication numbers.

## Scripts for Data Collection

The scripts for crawling the database are located in the `scripts` folder. Follow the steps below to collect the data:

1. Run `get_journal_info.py` and `get_conference_info.py` to retrieve all journal and conference publication numbers.
2. Run `get_all_publication_pubnumber.py` to gather all publication numbers.
3. Use `download_journal_paper_info.py` and `download_conference_paper_info.py` to download the article information.
4. Finally, execute `post_process.py` for data post-processing. The intermediate files generated during the process are saved in the `tmp` folder.

## License

This repository is licensed under the GNU General Public License.


