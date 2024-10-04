# CIS6930FA24 -- Project 0

## Name:

Rohan Ponuganti

## Project Description

This Python package retrieves PDF file from the Norman, Oklahoma police department's website, extracts the incident data from the PDF using `pypdf` and stores the data in an SQLite database. Various test scripts are also included to test the robustness of the package using pytest.

The `main.py` file is the entry point of the package and contains the `main()` function which provides the outline of the data extraction process. The `utils.py` file contains all of the helper functions `fetch_incidents()`, `extract_incidents()`, `create_db()`, `populate_db()`, `get_db_conn()` and `status()`.

# How to install

1. Clone the repository using `git clone https://github.com/codemachine69/cis6930fa24-project0.git`.
2. Ensure you have `pipenv` installed in your machine. Use `pip install pipenv` or `brew install pipenv`(For Homebrew).
3. Run `pipenv install -e .`

## How to run

For fetching incident data from the Oklahoma PD's website url, use:
`pipenv run python project0/main.py --incidents <PDF-url>`

## How to run tests using pytest

`pipenv run python -m pytest -v`

## How to add dependency using pipenv

`pipenv install <dependency-name>`

## Video on how to run

![Watch the video](https://youtu.be/0XLCju5xVoA)

## Functions

1. `main()` - This is the core function that ties all the utility functions together in a workflow to achieve the desired result of processing the incidents from the Norman Police Department.
2. `fetch_incidents()` - This function takes a URL as an input, representing the location of an incident PDF report. It makes an HTTP request to fetch the PDF file from the provided URL. It returns a file-like BytesIO object containing the PDF data in binary form, which can then be processed.
3. `extract_incidents()` - Parses the PDF text to extract the required incident information fields (Date / Time, Incident Number, Location, Nature, and Incident ORI) for storage in the database. It returns a list of tuples, where each tuple contains the extracted fields.
4. `create_db()` - Initializes the SQLite database and ensures that the incidents table is ready to store the extracted data. It returns a connection object to the SQLite database.
5. `get_db_conn()` - This function retrieves the connection for the created database.
6. `populate_db()` - This function populates the SQLite database with extracted incident data.
7. `status()` - Provides a summarized count of each incident type stored in the database, allowing quick analysis of the data.

## Assumptions

1. The functions were written keeping in mind that the provided URL might not be valid. Proper exception handling has been done to handle invalid URL.
2. The Oklahoma PD URL is assumed to be stable and accessible at all times. No retries or alternative strategies are implemented in case of API downtime.
3. It is assumed that the URL response fields will always be in the expected format. Any other data structure or missing fields could cause errors.
4. It is assumed that all incident summary PDFs from the Norman Police Department follow a consistent structure. The expected format includes lines with the following fields in this order: Date/Time, Incident Number, Location, Nature, and Incident ORI.
5. Code is designed to handle multiline location fields.

## Bugs

1. The script doesn't handle cases where the fields contain abnormal data.
2. If the structure or format of the PDFs on the Norman Police Department website changes (e.g., new headers, field rearrangement), the extract_incidents function may fail to correctly parse the data, resulting in missing or improperly extracted incidents.
3. The code is designed to handle irregular data to an extent, but will fail if new unknown test cases appear.
