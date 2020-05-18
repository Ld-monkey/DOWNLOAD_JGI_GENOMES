# DOWNLOAD JGI GENOMES

## Introduction

Dans le cadre de mon stage de métagenomique et en me basant sur le script perl de guileonard sur son github https://github.com/guyleonard/get_jgi_genomes, j'ai automatisé le téléchargement de toutes les séquences nucléotidiques dans la base de donnée JGI dans le langague Python.

## Source :+1:

Ce travail est une adaptation du travail original de Guileonard dans le repository suivant : https://github.com/guyleonard/get_jgi_genomes .

## Pourquoi :question:

   - [ ] Car le langague Python est un langague supérieur a Perl (Python > Perl). :satisfied:
   - [ ] Pour corriger certaines erreurs de permission lors du téléchargement du fichier xml sous Debian.
   - [x] J'aime tout reprogrammer pour tout bien comprendre en tant que bio-informaticien novice <del>et perde mon temps a ça</del>.
   - [x] Pour l'intrégrer dans mon pipeline de métagenomique : https://github.com/Zygnematophyce/CLINICAL_METAGENOMICS . 
   
## Utilisation :mortar_board:

```bash
python src/main_download_jgi_genomes.py -u <username> -p <password>
```

## Aide 

```bash
Download JGI genomes !
usage: main_download_jgi_genomes.py [-h] [-u U] [-p P] [-c C] [-db DB] [-l L]

main_download_jgi_genomes.py

optional arguments:
  -h, --help  show this help message and exit
  -u U        Username.
  -p P        Password.
  -c C        Cookies.
  -db DB      Which databases between : mycocosm, phycocosm, phytozome or
              metazome.
  -l L        Only the list xml of database.
```
