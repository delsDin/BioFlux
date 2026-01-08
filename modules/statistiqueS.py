from datetime import datetime, timedelta
import os
import sys

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

#============================================================================
# PRINCIPAL
# ============================================================================
def voir_statistiques(donnees):
    """
    Affiche les statistiques complètes des données
    """
    # Vérifier s'il y a des données
    if not donnees:
        print("\n📭 Aucune donnée disponible pour afficher les statistiques.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Menu des statistiques
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "═"*60)
        print("📊 STATISTIQUES PERSONNELLES")
        print("═"*60)
        
        # Informations générales
        total_jours = len(donnees)
        dates = sorted(donnees.keys())
        date_debut = dates[0] if dates else "N/A"
        date_fin = dates[-1] if dates else "N/A"
        
        print(f"\n📅 Période couverte : {date_debut} à {date_fin}")
        print(f"📊 Nombre total de jours enregistrés : {total_jours}")
        
        # Statistiques rapides
        jours_avec_sommeil = sum(1 for d in donnees.values() if d.get('sommeil'))
        jours_avec_sport = sum(1 for d in donnees.values() if d.get('sport') and d['sport'].get('duree', 0) > 0)
        jours_avec_depenses = sum(1 for d in donnees.values() if d.get('depenses'))
        
        print(f"\n🎯 COUVERTURE DES DONNÉES :")
        print(f"   • Jours avec données de sommeil : {jours_avec_sommeil} ({jours_avec_sommeil/total_jours*100:.1f}%)")
        print(f"   • Jours avec activité sportive : {jours_avec_sport} ({jours_avec_sport/total_jours*100:.1f}%)")
        print(f"   • Jours avec dépenses : {jours_avec_depenses} ({jours_avec_depenses/total_jours*100:.1f}%)")
        
        print("\n" + "═"*60)
        print("📈 MENU DES STATISTIQUES")
        print("═"*60)
        print("1. 😴 Statistiques du sommeil")
        print("2. 🏃 Statistiques du sport")
        print("3. 💰 Statistiques des dépenses")
        print("4. 📊 Statistiques générales")
        print("5. 📅 Statistiques par période")
        print("6. 📋 Rapport complet")
        print("7. 💾 Exporter le rapport (TXT)")
        print("8. ↩️  Retour au menu principal")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            statistiques_sommeil(donnees)
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "2":
            statistiques_sport(donnees)
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "3":
            statistiques_depenses(donnees)
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "4":
            statistiques_generales(donnees)
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "5":
            menu_statistiques_periode(donnees)
        elif choix == "6":
            generer_rapport_complet(donnees)
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "7":
            exporter_rapport_txt(donnees, nom_fichier=None)
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "8":
            break
        
        else:
            print("❌ Choix invalide")
            input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# 1. STATISTIQUES DU SOMMEIL
# ============================================================================
def statistiques_sommeil(donnees):
    """Affiche les statistiques détaillées du sommeil"""
    print("geeeeeeeeeeeeeeeeeeeee")
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Extraire les données de sommeil
    donnees_sommeil = []
    donnees_qualite = []
    
    for date_str, valeurs in donnees.items():
        sommeil = valeurs.get('sommeil', {})
        if sommeil and 'duree' in sommeil:
            donnees_sommeil.append((date_str, sommeil['duree']))
        if sommeil and 'qualite' in sommeil:
            donnees_qualite.append((date_str, sommeil['qualite']))
    
    if not donnees_sommeil:
        print("\n😴 AUCUNE DONNÉE DE SOMMEIL DISPONIBLE")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print("\n" + "═"*60)
    print("😴 STATISTIQUES DU SOMMEIL")
    print("═"*60)
    
    # Calculs de base
    durees = [d[1] for d in donnees_sommeil]
    moyenne_duree = sum(durees) / len(durees)
    min_duree = min(durees)
    max_duree = max(durees)
    
    # Trouver les dates des min/max
    date_min_duree = [d[0] for d in donnees_sommeil if d[1] == min_duree][0]
    date_max_duree = [d[0] for d in donnees_sommeil if d[1] == max_duree][0]
    
    print(f"\n📊 BASÉ SUR {len(donnees_sommeil)} JOURS DE DONNÉES")
    print("-" * 40)
    
    print(f"\n⏰ DURÉE DU SOMMEIL :")
    print(f"   • Moyenne : {moyenne_duree:.1f} heures")
    print(f"   • Minimum : {min_duree:.1f} heures ({date_min_duree})")
    print(f"   • Maximum : {max_duree:.1f} heures ({date_max_duree})")
    
    # Analyse de la distribution
    print(f"\n📈 DISTRIBUTION :")
    categories = {
        "Très court (<6h)": sum(1 for d in durees if d < 6),
        "Court (6-7h)": sum(1 for d in durees if 6 <= d < 7),
        "Normal (7-8h)": sum(1 for d in durees if 7 <= d < 8),
        "Long (8-9h)": sum(1 for d in durees if 8 <= d < 9),
        "Très long (>9h)": sum(1 for d in durees if d >= 9)
    }
    
    for categorie, count in categories.items():
        if count > 0:
            pourcentage = count / len(durees) * 100
            barre = "█" * int(pourcentage / 2)  # Barre de progression
            print(f"   • {categorie:15} : {count:3} jours ({pourcentage:5.1f}%) {barre}")
    
    # Statistiques de qualité si disponibles
    if donnees_qualite:
        qualites = [q[1] for q in donnees_qualite]
        moyenne_qualite = sum(qualites) / len(qualites)
        min_qualite = min(qualites)
        max_qualite = max(qualites)
        
        print(f"\n⭐ QUALITÉ DU SOMMEIL ({len(donnees_qualite)} jours) :")
        print(f"   • Moyenne : {moyenne_qualite:.1f}/10")
        print(f"   • Minimum : {min_qualite}/10")
        print(f"   • Maximum : {max_qualite}/10")
        
        # Corrélation durée-qualité (si les deux données existent pour les mêmes jours)
        dates_communes = set([d[0] for d in donnees_sommeil]) & set([q[0] for q in donnees_qualite])
        if dates_communes:
            correlations = []
            for date in dates_communes:
                duree = next(d[1] for d in donnees_sommeil if d[0] == date)
                qualite = next(q[1] for q in donnees_qualite if q[0] == date)
                correlations.append((duree, qualite))
            
            if len(correlations) > 1:
                # Calcul simple de corrélation
                durees_corr = [c[0] for c in correlations]
                qualites_corr = [c[1] for c in correlations]
                
                # Moyennes
                moy_d = sum(durees_corr) / len(durees_corr)
                moy_q = sum(qualites_corr) / len(qualites_corr)
                
                # Calcul du coefficient de corrélation simplifié
                num = sum((d - moy_d) * (q - moy_q) for d, q in zip(durees_corr, qualites_corr))
                den_d = sum((d - moy_d) ** 2 for d in durees_corr)
                den_q = sum((q - moy_q) ** 2 for q in qualites_corr)
                
                if den_d > 0 and den_q > 0:
                    correlation = num / ((den_d * den_q) ** 0.5)
                    print(f"\n🔗 CORRÉLATION DURÉE-QUALITÉ :")
                    print(f"   • Coefficient : {correlation:.2f}")
                    if correlation > 0.3:
                        print(f"   • Interprétation : Plus de sommeil = meilleure qualité")
                    elif correlation < -0.3:
                        print(f"   • Interprétation : Plus de sommeil = qualité moindre")
                    else:
                        print(f"   • Interprétation : Pas de corrélation forte")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS :")
    if moyenne_duree < 7:
        print(f"   ⚠️  Votre sommeil moyen est inférieur aux recommandations (7-9h)")
    elif moyenne_duree > 9:
        print(f"   ⚠️  Votre sommeil moyen est supérieur aux recommandations (7-9h)")
    else:
        print(f"   ✅ Votre sommeil moyen est dans la plage recommandée (7-9h)")
    
    if donnees_qualite and moyenne_qualite < 7:
        print(f"   ⚠️  La qualité moyenne de votre sommeil pourrait être améliorée")
    
    print(f"\n" + "═"*60)

#============================================================================
# 2. STATISTIQUES DU SPORT
# ============================================================================
def statistiques_sport(donnees):
    """Affiche les statistiques détaillées du sport"""
    import os
    from collections import Counter
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Extraire les données de sport
    donnees_sport = []
    types_sport = []
    intensites = []
    
    for date_str, valeurs in donnees.items():
        sport = valeurs.get('sport', {})
        if sport and sport.get('duree', 0) > 0:
            donnees_sport.append((date_str, sport))
            types_sport.append(sport.get('type', 'Non spécifié'))
            intensites.append(sport.get('intensite', 'Non spécifiée'))
    
    if not donnees_sport:
        print("\n🏃 AUCUNE DONNÉE D'ACTIVITÉ SPORTIVE DISPONIBLE")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print("\n" + "═"*60)
    print("🏃 STATISTIQUES DU SPORT")
    print("═"*60)
    
    total_jours = len(donnees)
    jours_sport = len(donnees_sport)
    frequence = (jours_sport / total_jours) * 100
    
    print(f"\n📊 BASÉ SUR {jours_sport} JOURS D'ACTIVITÉ ({frequence:.1f}% du temps)")
    print("-" * 40)
    
    # Durées
    durees = [s[1].get('duree', 0) for s in donnees_sport]
    total_minutes = sum(durees)
    moyenne_duree = total_minutes / jours_sport if jours_sport > 0 else 0
    
    # Convertir en heures/minutes
    heures_total = total_minutes // 60
    minutes_total = total_minutes % 60
    
    heures_moyen = moyenne_duree // 60
    minutes_moyen = moyenne_duree % 60
    
    print(f"\n⏱️  TEMPS TOTAL D'ACTIVITÉ :")
    print(f"   • Total : {heures_total}h{minutes_total:02d} ({total_minutes} minutes)")
    print(f"   • Moyenne par séance : {moyenne_duree:.0f} minutes")
    print(f"   • Moyenne par jour (tous jours) : {total_minutes/total_jours:.0f} minutes")
    
    # Types de sport
    if types_sport:
        compteur_types = Counter(types_sport)
        print(f"\n🎯 TYPES D'ACTIVITÉ PRATIQUÉS :")
        for type_sport, count in compteur_types.most_common():
            pourcentage = (count / jours_sport) * 100
            print(f"   • {type_sport:20} : {count:3} fois ({pourcentage:5.1f}%)")
    
    # Intensités
    if intensites and any(i != 'Non spécifiée' for i in intensites):
        compteur_intensites = Counter(intensites)
        print(f"\n⚡ RÉPARTITION PAR INTENSITÉ :")
        for intensite, count in compteur_intensites.most_common():
            if intensite != 'Non spécifiée':
                pourcentage = (count / jours_sport) * 100
                print(f"   • {intensite:15} : {count:3} séances ({pourcentage:5.1f}%)")
    
    # Fréquence par jour de la semaine
    print(f"\n📅 FRÉQUENCE PAR JOUR DE LA SEMAINE :")
    jours_francais = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    for i, jour in enumerate(jours_francais):
        jours_avec_sport = sum(1 for date_str, _ in donnees_sport 
                              if datetime.strptime(date_str, "%Y-%m-%d").weekday() == i)
        total_jours_semaine = sum(1 for date_str in donnees.keys()
                                 if datetime.strptime(date_str, "%Y-%m-%d").weekday() == i)
        
        if total_jours_semaine > 0:
            pourcentage = (jours_avec_sport / total_jours_semaine) * 100
            barre = "█" * int(pourcentage / 5)  # Barre de progression
            print(f"   • {jour:10} : {jours_avec_sport:2}/{total_jours_semaine:2} jours ({pourcentage:5.1f}%) {barre}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS :")
    if frequence < 50:
        print(f"   ⚠️  Vous faites du sport moins de 50% du temps")
        print(f"   🎯 Objectif : Au moins 3-4 fois par semaine")
    else:
        print(f"   ✅ Excellente fréquence d'activité !")
    
    if moyenne_duree < 30:
        print(f"   ⚠️  Durée moyenne des séances inférieure à 30 minutes")
        print(f"   🎯 Objectif : 30-60 minutes par séance")
    
    print(f"\n" + "═"*60)

# ============================================================================
# 3. STATISTIQUES DES DÉPENSES
# ============================================================================
def statistiques_depenses(donnees):
    """Affiche les statistiques détaillées des dépenses"""
    import os
    from collections import Counter, defaultdict
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Extraire toutes les dépenses
    toutes_depenses = []
    depenses_par_jour = []
    
    for date_str, valeurs in donnees.items():
        depenses = valeurs.get('depenses', [])
        if depenses:
            total_jour = sum(d.get('montant', 0) for d in depenses)
            depenses_par_jour.append((date_str, total_jour))
            for depense in depenses:
                toutes_depenses.append((date_str, depense))
    
    if not toutes_depenses:
        print("\n💰 AUCUNE DONNÉE DE DÉPENSES DISPONIBLE")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    total_transactions = len(toutes_depenses)
    jours_avec_depenses = len(depenses_par_jour)
    
    print("\n" + "═"*60)
    print("💰 STATISTIQUES DES DÉPENSES")
    print("═"*60)
    
    print(f"\n📊 BASÉ SUR {total_transactions} TRANSACTIONS SUR {jours_avec_depenses} JOURS")
    print("-" * 40)
    
    # Montants totaux et moyens
    montants = [d[1].get('montant', 0) for d in toutes_depenses]
    total_general = sum(montants)
    moyenne_transaction = total_general / total_transactions if total_transactions > 0 else 0
    
    totaux_jour = [d[1] for d in depenses_par_jour]
    moyenne_journaliere = sum(totaux_jour) / jours_avec_depenses if jours_avec_depenses > 0 else 0
    moyenne_tous_jours = total_general / len(donnees) if donnees else 0
    
    print(f"\n💵 MONTANTS :")
    print(f"   • Total général : {total_general:.2f}€")
    print(f"   • Moyenne par transaction : {moyenne_transaction:.2f}€")
    print(f"   • Moyenne les jours avec dépenses : {moyenne_journaliere:.2f}€")
    print(f"   • Moyenne tous jours confondus : {moyenne_tous_jours:.2f}€")
    
    # Dépenses par catégorie
    depenses_par_categorie = defaultdict(float)
    transactions_par_categorie = defaultdict(int)
    
    for _, depense in toutes_depenses:
        categorie = depense.get('categorie', 'Non catégorisé')
        montant = depense.get('montant', 0)
        depenses_par_categorie[categorie] += montant
        transactions_par_categorie[categorie] += 1
    
    print(f"\n📊 RÉPARTITION PAR CATÉGORIE :")
    
    # Trier par montant décroissant
    categories_triees = sorted(depenses_par_categorie.items(), key=lambda x: x[1], reverse=True)
    
    for categorie, montant in categories_triees:
        pourcentage = (montant / total_general) * 100
        nb_transactions = transactions_par_categorie[categorie]
        moyenne_cat = montant / nb_transactions if nb_transactions > 0 else 0
        
        barre = "█" * int(pourcentage / 2)  # Barre de progression
        print(f"   • {categorie:15} : {montant:8.2f}€ ({pourcentage:5.1f}%) | "
              f"{nb_transactions:2} trans. | moy: {moyenne_cat:.2f}€ {barre}")
    
    # Jours les plus/moins chers
    if depenses_par_jour:
        depenses_par_jour.sort(key=lambda x: x[1])
        moins_cher = depenses_par_jour[0]
        plus_cher = depenses_par_jour[-1]
        
        print(f"\n📅 JOURS EXTRÊMES :")
        print(f"   • Jour le moins cher : {moins_cher[0]} - {moins_cher[1]:.2f}€")
        print(f"   • Jour le plus cher : {plus_cher[0]} - {plus_cher[1]:.2f}€")
    
    # Fréquence des dépenses
    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    depenses_par_joursemaine = defaultdict(float)
    
    for date_str, total in depenses_par_jour:
        jour_semaine = datetime.strptime(date_str, "%Y-%m-%d").weekday()
        depenses_par_joursemaine[jours_semaine[jour_semaine]] += total
    
    print(f"\n📅 DÉPENSES PAR JOUR DE LA SEMAINE :")
    for jour in jours_semaine:
        total = depenses_par_joursemaine[jour]
        if total > 0:
            jours_comptes = sum(1 for d in depenses_par_jour 
                               if jours_semaine[datetime.strptime(d[0], "%Y-%m-%d").weekday()] == jour)
            moyenne_jour = total / jours_comptes if jours_comptes > 0 else 0
            print(f"   • {jour:10} : {total:8.2f}€ (moy: {moyenne_jour:.2f}€)")
    
    # Recommandations
    print(f"\n💡 ANALYSE ET RECOMMANDATIONS :")
    
    # Identifier la catégorie principale
    categorie_principale = categories_triees[0][0] if categories_triees else "Aucune"
    montant_principale = categories_triees[0][1] if categories_triees else 0
    
    print(f"   • Catégorie principale : {categorie_principale} ({montant_principale:.2f}€)")
    
    if moyenne_journaliere > 50:
        print(f"   ⚠️  Dépenses journalières moyennes élevées (>50€)")
        print(f"   🎯 Objectif : Réduire à moins de 40€/jour")
    else:
        print(f"   ✅ Dépenses journalières dans une fourchette raisonnable")
    
    if len(categories_triees) > 3:
        print(f"   ℹ️  Vos dépenses sont réparties sur {len(categories_triees)} catégories")
    
    print(f"\n" + "═"*60)

# ============================================================================
# 4. STATISTIQUES GÉNÉRALES
# ============================================================================
def statistiques_generales(donnees):
    """Affiche un tableau de bord général"""
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "═"*60)
    print("📊 TABLEAU DE BORD GÉNÉRAL")
    print("═"*60)
    
    total_jours = len(donnees)
    
    if total_jours == 0:
        print("\n📭 Aucune donnée disponible")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Calculer toutes les statistiques
    stats = calculer_stats_generales(donnees)
    
    print(f"\n📅 PÉRIODE : {stats['date_debut']} à {stats['date_fin']}")
    print(f"📊 JOURS ENREGISTRÉS : {total_jours}")
    
    print(f"\n{'='*60}")
    print("🎯 RÉSUMÉ DES HABITUDES")
    print(f"{'='*60}")
    
    # Afficher sous forme de tableau
    #print(f"\n{'Catégorie':<15} {'Jours':<8} {'%':<8} {'Moyenne':<12} {'Score':<6}")
    print(f"\n{'Catégorie':<15} {'Jours':<12} {'%':<9} {'Moyenne':<12} {'Score':<6}")
    print(f"{'-'*55}")
    
    # Sommeil
    jours_sommeil = stats['jours_sommeil']
    pourc_sommeil = (jours_sommeil / total_jours) * 100
    moy_sommeil = stats['moyenne_sommeil']
    score_sommeil = "✅" if moy_sommeil >= 7 else "⚠️"
    print(f"{'😴 Sommeil':<15} {jours_sommeil:<8} {pourc_sommeil:<13.1f} {moy_sommeil:<12.1f} {score_sommeil:<6}")
    
    # Sport
    jours_sport = stats['jours_sport']
    pourc_sport = (jours_sport / total_jours) * 100
    moy_sport = stats['moyenne_sport_min']
    score_sport = "✅" if pourc_sport >= 50 else "⚠️"
    print(f"{'🏃 Sport':<15} {jours_sport:<8} {pourc_sport:<13.1f} {moy_sport:<12.0f} {score_sport:<6}")
    
    # Dépenses
    jours_depenses = stats['jours_depenses']
    pourc_depenses = (jours_depenses / total_jours) * 100
    moy_depenses = stats['moyenne_depenses_jour']
    score_depenses = "✅" if moy_depenses <= 40 else "⚠️"
    print(f"{'💰 Dépenses':<15} {jours_depenses:<8} {pourc_depenses:<13.1f} {moy_depenses:<11.2f} {score_depenses:<6}")
    
    print(f"\n{'='*60}")
    print("📈 INDICATEURS CLÉS")
    print(f"{'='*60}")
    
    # Score global
    score_global = calculer_score_global(stats)
    print(f"\n🏆 SCORE GLOBAL : {score_global}/100")
    
    # Barre de progression du score
    barre_score = "█" * int(score_global / 2) + "░" * (50 - int(score_global / 2))
    print(f"   [{barre_score}]")
    
    # Interprétation du score
    if score_global >= 80:
        print(f"   🎉 Excellentes habitudes !")
    elif score_global >= 60:
        print(f"   👍 Bonnes habitudes, quelques améliorations possibles")
    elif score_global >= 40:
        print(f"   ⚠️  Habitudes moyennes, des progrès à faire")
    else:
        print(f"   💪 Des améliorations significatives sont possibles")
    
    
    # Recommandations personnalisées
    print(f"\n💡 RECOMMANDATIONS PERSONNALISÉES :")
    
    recommendations = generer_recommandations(stats, donnees)
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print(f"\n" + "═"*60)

# ============================================================================
# 5. STATISTIQUES PAR PÉRIODE
# ============================================================================
def menu_statistiques_periode(donnees):
    """
    Menu pour afficher les statistiques par période
    """
    import os
    from datetime import datetime, timedelta
    
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "═"*60)
        print("📅 STATISTIQUES PAR PÉRIODE")
        print("═"*60)
        
        total_jours = len(donnees)
        dates = sorted(donnees.keys())
        date_debut = dates[0] if dates else "N/A"
        date_fin = dates[-1] if dates else "N/A"
        
        print(f"\n📊 Données disponibles : {total_jours} jours")
        print(f"📅 Période : {date_debut} à {date_fin}")
        
        print("\n" + "═"*60)
        print("📈 CHOISIR UNE PÉRIODE")
        print("═"*60)
        print("1. 📊 7 derniers jours")
        print("2. 📊 30 derniers jours")
        print("3. 📊 Ce mois-ci")
        print("4. 📊 Le mois dernier")
        print("5. 📊 Personnaliser une période")
        print("6. 📊 Comparer deux périodes")
        print("7. 📊 Toutes les données (global)")
        print("8. ↩️  Retour aux statistiques")
        
        choix = input("\nVotre choix : ").strip()
        
        if choix == "1":
            # 7 derniers jours
            stats_7j = calculer_statistiques_periode(donnees, jours=7)
            afficher_statistiques_periode(stats_7j, "7 derniers jours")
        
        elif choix == "2":
            # 30 derniers jours
            stats_30j = calculer_statistiques_periode(donnees, jours=30)
            afficher_statistiques_periode(stats_30j, "30 derniers jours")
        
        elif choix == "3":
            # Ce mois-ci
            stats_mois_courant = calculer_statistiques_mois(donnees, mois_courant=True)
            afficher_statistiques_periode(stats_mois_courant, "ce mois-ci")
        
        elif choix == "4":
            # Mois dernier
            stats_mois_precedent = calculer_statistiques_mois(donnees, mois_courant=False)
            afficher_statistiques_periode(stats_mois_precedent, "le mois dernier")
        
        elif choix == "5":
            # Période personnalisée
            periode_perso = choisir_periode_personnalisee(donnees)
            if periode_perso:
                stats_perso = calculer_statistiques_periode_custom(donnees, periode_perso[0], periode_perso[1])
                afficher_statistiques_periode(stats_perso, f"du {periode_perso[0]} au {periode_perso[1]}")
        
        elif choix == "6":
            # Comparer deux périodes
            comparer_deux_periodes(donnees)
        
        elif choix == "7":
            # Toutes les données
            stats_globales = calculer_statistiques_globales(donnees)
            afficher_statistiques_periode(stats_globales, "toutes les données")
        
        elif choix == "8":
            break
        
        else:
            print("❌ Choix invalide")
        
        input("\nAppuyez sur Entrée pour continuer...")

# ============================================
# 6. RAPPORT STATISTIQUES COMPLET
# ============================================
def generer_rapport_complet(donnees):
    """
    Génère un rapport statistique complet des données
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible pour générer un rapport")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*80)
    print("📊 RAPPORT STATISTIQUE COMPLET")
    print("═"*80)
    
    # ============================================
    # 1. INFORMATIONS GÉNÉRALES
    # ============================================
    print("\n" + "─"*80)
    print("📋 INFORMATIONS GÉNÉRALES")
    print("─"*80)
    
    dates = sorted(donnees.keys())
    nb_jours = len(donnees)
    
    date_debut = datetime.strptime(dates[0], "%Y-%m-%d")
    date_fin = datetime.strptime(dates[-1], "%Y-%m-%d")
    periode_totale = (date_fin - date_debut).days + 1
    
    print(f"📅 Période analysée : {dates[0]} au {dates[-1]}")
    print(f"📊 Nombre de jours enregistrés : {nb_jours}")
    print(f"📆 Période totale : {periode_totale} jour(s)")
    print(f"📈 Taux de remplissage : {(nb_jours/periode_totale)*100:.1f}%")
    
    # ============================================
    # 2. STATISTIQUES SOMMEIL
    # ============================================
    print("\n" + "─"*80)
    print("😴 STATISTIQUES SOMMEIL")
    print("─"*80)
    
    durees_sommeil = []
    qualites_sommeil = []
    jours_avec_sommeil = 0
    
    for date_str, valeurs in donnees.items():
        sommeil = valeurs.get('sommeil', {})
        if sommeil:
            jours_avec_sommeil += 1
            if 'duree' in sommeil:
                durees_sommeil.append(sommeil['duree'])
            if 'qualite' in sommeil:
                qualites_sommeil.append(sommeil['qualite'])
    
    print(f"📊 Jours avec données de sommeil : {jours_avec_sommeil}/{nb_jours} ({(jours_avec_sommeil/nb_jours)*100:.1f}%)")
    
    if durees_sommeil:
        duree_moyenne = sum(durees_sommeil) / len(durees_sommeil)
        duree_min = min(durees_sommeil)
        duree_max = max(durees_sommeil)
        
        print(f"\n⏰ DURÉE DE SOMMEIL")
        print(f"   • Moyenne : {duree_moyenne:.2f}h")
        print(f"   • Minimum : {duree_min:.2f}h")
        print(f"   • Maximum : {duree_max:.2f}h")
        print(f"   • Total cumulé : {sum(durees_sommeil):.2f}h")
        
        # Évaluation
        if duree_moyenne >= 7 and duree_moyenne <= 9:
            print(f"   ✅ Durée moyenne idéale")
        elif duree_moyenne < 7:
            print(f"   ⚠️  Durée moyenne insuffisante (recommandé: 7-9h)")
        else:
            print(f"   ⚠️  Durée moyenne élevée")
        
        # Distribution
        print(f"\n   📊 RÉPARTITION")
        moins_6h = sum(1 for d in durees_sommeil if d < 6)
        entre_6_8h = sum(1 for d in durees_sommeil if 6 <= d < 8)
        entre_8_9h = sum(1 for d in durees_sommeil if 8 <= d < 9)
        plus_9h = sum(1 for d in durees_sommeil if d >= 9)
        
        print(f"   • Moins de 6h : {moins_6h} jour(s) ({(moins_6h/len(durees_sommeil))*100:.1f}%)")
        print(f"   • 6-8h : {entre_6_8h} jour(s) ({(entre_6_8h/len(durees_sommeil))*100:.1f}%)")
        print(f"   • 8-9h : {entre_8_9h} jour(s) ({(entre_8_9h/len(durees_sommeil))*100:.1f}%)")
        print(f"   • Plus de 9h : {plus_9h} jour(s) ({(plus_9h/len(durees_sommeil))*100:.1f}%)")
    
    if qualites_sommeil:
        qualite_moyenne = sum(qualites_sommeil) / len(qualites_sommeil)
        qualite_min = min(qualites_sommeil)
        qualite_max = max(qualites_sommeil)
        
        print(f"\n⭐ QUALITÉ DE SOMMEIL")
        print(f"   • Moyenne : {qualite_moyenne:.2f}/10")
        print(f"   • Minimum : {qualite_min}/10")
        print(f"   • Maximum : {qualite_max}/10")
        
        # Barre de progression
        barre = "█" * int(qualite_moyenne) + "░" * (10 - int(qualite_moyenne))
        print(f"   • Visualisation : [{barre}]")
        
        # Évaluation
        if qualite_moyenne >= 7:
            print(f"   ✅ Qualité de sommeil bonne")
        elif qualite_moyenne >= 5:
            print(f"   ⚠️  Qualité de sommeil moyenne")
        else:
            print(f"   ❌ Qualité de sommeil faible")
        
        # Distribution
        print(f"\n   📊 RÉPARTITION")
        mauvais = sum(1 for q in qualites_sommeil if q <= 3)
        moyen = sum(1 for q in qualites_sommeil if 4 <= q <= 6)
        bon = sum(1 for q in qualites_sommeil if 7 <= q <= 8)
        excellent = sum(1 for q in qualites_sommeil if q >= 9)
        
        print(f"   • Mauvais (1-3) : {mauvais} jour(s) ({(mauvais/len(qualites_sommeil))*100:.1f}%)")
        print(f"   • Moyen (4-6) : {moyen} jour(s) ({(moyen/len(qualites_sommeil))*100:.1f}%)")
        print(f"   • Bon (7-8) : {bon} jour(s) ({(bon/len(qualites_sommeil))*100:.1f}%)")
        print(f"   • Excellent (9-10) : {excellent} jour(s) ({(excellent/len(qualites_sommeil))*100:.1f}%)")
    
    # ============================================
    # 3. STATISTIQUES SPORT
    # ============================================
    print("\n" + "─"*80)
    print("🏃 STATISTIQUES ACTIVITÉ SPORTIVE")
    print("─"*80)
    
    durees_sport = []
    types_sport = {}
    intensites = {"faible": 0, "moyenne": 0, "élevée": 0}
    jours_avec_sport = 0
    
    for date_str, valeurs in donnees.items():
        sport = valeurs.get('sport', {})
        if sport and sport.get('duree', 0) > 0:
            jours_avec_sport += 1
            durees_sport.append(sport['duree'])
            
            # Types de sport
            type_sport = sport.get('type', 'Non spécifié')
            types_sport[type_sport] = types_sport.get(type_sport, 0) + 1
            
            # Intensités
            intensite = sport.get('intensite', '').lower()
            if intensite in intensites:
                intensites[intensite] += 1
    
    print(f"📊 Jours avec activité sportive : {jours_avec_sport}/{nb_jours} ({(jours_avec_sport/nb_jours)*100:.1f}%)")
    
    if durees_sport:
        duree_totale = sum(durees_sport)
        duree_moyenne = duree_totale / len(durees_sport)
        duree_min = min(durees_sport)
        duree_max = max(durees_sport)
        
        print(f"\n⏱️  DURÉE D'ACTIVITÉ")
        print(f"   • Total cumulé : {duree_totale} minutes ({duree_totale/60:.2f}h)")
        print(f"   • Moyenne par séance : {duree_moyenne:.1f} minutes")
        print(f"   • Minimum : {duree_min} minutes")
        print(f"   • Maximum : {duree_max} minutes")
        print(f"   • Moyenne par jour (sur toute la période) : {duree_totale/nb_jours:.1f} min/jour")
        
        # Objectif hebdomadaire (150 min recommandé par OMS)
        moyenne_hebdo = (duree_totale / nb_jours) * 7
        print(f"\n   🎯 OBJECTIF HEBDOMADAIRE")
        print(f"   • Votre moyenne : {moyenne_hebdo:.0f} min/semaine")
        print(f"   • Objectif OMS : 150 min/semaine")
        if moyenne_hebdo >= 150:
            print(f"   ✅ Objectif atteint ! ({(moyenne_hebdo/150)*100:.0f}%)")
        else:
            print(f"   ⚠️  {150-moyenne_hebdo:.0f} min manquantes ({(moyenne_hebdo/150)*100:.0f}%)")
        
        # Distribution des durées
        print(f"\n   📊 RÉPARTITION DES SÉANCES")
        courte = sum(1 for d in durees_sport if d < 30)
        moyenne_duree = sum(1 for d in durees_sport if 30 <= d < 60)
        longue = sum(1 for d in durees_sport if d >= 60)
        
        print(f"   • Courte (<30 min) : {courte} séance(s) ({(courte/len(durees_sport))*100:.1f}%)")
        print(f"   • Moyenne (30-60 min) : {moyenne_duree} séance(s) ({(moyenne_duree/len(durees_sport))*100:.1f}%)")
        print(f"   • Longue (≥60 min) : {longue} séance(s) ({(longue/len(durees_sport))*100:.1f}%)")
    
    if types_sport:
        print(f"\n🏋️  TYPES D'ACTIVITÉS")
        types_tries = sorted(types_sport.items(), key=lambda x: x[1], reverse=True)
        for i, (type_act, count) in enumerate(types_tries[:10], 1):
            pourcentage = (count / jours_avec_sport) * 100
            barre = "█" * int(pourcentage / 5)
            print(f"   {i}. {type_act}: {count} fois ({pourcentage:.1f}%) {barre}")
        
        if len(types_tries) > 10:
            print(f"   ... et {len(types_tries)-10} autre(s) activité(s)")
    
    if any(intensites.values()):
        total_intensites = sum(intensites.values())
        print(f"\n💪 INTENSITÉS")
        for intensite, count in intensites.items():
            if count > 0:
                pourcentage = (count / total_intensites) * 100
                print(f"   • {intensite.capitalize()} : {count} séance(s) ({pourcentage:.1f}%)")
    
    # ============================================
    # 4. STATISTIQUES DÉPENSES
    # ============================================
    print("\n" + "─"*80)
    print("💰 STATISTIQUES DÉPENSES")
    print("─"*80)
    
    montants_journaliers = []
    categories_depenses = {}
    total_depenses = 0
    nb_transactions = 0
    jours_avec_depenses = 0
    
    for date_str, valeurs in donnees.items():
        depenses = valeurs.get('depenses', [])
        if depenses:
            jours_avec_depenses += 1
            montant_jour = 0
            
            for depense in depenses:
                montant = depense.get('montant', 0)
                categorie = depense.get('categorie', 'Non catégorisé')
                
                montant_jour += montant
                total_depenses += montant
                nb_transactions += 1
                
                categories_depenses[categorie] = categories_depenses.get(categorie, 0) + montant
            
            montants_journaliers.append(montant_jour)
    
    print(f"📊 Jours avec dépenses : {jours_avec_depenses}/{nb_jours} ({(jours_avec_depenses/nb_jours)*100:.1f}%)")
    print(f"📊 Nombre total de transactions : {nb_transactions}")
    
    if montants_journaliers:
        depense_moyenne = sum(montants_journaliers) / len(montants_journaliers)
        depense_min = min(montants_journaliers)
        depense_max = max(montants_journaliers)
        
        print(f"\n💵 MONTANTS")
        print(f"   • Total cumulé : {total_depenses:.2f}$")
        print(f"   • Moyenne par jour (avec dépenses) : {depense_moyenne:.2f}$")
        print(f"   • Moyenne par jour (sur toute période) : {total_depenses/nb_jours:.2f}$")
        print(f"   • Minimum (par jour) : {depense_min:.2f}$")
        print(f"   • Maximum (par jour) : {depense_max:.2f}$")
        print(f"   • Moyenne par transaction : {total_depenses/nb_transactions:.2f}$")
        
        # Projections
        print(f"\n   📈 PROJECTIONS")
        depense_hebdo = (total_depenses / nb_jours) * 7
        depense_mensuelle = (total_depenses / nb_jours) * 30
        depense_annuelle = (total_depenses / nb_jours) * 365
        
        print(f"   • Hebdomadaire : {depense_hebdo:.2f}$")
        print(f"   • Mensuelle : {depense_mensuelle:.2f}$")
        print(f"   • Annuelle : {depense_annuelle:.2f}$")
        
        # Distribution
        print(f"\n   📊 RÉPARTITION DES DÉPENSES JOURNALIÈRES")
        faible = sum(1 for m in montants_journaliers if m < 20)
        moyen = sum(1 for m in montants_journaliers if 20 <= m < 50)
        eleve = sum(1 for m in montants_journaliers if 50 <= m < 100)
        tres_eleve = sum(1 for m in montants_journaliers if m >= 100)
        
        print(f"   • Faible (<20$) : {faible} jour(s) ({(faible/len(montants_journaliers))*100:.1f}%)")
        print(f"   • Moyen (20-50$) : {moyen} jour(s) ({(moyen/len(montants_journaliers))*100:.1f}%)")
        print(f"   • Élevé (50-100$) : {eleve} jour(s) ({(eleve/len(montants_journaliers))*100:.1f}%)")
        print(f"   • Très élevé (≥100$) : {tres_eleve} jour(s) ({(tres_eleve/len(montants_journaliers))*100:.1f}%)")
    
    if categories_depenses:
        print(f"\n🏷️  DÉPENSES PAR CATÉGORIE")
        categories_triees = sorted(categories_depenses.items(), key=lambda x: x[1], reverse=True)
        
        for i, (categorie, montant) in enumerate(categories_triees[:10], 1):
            pourcentage = (montant / total_depenses) * 100
            barre = "█" * int(pourcentage / 5)
            print(f"   {i}. {categorie}: {montant:.2f}$ ({pourcentage:.1f}%) {barre}")
        
        if len(categories_triees) > 10:
            autres = sum(m for c, m in categories_triees[10:])
            print(f"   ... Autres ({len(categories_triees)-10} catégories): {autres:.2f}$")
    
    # ============================================
    # 5. SCORE DE BIEN-ÊTRE GLOBAL
    # ============================================
    print("\n" + "─"*80)
    print("🌟 SCORE DE BIEN-ÊTRE GLOBAL")
    print("─"*80)
    
    score_total = 0
    score_max = 0
    
    # Score sommeil (sur 40 points)
    if durees_sommeil:
        score_max += 40
        
        # Durée (20 points)
        if duree_moyenne >= 7 and duree_moyenne <= 9:
            score_sommeil_duree = 20
        elif duree_moyenne >= 6 and duree_moyenne <= 10:
            score_sommeil_duree = 15
        else:
            score_sommeil_duree = 10
        
        # Qualité (20 points)
        if qualites_sommeil:
            score_sommeil_qualite = (qualite_moyenne / 10) * 20
        else:
            score_sommeil_qualite = 15  # Score par défaut
        
        score_sommeil_total = score_sommeil_duree + score_sommeil_qualite
        score_total += score_sommeil_total
        
        print(f"😴 SOMMEIL : {score_sommeil_total:.1f}/40 points")
        print(f"   • Durée : {score_sommeil_duree}/20")
        print(f"   • Qualité : {score_sommeil_qualite:.1f}/20")
    
    # Score sport (sur 30 points)
    if durees_sport:
        score_max += 30
        
        # Fréquence (15 points)
        frequence = (jours_avec_sport / nb_jours) * 100
        if frequence >= 50:
            score_sport_freq = 15
        elif frequence >= 30:
            score_sport_freq = 10
        else:
            score_sport_freq = 5
        
        # Durée moyenne (15 points)
        if moyenne_hebdo >= 150:
            score_sport_duree = 15
        elif moyenne_hebdo >= 100:
            score_sport_duree = 10
        else:
            score_sport_duree = 5
        
        score_sport_total = score_sport_freq + score_sport_duree
        score_total += score_sport_total
        
        print(f"🏃 SPORT : {score_sport_total}/30 points")
        print(f"   • Fréquence : {score_sport_freq}/15")
        print(f"   • Volume : {score_sport_duree}/15")
    
    # Score dépenses (sur 30 points)
    if montants_journaliers:
        score_max += 30
        
        # Contrôle des dépenses (30 points basé sur régularité)
        depense_quotidienne = total_depenses / nb_jours
        
        if depense_quotidienne < 30:
            score_depenses = 30
        elif depense_quotidienne < 50:
            score_depenses = 20
        else:
            score_depenses = 10
        
        score_total += score_depenses
        
        print(f"💰 DÉPENSES : {score_depenses}/30 points")
        print(f"   • Contrôle budgétaire")
    
    # Score final
    if score_max > 0:
        pourcentage_final = (score_total / score_max) * 100
        
        print(f"\n{'═'*80}")
        print(f"🎯 SCORE GLOBAL : {score_total:.1f}/{score_max} points ({pourcentage_final:.1f}%)")
        
        barre = "█" * int(pourcentage_final / 5) + "░" * (20 - int(pourcentage_final / 5))
        print(f"   [{barre}]")
        
        if pourcentage_final >= 80:
            print(f"   ⭐⭐⭐ EXCELLENT ! Continuez comme ça !")
        elif pourcentage_final >= 60:
            print(f"   ⭐⭐ BIEN ! Quelques améliorations possibles")
        elif pourcentage_final >= 40:
            print(f"   ⭐ MOYEN. Des efforts sont nécessaires")
        else:
            print(f"   ⚠️  FAIBLE. Beaucoup d'améliorations à faire")
        print(f"{'═'*80}")
    
    # ============================================
    # 6. RECOMMANDATIONS
    # ============================================
    print("\n" + "─"*80)
    print("💡 RECOMMANDATIONS PERSONNALISÉES")
    print("─"*80)
    
    recommandations = []
    
    # Sommeil
    if durees_sommeil:
        if duree_moyenne < 7:
            recommandations.append("😴 Augmentez votre temps de sommeil (objectif: 7-9h)")
        if qualites_sommeil and qualite_moyenne < 7:
            recommandations.append("😴 Travaillez sur la qualité de votre sommeil (routine, environnement)")
    
    # Sport
    if jours_avec_sport == 0:
        recommandations.append("🏃 Commencez une activité physique régulière")
    elif durees_sport and moyenne_hebdo < 150:
        recommandations.append(f"🏃 Augmentez votre activité physique ({150-moyenne_hebdo:.0f} min manquantes/semaine)")
    
    # Dépenses
    if montants_journaliers:
        if depense_moyenne > 50:
            recommandations.append("💰 Essayez de réduire vos dépenses quotidiennes")
        if len(categories_depenses) > 10:
            recommandations.append("💰 Simplifiez vos catégories de dépenses pour mieux suivre votre budget")
    
    if recommandations:
        for i, rec in enumerate(recommandations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   ✅ Excellent travail ! Continuez sur cette lancée !")
    
    print("\n" + "═"*80)
    print("📊 FIN DU RAPPORT")
    print("═"*80)

# ============================================
# 7. EXPORTER RAPPORT VERS .TEXT
# ============================================
def exporter_rapport_txt(donnees, nom_fichier=None):
    """
    Exporte le rapport complet au format .txt
    """
    if not donnees:
        print("❌ Aucune donnée à exporter")
        return

    dossier = 'Statistiques_Raport'
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    # Nom du fichier par défaut
    if nom_fichier is None:
        date_export = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nom_fichier = f"{dossier}/rapport_statistique_{date_export}.txt"

    # Sauvegarde de la sortie standard
    stdout_original = sys.stdout

    try:
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            sys.stdout = fichier  # redirection des print()
            
            # Appel de TON rapport existant
            generer_rapport_complet(donnees)

        sys.stdout = stdout_original
        print(f"✅ Rapport exporté avec succès : {os.path.abspath(nom_fichier)}")

    except Exception as e:
        sys.stdout = stdout_original
        print(f"❌ Erreur lors de l’export : {e}")



 
# ============================================================================
# FONCTIONS DE CALCUL DES STATISTIQUES PAR PÉRIODE
# ============================================================================
def calculer_statistiques_periode(donnees, jours=7):
    """
    Calcule les statistiques pour les N derniers jours
    """
    from datetime import datetime, timedelta
    
    date_fin = datetime.now().date()
    date_debut = date_fin - timedelta(days=jours-1)
    
    # Filtrer les données de la période
    donnees_periode = {}
    for date_str, valeurs in donnees.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_debut <= date_obj <= date_fin:
            donnees_periode[date_str] = valeurs
    
    return {
        'donnees': donnees_periode,
        'date_debut': date_debut.strftime("%Y-%m-%d"),
        'date_fin': date_fin.strftime("%Y-%m-%d"),
        'total_jours': len(donnees_periode),
        'jours_demandes': jours,
        'taux_completude': (len(donnees_periode) / jours) * 100 if jours > 0 else 0
    }

def calculer_statistiques_mois(donnees, mois_courant=True):
    """
    Calcule les statistiques pour le mois courant ou précédent
    """
    from datetime import datetime
    
    maintenant = datetime.now()
    
    if mois_courant:
        # Mois courant
        annee = maintenant.year
        mois = maintenant.month
        periode_nom = "ce mois-ci"
    else:
        # Mois précédent
        if maintenant.month == 1:
            annee = maintenant.year - 1
            mois = 12
        else:
            annee = maintenant.year
            mois = maintenant.month - 1
        periode_nom = "le mois dernier"
    
    # Premier et dernier jour du mois
    date_debut = datetime(annee, mois, 1).date()
    
    if mois == 12:
        date_fin = datetime(annee + 1, 1, 1).date() - timedelta(days=1)
    else:
        date_fin = datetime(annee, mois + 1, 1).date() - timedelta(days=1)
    
    # Filtrer les données du mois
    donnees_mois = {}
    for date_str, valeurs in donnees.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_debut <= date_obj <= date_fin:
            donnees_mois[date_str] = valeurs
    
    jours_dans_mois = (date_fin - date_debut).days + 1
    
    return {
        'donnees': donnees_mois,
        'date_debut': date_debut.strftime("%Y-%m-%d"),
        'date_fin': date_fin.strftime("%Y-%m-%d"),
        'total_jours': len(donnees_mois),
        'jours_dans_mois': jours_dans_mois,
        'taux_completude': (len(donnees_mois) / jours_dans_mois) * 100 if jours_dans_mois > 0 else 0,
        'periode_nom': periode_nom,
        'mois': mois,
        'annee': annee
    }

def choisir_periode_personnalisee(donnees):
    """
    Permet à l'utilisateur de choisir une période personnalisée
    """
    from datetime import datetime
    
    if not donnees:
        print("📭 Aucune donnée disponible")
        return None
    
    dates_disponibles = sorted(donnees.keys())
    print(f"\n📅 Dates disponibles : {dates_disponibles[0]} à {dates_disponibles[-1]}")
    
    print("\n" + "-"*40)
    print("📅 CHOISIR UNE PÉRIODE PERSONNALISÉE")
    print("-"*40)
    
    # Date de début
    while True:
        date_debut = input("\nDate de début (AAAA-MM-JJ) : ").strip()
        if not date_debut:
            print("❌ Annulé")
            return None
        
        try:
            date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d").date()
            if date_debut < dates_disponibles[0]:
                print(f"⚠️  Date avant la première donnée ({dates_disponibles[0]})")
                continuer = input("Continuer quand même ? (O/N) : ").strip().lower()
                if continuer not in ['o', 'oui', 'y', 'yes']:
                    continue
            break
        except ValueError:
            print("❌ Format invalide. Utilisez AAAA-MM-JJ")
    
    # Date de fin
    while True:
        date_fin = input("Date de fin (AAAA-MM-JJ) : ").strip()
        if not date_fin:
            print("❌ Annulé")
            return None
        
        try:
            date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d").date()
            
            if date_fin_obj < date_debut_obj:
                print("❌ La date de fin doit être après la date de début")
                continue
            
            if date_fin > dates_disponibles[-1]:
                print(f"⚠️  Date après la dernière donnée ({dates_disponibles[-1]})")
                continuer = input("Continuer quand même ? (O/N) : ").strip().lower()
                if continuer not in ['o', 'oui', 'y', 'yes']:
                    continue
            break
        except ValueError:
            print("❌ Format invalide. Utilisez AAAA-MM-JJ")
    
    return (date_debut, date_fin)

def calculer_statistiques_periode_custom(donnees, date_debut_str, date_fin_str):
    """
    Calcule les statistiques pour une période personnalisée
    """
    from datetime import datetime, timedelta
    
    date_debut = datetime.strptime(date_debut_str, "%Y-%m-%d").date()
    date_fin = datetime.strptime(date_fin_str, "%Y-%m-%d").date()
    
    # Filtrer les données de la période
    donnees_periode = {}
    for date_str, valeurs in donnees.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_debut <= date_obj <= date_fin:
            donnees_periode[date_str] = valeurs
    
    jours_periode = (date_fin - date_debut).days + 1
    
    return {
        'donnees': donnees_periode,
        'date_debut': date_debut_str,
        'date_fin': date_fin_str,
        'total_jours': len(donnees_periode),
        'jours_periode': jours_periode,
        'taux_completude': (len(donnees_periode) / jours_periode) * 100 if jours_periode > 0 else 0
    }

def calculer_statistiques_globales(donnees):
    """
    Calcule les statistiques pour toutes les données
    """
    return {
        'donnees': donnees,
        'total_jours': len(donnees),
        'periode_nom': 'toutes les données'
    }

def afficher_statistiques_periode(periode_stats, titre_periode):
    """
    Affiche les statistiques d'une période
    """
    import os
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    donnees = periode_stats['donnees']
    
    if not donnees:
        print(f"\n📭 Aucune donnée disponible pour {titre_periode}")
        return
    
    print("\n" + "═"*60)
    print(f"📊 STATISTIQUES - {titre_periode.upper()}")
    print("═"*60)
    
    # Informations sur la période
    if 'date_debut' in periode_stats and 'date_fin' in periode_stats:
        print(f"\n📅 Période : {periode_stats['date_debut']} à {periode_stats['date_fin']}")
    
    print(f"📊 Jours avec données : {periode_stats['total_jours']}")
    
    if 'taux_completude' in periode_stats:
        print(f"📈 Complétude : {periode_stats['taux_completude']:.1f}%")
    
    print("\n" + "═"*60)
    
    # Calculer les statistiques détaillées
    stats_sommeil = calculer_stats_sommeil_periode(donnees)
    stats_sport = calculer_stats_sport_periode(donnees)
    stats_depenses = calculer_stats_depenses_periode(donnees)
    
    # Afficher les statistiques par catégorie
    print("\n😴 SOMMEIL :")
    print("-" * 40)
    if stats_sommeil['jours'] > 0:
        print(f"   • Jours enregistrés : {stats_sommeil['jours']}")
        print(f"   • Moyenne durée : {stats_sommeil['moyenne_duree']:.1f}h")
        print(f"   • Minimum : {stats_sommeil['min_duree']:.1f}h")
        print(f"   • Maximum : {stats_sommeil['max_duree']:.1f}h")
        if stats_sommeil['moyenne_qualite'] > 0:
            print(f"   • Qualité moyenne : {stats_sommeil['moyenne_qualite']:.1f}/10")
    else:
        print("   Aucune donnée de sommeil")
    
    print("\n🏃 ACTIVITÉ SPORTIVE :")
    print("-" * 40)
    if stats_sport['jours'] > 0:
        print(f"   • Jours avec sport : {stats_sport['jours']}")
        print(f"   • Fréquence : {stats_sport['frequence']:.1f}%")
        print(f"   • Temps total : {stats_sport['total_minutes']}min")
        print(f"   • Moyenne/séance : {stats_sport['moyenne_duree']:.0f}min")
        if stats_sport['activite_principale']:
            print(f"   • Activité principale : {stats_sport['activite_principale']}")
    else:
        print("   Aucune activité sportive")
    
    print("\n💰 DÉPENSES :")
    print("-" * 40)
    if stats_depenses['jours'] > 0:
        print(f"   • Jours avec dépenses : {stats_depenses['jours']}")
        print(f"   • Total : {stats_depenses['total']:.2f}€")
        print(f"   • Moyenne/jour (avec dépenses) : {stats_depenses['moyenne_par_jour']:.2f}€")
        print(f"   • Moyenne/tous les jours : {stats_depenses['moyenne_tous_jours']:.2f}€")
        if stats_depenses['categorie_principale']:
            print(f"   • Catégorie principale : {stats_depenses['categorie_principale']}")
    else:
        print("   Aucune dépense")
    
    print("\n" + "═"*60)
    
    # Score de la période
    score = calculer_score_periode(stats_sommeil, stats_sport, stats_depenses)
    print(f"\n🏆 SCORE DE LA PÉRIODE : {score}/100")
    
    # Barre de progression
    barre = "█" * int(score / 2) + "░" * (50 - int(score / 2))
    print(f"   [{barre}]")
    
    # Interprétation
    if score >= 80:
        print("   🎉 Excellente période !")
    elif score >= 60:
        print("   👍 Bonne période")
    elif score >= 40:
        print("   ⚠️  Période moyenne")
    else:
        print("   💪 Des améliorations possibles")
    
    print("\n" + "═"*60)
    
# ============================================================================
# FONCTIONS DE CALCUL SPÉCIFIQUES
# ============================================================================

def calculer_stats_sommeil_periode(donnees):
    """Calcule les statistiques de sommeil pour une période"""
    stats = {
        'jours': 0,
        'moyenne_duree': 0,
        'min_duree': 24,
        'max_duree': 0,
        'moyenne_qualite': 0,
        'total_duree': 0
    }
    
    durees = []
    qualites = []
    
    for valeurs in donnees.values():
        sommeil = valeurs.get('sommeil', {})
        if sommeil and 'duree' in sommeil:
            duree = sommeil['duree']
            stats['jours'] += 1
            durees.append(duree)
            stats['total_duree'] += duree
            
            if duree < stats['min_duree']:
                stats['min_duree'] = duree
            if duree > stats['max_duree']:
                stats['max_duree'] = duree
            
            if 'qualite' in sommeil:
                qualites.append(sommeil['qualite'])
    
    if durees:
        stats['moyenne_duree'] = sum(durees) / len(durees)
    
    if qualites:
        stats['moyenne_qualite'] = sum(qualites) / len(qualites)
    
    if stats['min_duree'] == 24:  # Si aucune donnée
        stats['min_duree'] = 0
    
    return stats

def calculer_stats_sport_periode(donnees):
    """Calcule les statistiques de sport pour une période"""
    from collections import Counter
    
    stats = {
        'jours': 0,
        'total_minutes': 0,
        'moyenne_duree': 0,
        'frequence': 0,
        'activite_principale': '',
        'types': Counter()
    }
    
    total_jours = len(donnees)
    durees = []
    types = []
    
    for valeurs in donnees.values():
        sport = valeurs.get('sport', {})
        if sport and sport.get('duree', 0) > 0:
            duree = sport['duree']
            stats['jours'] += 1
            stats['total_minutes'] += duree
            durees.append(duree)
            
            type_sport = sport.get('type', 'Non spécifié')
            types.append(type_sport)
            stats['types'][type_sport] += 1
    
    if durees:
        stats['moyenne_duree'] = sum(durees) / len(durees)
    
    if total_jours > 0:
        stats['frequence'] = (stats['jours'] / total_jours) * 100
    
    if stats['types']:
        stats['activite_principale'] = stats['types'].most_common(1)[0][0]
    
    return stats

def calculer_stats_depenses_periode(donnees):
    """Calcule les statistiques de dépenses pour une période"""
    from collections import Counter, defaultdict
    
    stats = {
        'jours': 0,
        'total': 0,
        'moyenne_par_jour': 0,
        'moyenne_tous_jours': 0,
        'categorie_principale': '',
        'total_transactions': 0
    }
    
    totaux_journaliers = []
    categories = defaultdict(float)
    
    for valeurs in donnees.values():
        depenses = valeurs.get('depenses', [])
        if depenses:
            total_jour = sum(d.get('montant', 0) for d in depenses)
            stats['jours'] += 1
            stats['total'] += total_jour
            stats['total_transactions'] += len(depenses)
            totaux_journaliers.append(total_jour)
            
            for depense in depenses:
                categorie = depense.get('categorie', 'Non catégorisé')
                montant = depense.get('montant', 0)
                categories[categorie] += montant
    
    if totaux_journaliers:
        stats['moyenne_par_jour'] = sum(totaux_journaliers) / len(totaux_journaliers)
    
    total_jours = len(donnees)
    if total_jours > 0:
        stats['moyenne_tous_jours'] = stats['total'] / total_jours
    
    if categories:
        stats['categorie_principale'] = max(categories.items(), key=lambda x: x[1])[0]
    
    return stats

def calculer_score_periode(stats_sommeil, stats_sport, stats_depenses):
    """Calcule un score global pour la période"""
    score = 0
    
    # Score sommeil (max 40 points)
    if stats_sommeil['jours'] > 0:
        duree_moyenne = stats_sommeil['moyenne_duree']
        if 7 <= duree_moyenne <= 9:
            score += 40  # Parfait
        elif 6 <= duree_moyenne < 7 or 9 < duree_moyenne <= 10:
            score += 30  # Acceptable
        elif duree_moyenne > 0:
            score += 20  # À améliorer
    
    # Score sport (max 30 points)
    if stats_sport['jours'] > 0:
        frequence = stats_sport['frequence']
        if frequence >= 50:
            score += 30  # Très régulier
        elif frequence >= 30:
            score += 20  # Régulier
        elif frequence >= 10:
            score += 10  # Occasionnel
    
    # Score dépenses (max 30 points)
    if stats_depenses['jours'] > 0:
        moyenne_journaliere = stats_depenses['moyenne_par_jour']
        if moyenne_journaliere <= 30:
            score += 30  # Très bon contrôle
        elif moyenne_journaliere <= 50:
            score += 20  # Bon contrôle
        elif moyenne_journaliere <= 80:
            score += 10  # Controle moyen
    
    return min(100, score)  # Limiter à 100

# ============================================================================
# FONCTIONS DE COMPARAISON
# ============================================================================

def comparer_deux_periodes(donnees):
    """
    Compare les statistiques de deux périodes
    """
    from datetime import datetime, timedelta
    
    print("\n" + "═"*60)
    print("📊 COMPARAISON DE DEUX PÉRIODES")
    print("═"*60)
    
    # Période 1
    print("\n📅 PÉRIODE 1 :")
    periode1 = choisir_periode_personnalisee(donnees)
    if not periode1:
        return
    
    stats1 = calculer_statistiques_periode_custom(donnees, periode1[0], periode1[1])
    
    # Période 2
    print("\n📅 PÉRIODE 2 :")
    periode2 = choisir_periode_personnalisee(donnees)
    if not periode2:
        return
    
    stats2 = calculer_statistiques_periode_custom(donnees, periode2[0], periode2[1])
    
    # Afficher la comparaison
    afficher_comparaison_periodes(stats1, stats2)

def afficher_comparaison_periodes(stats1, stats2):
    """Affiche la comparaison entre deux périodes"""
    import os
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "═"*60)
    print("📊 COMPARAISON DES PÉRIODES")
    print("═"*60)
    
    print(f"\n📅 Période 1 : {stats1['date_debut']} à {stats1['date_fin']}")
    print(f"   • {stats1['total_jours']} jours ({stats1['taux_completude']:.1f}% de complétude)")
    
    print(f"\n📅 Période 2 : {stats2['date_debut']} à {stats2['date_fin']}")
    print(f"   • {stats2['total_jours']} jours ({stats2['taux_completude']:.1f}% de complétude)")
    
    print("\n" + "═"*60)
    print("📈 COMPARAISON DÉTAILLÉE")
    print("═"*60)
    
    # Comparer les statistiques
    comparer_categorie("SOMMEIL", stats1, stats2, 'sommeil')
    comparer_categorie("SPORT", stats1, stats2, 'sport')
    comparer_categorie("DÉPENSES", stats1, stats2, 'depenses')
    
    print("\n" + "═"*60)
    
    # Déterminer quelle période est meilleure
    score1 = calculer_score_periode(
        calculer_stats_sommeil_periode(stats1['donnees']),
        calculer_stats_sport_periode(stats1['donnees']),
        calculer_stats_depenses_periode(stats1['donnees'])
    )
    
    score2 = calculer_score_periode(
        calculer_stats_sommeil_periode(stats2['donnees']),
        calculer_stats_sport_periode(stats2['donnees']),
        calculer_stats_depenses_periode(stats2['donnees'])
    )
    
    print(f"\n🏆 SCORES :")
    print(f"   • Période 1 : {score1}/100")
    print(f"   • Période 2 : {score2}/100")
    
    if score1 > score2:
        difference = score1 - score2
        print(f"\n📈 La période 1 est meilleure de {difference} points")
    elif score2 > score1:
        difference = score2 - score1
        print(f"\n📈 La période 2 est meilleure de {difference} points")
    else:
        print(f"\n📊 Les deux périodes sont équivalentes")
    
    print("\n" + "═"*60)

def comparer_categorie(nom_categorie, stats1, stats2, type_categorie):
    """Compare une catégorie spécifique entre deux périodes"""
    print(f"\n{nom_categorie} :")
    print("-" * 40)
    
    if type_categorie == 'sommeil':
        data1 = calculer_stats_sommeil_periode(stats1['donnees'])
        data2 = calculer_stats_sommeil_periode(stats2['donnees'])
        
        if data1['jours'] > 0 and data2['jours'] > 0:
            print(f"   • Durée moyenne : {data1['moyenne_duree']:.1f}h vs {data2['moyenne_duree']:.1f}h")
            diff_duree = data1['moyenne_duree'] - data2['moyenne_duree']
            if diff_duree > 0:
                print(f"     → +{diff_duree:.1f}h dans la période 1")
            elif diff_duree < 0:
                print(f"     → {diff_duree:.1f}h dans la période 1")
            
            print(f"   • Jours enregistrés : {data1['jours']} vs {data2['jours']}")
    
    elif type_categorie == 'sport':
        data1 = calculer_stats_sport_periode(stats1['donnees'])
        data2 = calculer_stats_sport_periode(stats2['donnees'])
        
        if data1['jours'] > 0 or data2['jours'] > 0:
            print(f"   • Fréquence : {data1['frequence']:.1f}% vs {data2['frequence']:.1f}%")
            diff_freq = data1['frequence'] - data2['frequence']
            if diff_freq > 0:
                print(f"     → +{diff_freq:.1f}% dans la période 1")
            
            print(f"   • Temps total : {data1['total_minutes']}min vs {data2['total_minutes']}min")
    
    elif type_categorie == 'depenses':
        data1 = calculer_stats_depenses_periode(stats1['donnees'])
        data2 = calculer_stats_depenses_periode(stats2['donnees'])
        
        if data1['jours'] > 0 and data2['jours'] > 0:
            print(f"   • Total dépenses : {data1['total']:.2f}€ vs {data2['total']:.2f}€")
            diff_total = data1['total'] - data2['total']
            if diff_total > 0:
                print(f"     → +{diff_total:.2f}€ dans la période 1")
            
            print(f"   • Moyenne/jour : {data1['moyenne_par_jour']:.2f}€ vs {data2['moyenne_par_jour']:.2f}€")


# ============================================================================
# FONCTIONS AUXILIAIRES
# ============================================================================

def calculer_stats_generales(donnees):
    """Calcule toutes les statistiques générales"""
    from datetime import datetime
    
    stats = {
        'total_jours': len(donnees),
        'date_debut': min(donnees.keys()) if donnees else "N/A",
        'date_fin': max(donnees.keys()) if donnees else "N/A",
        'jours_sommeil': 0,
        'jours_sport': 0,
        'jours_depenses': 0,
        'moyenne_sommeil': 0,
        'moyenne_sport_min': 0,
        'moyenne_depenses_jour': 0
    }
    
    total_sommeil = 0
    total_sport = 0
    total_depenses = 0
    
    for valeurs in donnees.values():
        # Sommeil
        sommeil = valeurs.get('sommeil', {})
        if sommeil and 'duree' in sommeil:
            stats['jours_sommeil'] += 1
            total_sommeil += sommeil['duree']
        
        # Sport
        sport = valeurs.get('sport', {})
        if sport and sport.get('duree', 0) > 0:
            stats['jours_sport'] += 1
            total_sport += sport['duree']
        
        # Dépenses
        depenses = valeurs.get('depenses', [])
        if depenses:
            stats['jours_depenses'] += 1
            total_depenses += sum(d.get('montant', 0) for d in depenses)
    
    # Calcul des moyennes
    if stats['jours_sommeil'] > 0:
        stats['moyenne_sommeil'] = total_sommeil / stats['jours_sommeil']
    
    if stats['jours_sport'] > 0:
        stats['moyenne_sport_min'] = total_sport / stats['jours_sport']
    
    if stats['jours_depenses'] > 0:
        stats['moyenne_depenses_jour'] = total_depenses / stats['jours_depenses']
    
    # Moyenne tous jours confondus
    stats['moyenne_sommeil_tous'] = total_sommeil / stats['total_jours'] if stats['total_jours'] > 0 else 0
    stats['moyenne_sport_tous'] = total_sport / stats['total_jours'] if stats['total_jours'] > 0 else 0
    stats['moyenne_depenses_tous'] = total_depenses / stats['total_jours'] if stats['total_jours'] > 0 else 0
    
    return stats

def calculer_score_global(stats):
    """Calcule un score global basé sur les habitudes"""
    score = 0
    
    # Score sommeil (max 40 points)
    if stats['moyenne_sommeil'] >= 7:
        score += min(40, (stats['moyenne_sommeil'] / 9) * 40)
    
    # Score sport (max 30 points)
    frequence_sport = stats['jours_sport'] / stats['total_jours'] if stats['total_jours'] > 0 else 0
    score += min(30, frequence_sport * 30)
    
    # Score dépenses (max 30 points)
    if stats['moyenne_depenses_jour'] > 0:
        # Moins de dépenses = meilleur score
        score_depenses = max(0, 30 - (stats['moyenne_depenses_jour'] / 100 * 30))
        score += min(30, score_depenses)
    
    return int(score)

def generer_recommandations(stats, donnees):
    """
    Version détaillée avec analyse approfondie
    
    Args:
        stats: Statistiques calculées
        donnees: Données brutes (optionnel pour analyse détaillée)
    
    Returns:
        dict: Recommandations structurées par catégorie et priorité
    """
    recommendations = {
        'sommeil': [],
        'sport': [],
        'depenses': [],
        'general': [],
        'priorite_haute': [],
        'priorite_moyenne': [],
        'priorite_basse': []
    }
    
    if not stats or stats.get('total_jours', 0) < 3:
        recommendations['general'].append("📅 Continuez à enregistrer vos données quotidiennement")
        return recommendations
    
    total_jours = stats['total_jours']
    
    # ==============================================================
    # ANALYSE DU SOMMEIL
    # ==============================================================
    if stats.get('jours_sommeil', 0) > 0:
        moyenne_sommeil = stats.get('moyenne_sommeil', 0)
        couverture_sommeil = (stats['jours_sommeil'] / total_jours) * 100
        
        # Priorité HAUTE : Sommeil très insuffisant
        if moyenne_sommeil < 6:
            msg = f"Sommeil critique : {moyenne_sommeil:.1f}h seulement"
            recommendations['sommeil'].append(msg)
            recommendations['priorite_haute'].append(f"{msg} - Moins de 6h affecte la santé")
        
        # Priorité MOYENNE : Améliorations possibles
        elif moyenne_sommeil < 7:
            msg = f"Sommeil à améliorer : {moyenne_sommeil:.1f}h, viser 7-8h"
            recommendations['sommeil'].append(msg)
            recommendations['priorite_moyenne'].append(msg)
        
        # Priorité BASSE : Bonnes habitudes
        elif 7 <= moyenne_sommeil <= 8:
            msg = f"Excellent sommeil : {moyenne_sommeil:.1f}h dans la plage idéale"
            recommendations['sommeil'].append(msg)
            recommendations['priorite_basse'].append(msg)
        
        # Sommeil excessif
        elif moyenne_sommeil > 9:
            msg = f"Sommeil excessif : {moyenne_sommeil:.1f}h, vérifier la qualité"
            recommendations['sommeil'].append(msg)
            recommendations['priorite_moyenne'].append(msg)
        
        # Couverture des données
        if couverture_sommeil < 70:
            msg = f"Suivi incomplet : {couverture_sommeil:.0f}% des nuits seulement"
            recommendations['sommeil'].append(msg)
            recommendations['priorite_moyenne'].append(f"Enregistrez votre sommeil plus régulièrement")
    
    # ==============================================================
    # ANALYSE DU SPORT
    # ==============================================================
    if stats.get('jours_sport', 0) > 0:
        jours_sport = stats['jours_sport']
        moyenne_sport = stats.get('moyenne_sport_min', 0)
        frequence = (jours_sport / total_jours) * 100
        
        # Fréquence
        if frequence < 30:  # < 2 fois/semaine
            msg = f"Fréquence très faible : {frequence:.0f}% des jours"
            recommendations['sport'].append(msg)
            recommendations['priorite_haute'].append("Augmentez l'activité physique à 3x/semaine")
        
        elif frequence < 50:  # 2-3 fois/semaine
            msg = f"Bonne fréquence : {frequence:.0f}% des jours"
            recommendations['sport'].append(msg)
            recommendations['priorite_moyenne'].append("Essayez d'atteindre 4-5x/semaine")
        
        else:  # > 3 fois/semaine
            msg = f"Fréquence excellente : {frequence:.0f}% des jours"
            recommendations['sport'].append(msg)
            recommendations['priorite_basse'].append("Maintenez cette régularité !")
        
        # Durée
        if moyenne_sport > 0:
            if moyenne_sport < 20:
                msg = f"Séances courtes : {moyenne_sport:.0f}min en moyenne"
                recommendations['sport'].append(msg)
                recommendations['priorite_moyenne'].append("Augmentez progressivement à 30min")
            
            elif 20 <= moyenne_sport <= 45:
                msg = f"Durée optimale : {moyenne_sport:.0f}min/séance"
                recommendations['sport'].append(msg)
            
            elif moyenne_sport > 60:
                msg = f"Séances très longues : {moyenne_sport:.0f}min"
                recommendations['sport'].append(msg)
                recommendations['priorite_moyenne'].append("Assurez une bonne récupération")
    
    # ==============================================================
    # ANALYSE DES DÉPENSES
    # ==============================================================
    if stats.get('jours_depenses', 0) > 0:
        moyenne_depenses = stats.get('moyenne_depenses_jour', 0)
        
        if moyenne_depenses > 0:
            # Catégoriser le niveau de dépenses
            if moyenne_depenses < 15:
                msg = f"Dépenses très basses : {moyenne_depenses:.1f}€/jour"
                recommendations['depenses'].append(msg)
            
            elif 15 <= moyenne_depenses <= 35:
                msg = f"Dépenses raisonnables : {moyenne_depenses:.1f}€/jour"
                recommendations['depenses'].append(msg)
                recommendations['priorite_basse'].append("Continuez ce bon contrôle")
            
            elif 35 < moyenne_depenses <= 60:
                msg = f"Dépenses modérées : {moyenne_depenses:.1f}€/jour"
                recommendations['depenses'].append(msg)
                recommendations['priorite_moyenne'].append("Pourriez-vous économiser 10% ?")
            
            elif moyenne_depenses > 60:
                msg = f"Dépenses élevées : {moyenne_depenses:.1f}€/jour"
                recommendations['depenses'].append(msg)
                recommendations['priorite_haute'].append("Analysez vos principales catégories de dépenses")
    
    # ==============================================================
    # ANALYSE DE LA RÉGULARITÉ (si données disponibles)
    # ==============================================================
    if donnees and len(donnees) >= 7:
        # Analyser la régularité hebdomadaire
        jours_par_semaine = analyser_regularite_semaine(donnees)
        
        for categorie, regularite in jours_par_semaine.items():
            if regularite < 2:  # Moins de 2 jours/semaine
                recommendations['general'].append(
                    f"{categorie} irrégulier : {regularite:.1f} jours/semaine en moyenne"
                )
            elif regularite >= 4:  # Plus de 4 jours/semaine
                recommendations['general'].append(
                    f"{categorie} très régulier : {regularite:.1f} jours/semaine"
                )
    
    # ==============================================================
    # RECOMMANDATIONS PERSONNALISÉES BASÉES SUR LES CORRÉLATIONS
    # ==============================================================
    if donnees and len(donnees) >= 10:
        correlations = analyser_correlations(donnees)
        
        for corr in correlations:
            if abs(corr['force']) > 0.5:  # Corrélation forte
                if corr['force'] > 0:
                    msg = f"{corr['element1']} et {corr['element2']} sont liés positivement"
                else:
                    msg = f"{corr['element1']} et {corr['element2']} sont liés négativement"
                
                recommendations['general'].append(msg)
                
                # Ajouter une recommandation basée sur la corrélation
                if "sommeil" in corr['element1'].lower() and "sport" in corr['element2'].lower():
                    if corr['force'] > 0:
                        recommendations['priorite_moyenne'].append(
                            "Le sport améliore votre sommeil - maintenez cette habitude !"
                        )
    
    # ==============================================================
    # RECOMMANDATIONS CONTEXTUELLES
    # ==============================================================
    from datetime import datetime
    
    # Saison
    mois = datetime.now().month
    if mois in [12, 1, 2]:  # Hiver
        recommendations['general'].append(
            "Conseil hivernal : La lumière du jour est rare, pensez à la vitamine D"
        )
    elif mois in [6, 7, 8]:  # Été
        recommendations['general'].append(
            "Conseil estival : Profitez des longues journées pour des activités extérieures"
        )
    
    # Jour de la semaine
    jour = datetime.now().weekday()
    if jour == 4:  # Vendredi
        recommendations['general'].append(
            "Vendredi : Bon moment pour planifier les activités du week-end"
        )
    elif jour == 0:  # Lundi
        recommendations['general'].append(
            "Lundi : Jour idéal pour fixer vos objectifs de la semaine"
        )
    
    # ==============================================================
    # PRIORISATION ET LIMITATION
    # ==============================================================
    # Limiter le nombre total de recommandations
    max_recommandations = 10
    
    # Compter toutes les recommandations
    toutes_recommandations = []
    for categorie in ['priorite_haute', 'priorite_moyenne', 'priorite_basse', 
                      'sommeil', 'sport', 'depenses', 'general']:
        toutes_recommandations.extend(recommendations[categorie])
    
    if len(toutes_recommandations) > max_recommandations:
        # Garder les plus prioritaires
        recommendations['priorite_haute'] = recommendations['priorite_haute'][:3]
        recommendations['priorite_moyenne'] = recommendations['priorite_moyenne'][:3]
        recommendations['priorite_basse'] = recommendations['priorite_basse'][:2]
        recommendations['general'] = recommendations['general'][:2]
        
        # Reconstruire la liste complète
        final_recommendations = []
        final_recommendations.extend(recommendations['priorite_haute'])
        final_recommendations.extend(recommendations['priorite_moyenne'])
        final_recommendations.extend(recommendations['general'])
        
        if len(final_recommendations) < max_recommandations:
            final_recommendations.extend(recommendations['priorite_basse'])
        
        # Tronquer si nécessaire
        final_recommendations = final_recommendations[:max_recommandations]
        
        # Formater pour retour simple
        return final_recommendations
    
    # Retourner toutes les recommandations si moins de la limite
    return toutes_recommandations

def analyser_regularite_semaine(donnees):
    """
    Analyse la régularité hebdomadaire des habitudes
    """
    from datetime import datetime
    from collections import defaultdict
    
    regularite = {
        'sommeil': 0,
        'sport': 0,
        'depenses': 0
    }
    
    compteurs = defaultdict(lambda: defaultdict(int))
    
    for date_str, valeurs in donnees.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        annee_semaine = f"{date_obj.year}-{date_obj.isocalendar()[1]}"  # Année-semaine
        
        # Compter les occurrences par semaine
        if valeurs.get('sommeil'):
            compteurs[annee_semaine]['sommeil'] += 1
        if valeurs.get('sport') and valeurs['sport'].get('duree', 0) > 0:
            compteurs[annee_semaine]['sport'] += 1
        if valeurs.get('depenses'):
            compteurs[annee_semaine]['depenses'] += 1
    
    # Calculer les moyennes par semaine
    if compteurs:
        for categorie in ['sommeil', 'sport', 'depenses']:
            total = sum(compteurs[semaine][categorie] for semaine in compteurs)
            regularite[categorie] = total / len(compteurs)
    
    return regularite

def analyser_correlations(donnees):
    """
    Analyse les corrélations entre différentes habitudes
    """
    correlations = []
    
    # Préparer les données
    sommeil_durees = []
    sport_durees = []
    depenses_totales = []
    qualites_sommeil = []
    
    for valeurs in donnees.values():
        # Sommeil
        sommeil = valeurs.get('sommeil', {})
        if sommeil and 'duree' in sommeil:
            sommeil_durees.append(sommeil['duree'])
            if 'qualite' in sommeil:
                qualites_sommeil.append(sommeil['qualite'])
        else:
            sommeil_durees.append(None)
            qualites_sommeil.append(None)
        
        # Sport
        sport = valeurs.get('sport', {})
        if sport and 'duree' in sport:
            sport_durees.append(sport['duree'])
        else:
            sport_durees.append(0)
        
        # Dépenses
        depenses = valeurs.get('depenses', [])
        total = sum(d.get('montant', 0) for d in depenses)
        depenses_totales.append(total)
    
    # Calculer les corrélations entre paires valides
    pairs = [
        ('Durée sommeil', 'Durée sport', sommeil_durees, sport_durees),
        ('Durée sommeil', 'Dépenses', sommeil_durees, depenses_totales),
        ('Durée sport', 'Dépenses', sport_durees, depenses_totales),
    ]
    
    # Ajouter qualité si disponible
    if any(q is not None for q in qualites_sommeil):
        pairs.append(('Qualité sommeil', 'Durée sport', qualites_sommeil, sport_durees))
        pairs.append(('Qualité sommeil', 'Dépenses', qualites_sommeil, depenses_totales))
    
    for nom1, nom2, data1, data2 in pairs:
        # Filtrer les paires valides (sans None)
        filtered_pairs = [(d1, d2) for d1, d2 in zip(data1, data2) 
                         if d1 is not None and d2 is not None]
        
        if len(filtered_pairs) >= 5:  # Minimum 5 points pour analyse
            d1_filtered, d2_filtered = zip(*filtered_pairs)
            correlation = calculer_correlation_simple(list(d1_filtered), list(d2_filtered))
            
            if abs(correlation) > 0.3:  # Seuil pour considérer comme intéressant
                correlations.append({
                    'element1': nom1,
                    'element2': nom2,
                    'force': correlation,
                    'echantillon': len(filtered_pairs)
                })
    
    return correlations

def calculer_correlation_simple(liste1, liste2):
    """
    Calcule un coefficient de corrélation simplifié
    """
    if len(liste1) != len(liste2) or len(liste1) < 2:
        return 0
    
    # Calcul des moyennes
    moy1 = sum(liste1) / len(liste1)
    moy2 = sum(liste2) / len(liste2)
    
    # Calcul du numérateur et dénominateurs
    numerateur = sum((x - moy1) * (y - moy2) for x, y in zip(liste1, liste2))
    denom1 = sum((x - moy1) ** 2 for x in liste1)
    denom2 = sum((y - moy2) ** 2 for y in liste2)
    
    if denom1 == 0 or denom2 == 0:
        return 0
    
    return numerateur / ((denom1 * denom2) ** 0.5)

