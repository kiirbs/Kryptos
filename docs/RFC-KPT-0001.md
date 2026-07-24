# RFC-KPT-0001
## Format de fichier Kryptos

### Statut

Draft

---

## Objectif

Définir le format des fichiers `.kpt`.

---

## Structure

### Générale

| Block | Taille | Description | Statut |
|-------|--------|-------------|--------|
| Header | 16o | Parcourir le fichier | 🟢 Validé |
| Métadonnées | Variable | Informations complémentaires | 🟡 À définir |
| Données chiffrées | Variable | Contenu du fichier | 🟢 Validé |
| Hash | Variable | Vérification d'intégrité | 🟡 À définir |

---

### Header

| Champ | Taille | Description | Statut |
|-------|--------|-------------|--------|
| Magic Number | 4o | Identifiant du format | 🟢 Validé |
| Version | 1o | Version logiciel | 🟢 Validé |
| Algorithme | 1o | Algorithme utilisé | 🟢 Validé |
| Flags | 1o | Huit flags | 🟡 À définir |
| Réservé | 1o | Emplacement réservé | 🟢 Validé |

---

### Chunk

| Champ | Taille | Description | Statut |
|-------|--------|-------------|--------|
| Chunk Type | 1o | Nom du block en numérique | 🟢 Validé |
| Chunk Size | 8o | Taille du block | 🟢 Validé |
| Contenu | Variable | Contenu du block | 🟢 Validé |

---

## Décisions

- Header de taille fixe
    - Lecture rapide
    - Compatible avec les futures versions
    - Structure stable

- Métadonnées optionnelles
    - Respect de la confidentialité
    - Réduction de la taille des fichiers
    - Flexibilité

- Algorithmes représentés par un identifiant numérique
    - Format compact
    - Lecture rapide
    - Extensible

- Le format `.kpt` est un conteneur binaire orienté blocs
    - Il est composé de :
        - Un header fixe de 8 octets
        - Une suite de blocs indépendants
    - Chaque bloc possède :
        - Un identifiant
        - Une taille
        - Un contenu
    - Avantages :
        - Extensible
        - Responsabilité unique
        - Simple

---

## Questions ouvertes

- Taille de la signature ?
- Taille de la version ?
- Format du hash ?
- Les métadonnées sont-elles obligatoires ?