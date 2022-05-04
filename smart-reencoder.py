from modules.fstools import detect_file_to_reencode, moving_file_to_reencode
from modules.videotools import mp4_hd720_converter
from pathlib import Path
import sys


if __name__ == '__main__':

    repertoire = Path(sys.argv[1])

    delete = False
    if len(sys.argv) == 3 and sys.argv[2] == '--delete':
        delete = True

    liste_fichiers = detect_file_to_reencode(repertoire)

    if(len(liste_fichiers) != 0):
        print("Fichiers à ré-encoder : ")
        for fichier in liste_fichiers:
            print(f" -> {str(fichier)}")
        print()
        yesno = input(f"Lancer le ré-encodage de {len(liste_fichiers)} fichier(s) ? (Non) : ")
        if yesno in ('y', 'Y', 'o', 'O', 'yes', 'Yes', 'YES', 'oui', 'Oui', 'OUI'):
            a_reencoder = moving_file_to_reencode(repertoire, liste_fichiers)
            mp4_hd720_converter(a_reencoder, delete)
    else:
        print("Aucun fichiers à ré-encoder.")