# Copyright (c) 2025 MARCEL DINLA
# Tous droits réservés. 

import os
from modules import fonction as fc
from modules.integrite import verify_signature
from modules.license_check import verify_license
from modules.fonction import Couleurs
import sys

try:
    import readline
except ImportError:
    pass

if __name__ == '__main__' :
    
    
    if not verify_signature():
        print(Couleurs.ROUGE_SOMBRE,"\n🚫 Programme modifié ou non authentique !\n", Couleurs.RESET)
        sys.exit()

    verify_license()
    try :
      fc.afficher_accueil()
    
      if not os.path.exists('Data'):
        os.makedirs('Data')
      donnees = fc.load_ini()

      
      fc.afficher_menu_principal()
      fc.menu_principal(donnees)
    except KeyboardInterrupt :
       print("\n\nInterruption du prgramme détectée... !")
    except Exception as e :
       print(f"\n\nArrêt du programme. Erreur : {e}")