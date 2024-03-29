import requests
from bs4 import BeautifulSoup
import csv
import sys


def user_input(argv):
    if len(argv) == 3:

        try:
            name_of_the_district = str(argv[1])
            csv_file_name = str(argv[2])

            if name_of_the_district == "Zahraničí":
                sys.exit("Please select only districts located in Czech Republic.")

        except ValueError as e:
            sys.exit(f"Wrong type of arguments, {e} error occured.")
    else:
        sys.exit(f"Wrong number of arguments.")

    return name_of_the_district, csv_file_name


def get_soup(url):
    try:
        soup = requests.get(url)
        soup = BeautifulSoup(soup.text, "html.parser")
        return soup
    except requests.exceptions.ConnectionError as e:
        sys.exit(f"Problem with connection: {e}")
    except requests.exceptions.InvalidURL as e:
        sys.exit(f"Problem with URL: {e}")


def process_main_url(url):
    main_url = "/".join(url.split("/")[0:5])
    return main_url


def get_district_url(url, name_of_the_district):
    tables = get_soup(url).find_all("table", {"class": "table"})

    for table in tables:
        table_rows = table.find_all("tr")[2:]
        for table_cell in table_rows:
            if table_cell.find_all("td")[1].text == name_of_the_district:
                district_url = f"{process_main_url(url)}/{table_cell.find_all('td')[3].find('a')['href']}"
                return district_url
    else:
        sys.exit(f"There are no results for district named {name_of_the_district}.")


def fix_space(string):
    try:
        return int(string.replace("\xa0", ""))
    except ValueError as e:
        sys.exit(f"Problem with value: {e}")


def read_district_unit_data(url, district_unit_url):
    soup = get_soup(f"{process_main_url(url)}/{district_unit_url}")
    unit_data = dict()

    unit_data["Voters"] = fix_space(soup.find("td", {"headers": "sa2"}).text)
    unit_data["Submitted envelopes"] = fix_space(soup.find("td", {"headers": "sa3"}).text)
    unit_data["Valid votes"] = fix_space(soup.find("td", {"headers": "sa6"}).text)

    return unit_data


def read_district_unit_parties_data(url, district_unit_url):
    soup = get_soup(f"{process_main_url(url)}/{district_unit_url}")
    unit_data = dict()

    tables = soup.find_all("table", {"class": "table"})

    for table in tables:
        table_rows = table.find_all("tr")
        for table_cell in table_rows:
            try:
                unit_data[table_cell.find("td", {"class": "overflow_name"}).text] = \
                    fix_space(table_cell.find_all("td", {"class": "cislo"})[1].text)
            except (AttributeError, IndexError):
                continue

    return unit_data


def read_all_district_data(url, name_of_the_district):
    unit_list = list()
    soup = get_soup(get_district_url(url, name_of_the_district))
    tables = soup.find_all("table", {"class": "table"})

    for table in tables:
        table_rows = table.find_all("tr")[2:]

        for table_cell in table_rows:
            try:
                unit_data = {"Unit code": table_cell.find_all("td")[0].text,
                             "Unit name": table_cell.find_all("td")[1].text,}

                unit_data.update(read_district_unit_data(url, table_cell.find_all('td')[0].find('a')['href']))
                unit_data.update(read_district_unit_parties_data(url, table_cell.find_all('td')[0].find('a')['href']))
                unit_list.append(unit_data)

            except TypeError:
                continue
    return unit_list


def write_csv(csv_file_name, extracted_data):
    with open(csv_file_name + ".csv", "w", newline="") as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=extracted_data[0].keys())

        try:
            writer.writeheader()
            writer.writerows(extracted_data)
        except csv.Error as e:
            sys.exit(f"CSV Error: {e}")


if __name__ == "__main__":

    url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    name_of_the_district, csv_file_name = user_input(sys.argv)
    extracted_data = read_all_district_data(url, name_of_the_district)
    write_csv(csv_file_name, extracted_data)
