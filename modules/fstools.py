import ffmpeg
from pathlib import Path


def detect_file_to_reencode(repertoire: Path) -> Path:
    if repertoire.exists() and repertoire.is_dir():
        liste_fichiers = []
        for fichier in repertoire.glob('*.*'):
            if fichier.is_file():
                try:
                    resultat = ffmpeg.probe(fichier)
                    video_streams = [stream for stream in resultat['streams'] if stream['codec_type'] == 'video']
                    resolution = video_streams[0]['height']
                    codec = video_streams[0]['codec_name']
                    if resolution != 720 or codec != 'h264':
                        liste_fichiers.append(fichier)
                except Exception as e:
                    print(f"Skipping '{fichier}'")
        return liste_fichiers
    else:
        raise Exception("Erreur sur le répertoire sélectionné : '{}'".format(repertoire.name))


def moving_file_to_reencode(repertoire: Path, liste_fichiers: list) -> Path:
    if repertoire.exists() and repertoire.is_dir():
        rep_reencodage = repertoire / 'smart-reencoder'
        rep_reencodage.mkdir(exist_ok=True)

        for fichier in liste_fichiers:
            fichier.rename(rep_reencodage / fichier.name)

        return rep_reencodage
    else:
        raise Exception("Erreur sur le répertoire sélectionné : '{}'".format(repertoire.name))
