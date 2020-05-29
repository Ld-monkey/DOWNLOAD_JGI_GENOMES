# coding : utf-8

"""
@author : Zygnematophyce
Master II BI - 2020
program : jgi_id_to_ncbi_id_taxonomy.py
"""

from ete3 import NCBITaxa
import argparse
import csv
import os


def arguments():
    """ Method that define all arguments ."""

    parser = argparse.ArgumentParser(description="jgi_id_to_ncbi_id_taxonomy.py")

    parser.add_argument("-csv",
                        help="Comma-separated values",
                        type=str)
    parser.add_argument("-path_sequence",
                        help="directory with all fasta sequences /data/sequence/",
                        type=str)
    args = parser.parse_args()

    return args.csv, args.path_sequence

def add_ncbi_id_taxonym_in_csv(csv_file, output_csv_name):
    """Method that open the csv file to read and write ncbi id taxonomy. """

    try:
        with open(csv_file, "r") as csv_file_read, \
             open(output_csv_name, "w", newline="") as csv_file_write:

             # Define variable for writing and reading.
             csv_read = csv.reader(csv_file_read, delimiter=",")
             csv_writer = csv.writer(csv_file_write)

             # Count the number of line.
             count_line = 0

             # For each row in csv file.
             for row in csv_read:
                 # For the first line with fieldline just copy.
                 if count_line == 0:
                     csv_writer.writerow(row)
                 else:
                     # Definie specie with the first column of csv.
                     print("---------------------------")
                     specie = [str(row[0])]
                     print("Specie:", specie)
                     
                     # Try to find a taxonomic id from ncbi.
                     ncbi_id_taxid = ncbi.get_name_translator(specie)
                     print("id:", ncbi_id_taxid)

                     # Check if dictonnary with taxonomic id is empty in rare cases.
                     if bool(ncbi_id_taxid) is False:

                         print("-----------")
                         # The flag for while condition.
                         flag = False
                         print("on a pas trouvé l'id dans un premier temps")
                         print("flag=", flag)
                         print("type flag=",type(flag))

                         # Split the end name of specie to search less specific taxon.
                         row_name_split = specie[0].rsplit(" ", 1)[0]
                         print("specie:", row_name_split)

                         print("juste avant la loop.")
                         while flag is False:
                             print("je rentre dans la loop")
                             # Try to find a taxonomic id from ncbi.
                             ncbi_id_taxid = ncbi.get_name_translator([row_name_split])
                             print("id: ", ncbi_id_taxid)

                             # Check if in this case id taxonomic was found.
                             if bool(ncbi_id_taxid) is True:
                                 print("-----")
                                 print("on marque identifiant")
                                 print("specie", ncbi_id_taxid)
                                 ncbi_id = ncbi_id_taxid.get(str(row_name_split))[0]
                                 print("id", ncbi_id)
                                 row.append(ncbi_id)
                                 csv_writer.writerow(row)
                                 flag = True
                             elif bool(ncbi_id_taxid) is False and len(row_name_split.split()) != 1:
                                 print("-----")
                                 print("on raccourcie encore ...")
                                 # Split again to search older taxonomic.
                                 row_name_split = row_name_split.rsplit(" ", 1)[0]
                                 print("specie :", row_name_split)
                             else:
                                 print("-----")
                                 print("c'est un fail pour id on quitte")
                                 # Finaly if nothing was found quit the loop in write
                                 # blank in the line.
                                 row.append("")
                                 csv_writer.writerow(row)
                                 flag = True
                     else:
                         # Taxonomic id was found write it at the end of csv row.
                         ncbi_id = ncbi_id_taxid.get(row[0])[0] 
                         row.append(ncbi_id)
                         csv_writer.writerow(row)
                 count_line += 1
        print("Output csv done !")
    except IOError:
        print("Error in opening of csv file.")
        exit()

def add_ncbi_id_in_fasta(complete_csv_file, path_sequence):
    """ Method that read csv file and add taxonomic ncbi id in fasta description."""

    with open(complete_csv_file, "r") as csv_reader:
        csv_read = csv.reader(csv_reader, delimiter=",")
        for row in csv_read:
            try:
                # Replace jdi id to ncbi taxonic.
                with open(path_sequence+row[2], "r") as fasta_read:
                    print("Fasta :", path_sequence+row[2])
                    with open(path_sequence+row[2]+".out", "w") as fasta_file_write:
                        for line in fasta_read:
                            if line.startswith(">") is True:
                                modified_line = line[0:4]+"|kraken:taxid|"+row[3]+"|" + line[5:]
                                fasta_file_write.write(line.replace(line, modified_line))
                            else:
                                fasta_file_write.write(line)
                        os.remove(path_sequence+row[2])
                        os.rename(path_sequence+row[2]+".out", path_sequence+row[2])
                        print("Output {} done .".format(row[2]))
            except IOError:
                print("Error impossible to open {}".format(row[2]))
                with open("impossible_opening.txt", "a") as nothing_open:
                    nothing_open.write(row[2]+"\n")

if __name__ == "__main__":
    print("JGI ID to NCBI ID taxonomy !")

    # Download the latest taxonomic database from the NCBI.
    ncbi = NCBITaxa()

    try:
        version = ncbi._NCBITaxa__get_db_version()
        print("version :", version)
    except Exception:
        version = None

    # Get all parameters.
    CSV_FILE, PATH_SEQUENCE = arguments()
    print("csv :", CSV_FILE)

    # Name of output csv.
    output_csv = "output_fungi_csv.csv"

    # Complete de csv file with ncbi taxonomic id.
    add_ncbi_id_taxonym_in_csv(csv_file=CSV_FILE,
                               output_csv_name=output_csv)

    # Change the fasta file with the kraken instruction |kraken:taxon| and good ncbi id.
    add_ncbi_id_in_fasta(complete_csv_file=output_csv,
                        path_sequence=PATH_SEQUENCE)

