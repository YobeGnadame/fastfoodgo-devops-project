"""
Tests unitaires pour le module de gestion des commandes FastFoodGo.
"""

import pytest
from src.commande import (
    calcul_total_commande,
    validation_transition_statut,
    CommandeError,
    StatusTransitionError,
)

# Tests pour la fonction calcul_total_commande


def test_calcul_total_commande_cas_nominal():
    """Test du cas nominal avec une liste d'articles valide."""
    articles = [
        {'prix': 10.5, 'quantite': 2},
        {'prix': 5.0, 'quantite': 1},
        {'prix': 2.25, 'quantite': 4},
    ]
    assert calcul_total_commande(articles) == 35.0


def test_calcul_total_commande_cas_limite_un_article():
    """Test du cas limite avec un seul article."""
    articles = [{'prix': 15.0, 'quantite': 1}]
    assert calcul_total_commande(articles) == 15.0


def test_calcul_total_commande_cas_limite_quantite_zero():
    """Test du cas limite avec une quantité de zéro."""
    articles = [
        {'prix': 10.0, 'quantite': 2},
        {'prix': 5.0, 'quantite': 0},
    ]
    assert calcul_total_commande(articles) == 20.0


def test_calcul_total_commande_cas_limite_prix_zero():
    """Test du cas limite avec un prix de zéro."""
    articles = [
        {'prix': 0.0, 'quantite': 5},
        {'prix': 12.5, 'quantite': 2},
    ]
    assert calcul_total_commande(articles) == 25.0


def test_calcul_total_commande_erreur_liste_vide():
    """Test d'erreur avec une liste d'articles vide."""
    with pytest.raises(CommandeError, match="La liste des articles ne peut pas être vide."):
        calcul_total_commande([])


def test_calcul_total_commande_erreur_prix_negatif():
    """Test d'erreur avec un prix négatif."""
    articles = [{'prix': -10.0, 'quantite': 2}]
    with pytest.raises(CommandeError, match="Le prix et la quantité ne peuvent pas être négatifs."):
        calcul_total_commande(articles)


def test_calcul_total_commande_erreur_quantite_negative():
    """Test d'erreur avec une quantité négative."""
    articles = [{'prix': 10.0, 'quantite': -2}]
    with pytest.raises(CommandeError, match="Le prix et la quantité ne peuvent pas être négatifs."):
        calcul_total_commande(articles)


def test_calcul_total_commande_erreur_cle_manquante():
    """Test d'erreur avec une clé manquante dans un article."""
    articles = [{'prix': 10.0}]
    with pytest.raises(CommandeError, match="Chaque article doit avoir les clés 'prix' et 'quantite'."):
        calcul_total_commande(articles)


def test_calcul_total_commande_erreur_type_invalide():
    """Test d'erreur avec un type de données invalide pour le prix."""
    articles = [{'prix': 'dix', 'quantite': 2}]
    with pytest.raises(TypeError, match="Le prix et la quantité doivent être des nombres."):
        calcul_total_commande(articles)


# Tests pour la fonction validation_transition_statut


@pytest.mark.parametrize(
    "statut_actuel, nouveau_statut",
    [
        ('en_attente', 'confirmee'),
        ('confirmee', 'en_preparation'),
        ('en_preparation', 'prete'),
        ('prete', 'livree'),
        ('confirmee', 'annulee'),
    ]
)
def test_validation_transition_statut_cas_nominal(statut_actuel, nouveau_statut):
    """Test des transitions de statut valides."""
    assert validation_transition_statut(statut_actuel, nouveau_statut) is True


@pytest.mark.parametrize(
    "statut_actuel, nouveau_statut, message_erreur",
    [
        ('en_attente', 'prete', "Transition de 'en_attente' à 'prete' non autorisée."),
        ('livree', 'en_preparation', "Transition de 'livree' à 'en_preparation' non autorisée."),
        ('annulee', 'confirmee', "Transition de 'annulee' à 'confirmee' non autorisée."),
    ]
)
def test_validation_transition_statut_erreur_transition_invalide(statut_actuel, nouveau_statut, message_erreur):
    """Test des transitions de statut invalides."""
    with pytest.raises(StatusTransitionError, match=message_erreur):
        validation_transition_statut(statut_actuel, nouveau_statut)


def test_validation_transition_statut_erreur_statut_actuel_invalide():
    """Test d'erreur avec un statut actuel qui n'existe pas."""
    with pytest.raises(ValueError, match="Statut actuel invalide: inexistant."):
        validation_transition_statut('inexistant', 'confirmee')


def test_validation_transition_statut_erreur_nouveau_statut_invalide():
    """Test d'erreur avec un nouveau statut qui n'existe pas."""
    with pytest.raises(ValueError, match="Nouveau statut invalide: inexistant."):
        validation_transition_statut('en_attente', 'inexistant')


def test_validation_transition_statut_erreur_statuts_identiques():
    """Test d'erreur lorsque le nouveau statut est identique à l'actuel."""
    with pytest.raises(StatusTransitionError, match="Le nouveau statut doit être différent du statut actuel."):
        validation_transition_statut('confirmee', 'confirmee')


def test_validation_transition_statut_cas_limite_espaces_et_casse():
    """Test avec des espaces et des casses différentes pour les statuts."""
    assert validation_transition_statut('  EN_ATTENTE  ', '  Confirmee  ') is True
