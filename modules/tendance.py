# Copyright (c) 2025 MARCEL DINLA
# Tous droits réservés.

from datetime import datetime
import os

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
# MENU AFFICHER LES TENDANCES
# ============================================
def menu_tendances(donnees):
    """
    Menu d'analyse des tendances et évolutions
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("═"*70)
        print(Couleurs.GRAS, Couleurs.ROSE)
        print("📈 ANALYSE DES TENDANCES")
        print(Couleurs.RESET)
        print("═"*70)
        
        if donnees:
            dates = sorted(donnees.keys())
            print(f"\n\t{len(donnees)} jour(s) disponible(s)")
            print(f"\t📅 Du {dates[0]} au {dates[-1]}")
        else:
            print("\n📭 Aucune donnée disponible")
        
        print("\n" + "─"*70)
        print(Couleurs.BLEU)
        print("📊 ÉVOLUTIONS TEMPORELLES")
        print("─"*70)
        print("\t1. Tendances sur 7 derniers jours")
        print("\t2. Tendances sur 30 derniers jours")
        print("\t3. Tendances sur période personnalisée")
        print("\t4. Comparaison mois par mois")
        print(Couleurs.RESET)

        print("\n" + "─"*70)
        print("📉 GRAPHIQUES ASCII")
        print("─"*70)
        print("\t5. Graphique évolution sommeil")
        print("\t6. Graphique évolution sport")
        print("\t7. Graphique évolution dépenses")
        print("\t8. Graphique combiné (tout)")
        
        print("\n" + "─"*70)
        print(Couleurs.VERT)
        print("🔍 ANALYSES AVANCÉES")
        print("─"*70)
        print("\t9. Analyse par jour de la semaine")
        print("\t10. Détection de cycles et habitudes")
        print("\t11. Objectifs vs Réalisations")
        print("\t12. Prédictions basées sur tendances")
        print(Couleurs.RESET)
        
        print("\n" + "─"*70)
        print("\t13. ↩️  Retour au menu principal")
        print("═"*70)
        
        choix = input("\nVotre choix : ").strip()
        
        try:
            if choix == "1":
                # 7 derniers jours
                analyser_periode(donnees, 7)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "2":
                # 30 derniers jours
                analyser_periode(donnees, 30)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "3":
                # Période personnalisée
                print("\n📅 PÉRIODE PERSONNALISÉE")
                try:
                    nb_jours = int(input("Nombre de jours à analyser : ").strip())
                    if nb_jours > 0:
                        analyser_periode(donnees, nb_jours)
                    else:
                        print("❌ Nombre de jours invalide")
                except ValueError:
                    print("❌ Entrée invalide")
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                # Comparaison mois par mois
                comparer_mois(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "5":
                # Graphique sommeil
                graphique_evolution_sommeil(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                # Graphique sport
                graphique_evolution_sport(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "7":
                # Graphique dépenses
                graphique_evolution_depenses(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "8":
                # Graphique combiné
                graphique_combine(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "9":
                # Analyse par jour de semaine
                analyser_jours_semaine(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "10":
                # Détection cycles
                detecter_cycles(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "11":
                # Objectifs vs réalisations
                analyser_objectifs(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "12":
                # Prédictions
                generer_predictions(donnees)
                input("\n\nAppuyez sur Entrée pour continuer...")
            
            elif choix == "13":
                # Retour
                break
            
            elif choix in ['e', 'exit', 'quitter', 'q']:
                # Retour
                break

            else:
                print("\n❌ Choix invalide")
                input("\nAppuyez sur Entrée pour continuer...")
            
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            import traceback
            traceback.print_exc()
            input("\nAppuyez sur Entrée pour continuer...")


# ============================================
# FONCTION 1 : ANALYSER PÉRIODE (1, 2, 3)
# ============================================
def analyser_periode(donnees, nb_jours):
    """
    Analyse des tendances sur une période donnée
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print(f"📈 TENDANCES SUR LES {nb_jours} DERNIERS JOURS")
    print("═"*70)
    
    # Obtenir les dates triées
    dates = sorted(donnees.keys(), reverse=True)[:nb_jours]
    dates.reverse()  # Remettre en ordre chronologique
    
    if len(dates) < nb_jours:
        print(f"\n\t⚠️  Seulement {len(dates)} jour(s) disponible(s)")
    
    print(f"\n\t        Période : {dates[0]} au {dates[-1]}")
    print(f"\t        {len(dates)} jour(s) analysé(s)")
    
    # === SOMMEIL ===
    print("\n" + "─"*70)
    print("😴 TENDANCES SOMMEIL")
    print("─"*70)
    
    durees_sommeil = []
    qualites_sommeil = []
    
    for date in dates:
        sommeil = donnees[date].get('sommeil', {})
        if 'duree' in sommeil:
            durees_sommeil.append(sommeil['duree'])
        if 'qualite' in sommeil:
            qualites_sommeil.append(sommeil['qualite'])
    
    if durees_sommeil:
        moyenne = sum(durees_sommeil) / len(durees_sommeil)
        print(f"\n\t⏰ Durée moyenne : {moyenne:.2f}h")
        
        # Tendance
        if len(durees_sommeil) >= 2:
            premiere_moitie = durees_sommeil[:len(durees_sommeil)//2]
            seconde_moitie = durees_sommeil[len(durees_sommeil)//2:]
            
            moy_debut = sum(premiere_moitie) / len(premiere_moitie)
            moy_fin = sum(seconde_moitie) / len(seconde_moitie)
            
            diff = moy_fin - moy_debut
            
            if diff > 0.5:
                print(f"\t   📈 TENDANCE À LA HAUSSE (+{diff:.2f}h)")
                print(f"\t      Vous dormez de plus en plus !")
            elif diff < -0.5:
                print(f"\t   📉 TENDANCE À LA BAISSE ({diff:.2f}h)")
                print(f"\t      Attention à la fatigue")
            else:
                print(f"\t   ➡️  TENDANCE STABLE")
    
    if qualites_sommeil:
        moyenne_qual = sum(qualites_sommeil) / len(qualites_sommeil)
        print(f"\n\t⭐ Qualité moyenne : {moyenne_qual:.2f}/10")
        
        # Tendance qualité
        if len(qualites_sommeil) >= 2:
            premiere_moitie = qualites_sommeil[:len(qualites_sommeil)//2]
            seconde_moitie = qualites_sommeil[len(qualites_sommeil)//2:]
            
            moy_debut = sum(premiere_moitie) / len(premiere_moitie)
            moy_fin = sum(seconde_moitie) / len(seconde_moitie)
            
            diff = moy_fin - moy_debut
            
            if diff > 1:
                print(f"\t   📈 AMÉLIORATION (+{diff:.1f} points)")
            elif diff < -1:
                print(f"\t   📉 DÉGRADATION ({diff:.1f} points)")
            else:
                print(f"\t   ➡️  STABLE")
    
    # === SPORT ===
    print("\n" + "─"*70)
    print("🏃 TENDANCES SPORT")
    print("─"*70)
    
    durees_sport = []
    jours_avec_sport = 0
    
    for date in dates:
        sport = donnees[date].get('sport', {})
        duree = sport.get('duree', 0)
        if duree > 0:
            durees_sport.append(duree)
            jours_avec_sport += 1
    
    frequence = (jours_avec_sport / len(dates)) * 100
    
    print(f"\n\t📊 Fréquence : {jours_avec_sport}/{len(dates)} jours ({frequence:.1f}%)")
    
    if durees_sport:
        total = sum(durees_sport)
        moyenne = total / len(durees_sport)
        
        print(f"\t   Durée totale : {total} minutes ({total/60:.2f}h)")
        print(f"\t   Durée moyenne par séance : {moyenne:.1f} minutes")
        
        # Tendance fréquence
        if len(dates) >= 2:
            premiere_moitie = dates[:len(dates)//2]
            seconde_moitie = dates[len(dates)//2:]
            
            sport_debut = sum(1 for d in premiere_moitie if donnees[d].get('sport', {}).get('duree', 0) > 0)
            sport_fin = sum(1 for d in seconde_moitie if donnees[d].get('sport', {}).get('duree', 0) > 0)
            
            freq_debut = (sport_debut / len(premiere_moitie)) * 100
            freq_fin = (sport_fin / len(seconde_moitie)) * 100
            
            diff = freq_fin - freq_debut
            
            if diff > 10:
                print(f"\n\t📈 FRÉQUENCE EN HAUSSE (+{diff:.1f}%)")
                print(f"\t   Vous êtes de plus en plus actif !")
            elif diff < -10:
                print(f"\n\t📉 FRÉQUENCE EN BAISSE ({diff:.1f}%)")
                print(f"\t   Essayez de maintenir la régularité")
            else:
                print(f"\n\t➡️  FRÉQUENCE STABLE")
    
    # === DÉPENSES ===
    print("\n" + "─"*70)
    print("💰 TENDANCES DÉPENSES")
    print("─"*70)
    
    montants_journaliers = []
    categories = {}
    
    for date in dates:
        depenses = donnees[date].get('depenses', [])
        montant_jour = sum(d['montant'] for d in depenses)
        montants_journaliers.append(montant_jour)
        
        for dep in depenses:
            cat = dep.get('categorie', 'Autre')
            categories[cat] = categories.get(cat, 0) + dep['montant']
    
    total = sum(montants_journaliers)
    moyenne = total / len(dates)
    
    print(f"\n\t💵 Total dépensé : {total:.2f}$")
    print(f"\t    Moyenne par jour : {moyenne:.2f}$")
    
    # Top 3 catégories
    if categories:
        print(f"\n\t🏷️  TOP 3 CATÉGORIES :")
        top_cat = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        for i, (cat, montant) in enumerate(top_cat, 1):
            pct = (montant / total) * 100
            print(f"\t   {i}. {cat}: {montant:.2f}$ ({pct:.1f}%)")
    
    # Tendance dépenses
    if len(montants_journaliers) >= 2:
        premiere_moitie = montants_journaliers[:len(montants_journaliers)//2]
        seconde_moitie = montants_journaliers[len(montants_journaliers)//2:]
        
        moy_debut = sum(premiere_moitie) / len(premiere_moitie)
        moy_fin = sum(seconde_moitie) / len(seconde_moitie)
        
        diff = moy_fin - moy_debut
        pct_diff = (diff / moy_debut * 100) if moy_debut > 0 else 0
        
        print(f"\n\t📈 TENDANCE :")
        if diff > 5:
            print(f"\t   AUGMENTATION (+{diff:.2f}$/jour, +{pct_diff:.1f}%)")
            print(f"\t   Attention à la hausse des dépenses")
        elif diff < -5:
            print(f"\t   DIMINUTION ({diff:.2f}$/jour, {pct_diff:.1f}%)")
            print(f"\t   Bonne maîtrise du budget !")
        else:
            print(f"\t      STABLE")
    
    # === SCORE GLOBAL ===
    print("\n" + "═"*70)
    print("🌟 ÉVALUATION GLOBALE DE LA PÉRIODE")
    print("═"*70)
    
    points = 0
    max_points = 0
    
    # Sommeil
    if durees_sommeil:
        max_points += 3
        if moyenne >= 7 and moyenne <= 9:
            points += 3
        elif moyenne >= 6:
            points += 2
        else:
            points += 1
    
    # Sport
    if jours_avec_sport > 0:
        max_points += 3
        if frequence >= 50:
            points += 3
        elif frequence >= 30:
            points += 2
        else:
            points += 1
    
    # Dépenses
    if montants_journaliers:
        max_points += 3
        if moyenne <= 30:
            points += 3
        elif moyenne <= 50:
            points += 2
        else:
            points += 1
    
    if max_points > 0:
        score_pct = (points / max_points) * 100
        print(f"\n\t🎯 Score : {points}/{max_points} ({score_pct:.0f}%)")
        
        if score_pct >= 80:
            print("\t   ⭐⭐⭐ EXCELLENTE PÉRIODE !")
        elif score_pct >= 60:
            print("\t   ⭐⭐ BONNE PÉRIODE")
        else:
            print("\t   ⭐ PÉRIODE À AMÉLIORER")
    
    print("\n" + "═"*70)


# ============================================
# FONCTION 2 : GRAPHIQUE ÉVOLUTION SOMMEIL (5)
# ============================================
def graphique_evolution_sommeil(donnees):
    """
    Graphique ASCII de l'évolution du sommeil
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print("😴 GRAPHIQUE ÉVOLUTION SOMMEIL (30 DERNIERS JOURS)")
    print("═"*70)
    
    # Récupérer les 30 derniers jours
    dates = sorted(donnees.keys(), reverse=True)[:30]
    dates.reverse()
    
    durees = []
    dates_avec_donnees = []
    
    for date in dates:
        sommeil = donnees[date].get('sommeil', {})
        if 'duree' in sommeil:
            durees.append(sommeil['duree'])
            dates_avec_donnees.append(date)
    
    if not durees:
        print("\n\t📭 Aucune donnée de sommeil")
        return
    
    # Statistiques
    moyenne = sum(durees) / len(durees)
    mini = min(durees)
    maxi = max(durees)
    
    print(f"\n\t📊 Statistiques :")
    print(f"\t   • Moyenne : {moyenne:.2f}h")
    print(f"\t   • Minimum : {mini:.2f}h")
    print(f"\t   • Maximum : {maxi:.2f}h")
    
    # Graphique
    print(f"\n\t📈 Graphique (chaque █ = 0.5h) :\n")
    
    hauteur_max = 12  # 12h max sur le graphique
    
    for i, (date, duree) in enumerate(zip(dates_avec_donnees, durees)):
        barres = int(duree * 2)  # 2 barres par heure
        graphe = "█" * barres
        
        # Couleur selon durée
        if duree < 6:
            symbole = "🔴"
        elif duree >= 7 and duree <= 9:
            symbole = "🟢"
        else:
            symbole = "🟡"
        
        # Afficher seulement les 15 derniers pour lisibilité
        if i >= len(dates_avec_donnees) - 15:
            date_court = date[-5:]  # MM-JJ
            print(f"\n\t{date_court} {symbole} {graphe} {duree:.1f}h")
    
    print(f"\n\t🟢 Optimal (7-9h)  🟡 Acceptable  🔴 Insuffisant (<6h)")
    print("═"*70)


# ============================================
# FONCTION 3 : ANALYSER JOURS DE LA SEMAINE (9)
# ============================================
def analyser_jours_semaine(donnees):
    """
    Analyse des habitudes par jour de la semaine
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print("📅 ANALYSE PAR JOUR DE LA SEMAINE")
    print("═"*70)
    
    jours_noms = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    # Initialiser les données par jour
    stats_jours = {i: {
        'sommeil': [],
        'sport': [],
        'depenses': [],
        'count': 0
    } for i in range(7)}
    
    # Collecter les données
    for date_str, valeurs in donnees.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        jour_semaine = date_obj.weekday()
        
        stats_jours[jour_semaine]['count'] += 1
        
        # Sommeil
        sommeil = valeurs.get('sommeil', {})
        if 'duree' in sommeil:
            stats_jours[jour_semaine]['sommeil'].append(sommeil['duree'])
        
        # Sport
        sport = valeurs.get('sport', {})
        if sport.get('duree', 0) > 0:
            stats_jours[jour_semaine]['sport'].append(sport['duree'])
        
        # Dépenses
        depenses = valeurs.get('depenses', [])
        if depenses:
            total = sum(d['montant'] for d in depenses)
            stats_jours[jour_semaine]['depenses'].append(total)
    
    # Afficher les résultats
    print("\n😴 SOMMEIL MOYEN PAR JOUR :")
    for i, nom in enumerate(jours_noms):
        if stats_jours[i]['sommeil']:
            moy = sum(stats_jours[i]['sommeil']) / len(stats_jours[i]['sommeil'])
            barres = "█" * int(moy)
            print(f"   {nom:10} : {barres} {moy:.2f}h")
        else:
            print(f"   {nom:10} : Pas de données")
    
    print("\n🏃 ACTIVITÉ SPORTIVE PAR JOUR :")
    for i, nom in enumerate(jours_noms):
        total_sport = len(stats_jours[i]['sport'])
        total_jours = stats_jours[i]['count']
        
        if total_jours > 0:
            freq = (total_sport / total_jours) * 100
            barres = "█" * int(freq / 10)
            print(f"   {nom:10} : {barres} {freq:.0f}% ({total_sport}/{total_jours} jours)")
        else:
            print(f"   {nom:10} : Pas de données")
    
    print("\n💰 DÉPENSES MOYENNES PAR JOUR :")
    for i, nom in enumerate(jours_noms):
        if stats_jours[i]['depenses']:
            moy = sum(stats_jours[i]['depenses']) / len(stats_jours[i]['depenses'])
            barres = "█" * int(moy / 5)
            print(f"   {nom:10} : {barres} {moy:.2f}$")
        else:
            print(f"   {nom:10} : Pas de données")
    
    # Insights
    print("\n" + "─"*70)
    print("💡 INSIGHTS :")
    
    # Meilleur jour sommeil
    meilleur_sommeil = max(range(7), key=lambda i: sum(stats_jours[i]['sommeil']) / len(stats_jours[i]['sommeil']) if stats_jours[i]['sommeil'] else 0)
    print(f"   😴 Meilleur sommeil : {jours_noms[meilleur_sommeil]}")
    
    # Jour le plus actif
    jour_plus_actif = max(range(7), key=lambda i: len(stats_jours[i]['sport']) / stats_jours[i]['count'] if stats_jours[i]['count'] > 0 else 0)
    print(f"   🏃 Jour le plus actif : {jours_noms[jour_plus_actif]}")
    
    # Jour le plus dépensier
    jour_depensier = max(range(7), key=lambda i: sum(stats_jours[i]['depenses']) / len(stats_jours[i]['depenses']) if stats_jours[i]['depenses'] else 0)
    print(f"   💰 Jour le plus dépensier : {jours_noms[jour_depensier]}")
    
    print("═"*70)


# ============================================
# FONCTION 4 : COMPARER MOIS PAR MOIS (4)
# ============================================
def comparer_mois(donnees):
    """
    Comparaison des statistiques mois par mois
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*80)
    print("📅 COMPARAISON MOIS PAR MOIS")
    print("═"*80)
    
    # Organiser les données par mois
    mois_data = {}
    
    for date_str, valeurs in donnees.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        mois_key = date_obj.strftime("%Y-%m")  # Format: 2024-12
        
        if mois_key not in mois_data:
            mois_data[mois_key] = {
                'dates': [],
                'sommeil_durees': [],
                'sommeil_qualites': [],
                'sport_durees': [],
                'sport_count': 0,
                'depenses_montants': [],
                'depenses_total': 0
            }
        
        mois_data[mois_key]['dates'].append(date_str)
        
        # Sommeil
        sommeil = valeurs.get('sommeil', {})
        if 'duree' in sommeil:
            mois_data[mois_key]['sommeil_durees'].append(sommeil['duree'])
        if 'qualite' in sommeil:
            mois_data[mois_key]['sommeil_qualites'].append(sommeil['qualite'])
        
        # Sport
        sport = valeurs.get('sport', {})
        if sport.get('duree', 0) > 0:
            mois_data[mois_key]['sport_durees'].append(sport['duree'])
            mois_data[mois_key]['sport_count'] += 1
        
        # Dépenses
        depenses = valeurs.get('depenses', [])
        if depenses:
            total_jour = sum(d['montant'] for d in depenses)
            mois_data[mois_key]['depenses_montants'].append(total_jour)
            mois_data[mois_key]['depenses_total'] += total_jour
    
    # Trier par mois
    mois_tries = sorted(mois_data.keys())
    
    if len(mois_tries) < 2:
        print("\n⚠️  Au moins 2 mois de données nécessaires pour la comparaison")
        return
    
    print(f"\n📊 {len(mois_tries)} mois analysé(s)\n")
    
    # Noms des mois en français
    noms_mois = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    
    # === TABLEAU COMPARATIF ===
    print("─"*80)
    print(f"{'MOIS':<15} {'JOURS':<8} {'SOMMEIL':<12} {'SPORT':<15} {'DÉPENSES':<15}")
    print("─"*80)
    
    for mois_key in mois_tries:
        data = mois_data[mois_key]
        annee, mois_num = mois_key.split('-')
        mois_nom = f"{noms_mois[int(mois_num)]} {annee}"
        
        nb_jours = len(data['dates'])
        
        # Sommeil
        if data['sommeil_durees']:
            moy_sommeil = sum(data['sommeil_durees']) / len(data['sommeil_durees'])
            sommeil_str = f"{moy_sommeil:.1f}h"
        else:
            sommeil_str = "N/A"
        
        # Sport
        if data['sport_count'] > 0:
            freq_sport = (data['sport_count'] / nb_jours) * 100
            sport_str = f"{freq_sport:.0f}%"
        else:
            sport_str = "0%"
        
        # Dépenses
        if data['depenses_montants']:
            moy_depenses = data['depenses_total'] / nb_jours
            depenses_str = f"{moy_depenses:.2f}$/j"
        else:
            depenses_str = "N/A"
        
        print(f"{mois_nom:<15} {nb_jours:<8} {sommeil_str:<12} {sport_str:<15} {depenses_str:<15}")
    
    print("─"*80)
    
    # === ÉVOLUTION DÉTAILLÉE ===
    print("\n" + "═"*80)
    print("📈 ÉVOLUTION DÉTAILLÉE")
    print("═"*80)
    
    # Sommeil
    print("\n😴 SOMMEIL :")
    for i, mois_key in enumerate(mois_tries):
        data = mois_data[mois_key]
        annee, mois_num = mois_key.split('-')
        mois_nom = f"{noms_mois[int(mois_num)]} {annee}"
        
        if data['sommeil_durees']:
            moy = sum(data['sommeil_durees']) / len(data['sommeil_durees'])
            barres = "█" * int(moy)
            
            # Calculer évolution
            if i > 0:
                mois_prec = mois_tries[i-1]
                data_prec = mois_data[mois_prec]
                if data_prec['sommeil_durees']:
                    moy_prec = sum(data_prec['sommeil_durees']) / len(data_prec['sommeil_durees'])
                    diff = moy - moy_prec
                    
                    if diff > 0.3:
                        trend = f"📈 +{diff:.1f}h"
                    elif diff < -0.3:
                        trend = f"📉 {diff:.1f}h"
                    else:
                        trend = "➡️  stable"
                else:
                    trend = ""
            else:
                trend = ""
            
            print(f"   {mois_nom:<15} {barres} {moy:.1f}h {trend}")
    
    # Sport
    print("\n🏃 ACTIVITÉ SPORTIVE :")
    for i, mois_key in enumerate(mois_tries):
        data = mois_data[mois_key]
        annee, mois_num = mois_key.split('-')
        mois_nom = f"{noms_mois[int(mois_num)]} {annee}"
        
        nb_jours = len(data['dates'])
        freq = (data['sport_count'] / nb_jours) * 100
        barres = "█" * int(freq / 10)
        
        # Calculer évolution
        if i > 0:
            mois_prec = mois_tries[i-1]
            data_prec = mois_data[mois_prec]
            nb_jours_prec = len(data_prec['dates'])
            freq_prec = (data_prec['sport_count'] / nb_jours_prec) * 100
            diff = freq - freq_prec
            
            if diff > 10:
                trend = f"📈 +{diff:.0f}%"
            elif diff < -10:
                trend = f"📉 {diff:.0f}%"
            else:
                trend = "➡️  stable"
        else:
            trend = ""
        
        print(f"   {mois_nom:<15} {barres} {freq:.0f}% ({data['sport_count']}/{nb_jours}j) {trend}")
    
    # Dépenses
    print("\n💰 DÉPENSES :")
    for i, mois_key in enumerate(mois_tries):
        data = mois_data[mois_key]
        annee, mois_num = mois_key.split('-')
        mois_nom = f"{noms_mois[int(mois_num)]} {annee}"
        
        nb_jours = len(data['dates'])
        
        if data['depenses_montants']:
            moy = data['depenses_total'] / nb_jours
            total = data['depenses_total']
            barres = "█" * int(moy / 5)
            
            # Calculer évolution
            if i > 0:
                mois_prec = mois_tries[i-1]
                data_prec = mois_data[mois_prec]
                if data_prec['depenses_montants']:
                    nb_jours_prec = len(data_prec['dates'])
                    moy_prec = data_prec['depenses_total'] / nb_jours_prec
                    diff = moy - moy_prec
                    
                    if diff > 5:
                        trend = f"📈 +{diff:.2f}$"
                    elif diff < -5:
                        trend = f"📉 {diff:.2f}$"
                    else:
                        trend = "➡️  stable"
                else:
                    trend = ""
            else:
                trend = ""
            
            print(f"   {mois_nom:<15} {barres} {moy:.2f}$/j (Total: {total:.2f}$) {trend}")
    
    # === MEILLEUR ET PIRE MOIS ===
    print("\n" + "═"*80)
    print("🏆 RECORDS")
    print("═"*80)
    
    # Meilleur sommeil
    meilleur_sommeil = max(mois_tries, key=lambda m: sum(mois_data[m]['sommeil_durees']) / len(mois_data[m]['sommeil_durees']) if mois_data[m]['sommeil_durees'] else 0)
    annee, mois_num = meilleur_sommeil.split('-')
    print(f"\n😴 Meilleur sommeil : {noms_mois[int(mois_num)]} {annee}")
    
    # Mois le plus actif
    mois_actif = max(mois_tries, key=lambda m: mois_data[m]['sport_count'] / len(mois_data[m]['dates']))
    annee, mois_num = mois_actif.split('-')
    print(f"🏃 Mois le plus actif : {noms_mois[int(mois_num)]} {annee}")
    
    # Mois le plus économe
    mois_econome = min(mois_tries, key=lambda m: mois_data[m]['depenses_total'] / len(mois_data[m]['dates']) if mois_data[m]['depenses_montants'] else float('inf'))
    annee, mois_num = mois_econome.split('-')
    print(f"💰 Mois le plus économe : {noms_mois[int(mois_num)]} {annee}")
    
    print("\n" + "═"*80)

# ============================================
# FONCTION 5 : GRAPHIQUE ÉVOLUTION SPORT (6)
# ============================================
def graphique_evolution_sport(donnees):
    """
    Graphique ASCII de l'évolution du sport
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print("🏃 GRAPHIQUE ÉVOLUTION SPORT (30 DERNIERS JOURS)")
    print("═"*70)
    
    # Récupérer les 30 derniers jours
    dates = sorted(donnees.keys(), reverse=True)[:30]
    dates.reverse()
    
    durees = []
    dates_avec_sport = []
    types_sport = {}
    
    for date in dates:
        sport = donnees[date].get('sport', {})
        duree = sport.get('duree', 0)
        
        if duree > 0:
            durees.append(duree)
            dates_avec_sport.append(date)
            
            type_sport = sport.get('type', 'Non spécifié')
            types_sport[type_sport] = types_sport.get(type_sport, 0) + 1
    
    if not durees:
        print("\n📭 Aucune donnée de sport")
        return
    
    # Statistiques
    total = sum(durees)
    moyenne = total / len(durees)
    mini = min(durees)
    maxi = max(durees)
    frequence = (len(durees) / len(dates)) * 100
    
    print(f"\n📊 Statistiques :")
    print(f"   • Fréquence : {len(durees)}/{len(dates)} jours ({frequence:.1f}%)")
    print(f"   • Total : {total} minutes ({total/60:.2f}h)")
    print(f"   • Moyenne : {moyenne:.1f} minutes")
    print(f"   • Minimum : {mini} minutes")
    print(f"   • Maximum : {maxi} minutes")
    
    # Graphique
    print(f"\n📈 Graphique (chaque █ = 10 minutes) :\n")
    
    for date, duree in zip(dates_avec_sport, durees):
        barres = int(duree / 10)
        graphe = "█" * barres
        
        # Symbole selon durée
        if duree < 30:
            symbole = "🟡"  # Court
        elif duree < 60:
            symbole = "🟢"  # Modéré
        else:
            symbole = "🔵"  # Long
        
        date_court = date[-5:]  # MM-JJ
        print(f"{date_court} {symbole} {graphe} {duree}min")
    
    # Types d'activités
    if types_sport:
        print(f"\n🏋️  Types d'activités :")
        types_tries = sorted(types_sport.items(), key=lambda x: x[1], reverse=True)
        for type_act, count in types_tries[:5]:
            pct = (count / len(durees)) * 100
            print(f"   • {type_act}: {count} fois ({pct:.0f}%)")
    
    print(f"\n🔵 Long (≥60min)  🟢 Modéré (30-60min)  🟡 Court (<30min)")
    print("═"*70)


# ============================================
# FONCTION 6 : GRAPHIQUE ÉVOLUTION DÉPENSES (7)
# ============================================
def graphique_evolution_depenses(donnees):
    """
    Graphique ASCII de l'évolution des dépenses
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print("💰 GRAPHIQUE ÉVOLUTION DÉPENSES (30 DERNIERS JOURS)")
    print("═"*70)
    
    # Récupérer les 30 derniers jours
    dates = sorted(donnees.keys(), reverse=True)[:30]
    dates.reverse()
    
    montants_journaliers = []
    dates_avec_depenses = []
    categories = {}
    
    for date in dates:
        depenses = donnees[date].get('depenses', [])
        
        if depenses:
            total_jour = sum(d['montant'] for d in depenses)
            montants_journaliers.append(total_jour)
            dates_avec_depenses.append(date)
            
            # Collecter catégories
            for dep in depenses:
                cat = dep.get('categorie', 'Autre')
                categories[cat] = categories.get(cat, 0) + dep['montant']
    
    if not montants_journaliers:
        print("\n📭 Aucune donnée de dépenses")
        return
    
    # Statistiques
    total = sum(montants_journaliers)
    moyenne = total / len(montants_journaliers)
    moyenne_sur_periode = total / len(dates)
    mini = min(montants_journaliers)
    maxi = max(montants_journaliers)
    
    print(f"\n📊 Statistiques :")
    print(f"   • Jours avec dépenses : {len(montants_journaliers)}/{len(dates)} jours")
    print(f"   • Total : {total:.2f}$")
    print(f"   • Moyenne (jours avec dépenses) : {moyenne:.2f}$")
    print(f"   • Moyenne (tous les jours) : {moyenne_sur_periode:.2f}$")
    print(f"   • Minimum : {mini:.2f}$")
    print(f"   • Maximum : {maxi:.2f}$")
    
    # Graphique
    print(f"\n📈 Graphique (chaque █ = 5$) :\n")
    
    for date, montant in zip(dates_avec_depenses, montants_journaliers):
        barres = int(montant / 5)
        graphe = "█" * min(barres, 50)  # Limiter à 50 caractères
        
        # Symbole selon montant
        if montant < 20:
            symbole = "🟢"  # Faible
        elif montant < 50:
            symbole = "🟡"  # Moyen
        elif montant < 100:
            symbole = "🟠"  # Élevé
        else:
            symbole = "🔴"  # Très élevé
        
        date_court = date[-5:]  # MM-JJ
        print(f"{date_court} {symbole} {graphe} {montant:.2f}$")
    
    # Top catégories
    if categories:
        print(f"\n🏷️  Top 5 catégories :")
        cat_triees = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for i, (cat, montant) in enumerate(cat_triees[:5], 1):
            pct = (montant / total) * 100
            print(f"   {i}. {cat}: {montant:.2f}$ ({pct:.1f}%)")
    
    # Projection
    projection_mensuelle = moyenne_sur_periode * 30
    projection_annuelle = moyenne_sur_periode * 365
    
    print(f"\n📈 Projections :")
    print(f"   • Mensuelle : {projection_mensuelle:.2f}$")
    print(f"   • Annuelle : {projection_annuelle:.2f}$")
    
    print(f"\n🔴 Très élevé (≥100$)  🟠 Élevé (50-100$)  🟡 Moyen (20-50$)  🟢 Faible (<20$)")
    print("═"*70)


# ============================================
# FONCTION 7 : GRAPHIQUE COMBINÉ (8)
# ============================================
def graphique_combine(donnees):
    """
    Graphique combiné : sommeil, sport et dépenses sur le même graphique
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*80)
    print("📊 GRAPHIQUE COMBINÉ - VUE D'ENSEMBLE (30 DERNIERS JOURS)")
    print("═"*80)
    
    # Récupérer les 30 derniers jours
    dates = sorted(donnees.keys(), reverse=True)[:30]
    dates.reverse()
    
    print(f"\n📅 Période : {dates[0]} au {dates[-1]}")
    print(f"📊 {len(dates)} jour(s) analysé(s)\n")
    
    # Collecter toutes les données
    donnees_par_jour = []
    
    for date in dates:
        valeurs = donnees[date]
        
        # Sommeil (normalisé sur 10)
        sommeil = valeurs.get('sommeil', {})
        sommeil_score = (sommeil.get('duree', 0) / 10) * 10  # Normaliser sur 10
        
        # Sport (normalisé sur 10)
        sport = valeurs.get('sport', {})
        sport_duree = sport.get('duree', 0)
        sport_score = min((sport_duree / 60) * 10, 10)  # 60min = 10 points
        
        # Dépenses (normalisé inversé sur 10)
        depenses = valeurs.get('depenses', [])
        total_depenses = sum(d['montant'] for d in depenses)
        depenses_score = max(10 - (total_depenses / 10), 0)  # Moins de dépenses = meilleur score
        
        donnees_par_jour.append({
            'date': date,
            'sommeil': sommeil_score,
            'sport': sport_score,
            'depenses': depenses_score
        })
    
    # Afficher graphique combiné
    print("─"*80)
    print(f"{'DATE':<10} {'SOMMEIL':<20} {'SPORT':<20} {'DÉPENSES':<20}")
    print("─"*80)
    
    for data in donnees_par_jour[-15:]:  # Afficher les 15 derniers jours
        date_court = data['date'][-5:]
        
        # Barres pour chaque métrique
        barre_sommeil = "█" * int(data['sommeil'])
        barre_sport = "█" * int(data['sport'])
        barre_depenses = "█" * int(data['depenses'])
        
        print(f"{date_court:<10} {barre_sommeil:<20} {barre_sport:<20} {barre_depenses:<20}")
    
    print("─"*80)
    
    # Scores moyens
    moy_sommeil = sum(d['sommeil'] for d in donnees_par_jour) / len(donnees_par_jour)
    moy_sport = sum(d['sport'] for d in donnees_par_jour) / len(donnees_par_jour)
    moy_depenses = sum(d['depenses'] for d in donnees_par_jour) / len(donnees_par_jour)
    
    print(f"\n📊 SCORES MOYENS (sur 10) :")
    print(f"   😴 Sommeil : {moy_sommeil:.1f}/10")
    print(f"   🏃 Sport : {moy_sport:.1f}/10")
    print(f"   💰 Contrôle dépenses : {moy_depenses:.1f}/10")
    
    # Score global
    score_global = (moy_sommeil + moy_sport + moy_depenses) / 3
    print(f"\n🌟 SCORE GLOBAL : {score_global:.1f}/10")
    
    if score_global >= 7:
        print("   ⭐⭐⭐ EXCELLENT équilibre de vie !")
    elif score_global >= 5:
        print("   ⭐⭐ BON équilibre, des améliorations possibles")
    else:
        print("   ⭐ Des efforts nécessaires pour améliorer l'équilibre")
    
    print("\n💡 Note : Chaque barre █ = 1 point (max 10)")
    print("═"*80)


# ============================================
# FONCTION 8 : DÉTECTION DE CYCLES (10)
# ============================================
def detecter_cycles(donnees):
    """
    Détection de cycles et habitudes récurrentes
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print("🔄 DÉTECTION DE CYCLES ET HABITUDES")
    print("═"*70)
    
    if len(donnees) < 14:
        print("\n⚠️  Au moins 14 jours de données nécessaires pour l'analyse")
        return
    
    dates = sorted(donnees.keys())
    print(f"\n📊 Analyse de {len(dates)} jour(s)")
    
    # === CYCLES HEBDOMADAIRES ===
    print("\n" + "─"*70)
    print("📅 CYCLES HEBDOMADAIRES")
    print("─"*70)
    
    jours_noms = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    # Analyser sommeil par jour de semaine
    sommeil_par_jour = {i: [] for i in range(7)}
    sport_par_jour = {i: [] for i in range(7)}
    depenses_par_jour = {i: [] for i in range(7)}
    
    for date_str in dates:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        jour_semaine = date_obj.weekday()
        valeurs = donnees[date_str]
        
        # Sommeil
        sommeil = valeurs.get('sommeil', {})
        if 'duree' in sommeil:
            sommeil_par_jour[jour_semaine].append(sommeil['duree'])
        
        # Sport
        sport = valeurs.get('sport', {})
        if sport.get('duree', 0) > 0:
            sport_par_jour[jour_semaine].append(1)
        else:
            sport_par_jour[jour_semaine].append(0)
        
        # Dépenses
        depenses = valeurs.get('depenses', [])
        total = sum(d['montant'] for d in depenses)
        depenses_par_jour[jour_semaine].append(total)
    
    # Identifier les jours avec comportements récurrents
    print("\n😴 SOMMEIL : Jours avec durée constante")
    for i, nom in enumerate(jours_noms):
        if len(sommeil_par_jour[i]) >= 3:
            moy = sum(sommeil_par_jour[i]) / len(sommeil_par_jour[i])
            variance = sum((x - moy) ** 2 for x in sommeil_par_jour[i]) / len(sommeil_par_jour[i])
            
            if variance < 0.5:  # Faible variance = comportement régulier
                print(f"   ✅ {nom}: sommeil régulier (~{moy:.1f}h)")
    
    print("\n🏃 SPORT : Jours d'activité régulière")
    for i, nom in enumerate(jours_noms):
        if len(sport_par_jour[i]) >= 3:
            freq = sum(sport_par_jour[i]) / len(sport_par_jour[i])
            
            if freq >= 0.7:  # 70% du temps
                print(f"   ✅ {nom}: jour de sport habituel ({freq*100:.0f}%)")
    
    print("\n💰 DÉPENSES : Jours de dépenses élevées")
    for i, nom in enumerate(jours_noms):
        if len(depenses_par_jour[i]) >= 3:
            moy = sum(depenses_par_jour[i]) / len(depenses_par_jour[i])
            
            if moy > 40:
                print(f"   ⚠️  {nom}: jour de dépenses élevées (~{moy:.2f}$)")
    
    # === SÉRIES ET STREAKS ===
    print("\n" + "─"*70)
    print("🔥 SÉRIES (STREAKS)")
    print("─"*70)
    
    # Série de sport
    serie_sport_actuelle = 0
    serie_sport_max = 0
    serie_temp = 0
    
    for date_str in dates:
        sport = donnees[date_str].get('sport', {})
        if sport.get('duree', 0) > 0:
            serie_temp += 1
            serie_sport_max = max(serie_sport_max, serie_temp)
        else:
            serie_temp = 0
    
    # Série actuelle
    for date_str in reversed(dates):
        sport = donnees[date_str].get('sport', {})
        if sport.get('duree', 0) > 0:
            serie_sport_actuelle += 1
        else:
            break
    
    print(f"\n🏃 SPORT :")
    print(f"   • Série actuelle : {serie_sport_actuelle} jour(s)")
    print(f"   • Record : {serie_sport_max} jour(s) consécutifs")
    
    if serie_sport_actuelle >= 7:
        print(f"   🔥 Excellente régularité ! Continuez !")
    elif serie_sport_actuelle >= 3:
        print(f"   ✅ Bonne série en cours")
    
    # Série de bon sommeil (7-9h)
    serie_sommeil_actuelle = 0
    serie_sommeil_max = 0
    serie_temp = 0
    
    for date_str in dates:
        sommeil = donnees[date_str].get('sommeil', {})
        duree = sommeil.get('duree', 0)
        if 7 <= duree <= 9:
            serie_temp += 1
            serie_sommeil_max = max(serie_sommeil_max, serie_temp)
        else:
            serie_temp = 0
    
    for date_str in reversed(dates):
        sommeil = donnees[date_str].get('sommeil', {})
        duree = sommeil.get('duree', 0)
        if 7 <= duree <= 9:
            serie_sommeil_actuelle += 1
        else:
            break
    
    print(f"\n😴 SOMMEIL OPTIMAL (7-9h) :")
    print(f"   • Série actuelle : {serie_sommeil_actuelle} jour(s)")
    print(f"   • Record : {serie_sommeil_max} jour(s) consécutifs")
    
    # === PATTERNS DÉTECTÉS ===
    print("\n" + "─"*70)
    print("🔍 PATTERNS DÉTECTÉS")
    print("─"*70)
    
    patterns = []
    
    # Pattern week-end vs semaine
    we_sommeil = []
    semaine_sommeil = []
    
    for date_str in dates:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        jour_semaine = date_obj.weekday()
        sommeil = donnees[date_str].get('sommeil', {})
        
        if 'duree' in sommeil:
            if jour_semaine >= 5:  # Samedi, Dimanche
                we_sommeil.append(sommeil['duree'])
            else:
                semaine_sommeil.append(sommeil['duree'])
    
    if we_sommeil and semaine_sommeil:
        moy_we = sum(we_sommeil) / len(we_sommeil)
        moy_semaine = sum(semaine_sommeil) / len(semaine_sommeil)
        diff = moy_we - moy_semaine
        
        if abs(diff) > 1:
            if diff > 0:
                patterns.append(f"😴 Vous dormez {diff:.1f}h de plus le week-end")
            else:
                patterns.append(f"😴 Vous dormez {abs(diff):.1f}h de moins le week-end")
    
    if patterns:
        for pattern in patterns:
            print(f"   • {pattern}")
    else:
        print("   • Aucun pattern significatif détecté")
    
    print("\n" + "═"*70)


# ============================================
# FONCTION 9 : ANALYSER OBJECTIFS (11)
# ============================================
def analyser_objectifs(donnees):
    """
    Analyse objectifs vs réalisations
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print("🎯 OBJECTIFS VS RÉALISATIONS")
    print("═"*70)
    
    dates = sorted(donnees.keys())
    nb_jours = len(dates)
    
    print(f"\n📊 Analyse sur {nb_jours} jour(s)")
    
    # === OBJECTIFS SOMMEIL ===
    print("\n" + "─"*70)
    print("😴 OBJECTIF SOMMEIL : 7-9h par nuit")
    print("─"*70)
    
    durees_sommeil = []
    jours_objectif_atteint = 0
    
    for date_str in dates:
        sommeil = donnees[date_str].get('sommeil', {})
        if 'duree' in sommeil:
            duree = sommeil['duree']
            durees_sommeil.append(duree)
            if 7 <= duree <= 9:
                jours_objectif_atteint += 1
    
    if durees_sommeil:
        taux_reussite = (jours_objectif_atteint / len(durees_sommeil)) * 100
        moy = sum(durees_sommeil) / len(durees_sommeil)
        
        print(f"\n📊 Résultats :")
        print(f"   • Objectif atteint : {jours_objectif_atteint}/{len(durees_sommeil)} jours ({taux_reussite:.1f}%)")
        print(f"   • Durée moyenne : {moy:.2f}h")
        
        # Barre de progression
        barre_pleine = int(taux_reussite / 5)
        barre_vide = 20 - barre_pleine
        barre = "█" * barre_pleine + "░" * barre_vide
        print(f"   [{barre}] {taux_reussite:.0f}%")
        
        if taux_reussite >= 80:
            print(f"\n   ✅ EXCELLENT ! Objectif largement atteint")
        elif taux_reussite >= 60:
            print(f"\n   👍 BON ! Quelques améliorations possibles")
        elif taux_reussite >= 40:
            print(f"\n   ⚠️  MOYEN. Essayez d'améliorer la régularité")
        else:
            print(f"\n   ❌ INSUFFISANT. Priorité à donner au sommeil")
    
    # === OBJECTIFS SPORT ===
    print("\n" + "─"*70)
    print("🏃 OBJECTIF SPORT : 150 min/semaine (OMS)")
    print("─"*70)
    
    total_sport = 0
    jours_avec_sport = 0
    
    for date_str in dates:
        sport = donnees[date_str].get('sport', {})
        duree = sport.get('duree', 0)
        if duree > 0:
            total_sport += duree
            jours_avec_sport += 1
    
    moyenne_hebdo = (total_sport / nb_jours) * 7
    objectif_hebdo = 150
    taux_reussite_sport = min((moyenne_hebdo / objectif_hebdo) * 100, 100)
    
    print(f"\n📊 Résultats :")
    print(f"   • Total cumulé : {total_sport} minutes ({total_sport/60:.1f}h)")
    print(f"   • Moyenne hebdomadaire : {moyenne_hebdo:.0f} min")
    print(f"   • Objectif : {objectif_hebdo} min/semaine")
    print(f"   • Fréquence : {jours_avec_sport}/{nb_jours} jours ({(jours_avec_sport/nb_jours)*100:.1f}%)")
    
    # Barre de progression
    barre_pleine = int(taux_reussite_sport / 5)
    barre_vide = 20 - barre_pleine
    barre = "█" * barre_pleine + "░" * barre_vide
    print(f"   [{barre}] {taux_reussite_sport:.0f}%")
    
    if moyenne_hebdo >= objectif_hebdo:
        print(f"\n   ✅ OBJECTIF ATTEINT ! (+{moyenne_hebdo - objectif_hebdo:.0f} min)")
    else:
        manque = objectif_hebdo - moyenne_hebdo
        print(f"\n   ⚠️  {manque:.0f} min manquantes par semaine")
    
    # === OBJECTIFS DÉPENSES ===
    print("\n" + "─"*70)
    print("💰 OBJECTIF DÉPENSES : <50$/jour")
    print("─"*70)
    
    total_depenses = 0
    jours_objectif_depenses = 0
    montants_journaliers = []
    
    for date_str in dates:
        depenses = donnees[date_str].get('depenses', [])
        montant_jour = sum(d['montant'] for d in depenses)
        total_depenses += montant_jour
        montants_journaliers.append(montant_jour)
        
        if montant_jour <= 50:
            jours_objectif_depenses += 1
    
    moyenne_jour = total_depenses / nb_jours
    taux_reussite_depenses = (jours_objectif_depenses / nb_jours) * 100
    
    print(f"\n📊 Résultats :")
    print(f"   • Total cumulé : {total_depenses:.2f}$")
    print(f"   • Moyenne par jour : {moyenne_jour:.2f}$")
    print(f"   • Jours sous objectif : {jours_objectif_depenses}/{nb_jours} ({taux_reussite_depenses:.1f}%)")
    
    # Barre de progression
    barre_pleine = int(taux_reussite_depenses / 5)
    barre_vide = 20 - barre_pleine
    barre = "█" * barre_pleine + "░" * barre_vide
    print(f"   [{barre}] {taux_reussite_depenses:.0f}%")
    
    if moyenne_jour <= 50:
        print(f"\n   ✅ OBJECTIF ATTEINT ! Bon contrôle budgétaire")
    else:
        print(f"\n   ⚠️  {moyenne_jour - 50:.2f}$ de dépassement quotidien")
    
    # === SCORE GLOBAL ===
    print("\n" + "═"*70)
    print("🌟 SCORE GLOBAL D'ATTEINTE DES OBJECTIFS")
    print("═"*70)
    
    if durees_sommeil:
        score_total = (taux_reussite + taux_reussite_sport + taux_reussite_depenses) / 3
    else:
        score_total = (taux_reussite_sport + taux_reussite_depenses) / 2
    
    print(f"\n🎯 Score global : {score_total:.0f}%")
    
    barre_pleine = int(score_total / 5)
    barre_vide = 20 - barre_pleine
    barre = "█" * barre_pleine + "░" * barre_vide
    print(f"   [{barre}]")
    
    if score_total >= 80:
        print(f"\n   ⭐⭐⭐ EXCELLENT ! Tous les objectifs sont atteints")
    elif score_total >= 60:
        print(f"\n   ⭐⭐ BIEN ! La plupart des objectifs sont atteints")
    elif score_total >= 40:
        print(f"\n   ⭐ MOYEN. Des efforts sont nécessaires")
    else:
        print(f"\n   ❌ INSUFFISANT. Revoyez vos priorités")
    
    print("\n" + "═"*70)



# ============================================
# FONCTION 10 : GÉNÉRER PRÉDICTIONS (12)
# ============================================
def generer_predictions(donnees):
    """
    Générer des prédictions basées sur les tendances
    """
    if not donnees:
        print("\n📭 Aucune donnée disponible")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("═"*70)
    print("🔮 PRÉDICTIONS BASÉES SUR VOS TENDANCES")
    print("═"*70)
    
    dates = sorted(donnees.keys())
    
    if len(dates) < 7:
        print("\n⚠️  Au moins 7 jours de données nécessaires pour les prédictions")
        return
    
    print(f"\n📊 Analyse de {len(dates)} jour(s) de données")
    
    # === PRÉDICTION SOMMEIL ===
    print("\n" + "─"*70)
    print("😴 PRÉDICTION SOMMEIL (7 PROCHAINS JOURS)")
    print("─"*70)
    
    durees_sommeil = []
    for date_str in dates:
        sommeil = donnees[date_str].get('sommeil', {})
        if 'duree' in sommeil:
            durees_sommeil.append(sommeil['duree'])
    
    if len(durees_sommeil) >= 7:
        # Calculer tendance (simple moyenne mobile)
        derniers_7j = durees_sommeil[-7:]
        moy_recente = sum(derniers_7j) / len(derniers_7j)
        
        if len(durees_sommeil) >= 14:
            precedents_7j = durees_sommeil[-14:-7]
            moy_precedente = sum(precedents_7j) / len(precedents_7j)
            tendance = moy_recente - moy_precedente
        else:
            tendance = 0
        
        prediction = moy_recente + tendance
        prediction = max(0, min(prediction, 12))  # Limiter entre 0 et 12h
        
        print(f"\n📈 Tendance actuelle :")
        print(f"   • Moyenne 7 derniers jours : {moy_recente:.2f}h")
        
        if tendance > 0.3:
            print(f"   • Évolution : 📈 En amélioration (+{tendance:.2f}h)")
        elif tendance < -0.3:
            print(f"   • Évolution : 📉 En dégradation ({tendance:.2f}h)")
        else:
            print(f"   • Évolution : ➡️  Stable")
        
        print(f"\n🔮 Prédiction :")
        print(f"   • Durée attendue : ~{prediction:.1f}h par nuit")
        
        if 7 <= prediction <= 9:
            print(f"   ✅ Dans la zone optimale")
        elif prediction < 7:
            print(f"   ⚠️  Risque de sommeil insuffisant")
        else:
            print(f"   ℹ️  Sommeil prolongé prévu")
    
    # === PRÉDICTION SPORT ===
    print("\n" + "─"*70)
    print("🏃 PRÉDICTION ACTIVITÉ SPORTIVE")
    print("─"*70)
    
    jours_sport_recents = 0
    for date_str in dates[-7:]:
        sport = donnees[date_str].get('sport', {})
        if sport.get('duree', 0) > 0:
            jours_sport_recents += 1
    
    frequence_recente = (jours_sport_recents / min(len(dates), 7)) * 100
    
    print(f"\n📈 Tendance actuelle :")
    print(f"   • Fréquence récente : {jours_sport_recents}/7 jours ({frequence_recente:.0f}%)")
    
    print(f"\n🔮 Prédiction :")
    jours_sport_prevus = int((frequence_recente / 100) * 7)
    print(f"   • Jours d'activité prévus : {jours_sport_prevus}/7 prochains jours")
    
    if jours_sport_prevus >= 5:
        print(f"   ✅ Excellente régularité attendue")
    elif jours_sport_prevus >= 3:
        print(f"   👍 Bonne régularité attendue")
    else:
        print(f"   ⚠️  Régularité faible - Essayez d'augmenter")
    
    # === PRÉDICTION DÉPENSES ===
    print("\n" + "─"*70)
    print("💰 PRÉDICTION DÉPENSES")
    print("─"*70)
    
    depenses_recentes = []
    for date_str in dates[-7:]:
        depenses = donnees[date_str].get('depenses', [])
        total = sum(d['montant'] for d in depenses)
        depenses_recentes.append(total)
    
    moy_recente = sum(depenses_recentes) / len(depenses_recentes)
    
    # Calculer tendance
    if len(dates) >= 14:
        depenses_precedentes = []
        for date_str in dates[-14:-7]:
            depenses = donnees[date_str].get('depenses', [])
            total = sum(d['montant'] for d in depenses)
            depenses_precedentes.append(total)
        
        moy_precedente = sum(depenses_precedentes) / len(depenses_precedentes)
        tendance_depenses = moy_recente - moy_precedente
    else:
        tendance_depenses = 0
    
    prediction_depenses = moy_recente + tendance_depenses
    prediction_depenses = max(0, prediction_depenses)
    
    print(f"\n📈 Tendance actuelle :")
    print(f"   • Moyenne 7 derniers jours : {moy_recente:.2f}$/jour")
    
    if tendance_depenses > 5:
        print(f"   • Évolution : 📈 En hausse (+{tendance_depenses:.2f}$)")
    elif tendance_depenses < -5:
        print(f"   • Évolution : 📉 En baisse ({tendance_depenses:.2f}$)")
    else:
        print(f"   • Évolution : ➡️  Stable")
    
    print(f"\n🔮 Prédiction :")
    print(f"   • Dépense quotidienne attendue : ~{prediction_depenses:.2f}$")
    print(f"   • Prévision 7 jours : ~{prediction_depenses * 7:.2f}$")
    print(f"   • Prévision 30 jours : ~{prediction_depenses * 30:.2f}$")
    
    if prediction_depenses <= 40:
        print(f"   ✅ Budget sous contrôle")
    elif prediction_depenses <= 60:
        print(f"   ⚠️  Budget modéré")
    else:
        print(f"   ❌ Attention aux dépenses élevées")
    
    # === RECOMMANDATIONS ===
    print("\n" + "═"*70)
    print("💡 RECOMMANDATIONS")
    print("═"*70)
    
    recommandations = []
    
    if len(durees_sommeil) >= 7 and prediction < 7:
        recommandations.append("😴 Augmentez votre temps de sommeil pour atteindre 7-9h")
    
    if frequence_recente < 50:
        recommandations.append("🏃 Augmentez votre fréquence d'activité physique (objectif: 5j/semaine)")
    
    if prediction_depenses > 50:
        recommandations.append(f"💰 Réduisez vos dépenses de {prediction_depenses - 50:.2f}$/jour")
    
    if recommandations:
        for i, rec in enumerate(recommandations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   ✅ Continuez sur cette lancée ! Aucune recommandation particulière")
    
    print("\n" + "═"*70)
    print("💡 Note : Les prédictions sont basées sur vos tendances récentes")
    print("═"*70)
