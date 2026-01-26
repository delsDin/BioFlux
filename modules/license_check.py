from pathlib import Path
from datetime import datetime
import json, sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from modules.fonction import Couleurs

BASE_DIR = Path(__file__).resolve().parent.parent

LICENSE_FILE = BASE_DIR / "license.json"
LICENSE_SIG = BASE_DIR / "license.sig"
PUBLIC_KEY = BASE_DIR / "public_key.pem"

def verify_license():
    data = LICENSE_FILE.read_bytes()
    signature = LICENSE_SIG.read_bytes()

    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY.read_bytes()
    )

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except Exception:
        print(Couleurs.ROUGE_SOMBRE,"\n🚫 Licence invalide\n", Couleurs.RESET)
        sys.exit(1)

    lic = json.loads(data)

    if datetime.now() > datetime.fromisoformat(lic["expiry"]):
        print(Couleurs.ROUGE_SOMBRE,"\n⏰ Licence expirée\n", Couleurs.RESET)
        sys.exit(1)