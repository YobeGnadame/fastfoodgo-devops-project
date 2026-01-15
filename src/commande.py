"""
Module de gestion des commandes FastFoodGo.

Ce module contient les fonctions métier pour gérer les commandes,
notamment le calcul du total et la validation des transitions de statut.
"""


class CommandeError(Exception):
    """Exception levée pour les erreurs liées aux commandes."""
    pass


class StatusTransitionError(CommandeError):
    """Exception levée pour les transitions de statut invalides."""
    pass


def calcul_total_commande(articles):
    """
    Calcule le montant total d'une commande.
    
    Args:
        articles (list): Liste de dictionnaires contenant les articles.
                        Chaque article doit avoir les clés 'prix' et 'quantite'.
    
    Returns:
        float: Le montant total de la commande.
    
    Raises:
        CommandeError: Si la liste est vide ou si un article est invalide.
        TypeError: Si le type des données n'est pas correct.
    """
    if not isinstance(articles, list):
        raise TypeError("Les articles doivent être une liste.")
    
    if len(articles) == 0:
        raise CommandeError("La liste des articles ne peut pas être vide.")
    
    total = 0.0
    
    for article in articles:
        if not isinstance(article, dict):
            raise TypeError("Chaque article doit être un dictionnaire.")
        
        if 'prix' not in article or 'quantite' not in article:
            raise CommandeError("Chaque article doit avoir les clés 'prix' et 'quantite'.")
        
        prix = article['prix']
        quantite = article['quantite']
        
        if not isinstance(prix, (int, float)) or not isinstance(quantite, (int, float)):
            raise TypeError("Le prix et la quantité doivent être des nombres.")
        
        if prix < 0 or quantite < 0:
            raise CommandeError("Le prix et la quantité ne peuvent pas être négatifs.")
        
        total += prix * quantite
    
    return round(total, 2)


# Statuts valides pour une commande
STATUTS_VALIDES = ['en_attente', 'confirmee', 'en_preparation', 'prete', 'livree', 'annulee']

# Transitions de statut autorisées
TRANSITIONS_AUTORISEES = {
    'en_attente': ['confirmee', 'annulee'],
    'confirmee': ['en_preparation', 'annulee'],
    'en_preparation': ['prete', 'annulee'],
    'prete': ['livree'],
    'livree': [],
    'annulee': []
}


def validation_transition_statut(statut_actuel, nouveau_statut):
    """
    Valide la transition d'une commande d'un statut à un autre.
    
    Args:
        statut_actuel (str): Le statut actuel de la commande.
        nouveau_statut (str): Le nouveau statut souhaité.
    
    Returns:
        bool: True si la transition est valide, False sinon.
    
    Raises:
        StatusTransitionError: Si la transition n'est pas autorisée.
        ValueError: Si l'un des statuts n'existe pas.
    """
    if not isinstance(statut_actuel, str) or not isinstance(nouveau_statut, str):
        raise TypeError("Les statuts doivent être des chaînes de caractères.")
    
    statut_actuel = statut_actuel.lower().strip()
    nouveau_statut = nouveau_statut.lower().strip()
    
    if statut_actuel not in STATUTS_VALIDES:
        raise ValueError(f"Statut actuel invalide: {statut_actuel}. Statuts valides: {STATUTS_VALIDES}")
    
    if nouveau_statut not in STATUTS_VALIDES:
        raise ValueError(f"Nouveau statut invalide: {nouveau_statut}. Statuts valides: {STATUTS_VALIDES}")
    
    if statut_actuel == nouveau_statut:
        raise StatusTransitionError("Le nouveau statut doit être différent du statut actuel.")
    
    if nouveau_statut not in TRANSITIONS_AUTORISEES[statut_actuel]:
        transitions_possibles = TRANSITIONS_AUTORISEES[statut_actuel]
        raise StatusTransitionError(
            f"Transition de '{statut_actuel}' à '{nouveau_statut}' non autorisée. "
            f"Transitions possibles: {transitions_possibles}"
        )
    
    return True
