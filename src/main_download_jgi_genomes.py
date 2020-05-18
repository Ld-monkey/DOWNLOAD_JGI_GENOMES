# coding : utf-8

"""
@author : Zygnematophyce
Master II BI - 2020
program : main_download_jgi_genomes.py
"""

import argparse
import subprocess

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
    subprocess.run(["curl  --silent 'https://signon.jgi.doe.gov/signon/create' \
    --data-urlencode \
    'login="+username+"' \
    --data-urlencode \
    'password="+password+"' \
    -c cookies > /dev/null"], shell=True)

if __name__ == "__main__":
    print("Download JGI genomes !")

    # Get all parameters
    JGI_USERNAME, JGI_PASSWORD = arguments()

    # Check if cookie already exists.
    download_cookie(JGI_USERNAME, JGI_PASSWORD)
