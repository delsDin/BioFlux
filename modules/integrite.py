from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PUBLIC_KEY_FILE = BASE_DIR / "public_key.pem"
SIGNATURE_FILE = BASE_DIR / "signature.sig"

FILES_TO_VERIFY = [
    BASE_DIR / "main.py",
    BASE_DIR / "README.md",
    BASE_DIR / "modules" / "integrite.py",
    BASE_DIR / "modules" / "fonction.py",
    BASE_DIR / "modules" / "statistiques.py",
    BASE_DIR / "modules" / "tendance.py",
    BASE_DIR / "modules" / "license_check.py",
]

def verify_signature() -> bool:
    try:
        # Charger clé publique
        with open(PUBLIC_KEY_FILE, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        # Recalcul du hash
        digest = hashes.Hash(hashes.SHA256())
        for file in FILES_TO_VERIFY:
            if not file.exists():
                print(f"❌ Fichier manquant : {file.name}")
                return False
            digest.update(file.read_bytes())

        # Charger signature
        with open(SIGNATURE_FILE, "rb") as f:
            signature = f.read()

        # Vérification
        public_key.verify(
            signature,
            digest.finalize(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except Exception:
        return False
