File works as a vote results scfaper. It takes district name and returns result for this udistrict. Results are from year 2017.

Libaries used are saved in requrements.txt and can be installed by using: 

    pip install -r requirements.txt

Script is used by starting the script with two parameters:
  1. Name of the district
  2. Name of the resulting CSV file
  
Examples of how to start the script:

  Linux:
  
    sudo python3 ./main.py name_of_district name_of_csv_file
  Windows:
  
    C:\Python\Python C:\Python\Project\main.py name_of_district name_of_csv_file
    
Output fomrat:

  Output of the script is csv file that is formated as follow:
  
    Column 1: unit_code  == code of the specific district unit
    Column 2: unit_name  == name of the specific district unit
    Column 3: submitted_envelopes == Number of submitted envelopes
    Column 4: valid_votes  == number of valid votes
    Column 5: voters  == number of voters
    
List of functions:

  Input:
  
    def user_input(argv) - Takes user parameters that are used as imput for data extraction. Output of this function are two two string variables             (name_of_the_district, file_name)
    def get_soup(url) - Creates soup from provided URL. Output of this function is soup object.
    def process_main_url(url) - Process main url so it can be used with other related urls. Output is string containing processed part of the main url that can be used for further adresses.
    def get_district_url(url, name_of_the_district) - Process url of given district based on provided district name and returns url string of such district detail.

  Data Extraction:
    
    def fix_space(string) - Function that takes incorrectly formated space in number and fixes it. When numbers data are extracted they might have incorrect character formating. This is fixed by  this function which returns fixed number as a string.
    def read_district_unit_data(url, district_unit_url) - Extracts data from individual district units. Returns Voters, Valid votes and Submitted envelopes.
    def read_district_unit_parties_data(url, district_unit_url) - Extracts data about parties and voes they recieved for given district.
    def read_all_district_data(url, name_of_the_district - Extracts Voters, Valid votes and Submitted envelopes using read_district_unit_data function. Also extracts Unit code and Unit name of the district unit. All of this is returned as a List containing dictionaries contaning all of this info.
  
  Writing into CSV:
  
    def write_csv(file_name, extracted_data) - Takes extracted data and name of the file. Returns table with the values in a file according the provided name as a argument.
