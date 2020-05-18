# coding : utf-8

"""
@author : Zygnematophyce
Master II BI - 2020
program : main_download_jgi_genomes.py
"""

import argparse
import subprocess
import os

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
                        help="Wich database : mycocosm, phycocosm, phytozome or metazome.",
                        type=str)
    parser.add_argument("-l",
                        help="Only the list xml of database.")
    args = parser.parse_args()
    return args.u, args.p

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

if __name__ == "__main__":
    print("Download JGI genomes !")

    # Get all parameters.
    JGI_USERNAME, JGI_PASSWORD = arguments()

    # Check if cookie already exists.
    if os.path.isfile("cookies"):
        print("Already logged.")
    else:
        print("Create cookie file with identifiant.")
        download_cookie(JGI_USERNAME, JGI_PASSWORD)

    # Test to download xml file for fungi database (mycocosm).
    if os.path.isfile("fungi"+"_file.xml"):
        print("Dababase with xml file already exists")
    else:
        download_xml("fungi", "cookies")
