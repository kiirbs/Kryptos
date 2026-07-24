# RFC-KPT-0001
## Format de fichier Kryptos

### Statut

Draft

---

## Objectif

Définir le format des fichiers `.kpt`.

---

## Principes de conception

- Format extensible
- Header minimal
- Chunks indépendants
- Aucune information redondante
- Compatibilité ascendante

---

## Structure

### Générale

| Block | Taille | Description | Statut |
|-------|--------|-------------|--------|
| Header | 8o | Parcourir le fichier | 🟢 Validé | 
| Métadonnées | Variable | Informations complémentaires | 🟡 À définir |
| Données chiffrées | Variable | Contenu du fichier | 🟢 Validé |
| Hash | Variable | Vérification d'intégrité | 🟡 À définir |

### Header

| Champ | Taille | Description | Statut | Endianness |
|-------|--------|-------------|--------|------------|
| Magic Number | 4o | Identifiant du format | 🟢 Validé | Oui |
| Version | 1o | Version logiciel | 🟢 Validé | Non |
| Header Size | 1o | Taille du header | 🟢 Validé | Non |
| Algorithme | 1o | Algorithme utilisé | 🟢 Validé | Non |
| Flags | 1o | Huit flags | 🟡 À définir | Non |

### Chunk

| Champ | Taille | Description | Statut | Endianness |
|-------|--------|-------------|--------|------------|
| Chunk Type | 1o | Identifiant numérique du chunk | 🟢 Validé | Non |
| Chunk Size | 8o | Taille du block | 🟢 Validé | Oui |
| Contenu | Variable | Contenu du block | 🟢 Validé | Oui |

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

- Implementation en Big Endian
    - Lisible
    - Simple
    - Souvent utilisé

---

## Questions ouvertes

- Taille de la signature ?
- Taille de la version ?
- Format du hash ?
- Les métadonnées sont-elles obligatoires ?