# modules/videotools.py
from pathlib import Path
import ffmpeg
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration optimisée pour une VM 6 cœurs
DEFAULT_WORKERS = 2      # 2 encodages simultanés
DEFAULT_THREADS = 3      # 3 threads FFmpeg par encodage

def _encode_video(source: Path, destination: Path, options: dict, delete: bool):
    """Encode une seule vidéo."""
    try:
        (
            ffmpeg
            .input(str(source))
            .output(str(destination), **options, threads=str(DEFAULT_THREADS))
            .run(overwrite_output=True, quiet=True)
        )
        if delete:
            source.unlink()
        return f"✅ Encodé : {source.name}"
    except Exception as e:
        return f"❌ Erreur sur {source.name} : {e}"

def mp4_converter(repertoire: Path, delete=False, max_workers=None) -> None:
    """
    Convertit les vidéos d'un répertoire en MP4 540p, en parallèle.
    max_workers : nombre max de conversions simultanées (défaut = 2 pour une VM 6 cores)
    """
    options = {'c:v': 'libx264', 'crf': '20', 'c:a': 'aac', 'q:a': 100, 's': 'qhd'}
    repertoire = Path(repertoire)

    if not repertoire.is_dir():
        print("Erreur : Le répertoire contenant les vidéos à encoder est introuvable.")
        return

    liste = list(repertoire.glob('*.*'))
    if not liste:
        print("Aucun fichier à encoder.")
        return

    workers = max_workers or DEFAULT_WORKERS
    print(f"🧩 Détection : {len(liste)} fichiers à encoder.")
    print(f"🧵 Utilisation de {workers} workers (threads ffmpeg={DEFAULT_THREADS})\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for source in liste:
            destination = repertoire / f"{source.stem}-OUT.mp4"
            futures.append(executor.submit(_encode_video, source, destination, options, delete))

        for i, future in enumerate(as_completed(futures), 1):
            print(f"[{i}/{len(liste)}] {future.result()}")

    print("\n✅ Encodage terminé.")
