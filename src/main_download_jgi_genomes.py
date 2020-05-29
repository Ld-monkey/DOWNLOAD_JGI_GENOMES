# coding : utf-8

"""
@author : Zygnematophyce
Master II BI - 2020
program : main_download_jgi_genomes.py
"""

import argparse
import subprocess
import os
import csv
import xml.etree.ElementTree as ET


def is_cookie(cookie):
    """ Method that return boolean to verifie if cookie is found or not. """

    if os.path.isfile(cookie):
        return True
    else:
        return False

def is_xml(xml_file):
    """ Method that return boolean to verifie if download xml file is found. """

    if os.path.isfile(str(xml_file)):
        print("Dababase with xml file already exists")
        return True
    else:
        return False

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
    parser.add_argument("-c",
                        help="Cookies.",
                        type=str)
    parser.add_argument("-db",
                        help="Which databases between : mycocosm, phycocosm,\
                        phytozome or metazome.",
                        choices=["fungi", "phycocosm"],
                        type=str)
    parser.add_argument("-out",
                        help="Output folder of database e.g: results/databases/",
                        nargs="?",
                        const="results/",
                        type=str)
    # parser.add_argument("-l",
    #                     help="Only the list xml of database.")
    args = parser.parse_args()

    # Check if cookie already exists.
    if args.c is None:
        default_cookie_name = "cookies"
        if is_cookie(default_cookie_name) is True:
            print("Already logged.")
            args.c = default_cookie_name
        else:
            print("Create cookie file with identifiant")
            download_cookie(username=args.u, password=args.p, cookie=default_cookie_name)
            args.c = default_cookie_name
    else:
        # Create cookie is specific name.
        print("Create cookie named {}".format(args.c))
        download_cookie(username=args.u, password=args.p, cookie=args.c)

    return args.u, args.p, args.c, args.db, args.out

def download_cookie(username, password, cookie):
    """ Method to download cookie ."""

    subprocess.run(["curl \
    --silent 'https://signon.jgi.doe.gov/signon/create' \
    --data-urlencode \
    'login="+username+"' \
    --data-urlencode \
    'password="+password+"' \
    -c "+cookie+" > /dev/null"], shell=True)

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

    print("Download {} xml done !".format(database))

    # Remove "&quot" part in the xml file with sed command.
    subprocess.run(["sed -i \'s/&quot;//g\' "+database+"_files.xml"], shell=True)
    print("Remove &quot")

    # Give 664 permission of xml file for Debian bug.
    os.chmod(database+"_files.xml", 0o664)

def download_database(list_url, database, cookie, path_output_folder):
    """ Method to download database from a list of url. """

    print("Donwloading database !")
    # Check if result folder exists.
    create_folder(path_output_folder+str(database))

    # Check if the list of url is empty.
    if not list_url:
        print("The list of url is empty")
    else:
        for downloaded_file in list_url:
            print(downloaded_file)

            basename_file = os.path.basename(downloaded_file)

            subprocess.run(["curl \
            'https://genome.jgi.doe.gov"+downloaded_file+"' \
            -b "+cookie+" \
            > "+path_output_folder+database+"/"+basename_file+" "], shell=True)

# Doit différencier la création d'un csv a celui du retour de url.
def get_url_CDS_mycocosm_xml(xml_file):
    """ Method that return a list of urls for coding sequences of mycocosm.  """

    # Load xml file and create a tree and get root of xml file.
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # List with all urls of coding sequences of mycocosm.
    url_CDS = list()
    label_CDS = list()

    # Filtering all sequences that we don't want.
    filtering_sequence = ["primary", "secondary", "alleles", "diploid", "old"]

    # The xpath of coding sequence in xml file.
    query_coding_sequence = '.[@name="fungi"]'\
        '/folder[@name="Files"]'\
        '/folder[@name="Annotation"]'\
        '/folder[@name="Filtered Models (best)"]'\
        '/folder[@name="CDS"]'

    with open("all_organisms.csv", mode="w") as csv_file:
        fieldnames = ["organisms", "jgi_fullname", "jgi_basename", "ncbi_id_taxonomy"]
        csv_write = csv.writer(csv_file,
                               delimiter=",",
                               quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        # Write csv header.
        csv_write.writerow(fieldnames)

        # For each coding sequence recover all urls attributes.
        for CDS in root.find(query_coding_sequence):
            label = CDS.get("label")
            url = CDS.get("url")
            jgi_fullname = CDS.get("filename")
            jgi_basename = os.path.splitext(jgi_fullname)[0]

            # Condition that excludes unwanted coding sequences (depend on
            # filtering_sequences variable).
            if not any(unwanted_sequence in url for unwanted_sequence in filtering_sequence):
                url_CDS.append(url)
                csv_write.writerow([label, jgi_fullname, jgi_basename])

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

if __name__ == "__main__":
    print("Download JGI genomes !")

    # Get all parameters.
    JGI_USERNAME, JGI_PASSWORD, COOKIE, DATABASE, PATH_DB_OUTPUT = arguments()

    XML_FILE = DATABASE+"_files.xml"
    print("xml file is", XML_FILE)

    # Check if xml file is already exists.
    if is_xml(XML_FILE) is False:
        download_xml(database=DATABASE, cookie=COOKIE)

    # Get all coding sequences urls from xml file.
    ALL_URLS_CDS = get_url_CDS_mycocosm_xml(XML_FILE)

    # Download the database.
    download_database(list_url=ALL_URLS_CDS,
                      database=DATABASE,
                      cookie=COOKIE,
                      path_output_folder=PATH_DB_OUTPUT)
