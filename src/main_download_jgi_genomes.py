# coding : utf-8

"""
@author : Zygnematophyce
Master II BI - 2020
program : main_download_jgi_genomes.py
"""

import argparse
import subprocess
import os
import xml.etree.ElementTree as ET

#e.g : get_jgi_genomes [-u <username> -p <password>] | [-c <cookies>] [-f | -a | -P 12 | -m 3] (-l)\n\n";
def arguments():
    """ Method that define all arguments ."""
    parser = argparse.ArgumentParser(description="main_download_jgi_genomes.py")
    parser.add_argument("-u",
                        help="Username.",
                        type=str)
    parser.add_argument("-p",
                        help="Password.",
                        type=str)
    # parser.add_argument("-c",
    #                     help="Cookies.",
    #                     type=str)
    parser.add_argument("-db",
                        help="Which databases between : mycocosm, phycocosm,\
                        phytozome or metazome.",
                        choices=["fungi", "phycocosm"],
                        type=str)
    # parser.add_argument("-l",
    #                     help="Only the list xml of database.")
    args = parser.parse_args()

    # Check if all parameters have a value.
    if not any(vars(args).values()):
        parser.print_help()
    return args.u, args.p, args.db

def download_cookie(username, password):
    """ Method to download cookie ."""
    subprocess.run(["curl \
    --silent 'https://signon.jgi.doe.gov/signon/create' \
    --data-urlencode \
    'login="+username+"' \
    --data-urlencode \
    'password="+password+"' \
    -c cookies > /dev/null"], shell=True)

def download_xml(database, cookie):
    """ Method to download xml file for specific database."""
    if os.path.isfile(database+"_file.xml"):
        print(database+"_file.xml already exists !")
    else:
        print("Download {} xml - This take some time ...\n".format(database))
        subprocess.run(["curl \
        'https://genome.jgi.doe.gov/portal/ext-api/downloads/get-directory?organism="+database+"' \
        -b "+cookie+" \
        > "+database+"_files.xml"], shell=True)

    # Remove "&quot" part in the xml file with sed command.
    subprocess.run(["sed -i \'s/&quot;//g\' "+database+"_files.xml"], shell=True)
    print("Download {} xml done !".format(database))

def get_url_CDS_mycocosm_xml(xml_file):
    """ Method that return a list of urls for coding sequences of mycocosm.  """

    # Load xml file and create a tree and get root of xml file.
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # List with all urls of coding sequences of mycocosm.
    url_CDS = list()

    # Filtering all sequences that we don't want.
    filtering_sequence = ["primary", "secondary", "alleles", "diploid", "old"]

    # The xpath of coding sequence in xml file.
    query_coding_sequence = '.[@name="fungi"]'\
        '/folder[@name="Files"]'\
        '/folder[@name="Annotation"]'\
        '/folder[@name="Filtered Models (best)"]'\
        '/folder[@name="CDS"]'

    # For each coding sequence recover all urls attributes.
    for CDS in root.find(query_coding_sequence):
        label = CDS.get("label")
        url = CDS.get("url")

        # Condition that excludes unwanted coding sequences (depend on
        # filtering_sequences variable).
        if not(any(unwanted_sequence in url for unwanted_sequence in filtering_sequence)):
            url_CDS.append(url)
        else:
            # Print unwanted sequence.
            print("unwanted sequence url:", url)
    return url_CDS

def create_folder(path_folder):
    """ Method to create folder if doesn't exists. """

    if os.path.exists(path_folder):
        print("{} already exists.".format(path_folder))
    else:
        try:
            os.makedirs(path_folder)
        except FileExistsError:
            print("Error to create folder")
            exit()

def download_database(list_url, database):
    """ Method to download database from a list of url. """

    # Check if result folder exists.
    create_folder("results/"+database)

    # Check if the list of url is empty.
    if not list_url:
        print("The list of url is empty")
    else:
        downloaded_file = list_url[0]
        print(downloaded_file)

        basename_file = os.path.basename(downloaded_file)
        print(basename_file)

        subprocess.run(["curl \
        'https://genome.jgi.doe.gov"+downloaded_file+"' \
        -b cookies \
        > results/"+database+"/"+basename_file+" "], shell=True)       

if __name__ == "__main__":
    print("Download JGI genomes !")

    # Get all parameters.
    JGI_USERNAME, JGI_PASSWORD, DATABASE = arguments()

    # Check if cookie already exists.
    if os.path.isfile("cookies"):
        print("Already logged.")
    else:
        print("Create cookie file with identifiant.")
        download_cookie(JGI_USERNAME, JGI_PASSWORD)

    # Test to download xml file for fungi database (mycocosm).
    if os.path.isfile(str(DATABASE)+"_files.xml"):
        print("Dababase with xml file already exists")
    else:
        download_xml(DATABASE, "cookies")

    XML_FILE = DATABASE+"_files.xml"
    print("xml file is", XML_FILE)

    # Get all coding sequences urls from xml file.
    ALL_URLS_CDS = get_url_CDS_mycocosm_xml(XML_FILE)

    # Download the database.
    download_database(ALL_URLS_CDS, DATABASE)
