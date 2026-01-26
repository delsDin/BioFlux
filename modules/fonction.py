# Copyright (c) 2025 MARCEL DINLA
# Tous droits réservés.
import json
import csv
from datetime import datetime,  timedelta
import time
import glob
import os
import sys

from modules import statistiques as stat
from modules import tendance as tend

class Couleurs:
        RESET = '\033[0m'
        VERT = '\033[92m'
        CYAN = '\033[96m'
        JAUNE = '\033[93m'
        ROSE = '\033[95m'
        BLEU = '\033[94m'
        GRAS = '\033[1m'
        ROUGE = '\033[91m'
        ROUGE_SOMBRE = '\033[31m'


# ============================================
# Charger les données au demarrage
# ============================================
def load_ini() :
    """
    Charger les anciennes au demarrage du programme
    """
    fichier = "Data/ini.json"
    try:
        if not os.path.exists(fichier):
            #print(Couleurs.ROUGE,f"\n⚠️ Fichier {fichier} corrompu !", Couleurs.RESET)
            return {}
        with open(fichier, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        return donnees
    except json.JSONDecodeError:
        #print(Couleurs.ROUGE,f"\n⚠️ Fichier {fichier} corrompu !", Couleurs.RESET)
        return {}
    except Exception as e:
        #print(Couleurs.ROUGE,f"\n⚠️ Fichier {fichier} corrompu ! Erreur : {e}", Couleurs.RESET)
        return {}


# ============================================
# Affiche un écran d'accueil au démarrage
# ============================================
def afficher_accueil():
    """Affiche un écran d'accueil au démarrage"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "═"*60)
    print("🌟 BIENVENUE DANS VOTRE CALCULATRICE DE STATISTIQUES 🌟")
    print("═"*60)
    
    print("\n📋 Cette application vous permet de :")
    print("   • Suivre votre sommeil quotidien")
    print("   • Enregistrer vos activités sportives")
    print("   • Contrôler vos dépenses")
    print("   • Analyser vos tendances et habitudes")
    
    print("\n🎯 Pour commencer :")
    print("   • Utilisez 'Saisir des données' pour votre première entrée")
    print("   • Consultez 'Aide' pour plus d'informations")
    print("   • Vos données sont automatiquement sauvegardées")
    
    print("\n" + "═"*60)

    input("\nAppuyez sur Entrée pour continuer vers le menu principal...")


# ============================================
# Affiche le menu principal avec un tableau stylisé
# ============================================
def afficher_menu_principal(nb_jours=0):  # Ajouter paramètre optionnel
    """Affiche le menu principal avec un tableau stylisé"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    largeur = 50
    
    titre = "CALCULATRICE DE STATISTIQUES PERSONNELLES"
    espace_titre = (largeur - len(titre)) // 2
    
    print(f"{Couleurs.CYAN}{Couleurs.GRAS}")
    print("╔" + "═" * (largeur - 2) + "╗")
    print("║" + " " * espace_titre + titre + " " * (largeur - 2 - espace_titre - len(titre)) + "║")
    
    date_actuelle = datetime.now().strftime("%d/%m/%Y")
    ligne_date = f"      {date_actuelle}      "
    espace_date = (largeur - len(ligne_date)) // 2
    print("║" + " " * espace_date + ligne_date + " " * (largeur - 2 - espace_date - len(ligne_date)) + "║")
    
    print("╠" + "═" * (largeur - 2) + "╣")
    
    options = [
        ("1. Saisir des données du jour", Couleurs.VERT),
        ("2. Voir mes statistiques", Couleurs.CYAN),
        ("3. Consulter une date spécifique", Couleurs.JAUNE),
        ("4. Afficher les tendances", Couleurs.ROSE),
        ("5. Gérer les données", Couleurs.BLEU),
        ("6. Aide / Instructions", Couleurs.CYAN),
        ("7. Quitter", Couleurs.VERT)
    ]
    
    for option, couleur in options:
        espace = (largeur - len(option) - 3)
        print(f"║ {couleur}{option}{Couleurs.RESET}{Couleurs.CYAN}" + " " * espace + "║")
    
    print("╚" + "═" * (largeur - 2) + "╝")
    print(Couleurs.RESET)
    
    # Afficher le nombre de jours enregistrés
    if nb_jours > 0:
        print(f"\n📊 {nb_jours} jour(s) enregistré(s)")


# ============================================
# Menu principal interactif de l'application
# ============================================
def menu_principal(donnees):
    """
    Menu principal interactif de l'application
    """
    while True:
        afficher_menu_principal(len(donnees))  # Passer le nombre de jours
        choix = input("\nVotre choix : ").strip()
        
        try:  
            if choix == "1":
                # Saisir des données du jour
                resultat = saisir_donnees()  # ← RÉCUPÉRER LE RÉSULTAT
                
                if resultat:  # Si l'utilisateur a confirmé
                    date_str, donnees_jour = resultat
                    donnees[date_str] = donnees_jour  # ← AJOUTER AU DICTIONNAIRE
                    print(f"\n✅ Données enregistrées pour le {date_str}")
                    
                    # Sauvegarder automatiquement
                    sauvegarder_json_avec_rotation(donnees, "donnees.json")
                
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "2":
                # Voir mes statistiques
                #print(Couleurs.VERT,"\n📈 Fonctionnalité en cours de développement...", Couleurs.RESET)
                #input("\nAppuyez sur Entrée pour continuer...")
                stat.voir_statistiques(donnees)
            
            elif choix == "3":
                # Consulter une date spécifique
                consulter_date_avance(donnees)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                # Afficher les tendances
                tend.menu_tendances(donnees)
                input("\nAppuyez sur Entrée pour continuer...")
                # menu_tendances(donnees)
            
            elif choix == "5":
                # Gérer les données
                donnees = menu_gestion_donnees(donnees, fichier = "donnees.json")
                
                # Sauvegarder après la gestion
                sauvegarder_json(donnees, fichier = "donnees.json")
                
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                # Aide / Instructions
                afficher_aide()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "7":
                # Quitter
                quitter_application_amelioree(donnees, fichier="Data/ini.json")
                break
            
            elif choix.lower() in ['q', 'quit', 'exit', 'quitter']:
                # Quitter avec raccourci
                quitter_application_amelioree(donnees, fichier="Data/ini.json")
                break
            
            elif choix == "":
                # Entrée vide
                continue
        
            else:
                print(f"\n❌ Choix '{choix}' invalide. Veuillez choisir entre 1 et 7.")
                input("\nAppuyez sur Entrée pour continuer...")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption détectée...")
            quitter_application_amelioree(donnees, fichier="donnees.json")
            break
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
            input("\nAppuyez sur Entrée pour continuer...")


# ============================================
# Saisie des données journalières avec validation
# ============================================
def saisir_donnees():
    """
    Saisie des données journalières avec validation
    """
    from datetime import date
    # 1. Gestion de la date
    aujourdhui = date.today()
    print(f"\nDate du jour : {aujourdhui}")
    
    changer_date = input("Saisir pour une autre date ? (o/N) : ").strip()
    if changer_date.lower() == 'o':
        while True:
            try:
                date_str = input("Date (format AAAA-MM-JJ) : ").strip()
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if date > aujourdhui:
                    print("❌ Date future non autorisée")
                    continue
                break
            except ValueError:
                print("❌ Format invalide. Utilisez AAAA-MM-JJ")
    else:
        date = aujourdhui
    
    date_str = str(date)  # ← IMPORTANT : Convertir en string
    
    # 2. Interface
    print("\n" + "═"*50)
    print(f"   SAISIE DES DONNÉES - {date}")
    print("═"*50)
    
    # 3. Saisie du SOMMEIL
    print("\n😴 SOMMEIL")
    sommeil = {}
    
    try:
        duree_str = input("   Durée (heures, ex: 7.5) : ").strip()
        if duree_str:
            duree = float(duree_str)
            if 0 <= duree <= 24:
                sommeil["duree"] = duree
            else:
                print("⚠️  Durée invalide, ignorée")
    except ValueError:
        print("⚠️  Valeur numérique invalide, ignorée")
    
    try:
        qualite_str = input("   Qualité (1-10, vide si non renseigné) : ").strip()
        if qualite_str:
            qualite = int(qualite_str)
            if 1 <= qualite <= 10:
                sommeil["qualite"] = qualite
            else:
                print("⚠️  Qualité doit être entre 1 et 10")
    except ValueError:
        print("⚠️  Valeur numérique invalide, ignorée")
    
    # 4. Saisie du SPORT
    print("\n🏃 ACTIVITÉ SPORTIVE")
    sport = {}
    
    sport_type = input("   Type (course, marche, vélo, etc.) : ").strip()
    if sport_type:
        sport["type"] = sport_type
    
    try:
        duree_sport_str = input("   Durée (minutes, vide si 0) : ").strip()
        if duree_sport_str:
            duree_sport = int(duree_sport_str)
            if duree_sport >= 0:
                sport["duree"] = duree_sport
            else:
                print("⚠️  Durée négative invalide")
    except ValueError:
        print("⚠️  Valeur numérique invalide, ignorée")
    
    intensite = input("   Intensité (faible, moyenne, élevée) : ").strip()
    if intensite:
        sport["intensite"] = intensite
    
    # 5. Saisie des DÉPENSES
    print("\n💰 DÉPENSES")
    depenses = []
    
    ajouter_depense = input("   Ajouter une dépense ? (O/N) : ").strip().lower()
    
    if ajouter_depense in ['o', 'oui', 'y', 'yes']:
        while True:
            print(f"\n   Dépense #{len(depenses) + 1}")
            categorie = input("   Catégorie (nourriture, transport, etc.) : ").strip()
            
            if not categorie:
                print("⚠️  Catégorie vide, arrêt de la saisie des dépenses")
                break
            
            try:
                montant_str = input("   Montant ($) : ").strip()
                if not montant_str:
                    print("⚠️  Montant obligatoire, dépense annulée")
                    continue
                
                montant = float(montant_str)
                if montant <= 0:
                    print("⚠️  Montant doit être positif")
                    continue
            except ValueError:
                print("❌ Montant invalide")
                continue
            
            description = input("   Description (optionnel) : ").strip()
            
            depense = {
                "categorie": categorie,
                "montant": montant
            }
            if description:
                depense["description"] = description
            
            depenses.append(depense)
            
            continuer = input("\n   Ajouter une autre dépense ? (O/N) : ").strip().lower()
            
            if continuer not in ['o', 'oui', 'y', 'yes']:
                break
    
    # 6. Création de la structure finale
    donnees_jour = {
        "sommeil": sommeil,
        "sport": sport,
        "depenses": depenses
    }
    
    # 7. Aperçu avant confirmation
    print("\n" + "═"*50)
    print("📋 APERÇU DES DONNÉES SAISIES")
    print("═"*50)
    
    if sommeil:
        duree_sommeil = sommeil.get('duree', 'Non renseigné')
        qualite_sommeil = sommeil.get('qualite', 'Non renseigné')
        print(f"😴 Sommeil : {duree_sommeil} H, Qualité : {qualite_sommeil}/10")
    else:
        print("😴 Sommeil : Non renseigné")
    
    if sport:
        type_sport = sport.get('type', 'Non spécifié')
        duree_sport = sport.get('duree', 0)
        print(f"🏃 Sport : {type_sport}, {duree_sport} minutes")
    else:
        print("🏃 Sport : Aucune activité")
    
    if depenses:
        total = sum(d['montant'] for d in depenses)
        print(f"💰 Dépenses : {len(depenses)} transaction(s), Total : {total:.2f}$")
    else:
        print("💰 Dépenses : Aucune dépense")
    
    # 8. Confirmation - PARTIE CORRIGÉE
    print("\n" + "═"*50)
    confirmer = input("Confirmer l'enregistrement ? (O/N) : ")
    confirmer = confirmer.strip().lower()
    
    if confirmer in ['o', 'oui', 'y', 'yes']:
        print("✅ Enregistrement effectué avec succès...")
        print(f"📅 Date : {date_str}")
        return (date_str, donnees_jour)  # ← RETOURNER UN TUPLE (date, données)
    else:
        print("❌ Saisie annulée")
        return None  # ← RETOURNER None si annulé


# ============================================
# MENU DE GESTION DES DONNÉES
# ============================================
def menu_gestion_donnees(donnees, fichier="donnees.json"):
    """
    Menu complet de gestion des données
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("═"*60)
        print(Couleurs.GRAS, Couleurs.BLEU)
        print("📂 GESTION DES DONNÉES")
        print(Couleurs.RESET)
        print("═"*60)
        
        # Afficher des infos sur les données actuelles
        if donnees:
            print(f"\n📊 État actuel : {len(donnees)} jour(s) enregistré(s)")
            dates = sorted(donnees.keys())
            print(f"📅 Période : {dates[0]} à {dates[-1]}")
        else:
            print("\n📭 Aucune donnée actuellement en mémoire")
        
        print("\n" + "─"*60)
        print(Couleurs.GRAS)
        print("SAUVEGARDE & CHARGEMENT")
        print(Couleurs.RESET)
        print("─"*60)
        print(Couleurs.VERT)
        print("\t1. 💾 Sauvegarder les données (JSON)")
        print("\t2. 📂 Charger des données (JSON)")
        print("\t3. 📤 Exporter en CSV")
        print("\t4. 📥 Importer depuis CSV")
        print("\t5. 🔄 Exporter en CSV séparés (sommeil, sport, dépenses)")
        print(Couleurs.RESET)
        
        print("\n" + "─"*60)
        print(Couleurs.GRAS)
        print("BACKUP & RESTAURATION")
        print(Couleurs.RESET)
        print("─"*60)
        print("\t6. 💼 Créer un backup complet")
        print("\t7. 📋 Lister les backups disponibles")
        print("\t8. ♻️  Restaurer depuis un backup")
        print("\t9. 🗑️  Supprimer les anciens backups")
        
        print("\n" + "─"*60)
        print(Couleurs.GRAS)
        print("MAINTENANCE")
        print(Couleurs.RESET)
        print("─"*60)
        print(Couleurs.CYAN)
        print("\t10. 🧹 Nettoyer les données (supprimer dates vides)")
        print("\t11. 🔍 Vérifier l'intégrité des données")
        print("\t12. 📊 Afficher les statistiques des fichiers")
        print("\t13. 🗑️  Supprimer TOUTES les données en mémoire")
        print("\t14. 💣  Supprimer TOUTES vos données")
        print(Couleurs.RESET)
        
        print("\n" + "─"*60)
        print("\t15. ↩️  Retour au menu principal")
        print("═"*60)
        
        choix = input("\nVotre choix : ").strip()
        
        try:
            if choix == "1":
                # Sauvegarder JSON
                print("\n💾 SAUVEGARDE JSON")
                if donnees :
                    nom_fichier = input(f"\nNom du fichier [{fichier}] : ").strip()
                    if not nom_fichier:
                        nom_fichier = fichier
                
                    if sauvegarder_json(donnees, f"Data/{nom_fichier}"):
                        print(f"✅ Sauvegarde réussie dans {nom_fichier}")
                    else:
                        print(Couleurs.ROUGE, "❌ Échec de la sauvegarde", Couleurs.RESET)
                else :
                    print(Couleurs.ROUGE,"\nAucune donnée disponible pour l'export", Couleurs.RESET)

                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "2":
                # Charger JSON
                print("\n📂 CHARGEMENT JSON")
                nom_fichier = input(f"\nNom du fichier [par defaut {fichier}] : ").strip()
                if not nom_fichier:
                    nom_fichier = fichier
                
                if os.path.exists(f"Data/{nom_fichier}"):
                    donnees_chargees = charger_json(f"Data/{nom_fichier}")
                    
                    if donnees_chargees:
                        print(f"\n📊 {len(donnees_chargees)} jour(s) trouvé(s)")
                        
                        if donnees:
                            print("\n⚠️  Vous avez déjà des données en mémoire")
                            print("\t1. Remplacer les données actuelles")
                            print("\t2. Fusionner avec les données actuelles")
                            print("\t3. Annuler")
                            
                            action = input("\nVotre choix : ").strip()
                            
                            if action == "1":
                                donnees.clear()
                                donnees.update(donnees_chargees)
                                print("✅ Données remplacées")
                            elif action == "2":
                                donnees.update(donnees_chargees)
                                print("✅ Données fusionnées")
                            else:
                                print("❌ Chargement annulé")
                        else:
                            donnees.update(donnees_chargees)
                            print("✅ Données chargées")
                    else:
                        print("❌ Aucune donnée trouvée dans le fichier")
                else:
                    print(f"❌ Fichier {nom_fichier} introuvable")
                
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "3":
                # Exporter CSV
                print("\n📤 EXPORT CSV")
                if donnees :
                    nom_fichier = input("Nom du fichier [ Par defaut donnees.csv] : ").strip()
                    if not nom_fichier:
                        nom_fichier = "Data/donnees.csv"
                
                    if sauvegarder_csv(nom_fichier, donnees):
                        print(f"✅ Export réussi dans {nom_fichier}")
                    else:
                        print("❌ Échec de l'export")
                else :
                    print(Couleurs.ROUGE,"\nAucune donnée disponible pour l'export", Couleurs.RESET)

                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                # Importer CSV
                print("\n📥 IMPORT CSV")
                file = nom_fichier = input("Nom du fichier [Par défaut donnees.csv] : ").strip()
                if not nom_fichier:
                    file = "donnees.csv"
                    nom_fichier = "Data/donnees.csv"
                
                if os.path.exists(nom_fichier):
                    donnees_csv = charger_csv(nom_fichier)
                    
                    if donnees_csv:
                        print(f"\n📊 {len(donnees_csv)} données trouvé(s)")
                        
                        if donnees:
                            print("\n⚠️  Fusionner avec les données actuelles ?")
                            confirmer = input("(O/N) : ").strip().lower()
                            if confirmer in ['o', 'oui', 'y', 'yes']:
                                donnees.update(donnees_csv)
                                print("✅ Données importées et fusionnées")
                            else:
                                print("❌ Import annulé")
                        else:
                            donnees.update(donnees_csv)
                            print("✅ Données importées")
                    else:
                        print("❌ Aucune donnée trouvée")
                else:
                    print(f"❌ Fichier {file} introuvable")
                
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "5":
                # Export CSV séparés
                print("\n📤 EXPORT CSV SÉPARÉS")
                if donnees :
                    dossier = input("\nNom du dossier [Par défaut export] : ").strip()
                    if not dossier:
                        dossier = "export"
                    
                    exporter_vers_csv_separe(dossier, donnees)
                else :
                    print(Couleurs.ROUGE,"\nAucune donnée disponible pour l'export", Couleurs.RESET)
                    
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                # Créer backup
                print("\n💼 CRÉATION DE BACKUP")
                if donnees :
                    dossier = input("\nDossier de backup [Par defaut backups] : ").strip()
                    if not dossier:
                        dossier = "Data/backups"
                    
                    fichier_backup = generer_backup_complet(donnees, dossier)
                    
                    if fichier_backup:
                        print(f"\n✅ Backup créé avec succès !")
                    else:
                        print(Couleurs.ROUGE, "\n❌ Échec de la création du backup", Couleurs.RESET)
                else :
                      print(Couleurs.ROUGE, "\n❌ Échec de la création du backup : Aucune donnée en mémoire !", Couleurs.RESET)

                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "7":
                # Lister backups
                print("\n📋 LISTE DES BACKUPS")
                dossier = "Data/backups"
                lister_backups(dossier)
                
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "8":
                # Restaurer backup
                print("\n♻️  RESTAURATION DE BACKUP")
                dossier = "Data/backups"

                restaurer_backup(dossier, donnees)

                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "9":
                # Supprimer anciens backups
                print("\n🗑️  NETTOYAGE DES BACKUPS")
                dossier = "Data/backups"
                supprimer_anciens_backups(dossier)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "10":
                # Nettoyer données
                print("\n🧹 NETTOYAGE DES DONNÉES")
                
                nettoyer_donnees(donnees)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "11":
                # Vérifier intégrité
                print("\n🔍 VÉRIFICATION DE L'INTÉGRITÉ")
                
                verifier_integrite(donnees)
                
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "12":
                statistiques_fichiers()
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "13":
                # Supprimer toutes les données en mémoire
                supprimer_donnees_memoire(donnees)
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "14":
                # Supprimer TOUTES les données utilisateur (fichiers + mémoire)
                print("\n💣 SUPPRESSION TOTALE DE TOUTES LES DONNÉES UTILISATEUR")
                supprimer_donnees_complet(donnees)
                input("\nAppuyez sur Entrée pour continuer...")    

            elif choix == "15":
                # Retour
                print("\n↩️  Retour au menu principal...")
                break
            
            elif choix.lower() in ['q', 'quitter', 'exit', 'e'] :
                # Retour
                print("\n↩️  Retour au menu principal...")
                break
           
            else:
                print("\n❌ Choix invalide")
                input("\nAppuyez sur Entrée pour continuer...")
        
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            import traceback
            traceback.print_exc()
            input("\nAppuyez sur Entrée pour continuer...")
    
    return donnees


# ============================================
# SAUVEGARDE AVEC FUSION DES DONNÉES
# ============================================
def sauvegarder_json(donnees, fichier="donnees.json"):
    """
    Sauvegarde avec fusion intelligente des données existantes
    """
    if donnees :
        try:
            # 1. Charger les données existantes
            donnees_existantes = {}
            if os.path.exists(fichier):
                try:
                    with open(fichier, 'r', encoding='utf-8') as f:
                        donnees_existantes = json.load(f)
                    print(f"\n📂 {len(donnees_existantes)} donnée(s) existante(s) chargée(s)")
                except json.JSONDecodeError:
                    print("⚠️  Fichier existant corrompu, création d'un nouveau")
                    donnees_existantes = {}
            
            # 2. Fusionner avec les nouvelles données
            # Les nouvelles données écrasent les anciennes pour la même date
            donnees_existantes.update(donnees)
            
            # 3. Sauvegarder le tout
            with open(fichier, 'w', encoding='utf-8') as f:
                json.dump(donnees_existantes, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Données sauvegardées : {len(donnees_existantes)} jour(s) total")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde JSON : {e}")
            return False
    else :
        print("Aucune donnée en mémoire !")


# ============================================
# Sauvegarde avec rotation des backups (garde les N derniers)
# ============================================
def sauvegarder_json_avec_rotation(donnees, fichier="Data/donnees.json", max_backups=10):
    """
    Sauvegarde avec rotation des backups (garde les N derniers)
    """
    try:
        dossier_backup = "Data/backups"
        
        # Créer le dossier backup s'il n'existe pas
        if not os.path.exists(dossier_backup):
            os.makedirs(dossier_backup)
        
        # 1. Créer un backup si le fichier existe
        if os.path.exists(fichier):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fichier_backup = os.path.join(dossier_backup, f"Data/donnees_{timestamp}.json")
            
            import shutil
            shutil.copy2(fichier, fichier_backup)
            print(f"💾 Backup créé : {fichier_backup}")
            
            # 2. Gérer la rotation (supprimer les vieux backups)
            backups = sorted(glob.glob(os.path.join(dossier_backup, "Data/donnees_*.json")))
            
            if len(backups) > max_backups:
                # Supprimer les plus anciens
                for vieux_backup in backups[:-max_backups]:
                    os.remove(vieux_backup)
                    print(f"🗑️  Ancien backup supprimé : {os.path.basename(vieux_backup)}")
        
        # 3. Charger et fusionner
        donnees_existantes = {}
        if os.path.exists(fichier):
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    donnees_existantes = json.load(f)
            except:
                pass
        
        donnees_existantes.update(donnees)
        
        # 4. Sauvegarder
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(donnees_existantes, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Données sauvegardées : {len(donnees_existantes)} jour(s)")
        
        # Afficher le nombre de backups
        backups_restants = len(glob.glob(os.path.join(dossier_backup, "Data/donnees_*.json")))
        print(f"📦 {backups_restants} backup(s) disponible(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        return False


# ============================================
# Charge les données depuis un fichier JSON
# ============================================
def charger_json(fichier):
    
    try:
        if not os.path.exists(fichier):
            print(f"\n📁 Fichier {fichier} non trouvé. Création d'une nouvelle structure.")
            return {}
        
        with open(fichier, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
        
        print(f"\n📂 {len(donnees)} données chargées depuis {fichier}")
        return donnees
    except json.JSONDecodeError:
        print(f"\n⚠️ Fichier {fichier} corrompu !")
        return {}
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement JSON : {e}")
        return {}


# ============================================
# Sauvegarde les données au format CSV   
# ============================================
def sauvegarder_csv(fichier, donnees):
    
    try:
        with open(fichier, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # En-tête
            writer.writerow(['date', 'sommeil_duree', 'sommeil_qualite', 
                           'sport_type', 'sport_duree', 'sport_intensite',
                           'depenses_categories', 'depenses_montants'])
            if donnees :
                for date_str, valeurs in donnees.items():
                    # Récupération des données sommeil
                    sommeil_duree = valeurs.get('sommeil', {}).get('duree', '')
                    sommeil_qualite = valeurs.get('sommeil', {}).get('qualite', '')
                    
                    # Récupération des données sport
                    sport_type = valeurs.get('sport', {}).get('type', '')
                    sport_duree = valeurs.get('sport', {}).get('duree', '')
                    sport_intensite = valeurs.get('sport', {}).get('intensite', '')
                    
                    # Récupération des dépenses
                    depenses = valeurs.get('depenses', [])
                    categories = []
                    montants = []
                    
                    for depense in depenses:
                        categories.append(depense.get('categorie', ''))
                        montants.append(str(depense.get('montant', 0)))
                    
                    # Écriture de la ligne
                    writer.writerow([
                        date_str,
                        sommeil_duree,
                        sommeil_qualite,
                        sport_type,
                        sport_duree,
                        sport_intensite,
                        '|'.join(categories),  # Séparateur pour multiples dépenses
                        '|'.join(montants)
                    ])
                print(f"✅ Données sauvegardées dans {fichier} (CSV)")
                return True
            else :
                print("\nAucune données à sauvegarder !")
                return False
    
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde CSV : {e}")
        return False


# ============================================
# Exporte les données vers plusieurs fichiers CSV spécialisés
# ============================================
def exporter_vers_csv_separe(dossier, donnees):
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(dossier):
        os.makedirs(dossier)
    
    # Fichier sommeil
    with open(f"{dossier}/sommeil.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'duree_heures', 'qualite'])
        
        for date_str, valeurs in donnees.items():
            sommeil = valeurs.get('sommeil', {})
            if sommeil:
                writer.writerow([
                    date_str,
                    sommeil.get('duree', ''),
                    sommeil.get('qualite', '')
                ])
    
    # Fichier sport
    with open(f"{dossier}/sport.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'type', 'duree_minutes', 'intensite'])
        
        for date_str, valeurs in donnees.items():
            sport = valeurs.get('sport', {})
            if sport:
                writer.writerow([
                    date_str,
                    sport.get('type', ''),
                    sport.get('duree', ''),
                    sport.get('intensite', '')
                ])
    
    # Fichier dépenses détaillé
    with open(f"{dossier}/depenses_detaille.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'categorie', 'montant'])
        
        for date_str, valeurs in donnees.items():
            depenses = valeurs.get('depenses', [])
            for depense in depenses:
                writer.writerow([
                    date_str,
                    depense.get('categorie', ''),
                    depense.get('montant', '')
                ])
    
    print(f"📤 Données exportées dans le dossier '{dossier}'")


# ============================================
# Charge les données depuis un fichier CSV
# ============================================
def charger_csv(fichier):
    
    donnees = {}
    
    try:
        if not os.path.exists(fichier):
            print(f"📁 Fichier {fichier} non trouvé.")
            return donnees
        
        with open(fichier, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for ligne in reader:
                date_str = ligne['date']
                
                # Construction de la structure sommeil
                sommeil = {}
                if ligne['sommeil_duree']:
                    sommeil['duree'] = float(ligne['sommeil_duree'])
                if ligne['sommeil_qualite']:
                    sommeil['qualite'] = int(ligne['sommeil_qualite'])
                
                # Construction de la structure sport
                sport = {}
                if ligne['sport_type']:
                    sport['type'] = ligne['sport_type']
                if ligne['sport_duree']:
                    sport['duree'] = int(ligne['sport_duree'])
                if ligne['sport_intensite']:
                    sport['intensite'] = ligne['sport_intensite']
                
                # Construction de la liste des dépenses
                depenses = []
                if ligne['depenses_categories'] and ligne['depenses_montants']:
                    categories = ligne['depenses_categories'].split('|')
                    montants = ligne['depenses_montants'].split('|')
                    
                    for cat, mont in zip(categories, montants):
                        if cat and mont:  # Vérifier que les champs ne sont pas vides
                            depenses.append({
                                'categorie': cat,
                                'montant': float(mont)
                            })
                
                # Construction de l'entrée complète
                donnees[date_str] = {
                    'sommeil': sommeil if sommeil else {},
                    'sport': sport if sport else {},
                    'depenses': depenses
                }
        
        print(f"📂 {len(donnees)} jours chargés depuis {fichier} (CSV)")
        return donnees
    except Exception as e:
        print(f"❌ Erreur lors du chargement CSV : {e}")
        return {}


# ============================================
# Affiche les instructions d'utilisation
# ============================================
def afficher_aide():
    """Affiche les instructions d'utilisation"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{'═'*60}")
    print("ℹ️   AIDE & INSTRUCTIONS")
    print(f"{'═'*60}")
    
    print("\n📋 FONCTIONNALITÉS PRINCIPALES :")
    print("─" * 40)
    print("1. 📊 Saisir des données")
    print("   • Enregistrez votre sommeil, activité sportive et dépenses")
    print("   • Plusieurs dépenses peuvent être ajoutées par jour")
    print("   • La date du jour est utilisée par défaut")
    
    print("\n2. 📈 Voir mes statistiques")
    print("   • Moyennes, minimums, maximums")
    print("   • Totaux par catégorie")
    print("   • Comparaisons par période")
    
    print("\n3. 📅 Consulter une date spécifique")
    print("   • Recherchez une date précise")
    print("   • Navigation entre les jours")
    print("   • Modification des données existantes")
    
    print("\n4. 📊 Afficher les tendances")
    print("   • Évolution sur 7, 30 jours")
    print("   • Graphiques ASCII")
    print("   • Détection des habitudes")
    
    print("\n5. 📂 Gérer les données")
    print("   • Import/Export CSV/JSON")
    print("   • Sauvegarde et restauration")
    print("   • Nettoyage des données")
    
    print(f"\n{'─'*40}")
    print("🎯 CONSEILS D'UTILISATION :")
    print("• Saisissez vos données quotidiennement pour des statistiques précises")
    print("• Utilisez les mêmes catégories pour les dépenses")
    print("• Exportez régulièrement vos données en backup")
    print("• Consultez les tendances hebdomadaires pour ajuster vos habitudes")
    
    print(f"\n{'═'*60}")


# ============================================
# Version améliorée avec meilleure gestion d'erreurs
# ============================================
def quitter_application_amelioree(donnees, fichier="Data/ini.json"):
    """
    Version améliorée avec meilleure gestion d'erreurs
    """
    print("\n" + "═"*50)
    print("👋 MERCI D'AVOIR UTILISÉ NOTRE APPLICATION !")
    print("═"*50)
    
    # Demander si l'utilisateur veut sauvegarder
    if donnees:
        
        try:
            
            # 1. Charger les données existantes
            donnees_existantes = {}
            if os.path.exists(fichier):
                try:
                    with open(fichier, 'r', encoding='utf-8') as f:
                        donnees_existantes = json.load(f)
                    print(f"\n📂 {len(donnees_existantes)} donnée(s) existante(s) chargée(s)")
                except json.JSONDecodeError:
                    print("⚠️  Fichier existant corrompu")
                    donnees_existantes = {}
            
            # 2. Fusionner avec les nouvelles données
            # Les nouvelles données écrasent les anciennes pour la même date
            donnees_existantes.update(donnees)
            
            # 3. Sauvegarder le tout
            with open(fichier, 'w', encoding='utf-8') as f:
                json.dump(donnees_existantes, f, indent=2, ensure_ascii=False)
            return True
                   
        except Exception as e:
            print(Couleurs.ROUGE,f"❌ Erreur lors de la sauvegarde : {e}", Couleurs.RESET)
            
            # Tentative de sauvegarde d'urgence
            try:
                fichier_urgence = f"Data/donnees_urgence_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(fichier_urgence, 'w', encoding='utf-8') as f:
                    json.dump(donnees, f, indent=2, ensure_ascii=False)
                print(f"💾 Sauvegarde d'urgence créée : {fichier_urgence}")
            except:
                print(Couleurs.ROUGE_SOMBRE,"❌ Impossible de sauvegarder. Vos données seront perdues.", Couleurs.RESET)
        
    
    # Résumé des données
    print("\n📊 Résumé de votre session :")
    if donnees:
        dates = sorted(donnees.keys())
        print(f"• Période : {dates[0]} à {dates[-1]}")
        print(f"• Total : {len(donnees)} jour(s) enregistré(s)")
        
        # Statistiques rapides
        jours_sommeil = sum(1 for d in donnees.values() if d.get('sommeil'))
        jours_sport = sum(1 for d in donnees.values() if d.get('sport') and d['sport'])
        
        total_depenses = 0
        for jour in donnees.values():
            if jour.get('depenses'):
                total_depenses += sum(dep.get('montant', 0) for dep in jour['depenses'])
        
        print(f"• Sommeil : {jours_sommeil} jour(s)")
        print(f"• Sport : {jours_sport} jour(s)")
        print(f"• Dépenses : {total_depenses:.2f}$")
    else:
        print("• Aucune donnée enregistrée durant cette session")
    
    print(f"\n{'═'*50}")
    print("À bientôt ! 😊", end="")
    for _ in range(10):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.5)

    print("\n" + "═"*50 + "\n")


# ============================================
# Crée un fichier de backup avec timestamp
# ============================================
def generer_backup_complet(donnees, dossier):
    """
    Crée un backup avec gestion robuste des erreurs
    """
    
    try:
        # Vérifier et créer le dossier
        print(f"Création du dossier {dossier} ", end="")
        for _ in range(5):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.5)
        print("\n")
        if not os.path.exists(dossier):
            os.makedirs(dossier)
            print(f"\n📁 Dossier créé: {dossier}")
        
        # Générer un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fichier_backup = os.path.join(dossier, f"backup_{timestamp}.json")
        
        # Écrire les données
        with open(fichier_backup, 'w', encoding='utf-8') as fichier:
            json.dump(donnees, fichier, indent=2, ensure_ascii=False)
        
        # Vérifier que le fichier a bien été créé
        if os.path.exists(fichier_backup):
            taille = os.path.getsize(fichier_backup)
            print(f"✅ Backup réussi!")
            print(f"Fichier: {fichier_backup}")
            print(f"Taille: {taille} octets")
            return fichier_backup
        else:
            print(Couleurs.ROUGE,"❌ Le fichier de backup n'a pas été créé", Couleurs.RESET)
            return None
            
    except PermissionError:
        print(Couleurs.ROUGE,"❌ Erreur de permission: Impossible d'écrire dans le dossier", Couleurs.RESET)
        return None
    except OSError as e:
        print(Couleurs.ROUGE,f"❌ Erreur système: {e}", Couleurs.RESET)
        return None
    except json.JSONDecodeError:
        print(Couleurs.ROUGE,"❌ Erreur: Les données ne peuvent pas être encodées en JSON", Couleurs.RESET)
        return None
    except Exception as e:
        print(Couleurs.ROUGE,f"❌ Erreur inattendue: {type(e).__name__}: {e}", Couleurs.RESET)
        return None


# ============================================
# Lister backups
# ============================================
def lister_backups(dossier):
    if os.path.exists(dossier):
        backups = sorted(glob.glob(os.path.join(dossier, "backup_*.json")), reverse=True)
        
        if backups:
            print(f"\n{len(backups)} backup(s) trouvé(s) :\n")
            for i, backup in enumerate(backups, 1):
                nom = os.path.basename(backup)
                taille = os.path.getsize(backup)
                date_modif = datetime.fromtimestamp(os.path.getmtime(backup))
                
                print(f"\t{i}. {nom}")
                print(f"\t   📅 {date_modif.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"\t   📦 {taille} octets")
                print()
        else:
            print("📭 Aucun backup trouvé")
    else:
        print(f"❌ Dossier {dossier} introuvable")


# ============================================
# Restaurer backup
# ============================================
def restaurer_backup(dossier, donnees) :

    if os.path.exists(dossier):
        backups = sorted(glob.glob(os.path.join(dossier, "backup_*.json")), reverse=True)
        
        if backups:
            print(f"\n{len(backups)} backup(s) disponible(s) :\n")
            for i, backup in enumerate(backups, 1):
                nom = os.path.basename(backup)
                date_modif = datetime.fromtimestamp(os.path.getmtime(backup))
                print(f"\t{i}. {nom} - {date_modif.strftime('%d/%m/%Y %H:%M')}")
            
            choix_backup = input("\nNuméro du backup à restaurer (0 pour annuler) : ").strip()
            
            try:
                num = int(choix_backup)
                if 1 <= num <= len(backups):
                    backup_choisi = backups[num-1]
                    
                    print(Couleurs.ROUGE,f"\n⚠️  Restaurer depuis {os.path.basename(backup_choisi)} ?", Couleurs.RESET)
                    if donnees:
                        print(Couleurs.ROUGE,"  Cela remplacera vos données actuelles !", Couleurs.RESET)
                    
                    confirmer = input("\nConfirmer ? (O/N) : ").strip().lower()
                    
                    if confirmer in ['o', 'oui', 'y', 'yes']:
                        print("Restauration en cours ", end="")
                        print("\n")
                        for _ in range(10):
                            sys.stdout.write(".")
                            sys.stdout.flush()
                            time.sleep(0.5)
                        donnees_backup = charger_json(backup_choisi)
                        
                        if donnees_backup:
                            donnees.clear()
                            donnees.update(donnees_backup)
                            print(f"✅ {len(donnees)} jour(s) restauré(s)")
                        else:
                            print(Couleurs.ROUGE_SOMBRE,"\n❌ Échec de la restauration. Aucune données trouvée !", Couleurs.RESET)
                    else:
                        print(Couleurs.ROUGE_SOMBRE,"\n❌ Restauration annulée", Couleurs.RESET)
                elif num == 0:
                    print(Couleurs.ROUGE_SOMBRE,"\n❌ Annulé", Couleurs.RESET)
                else:
                    print(Couleurs.ROUGE_SOMBRE,"\n❌ Numéro invalide", Couleurs.RESET)
            except ValueError:
                print(Couleurs.ROUGE_SOMBRE,"\n❌ Entrée invalide", Couleurs.RESET)
        else:
            print(Couleurs.ROUGE_SOMBRE,"\n📭 Aucun backup disponible", Couleurs.RESET)
    else:
        print(Couleurs.ROUGE_SOMBRE,f"\n❌ Dossier {dossier} introuvable", Couleurs.RESET)


# ============================================
# Supprimer anciens backups
# ============================================
def supprimer_anciens_backups(dossier) :
    if os.path.exists(dossier):
        backups = sorted(glob.glob(os.path.join(dossier, "backup_*.json")))
        
        if backups:
            print(f"\n{len(backups)} backup(s) trouvé(s)")
            garder = input("Combien voulez-vous garder ? [Par défaut 5] : ").strip()
            
            try:
                nb_garder = int(garder) if garder else 5
                
                if len(backups) > nb_garder:
                    a_supprimer = backups[:-nb_garder]
                    
                    print(Couleurs.ROUGE,f"\n⚠️  {len(a_supprimer)} backup(s) seront supprimé(s)", Couleurs.RESET)
                    confirmer = input("Confirmer ? (O/N) : ").strip().lower()
                    
                    if confirmer in ['o', 'oui', 'y', 'yes']:
                        print("", end="")

                        for _ in range(5):
                            sys.stdout.write(".")
                            sys.stdout.flush()
                            time.sleep(0.5)

                        for backup in a_supprimer:
                            os.remove(backup)
                            print(f"🗑️  Supprimé : {os.path.basename(backup)}")
                        print(f"\n✅ {len(a_supprimer)} backup(s) supprimé(s)")
                    else:
                        print(Couleurs.ROUGE_SOMBRE,"\n❌ Annulé", Couleurs.RESET)
                else:
                    print(Couleurs.ROUGE_SOMBRE,f"\nℹ️  Moins de {nb_garder} backups, rien à supprimer", Couleurs.RESET)
            except ValueError:
                print(Couleurs.ROUGE_SOMBRE,"\n❌ Nombre invalide", Couleurs.RESET)
        else:
            print(Couleurs.ROUGE_SOMBRE,"\n📭 Aucun backup trouvé", Couleurs.RESET)
    else:
        print(Couleurs.ROUGE_SOMBRE,f"\n❌ Dossier {dossier} introuvable", Couleurs.RESET)


# ============================================
# Nettoyer données
# ============================================            
def nettoyer_donnees(donnees) :
    dates_vides = []
    for date_str, valeurs in donnees.items():
        sommeil = valeurs.get('sommeil', {})
        sport = valeurs.get('sport', {})
        depenses = valeurs.get('depenses', [])
        
        if not sommeil and not sport and not depenses:
            dates_vides.append(date_str)
    
    if dates_vides:
        print(f"\n⚠️  {len(dates_vides)} date(s) vide(s) trouvée(s) :")
        for date in dates_vides[:5]:
            print(f"   • {date}")
        if len(dates_vides) > 5:
            print(f"   ... et {len(dates_vides)-5} autre(s)")
        
        confirmer = input("\nSupprimer ces dates ? (O/N) : ").strip().lower()
        
        if confirmer in ['o', 'oui', 'y', 'yes']:
            for date in dates_vides:
                del donnees[date]
            print(f"✅ {len(dates_vides)} date(s) supprimée(s)")
        else:
            print(Couleurs.ROUGE_SOMBRE,"\n❌ Nettoyage annulé", Couleurs.RESET)
    else:
        print("\n✅ Aucune date vide trouvée")


# ============================================
# Vérifier l'intégrité des données 
# ============================================  
def verifier_integrite(donnees) :
    problemes = []
                
    for date_str, valeurs in donnees.items():
        # Vérifier format date
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            problemes.append(f"Date invalide : {date_str}")
        
        # Vérifier structure sommeil
        if 'sommeil' in valeurs:
            sommeil = valeurs['sommeil']
            if 'duree' in sommeil:
                duree = sommeil['duree']
                if not isinstance(duree, (int, float)) or duree < 0 or duree > 24:
                    problemes.append(f"{date_str} : Durée sommeil invalide ({duree})")
            
            if 'qualite' in sommeil:
                qualite = sommeil['qualite']
                if not isinstance(qualite, int) or qualite < 1 or qualite > 10:
                    problemes.append(f"{date_str} : Qualité sommeil invalide ({qualite})")
        
        # Vérifier structure sport
        if 'sport' in valeurs:
            sport = valeurs['sport']
            if 'duree' in sport:
                duree = sport['duree']
                if not isinstance(duree, int) or duree < 0:
                    problemes.append(f"{date_str} : Durée sport invalide ({duree})")
        
        # Vérifier dépenses
        if 'depenses' in valeurs:
            depenses = valeurs['depenses']
            if not isinstance(depenses, list):
                problemes.append(f"{date_str} : Dépenses n'est pas une liste")
            else:
                for i, dep in enumerate(depenses):
                    if 'montant' in dep:
                        montant = dep['montant']
                        if not isinstance(montant, (int, float)) or montant <= 0:
                            problemes.append(f"{date_str} : Dépense #{i+1} montant invalide ({montant})")
    
    print(f"\n📊 Vérification de {len(donnees)} jour(s)")
    
    if problemes:
        print(f"\n⚠️  {len(problemes)} problème(s) détecté(s) :")
        for prob in problemes[:10]:
            print(f"   • {prob}")
        if len(problemes) > 10:
            print(f"   ... et {len(problemes)-10} autre(s)")
    else:
        print("\n✅ Aucun problème détecté")


# ============================================
# Statistiques fichiers
# ============================================
def statistiques_fichiers() :
    # Statistiques fichiers
    print("\n📊 STATISTIQUES DES FICHIERS")
    
    fichiers_a_verifier = [
        ("Data/donnees.json", "Données principales"),
        ("Data/donnees.csv", "Export CSV")
    ]
    
    print()
    for fichier_nom, description in fichiers_a_verifier:
        if os.path.exists(fichier_nom):
            taille = os.path.getsize(fichier_nom)
            date_modif = datetime.fromtimestamp(os.path.getmtime(fichier_nom))
            
            print(f"📄 {description} ({fichier_nom})")
            print(f"   📦 Taille : {taille:,} octets ({taille/1024:.2f} KB)")
            print(f"   📅 Modifié : {date_modif.strftime('%d/%m/%Y %H:%M:%S')}")
            print()
        else:
            print(f"❌ {description} ({fichier_nom}) : Non trouvé")
            print()
    
    # Backups
    dossier_backup = "backups"
    if os.path.exists(dossier_backup):
                    backups = glob.glob(os.path.join(dossier_backup, "backup_*.json"))
                    if backups:
                        taille_totale = sum(os.path.getsize(b) for b in backups)
                        print(f"💼 Backups : {len(backups)} fichier(s)")
                        print(f"   📦 Taille totale : {taille_totale:,} octets ({taille_totale/1024:.2f} KB)")
                        print()


# ============================================
# Supprimer toutes les données en mémoire
# ============================================               
def supprimer_donnees_memoire(donnees) :
    print("\n🗑️  SUPPRESSION TOTALE DES DONNÉES")
    print(Couleurs.ROUGE_SOMBRE,"\n⚠️ ATTENTION ⚠️", Couleurs.RESET)
    print("\tCette action est IRRÉVERSIBLE !")
    print(f"\tVous allez supprimer {len(donnees)} jour(s) de données")
    
    confirmation1 = input("\nTaper 'SUPPRIMER' pour confirmer : ").strip()
    
    if confirmation1 == "SUPPRIMER":
        confirmation2 = input("Êtes-vous vraiment sûr ? (oui/non) : ").strip().lower()
        
        if confirmation2 == "oui":
            spinner = "|/-\\"
            print("\n🔥 Suppression en cours...", end="", flush=True)
            for i in range(50):
                sys.stdout.write("\b" + spinner[i % len(spinner)])
                sys.stdout.flush()
                time.sleep(0.1)
            donnees.clear()
            print(Couleurs.VERT,"\nToutes les données ont été supprimées", Couleurs.RESET)
            print("💡 Les fichiers sauvegardés n'ont pas été supprimés")
        else:
            print(Couleurs.ROUGE_SOMBRE,"\n❌ Suppression annulée", Couleurs.RESET)
    else:
        print(Couleurs.ROUGE_SOMBRE,"\n❌ Suppression annulée", Couleurs.RESET)


# ============================================
# Supprimer TOUTES les données utilisateur (fichiers + mémoire)
# ============================================
def supprimer_donnees_complet(donnees) :

    print(Couleurs.ROUGE_SOMBRE, Couleurs.GRAS,"\n⚠️  ATTENTION MAXIMALE - DESTRUCTION TOTALE !", Couleurs.RESET)
    
    print("\nCette action va DÉFINITIVEMENT supprimer :")
    print("  • Toutes les données en mémoire")
    print("  • Le fichier donnees.json")
    print("  • Tous les fichiers CSV")
    print("  • TOUS les backups")
    print("  • Le dossier backups")
    print("  • Le dossier export")
    print("\n🔥 CETTE ACTION EST TOTALEMENT IRRÉVERSIBLE ! 🔥")
    
    print("\n" + "─"*60)
    confirmation1 = input("Taper 'DETRUIRE TOUT' pour continuer : ").strip()
    
    if confirmation1 == "DETRUIRE TOUT":
        print("\n⚠️  Êtes-vous ABSOLUMENT certain ?")
        print(Couleurs.ROUGE_SOMBRE,"\tToutes vos données seront PERDUES À JAMAIS !", Couleurs.RESET)
        confirmation2 = input("\nTaper 'OUI JE CONFIRME' : ").strip()
        
        if confirmation2 == "OUI JE CONFIRME":
            spinner = "|/-\\"
            print("\n🔥 Destruction en cours...", end="", flush=True)
            for i in range(50):
                sys.stdout.write("\b" + spinner[i % len(spinner)])
                sys.stdout.flush()
                time.sleep(0.1)

            fichiers_supprimes = 0
            dossiers_supprimes = 0
            
            try:
                # 1. Vider les données en mémoire
                donnees.clear()
                print("\n\n• Données en mémoire supprimées")
                """
                # 2. Supprimer donnees.json
                if os.path.exists("donnees.json"):
                    os.remove("donnees.json")
                    fichiers_supprimes += 1
                    print("• Donnees.json supprimé")
                
                # 3. Supprimer fichiers CSV
                for fichier_csv in glob.glob("*.csv"):
                    os.remove(fichier_csv)
                    fichiers_supprimes += 1
                    print(f"• {fichier_csv} supprimé")
                """
                # 4. Supprimer dossier backups
                if os.path.exists("Data"):
                    import shutil
                    shutil.rmtree("Data")
                    #dossiers_supprimes += 1
                    print("• Dossier Data supprimé")
                """"
                # 5. Supprimer dossier export
                if os.path.exists("export"):
                    import shutil
                    shutil.rmtree("export")
                    dossiers_supprimes += 1
                    print("• Dossier export supprimé")
                
                # 6. Supprimer dossier exports_json
                if os.path.exists("exports_json"):
                    import shutil
                    shutil.rmtree("exports_json")
                    dossiers_supprimes += 1
                    print("• Dossier exports_json supprimé")
                
                # 7. Supprimer fichiers d'urgence
                for fichier_urgence in glob.glob("donnees_urgence_*.json"):
                    os.remove(fichier_urgence)
                    fichiers_supprimes += 1
                    print(f"• {fichier_urgence} supprimé")
                """
                print(f"\n💣 DESTRUCTION TERMINÉE")
                #print(f"   {fichiers_supprimes} fichier(s) supprimé(s)")
                #print(f"   {dossiers_supprimes} dossier(s) supprimé(s)")
                print("\n🔥 Toutes vos données ont été définitivement effacées")
                print("💡 Vous repartez de zéro")
                
            except Exception as e:
                print(Couleurs.ROUGE,f"\n❌ Erreur lors de la suppression : {e}", Couleurs.RESET)
                print("⚠️  Certains fichiers n'ont peut-être pas été supprimés")
        else:
            print(Couleurs.ROUGE,"\n❌ Destruction annulée (2ème confirmation incorrecte)", Couleurs.RESET)
    else:
        print(Couleurs.ROUGE,"\n❌ Destruction annulée (1ère confirmation incorrecte)", Couleurs.RESET)
                
      
#============================================
# FONCTIONS DE CONSULTER_DATE_AVANCE
# ============================================
def formater_date(date_str):
    """Formate une date pour l'affichage"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        
        jour_semaine = jours_semaine[date_obj.weekday()]
        jour = date_obj.day
        mois_nom = mois[date_obj.month - 1]
        annee = date_obj.year
        
        return f"{jour_semaine} {jour} {mois_nom} {annee}"
    except:
        return date_str
   
def afficher_donnees_detaillees(date_str, donnees_jour):
    """Affiche les données détaillées d'un jour"""
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n" + "═"*60)
    print(f"📊 DONNÉES DÉTAILLÉES - {formater_date(date_str)}")
    print("═"*60)
    
    # Afficher le SOMMEIL
    sommeil = donnees_jour.get("sommeil", {})
    if sommeil:
        duree = sommeil.get("duree", "Non renseigné")
        qualite = sommeil.get("qualite", "Non renseigné")
        
        print("\n😴 SOMMEIL")
        print(f"   Durée : {duree} heures")
        print(f"   Qualité : {qualite}/10")
        
        # Ajouter une barre de progression pour la qualité
        if isinstance(qualite, (int, float)):
            barre = "█" * int(qualite) + "░" * (10 - int(qualite))
            print(f"   Visualisation : [{barre}]")
    else:
        print("\n😴 SOMMEIL : Non renseigné")

    # Afficher le SPORT
    sport = donnees_jour.get("sport", {})
    if sport and sport.get("duree", 0) > 0:  # ← CORRECTION: Vérifier si duree > 0
        type_sport = sport.get("type", "Non spécifié")
        duree_sport = sport.get("duree", 0)
        intensite = sport.get("intensite", "Non spécifiée")
        
        print("\n🏃 ACTIVITÉ SPORTIVE")
        print(f"   Type : {type_sport}")
        print(f"   Durée : {duree_sport} minutes")
        print(f"   Intensité : {intensite}")
        
        # Évaluation de l'effort
        if duree_sport < 30:
            evaluation = "Séance courte"
        elif duree_sport < 60:
            evaluation = "Séance modérée"
        else:
            evaluation = "Longue séance"
        print(f"   📝 {evaluation}")
    else:
        print("\n🏃 ACTIVITÉ SPORTIVE : Aucune activité")

    # Afficher les DÉPENSES
    depenses = donnees_jour.get("depenses", [])
    if depenses:
        print("\n💰 DÉPENSES")
        total = 0
        
        for i, depense in enumerate(depenses, 1):
            categorie = depense.get("categorie", "Non catégorisé")
            montant = depense.get("montant", 0)
            description = depense.get("description", "")
            
            total += montant
            
            print(f"   {i}. {categorie}: {montant:.2f}$")
            if description:
                print(f"      📝 {description}")
        
        print(f"\n   {'─'*30}")
        print(f"   TOTAL JOURNALIER : {total:.2f}$")
        
        # Analyse rapide
        if total > 50:
            print(f"   ⚠️  Dépenses élevées")
        elif total == 0:
            print(f"   ✅ Pas de dépenses aujourd'hui")
    else:
        print("\n💰 DÉPENSES : Aucune dépense")
    
    # Afficher des statistiques rapides
    print(f"\n{'─'*60}")
    print("📈 VUE D'ENSEMBLE")
    print("\n")

    # Calculer des indicateurs
    score_journee = 0
    commentaires = []

    # Score sommeil - CORRECTION: Initialiser duree_sommeil
    duree_sommeil = sommeil.get("duree", 0) if sommeil else 0
    if duree_sommeil >= 7:
        score_journee += 1
        commentaires.append("Sommeil suffisant")
    elif duree_sommeil > 0:
        commentaires.append("Sommeil insuffisant")

    # Score sport
    duree_sport = sport.get("duree", 0) if sport else 0
    if duree_sport >= 30:
        score_journee += 1
        commentaires.append("Activité physique OK")
    elif duree_sport > 0:
        commentaires.append("Activité physique faible")

    # Score dépenses
    if depenses:
        total_depenses = sum(d['montant'] for d in depenses)
        if total_depenses <= 30:
            score_journee += 1
            commentaires.append("Dépenses raisonnables")
        else:
            commentaires.append("Dépenses élevées")
    
    # Afficher le score
    print(f"   Score de la journée : {score_journee}/3")
    print("\n")
    if commentaires:
        for commentaire in commentaires:
            print(f"   • {commentaire}")
        
    print("═"*60)

def menu_options(date_str, donnees_jour, donnees):  # ← CORRECTION: Ajouter donnees en paramètre
    """Menu d'options pour la date consultée"""
    while True:
        print("\n📋 OPTIONS DISPONIBLES :")
        print("\n")
        print("  1.  Modifier les données")
        print("  2.  Afficher un résumé")
        print("  3.  Comparer avec la veille")
        print("  4.  Voir le jour suivant")
        print("  5.  Voir le jour précédent")
        print("  6.  Retour à la consultation")
        print("  7.  Retour au menu principal")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            # Modifier les données
            donnees = modifier_donnees_date(donnees, date_str)  # ← CORRECTION: Récupérer le résultat
            return "refresh"  # ← CORRECTION: Retourner pour rafraîchir l'affichage
        elif choix == "2":
            # Résumé
            afficher_resume(date_str, donnees_jour)
        elif choix == "3":
            # Comparer avec la veille
            comparer_veille(donnees, date_str)
        elif choix == "4":
            # Jour suivant
            return "suivant"
        elif choix == "5":
            # Jour précédent
            return "precedent"
        elif choix == "6":
            consulter_date_avance(donnees)
            return "refresh"
        elif choix == "7":
            return "menu"
        else:
            print(Couleurs.ROUGE,"❌ Choix invalide", Couleurs.RESET)


# ============================================
# Trouver dates proches
# ============================================
def trouver_dates_proches(donnees, date_reference, limite=5):
    """
    Trouve les dates les plus proches d'une date de référence
    """
    from datetime import datetime
    
    if not donnees:
        return []
    
    try:
        date_ref = datetime.strptime(date_reference, "%Y-%m-%d")
        dates_avec_ecarts = []
        
        for date_str in donnees.keys():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            ecart = abs((date_obj - date_ref).days)
            dates_avec_ecarts.append((date_str, ecart))
        
        # Trier par écart croissant
        dates_avec_ecarts.sort(key=lambda x: x[1])
        
        return dates_avec_ecarts[:limite]
    except:
        return []


# ============================================
# Consulter une date avec options interactives (Fonction principale)
# ============================================
def consulter_date_avance(donnees):
    """
    Consulte une date avec options interactives
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Début de la fonction principale
    print("\n" + "="*50)
    print("🔍 CONSULTATION AVANCÉE")
    print("="*50)
    
    # 1. Choix de la méthode de sélection
    print("\nComment souhaitez-vous sélectionner la date ?")
    print("1. Saisir une date manuellement")
    print("2. Choisir dans la liste des dates disponibles")
    print("3. Date la plus récente")
    print("4. ↩ Retour")
    
    methode = input("\nVotre choix : ").strip()
    
    if methode == "4":
        return
    
    # 2. Sélection de la date selon la méthode choisie
    date_str = None
    
    if methode == "1":
        # Saisie manuelle
        while True:
            date_input = input("\nEntrez la date (AAAA-MM-JJ) ou 'auj' pour aujourd'hui : ").strip()
            
            if date_input.lower() in ['auj', 'aujourdhui', 'today']:
                date_str = datetime.now().strftime("%Y-%m-%d")
                break
            elif date_input:
                try:
                    date_obj = datetime.strptime(date_input, "%Y-%m-%d")
                    date_str = date_obj.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    print(Couleurs.ROUGE,"❌ Format invalide. Utilisez AAAA-MM-JJ", Couleurs.RESET)
            else:
                print("⚠️  Veuillez entrer une date")
    
    elif methode == "2":
        # Choix dans la liste
        dates_disponibles = sorted(donnees.keys(), reverse=True)
        
        if not dates_disponibles:
            print("📭 Aucune donnée disponible")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print(f"\n📋 {len(dates_disponibles)} dates disponibles :")
        
        # Afficher par groupe de 10
        for i in range(0, len(dates_disponibles), 10):
            groupe = dates_disponibles[i:i+10]
            print(f"\nGroupe {i//10 + 1}:")
            for j, date_disp in enumerate(groupe, 1):
                print(f"  {i+j}. {formater_date(date_disp)}")
        
        while True:
            try:
                choix = input(f"\nNuméro de la date (1-{len(dates_disponibles)}) ou 0 pour annuler : ").strip()
                if not choix or choix == "0":
                    return
                
                idx = int(choix) - 1
                if 0 <= idx < len(dates_disponibles):
                    date_str = dates_disponibles[idx]
                    break
                else:
                    print(Couleurs.ROUGE,f"❌ Numéro invalide. Choisissez entre 1 et {len(dates_disponibles)}", Couleurs.RESET)
            except ValueError:
                print(Couleurs.ROUGE,"❌ Veuillez entrer un nombre", Couleurs.RESET)
    
    elif methode == "3":
        # Date la plus récente
        if donnees:
            date_str = max(donnees.keys())
            print(f"\n📅 Date la plus récente : {formater_date(date_str)}")
        else:
            print("📭 Aucune donnée disponible")
            input("\nAppuyez sur Entrée pour continuer...")
            return
    else:
        print(Couleurs.ROUGE,"❌ Choix invalide", Couleurs.RESET)
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # 3. Navigation entre les dates
    current_date_str = date_str
    
    while True:
        # Vérifier si la date existe
        if current_date_str not in donnees:
            print(f"\n📭 Aucune donnée pour le {formater_date(current_date_str)}")
            
            # Proposer les dates proches
            dates_proches = trouver_dates_proches(donnees, current_date_str)
            if dates_proches:
                print("\nDates disponibles à proximité :")
                for i, (date_proche, ecart) in enumerate(dates_proches[:3], 1):
                    print(f"  {i}. {formater_date(date_proche)} ({ecart} jour(s) d'écart)")
                
                choix_proche = input("\nChoisir une date proche ? (numéro ou N) : ").strip()
                if choix_proche.isdigit():
                    idx = int(choix_proche) - 1
                    if 0 <= idx < len(dates_proches):
                        current_date_str = dates_proches[idx][0]
                        continue
                else:
                    input("\nAppuyez sur Entrée pour continuer...")
                    break
            else:
                input("\nAppuyez sur Entrée pour continuer...")
                break
        
        # Afficher les données
        donnees_jour = donnees[current_date_str]
        afficher_donnees_detaillees(current_date_str, donnees_jour)
        
        # Menu d'options - CORRECTION: Passer donnees
        action = menu_options(current_date_str, donnees_jour, donnees)
        
        if action == "menu":
            break
        elif action == "refresh":
            # Rafraîchir l'affichage (après modification)
            continue
        elif action == "suivant":
            # Passer au jour suivant
            try:
                current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
                next_date = current_date + timedelta(days=1)
                current_date_str = next_date.strftime("%Y-%m-%d")
            except Exception as e:
                print(Couleurs.ROUGE,f"❌ Erreur : {e}", Couleurs.RESET)
                input("\nAppuyez sur Entrée pour continuer...")
                break
        elif action == "precedent":
            # Passer au jour précédent
            try:
                current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
                prev_date = current_date - timedelta(days=1)
                current_date_str = prev_date.strftime("%Y-%m-%d")
            except Exception as e:
                print(Couleurs.ROUGE,f"❌ Erreur : {e}", Couleurs.RESET)
                input("\nAppuyez sur Entrée pour continuer...")
                break
        else:
            # Autre action
            continue
    
    # Fin - pas besoin de message supplémentaire


# ============================================
# Afficher un resumé des données
# ============================================
def afficher_resume(date_str, donnees_jour):
    """Affiche un résumé compact des données"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "─"*40)
    print(f"📋 RÉSUMÉ - {date_str}")
    print("─"*40)
    
    # Sommeil
    sommeil = donnees_jour.get("sommeil", {})
    if sommeil:
        duree = sommeil.get("duree", "?")
        qualite = sommeil.get("qualite", "?")
        print(f"Sommeil : {duree}h | Qualité: {qualite}/10")
    else:
        print(f"Sommeil : Non renseigné")
    
    # Sport
    sport = donnees_jour.get("sport", {})
    if sport and sport.get("duree", 0) > 0:
        type_sport = sport.get("type", "Activité")
        duree = sport.get("duree", 0)
        print(f"Sport : {type_sport} ({duree}min)")
    else:
        print(f"Sport : Aucune activité")
    
    # Dépenses
    depenses = donnees_jour.get("depenses", [])
    if depenses:
        total = sum(d['montant'] for d in depenses)
        print(f"Dépenses : {len(depenses)} transaction(s) | Total: {total:.2f}$")
    else:
        print(f"Dépenses : Aucune dépense")
    
    print("─"*40)
    input("\n\nRetour ...")
    afficher_donnees_detaillees(date_str, donnees_jour)


# ============================================
# Modifie les données d'une date spécifique
# ============================================
def modifier_donnees_date(donnees, date_str):
    """
    Modifie les données d'une date spécifique
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Vérifier si la date existe dans les données
    if date_str not in donnees:
        print(f"❌ Aucune donnée trouvée pour le {date_str}")
        return donnees
    
    print(f"\n{'='*60}")
    print(f"✏️  MODIFICATION DES DONNÉES DU {date_str}")
    print(f"{'='*60}")
    
    # Récupérer les données actuelles
    donnees_jour = donnees[date_str].copy()  # Copie pour modification
    
    while True:
        # Afficher les données actuelles
        print("\nDONNÉES ACTUELLES :")
        print("-" * 40)
        
        # Afficher sommeil
        sommeil_actuel = donnees_jour.get("sommeil", {})
        if sommeil_actuel:
            duree = sommeil_actuel.get("duree", "Non renseigné")
            qualite = sommeil_actuel.get("qualite", "Non renseigné")
            print(f"SOMMEIL : {duree}h, Qualité: {qualite}/10")
        else:
            print(f"SOMMEIL : Non renseigné")
        
        # Afficher sport
        sport_actuel = donnees_jour.get("sport", {})
        if sport_actuel and sport_actuel.get("duree", 0) > 0:
            type_sport = sport_actuel.get("type", "Non spécifié")
            duree_sport = sport_actuel.get("duree", 0)
            intensite = sport_actuel.get("intensite", "Non spécifiée")
            print(f"SPORT : {type_sport}, {duree_sport}min, Intensité: {intensite}")
        else:
            print(f"SPORT : Aucune activité")
        
        # Afficher dépenses
        depenses_actuelles = donnees_jour.get("depenses", [])
        if depenses_actuelles:
            total = sum(d['montant'] for d in depenses_actuelles)
            print(f"DÉPENSES : {len(depenses_actuelles)} transaction(s), Total: {total:.2f}$")
        else:
            print(f"DÉPENSES : Aucune dépense")
        
        print("-" * 40)
        
        # Menu de modification
        print("\n📝 QUE VOULEZ-VOUS MODIFIER ?")
        print("1. Modifier le sommeil")
        print("2. Modifier l'activité sportive")
        print("3. Modifier les dépenses")
        print("4. Supprimer toutes les données de ce jour")
        print("5. Terminer la modification")
        print("6. Annuler (ne pas sauvegarder)")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            # Modifier le sommeil
            donnees_jour = modifier_sommeil(donnees_jour, sommeil_actuel)
        
        elif choix == "2":
            # Modifier le sport
            donnees_jour = modifier_sport(donnees_jour, sport_actuel)
        
        elif choix == "3":
            # Modifier les dépenses
            donnees_jour = modifier_depenses(donnees_jour, depenses_actuelles)
        
        elif choix == "4":
            # Supprimer toutes les données
            confirmer = input(Couleurs.ROUGE_SOMBRE,"\n⚠️  Êtes-vous sûr de vouloir supprimer TOUTES les données de ce jour ? (O/N) : ", Couleurs.RESET).strip().lower()
            if confirmer in ['o', 'oui', 'y', 'yes']:
                del donnees[date_str]
                print(f"🗑️  Toutes les données du {date_str} ont été supprimées")
                return donnees
        
        elif choix == "5":
            # Sauvegarder les modifications
            donnees[date_str] = donnees_jour
            print(f"✅ Modifications enregistrées pour le {date_str}")
            return donnees
        
        elif choix == "6":
            # Annuler sans sauvegarder
            print("❌ Modification annulée. Aucun changement n'a été enregistré.")
            return donnees
        
        else:
            print("❌ Choix invalide")


# ============================================
# Modifie les données de sommeil
# ============================================
def modifier_sommeil(donnees_jour, sommeil_actuel):
    """Modifie les données de sommeil"""
    print("\n" + "-"*30)
    print("✏️  MODIFICATION DU SOMMEIL")
    print("-"*30)
    
    nouveau_sommeil = sommeil_actuel.copy() if sommeil_actuel else {}
    
    print("\nOptions :")
    print("1. Modifier la durée")
    print("2. Modifier la qualité")
    print("3. Effacer les données de sommeil")
    print("4. Retour")
    
    choix = input("\nVotre choix : ").strip()
    
    if choix == "1":
        # Modifier la durée
        while True:
            ancienne_duree = nouveau_sommeil.get("duree", "Non renseigné")
            print(f"\nDurée actuelle : {ancienne_duree}h")
            
            nouvelle_duree = input("Nouvelle durée (heures, 0-24) : ").strip()
            
            if not nouvelle_duree:
                print("⚠️  Modification annulée")
                break
            
            try:
                duree = float(nouvelle_duree)
                if 0 <= duree <= 24:
                    nouveau_sommeil["duree"] = duree
                    print(f"✅ Durée modifiée : {duree}h")
                    break
                else:
                    print("❌ La durée doit être entre 0 et 24 heures")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")
    
    elif choix == "2":
        # Modifier la qualité
        while True:
            ancienne_qualite = nouveau_sommeil.get("qualite", "Non renseigné")
            print(f"\nQualité actuelle : {ancienne_qualite}/10")
            
            nouvelle_qualite = input("Nouvelle qualité (1-10) : ").strip()
            
            if not nouvelle_qualite:
                print("⚠️  Modification annulée")
                break
            
            try:
                qualite = int(nouvelle_qualite)
                if 1 <= qualite <= 10:
                    nouveau_sommeil["qualite"] = qualite
                    print(f"✅ Qualité modifiée : {qualite}/10")
                    break
                else:
                    print("❌ La qualité doit être entre 1 et 10")
            except ValueError:
                print("❌ Veuillez entrer un nombre entre 1 et 10")
    
    elif choix == "3":
        # Effacer les données
        confirmer = input("\nSupprimer toutes les données de sommeil ? (O/N) : ").strip().lower()
        if confirmer in ['o', 'oui', 'y', 'yes']:
            nouveau_sommeil = {}
            print("✅ Données de sommeil effacées")
    
    elif choix == "4":
        print("↩️  Retour")
        return donnees_jour
    
    else:
        print("❌ Choix invalide")
        return donnees_jour
    
    # Mettre à jour les données du jour
    donnees_jour["sommeil"] = nouveau_sommeil if nouveau_sommeil else {}
    return donnees_jour


# ============================================
# Modifie les données de sport
# ============================================
def modifier_sport(donnees_jour, sport_actuel):
    """Modifie les données de sport"""
    print("\n" + "-"*30)
    print("✏️  MODIFICATION DE L'ACTIVITÉ SPORTIVE")
    print("-"*30)
    
    nouveau_sport = sport_actuel.copy() if sport_actuel else {}
    
    print("\nOptions :")
    print("1. Modifier le type d'activité")
    print("2. Modifier la durée")
    print("3. Modifier l'intensité")
    print("4. Effacer les données de sport")
    print("5. Retour")
    
    choix = input("\nVotre choix : ").strip()
    
    if choix == "1":
        # Modifier le type
        ancien_type = nouveau_sport.get("type", "Non spécifié")
        print(f"\nType actuel : {ancien_type}")
        
        nouveau_type = input("Nouveau type (course, marche, vélo, etc.) : ").strip()
        
        if nouveau_type:
            nouveau_sport["type"] = nouveau_type
            print(f"✅ Type modifié : {nouveau_type}")
        else:
            print("⚠️  Modification annulée")
    
    elif choix == "2":
        # Modifier la durée
        while True:
            ancienne_duree = nouveau_sport.get("duree", 0)
            print(f"\nDurée actuelle : {ancienne_duree} minutes")
            
            nouvelle_duree = input("Nouvelle durée (minutes, 0-300) : ").strip()
            
            if not nouvelle_duree:
                print("⚠️  Modification annulée")
                break
            
            try:
                duree = int(nouvelle_duree)
                if 0 <= duree <= 300:
                    nouveau_sport["duree"] = duree
                    print(f"✅ Durée modifiée : {duree} minutes")
                    break
                else:
                    print("❌ La durée doit être entre 0 et 300 minutes")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")
    
    elif choix == "3":
        # Modifier l'intensité
        ancienne_intensite = nouveau_sport.get("intensite", "Non spécifiée")
        print(f"\nIntensité actuelle : {ancienne_intensite}")
        
        print("Intensités possibles : faible, moyenne, élevée")
        nouvelle_intensite = input("Nouvelle intensité : ").strip()
        
        if nouvelle_intensite:
            nouveau_sport["intensite"] = nouvelle_intensite
            print(f"✅ Intensité modifiée : {nouvelle_intensite}")
        else:
            print("⚠️  Modification annulée")
    
    elif choix == "4":
        # Effacer les données
        confirmer = input("\nSupprimer toutes les données de sport ? (O/N) : ").strip().lower()
        if confirmer in ['o', 'oui', 'y', 'yes']:
            nouveau_sport = {}
            print("✅ Données de sport effacées")
    
    elif choix == "5":
        print("↩️  Retour")
        return donnees_jour
    
    else:
        print("❌ Choix invalide")
        return donnees_jour
    
    # Mettre à jour les données du jour
    donnees_jour["sport"] = nouveau_sport if nouveau_sport else {}
    return donnees_jour


# ============================================
# Modifie les données de dépenses
# ============================================
def modifier_depenses(donnees_jour, depenses_actuelles):
    """Modifie les données de dépenses"""
    print("\n" + "-"*30)
    print("✏️  MODIFICATION DES DÉPENSES")
    print("-"*30)
    
    nouvelles_depenses = depenses_actuelles.copy() if depenses_actuelles else []
    
    while True:
        print(f"\nVous avez {len(nouvelles_depenses)} dépense(s) enregistrée(s)")
        
        if nouvelles_depenses:
            print("\n📋 LISTE DES DÉPENSES :")
            for i, dep in enumerate(nouvelles_depenses, 1):
                categorie = dep.get("categorie", "Non catégorisé")
                montant = dep.get("montant", 0)
                description = dep.get("description", "")
                
                print(f"{i}. {categorie}: {montant:.2f}$", end="")
                if description:
                    print(f" - {description}")
                else:
                    print()
        
        print("\nOptions :")
        print("1. Ajouter une nouvelle dépense")
        print("2. Modifier une dépense existante")
        print("3. Supprimer une dépense")
        print("4. Supprimer toutes les dépenses")
        print("5. Retour")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            # Ajouter une nouvelle dépense
            print("\n➕ AJOUT D'UNE NOUVELLE DÉPENSE")
            
            categorie = input("Catégorie : ").strip()
            if not categorie:
                print("❌ Catégorie obligatoire")
                continue
            
            montant_str = input("Montant ($) : ").strip()
            try:
                montant = float(montant_str)
                if montant <= 0:
                    print("❌ Le montant doit être positif")
                    continue
            except ValueError:
                print("❌ Montant invalide")
                continue
            
            description = input("Description (optionnel) : ").strip()
            
            nouvelle_depense = {
                "categorie": categorie,
                "montant": round(montant, 2)
            }
            if description:
                nouvelle_depense["description"] = description
            
            nouvelles_depenses.append(nouvelle_depense)
            print(f"✅ Dépense ajoutée : {categorie} - {montant:.2f}$")
        
        elif choix == "2":
            # Modifier une dépense existante
            if not nouvelles_depenses:
                print("📭 Aucune dépense à modifier")
                continue
            
            try:
                num = int(input(f"Numéro de la dépense à modifier (1-{len(nouvelles_depenses)}) : ").strip())
                if 1 <= num <= len(nouvelles_depenses):
                    idx = num - 1
                    depense = nouvelles_depenses[idx]
                    
                    print(f"\nModification de la dépense #{num}:")
                    print(f"Categorie: {depense.get('categorie')}")
                    print(f"Montant: {depense.get('montant', 0):.2f}$")
                    print(f"Description: {depense.get('description', '')}")
                    
                    # Modifier la catégorie
                    nouvelle_categorie = input(f"Nouvelle catégorie [{depense.get('categorie')}] : ").strip()
                    if nouvelle_categorie:
                        depense["categorie"] = nouvelle_categorie
                    
                    # Modifier le montant
                    nouveau_montant = input(f"Nouveau montant [{depense.get('montant', 0)}] : ").strip()
                    if nouveau_montant:
                        try:
                            montant = float(nouveau_montant)
                            if montant > 0:
                                depense["montant"] = round(montant, 2)
                            else:
                                print("❌ Le montant doit être positif")
                        except ValueError:
                            print("❌ Montant invalide")
                    
                    # Modifier la description
                    nouvelle_description = input(f"Nouvelle description [{depense.get('description', '')}] : ").strip()
                    if nouvelle_description:
                        depense["description"] = nouvelle_description
                    elif nouvelle_description == "":
                        # Si l'utilisateur tape Enter sur une description vide, garder vide
                        depense["description"] = ""
                    
                    nouvelles_depenses[idx] = depense
                    print(f"✅ Dépense #{num} modifiée")
                else:
                    print("❌ Numéro invalide")
            except ValueError:
                print("❌ Veuillez entrer un nombre")
        
        elif choix == "3":
            # Supprimer une dépense
            if not nouvelles_depenses:
                print("📭 Aucune dépense à supprimer")
                continue
            
            try:
                num = int(input(f"Numéro de la dépense à supprimer (1-{len(nouvelles_depenses)}) : ").strip())
                if 1 <= num <= len(nouvelles_depenses):
                    depense = nouvelles_depenses[num-1]
                    categorie = depense.get("categorie", "Inconnue")
                    montant = depense.get("montant", 0)
                    
                    confirmer = input(f"Supprimer {categorie} - {montant:.2f}$ ? (O/N) : ").strip().lower()
                    if confirmer in ['o', 'oui', 'y', 'yes']:
                        del nouvelles_depenses[num-1]
                        print(f"🗑️  Dépense #{num} supprimée")
                else:
                    print("❌ Numéro invalide")
            except ValueError:
                print("❌ Veuillez entrer un nombre")
        
        elif choix == "4":
            # Supprimer toutes les dépenses
            if nouvelles_depenses:
                total = sum(d['montant'] for d in nouvelles_depenses)
                confirmer = input(f"Supprimer toutes les {len(nouvelles_depenses)} dépenses (total: {total:.2f}$) ? (O/N) : ").strip().lower()
                if confirmer in ['o', 'oui', 'y', 'yes']:
                    nouvelles_depenses = []
                    print("🗑️  Toutes les dépenses supprimées")
            else:
                print("📭 Aucune dépense à supprimer")
        
        elif choix == "5":
            print("↩️  Retour")
            break
        
        else:
            print("❌ Choix invalide")
    
    # Mettre à jour les données du jour
    donnees_jour["depenses"] = nouvelles_depenses
    return donnees_jour


# ============================================
# Comparer le jour avec la veille
# ============================================
def comparer_veille(donnees, date_str):
    """Compare avec le jour précédent"""
    from datetime import datetime, timedelta
    
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_veille = (date_obj - timedelta(days=1)).strftime("%Y-%m-%d")
        
        if date_veille in donnees:
            print(f"\n📊 COMPARAISON AVEC LA VEILLE ({date_veille})")
            print("─" * 40)
            
            # Comparer le sommeil
            sommeil_auj = donnees[date_str].get("sommeil", {})
            sommeil_hier = donnees[date_veille].get("sommeil", {})
            
            if sommeil_auj.get("duree") and sommeil_hier.get("duree"):
                diff = sommeil_auj["duree"] - sommeil_hier["duree"]
                if diff > 0:
                    print(f"😴 Sommeil : +{diff:.1f}h par rapport à hier")
                elif diff < 0:
                    print(f"😴 Sommeil : {diff:.1f}h par rapport à hier")
                else:
                    print(f"😴 Sommeil : Même durée qu'hier")
            
            # Comparer le sport
            sport_auj = donnees[date_str].get("sport", {})
            sport_hier = donnees[date_veille].get("sport", {})
            
            duree_auj = sport_auj.get("duree", 0)
            duree_hier = sport_hier.get("duree", 0)
            
            if duree_auj > 0 or duree_hier > 0:
                diff = duree_auj - duree_hier
                if diff > 0:
                    print(f"🏃 Sport : +{diff}min d'activité")
                elif diff < 0:
                    print(f"🏃 Sport : {diff}min d'activité")
                else:
                    print(f"🏃 Sport : Même durée qu'hier")
            
            # Comparer les dépenses
            depenses_auj = donnees[date_str].get("depenses", [])
            depenses_hier = donnees[date_veille].get("depenses", [])
            
            total_auj = sum(d['montant'] for d in depenses_auj)
            total_hier = sum(d['montant'] for d in depenses_hier)
            
            diff_depenses = total_auj - total_hier
            if diff_depenses > 0:
                print(f"💰 Dépenses : +{diff_depenses:.2f}$ par rapport à hier")
            elif diff_depenses < 0:
                print(f"💰 Dépenses : {diff_depenses:.2f}$ par rapport à hier")
            else:
                print(f"💰 Dépenses : Même montant qu'hier")
            
        else:
            print(f"📭 Aucune donnée pour la veille ({date_veille})")
    except Exception as e:
        print(f"❌ Erreur lors de la comparaison : {e}")

