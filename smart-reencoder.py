# ./smart-reencoder.py
from modules.fstools import detect_file_to_reencode, moving_file_to_reencode
from modules.videotools import mp4_converter
from pathlib import Path
import sys


if __name__ == '__main__':
    repertoire = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not repertoire:
        print("Usage : python smart-reencoder.py <répertoire> [--delete] [--force] [--workers N]")
        sys.exit(1)

    delete = '--delete' in sys.argv
    force = '--force' in sys.argv

    # Gestion optionnelle du nombre de workers
    max_workers = None
    if '--workers' in sys.argv:
        try:
            idx = sys.argv.index('--workers')
            max_workers = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("⚠️  Option '--workers' invalide. Exemple : --workers 2")

    liste_fichiers = detect_file_to_reencode(repertoire, force)

    if liste_fichiers:
        print("Fichiers à ré-encoder : ")
        for fichier in liste_fichiers:
            print(f" -> {str(fichier)}")
        print()
        yesno = input(f"Lancer le ré-encodage de {len(liste_fichiers)} fichier(s) ? (Non) : ")
        if yesno.lower() in ('y', 'o', 'yes', 'oui'):
            a_reencoder = moving_file_to_reencode(repertoire, liste_fichiers)
            mp4_converter(a_reencoder, delete, max_workers=max_workers)
    else:
        print("Aucun fichier à ré-encoder.")
