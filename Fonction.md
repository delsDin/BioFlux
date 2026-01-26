1. Option dans le menu :

    1. Saisir des données du jour
        saisir_donnees()
        sauvegarder_json_avec_rotation() : Sauvegarde avec rotation des backups (garde les N derniers)

    2. Voir mes statistiques (les fonctions sont dans modules/statistiques.py)
        voir_statistiques()
            📈 MENU DES STATISTIQUES :
        
            1. Statistiques du sommeil"
                Fonction : statistiques_sommeil()

            2. Statistiques du sport"
                Fonction : statistiques_sport()

            3. Statistiques des dépenses"
                Fonction : statistiques_depenses()

            4. Statistiques générales"
                Fonction : statistiques_generales()

            5. Statistiques par période"
                Fonction principale : menu_statistiques_periode()
                    📈 CHOISIR UNE PÉRIODE
                    
                    1. 📊 7 derniers jours
                        calculer_statistiques_periode()
                        afficher_statistiques_periode

                    2. 📊 30 derniers jours
                        calculer_statistiques_periode()
                        afficher_statistiques_periode()

                    3. 📊 Ce mois-ci
                        calculer_statistiques_mois()
                        afficher_statistiques_periode()

                    4. 📊 Le mois dernier
                        calculer_statistiques_mois()
                        afficher_statistiques_periode()

                    5. 📊 Personnaliser une période
                        choisir_periode_personnalisee()
                        calculer_statistiques_periode_custom()
                        afficher_statistiques_periode()

                    6. 📊 Comparer deux périodes
                        Fonction principale : comparer_deux_periodes()
                            Fonctions : comparer_deux_periodes()
                                        afficher_comparaison_periodes()
                                        comparer_categorie

                    7. 📊 Toutes les données (global)
                        calculer_statistiques_globales()
                        afficher_statistiques_periode()

                
            6. Rapport complet"
                Fonction : generer_rapport_complet(donnees)

            7. Exporter le rapport (TXT)"
                Fonction : exporter_rapport_txt()

            FONCTIONS AUXILIAIRES :
                calculer_stats_generales()
                calculer_score_global()
                generer_recommandations()
                analyser_regularite_semaine()
                analyser_correlations()
                calculer_correlation_simple

    3. Consulter une date spécifique (fonctions dans fonctions.py)

        consulter_date_avance() : Consulte une date avec options interactives

        # Choix de la méthode de sélection
            
            1. Saisir une date manuellement
            2. Choisir dans la liste des dates disponibles
            3. Date la plus récente
            4. ↩ Retour

        Fonction : afficher_donnees_detaillees() Affiche les données détaillées d'un jour
            menu_options() Menu d'options pour la date consultée :
                📋 OPTIONS DISPONIBLES :
                
                1.  Modifier les données
                2.  Afficher un résumé
                3.  Comparer avec la veille
                4.  Voir le jour suivant
                5.  Voir le jour précédent
                6.  Retour à la consultation
                7.  Retour au menu principal

    4. Afficher les tendances (fonctions dans modules/tendance.py)

        menu_tendances() : Menu d'analyse des tendances et évolutions

            📊 ÉVOLUTIONS TEMPORELLES
        
                1. Tendances sur 7 derniers jours
                    analyser_periode() : Analyse des tendances sur une période donnée
                2. Tendances sur 30 derniers jours
                    analyser_periode() : Analyse des tendances sur une période donnée
                3. Tendances sur période personnalisée (en nombre de jours)
                    analyser_periode() : Analyse des tendances sur une période donnée
                4. Comparaison mois par mois
                    comparer_mois() : Comparaison des statistiques mois par mois

            📉 GRAPHIQUES ASCII
        
                5. Graphique évolution sommeil
                    graphique_evolution_sommeil : Graphique ASCII de l'évolution du sommeil
                6. Graphique évolution sport
                    graphique_evolution_sport : Graphique ASCII de l'évolution du sport
                7. Graphique évolution dépenses
                    graphique_evolution_depenses : Graphique ASCII de l'évolution des depenses
                8. Graphique combiné (tout)
                    graphique_combine() : Graphique combiné : sommeil, sport et dépenses sur le même graphique
            
            🔍 ANALYSES AVANCÉES
            
                9. Analyse par jour de la semaine
                    analyser_jours_semaine() : Analyse des habitudes par jour de la semaine
                10. Détection de cycles et habitudes
                    detecter_cycles() : Détection de cycles et habitudes récurrentes
                11. Objectifs vs Réalisations
                    analyser_objectifs() : Analyse objectifs vs réalisations
                12. Prédictions basées sur tendances
                    generer_predictions() : Générer des prédictions basées sur les tendances
        
            13. ↩️  Retour au menu principal
        
    5. Gérer les données (fonctions dans fonctions.py)

        menu_gestion_donnees() : Menu complet de gestion des données

            SAUVEGARDE & CHARGEMENT
            
                1. 💾 Sauvegarder les données (JSON)
                    sauvegarder_json() : Sauvegarde avec fusion intelligente des données existantes

                2. 📂 Charger des données (JSON)
                    charger_json()
                        Si déjà des données en mémoire :
                        1. Remplacer les données actuelles
                        2. Fusionner avec les données actuelles
                        3. Annuler

                3. 📤 Exporter en CSV
                    sauvegarder_csv()

                4. 📥 Importer depuis CSV
                    charger_csv() avec option de fusion avec less données existantes

                5. 🔄 Exporter en CSV séparés (sommeil, sport, dépenses)
                    exporter_vers_csv_separe() dans un dossier

            BACKUP & RESTAURATION
            
                6. 💼 Créer un backup complet
                    generer_backup_complet() : Crée un backup avec gestion robuste des erreurs

                7. 📋 Lister les backups disponibles
                    lister_backups() dans le dossier Backups si il existe

                8. ♻️  Restaurer depuis un backup
                    restaurer_backup() depuis le dossier Backups

                9. 🗑️  Supprimer les anciens backups
                    supprimer_anciens_backups() avec l'option de conserver un nombre donné
        
            MAINTENANCE
        
                10. 🧹 Nettoyer les données (supprimer dates vides)
                    nettoyer_donnees()

                11. 🔍 Vérifier l'intégrité des données
                    verifier_integrite() : Vérifier intégrité des données

                12. 📊 Afficher les statistiques des fichiers
                    statistiques_fichiers()

                13. 🗑️  Supprimer TOUTES les données en mémoire
                    supprimer_donnees_memoire() : Supprimer toutes les données en mémoire dans l'execution en cours

                14. 💣  Supprimer TOUTES vos données
                    supprimer_donnees_complet() : Supprimer TOUTES les données utilisateur (fichiers + mémoire)
            
            15. ↩️  Retour au menu principal

    6. Aide / Instructions (fonctions dans fonctions.py)
        afficher_aide() : Affiche les instructions d'utilisation


2. Autres fonctions :
    - load_ini() : Charger les anciennes au demarrage du programme
    - afficher_accueil() : Affiche un écran d'accueil au démarrage
    - afficher_menu_principal() : Affiche le menu principal avec un tableau stylisé
    - menu_principal() : Menu principal interactif de l'application
    - saisir_donnees() : Saisie des données journalières avec validation
    - quitter_application_amelioree() : Version améliorée avec meilleure gestion d'erreurs
    - afficher_resume() : Affiche un résumé compact des données
    - modifier_donnees_date() : Modifie les données d'une date spécifique
    - modifier_sommeil() : Modifie les données de sommeil
    - modifier_sport() : Modifie les données de sport
    - modifier_depenses() : Modifie les données de depenses
    - comparer_veille() : Compare avec le jour précédent

3. Classe : Couleurs

4. Securité

    1. Signature du projet (à fournir sur démande)
        - sign.py :

            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding, rsa
            from pathlib import Path

            generate_keys() : Generation d'une clé privée et une publique
            sign_project () : Signature du projet 

        - integrete.py :

            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from pathlib import Path

            FILES_TO_VERIFY = [
                BASE_DIR / "main.py",
                BASE_DIR / "modules" / "integrite.py",
                BASE_DIR / "modules" / "fonction.py",
                BASE_DIR / "modules" / "statistiques.py",
                BASE_DIR / "modules" / "tendance.py",
                BASE_DIR / "modules" / "license_check.py",
            ]

            . verify_signature() -> bool :
                Charger clé publique
                Recalcul du hash
                Charger signature
                Vérification

    2. Vérification de licence
        - generate_licence.py :

            import json
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from pathlib import Path

            license_data = {
                "user": "Dinla Marcel",
                "product": "BioFlux",
                "date": "29/12/2025",
                "expiry": "2030-12-31"
            }
            . Sauvegarder licence dans licence.json
            . Charger la clé privée
            . Signer

        - license_check.py :
            from pathlib import Path
            from datetime import datetime
            import json, sys
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding

            verify_license()