import os
import zipfile

ROOT = os.path.abspath(os.path.dirname(__file__))
OUT = os.path.join(ROOT, 'tv-test-analyzer.zip')

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        # skip __pycache__ and .git
        if '__pycache__' in root or '.git' in root:
            continue
        for file in files:
            full = os.path.join(root, file)
            rel = os.path.relpath(full, start=path)
            ziph.write(full, arcname=rel)

if __name__ == '__main__':
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        zipdir(ROOT, z)
    print('Created', OUT)
