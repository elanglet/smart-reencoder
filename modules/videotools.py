from pathlib import Path
import ffmpeg 
#
# COMMANDE DE REFERENCE : 
# 
# ffmpeg -i input.wmv -c:v libx264 -crf 15 -c:a aac -q:a 100 -s hd720 output.mp4
#
#
# Vérifier la présence du dossier 'vids' au même emplacement que ce script


def mp4_hd720_converter(repertoire: Path, delete=False) -> None:
    options = {'c:v': 'libx264', 'crf': '25', 'c:a': 'aac', 'q:a': 100, 's': 'hd720', 'loglevel': 'error'}
    repertoire = Path(repertoire)
    if not repertoire.is_dir():
        print("Erreur : Le répertoire contenant les vidéos à encoder est introuvable.")
    else:
        # Parcourir le contenu du répertoire
        liste = list(repertoire.glob('*.*'))
        cpt = 1
        for source in liste:
            # vid.stem -> nom du fichier sans le dossier et sans extension
            destination = repertoire / (source.stem + "-OUT.mp4")
            print(f"{cpt}/{len(liste)} - Encodage vers '{destination}'")
            ffmpeg.input(source).output(str(destination), **options).run()
            cpt += 1
            if delete:
                print(f"Encodage terminé, suppression de '{source}'")
                source.unlink()
