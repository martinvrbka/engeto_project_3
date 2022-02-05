File works as a vote results scfaper. It takes district name and returns result for this udistrict. Results are from year 2017.

Script is used by starting the script with two parameters:
  1. Name of the district
  2. Name of the resulting CSV file
  
Examples of how to start the script:

  Linux:
    sudo python3 ./main.py name_of_district name_of_csv_file
  Windows:
  
    C:\Python\Python (Python) C:\Python\Project\main.py name_of_district name_of_csv_file
    
Output fomrat:
  Output of the script is csv file that is formated as follow:
    Column 1: unit_code  == code of the specific district unit
    Column 2: unit_name  == name of the specific district unit
    Column 3: valid_votes  == number of valid votes
    Column 4: voters  == number of voters
    
List of functions:

  Input:
    def user_input(argv) - Takes user parameters that are used as imput for data extraction. Output of this function are two two string variables             (name_of_the_district, file_name)
    def get_soup(url) - Creates soup from provided URL. Output of this function is soup object.
    def process_main_url(url) - Process main url so it can be used with other related urls. Output is string containing processed part of the main url that can be used for further adresses.

  Data Extraction:
    
    
  
  Writing into CSV:
  
  
