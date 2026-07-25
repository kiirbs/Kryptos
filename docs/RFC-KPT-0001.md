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
- Séparation des responsabilités
- Compatibilité descendante lorsque possible
- Éviter les informations déductibles
- Les objets représentent les concepts de la spécification

---

## Invariants

- Un fichier commence toujours par un Header
- Le Header fait toujours 8 octets
- Tous les Chunks possèdent un Type et une Taille
- Les entiers multioctets sont encodés en Big Endian
- Un Chunk peut être ignoré s'il n'est pas reconnu

---

## Dictionnaire

### Chunk type

| ID | Chunk |
|----|-------|
| 0x01 | Métadonnées |
| 0x02 | Données chiffrées |
| 0x03 | Hash |

### Field type

| ID | Field | Description |
|----|-------|-------------|
| 0x01 | Original Filename | Restaurer le nom d'origine |
| 0x02 | MIME Type | Savoir quel type de fichier on déchiffre |
| 0x03 | Creation Timestamp | Conserver la date de création |
| 0x04 | Original File Size | Vérification et restauration |
| 0x05 | Comment | Laisser une note facultative |

### Version

| ID | Version |
|----|---------|
| 0x01 | V1 |

### Algorithme

| ID | Algo |
|----|------|
| 0x01 | XOR |

---

## Structure

### Générale

| Bloc | Taille | Description | Statut |
|-------|--------|-------------|--------|
| Header | 8o | Parcourir le fichier | 🟢 Validé | 
| Métadonnées | Variable | Informations complémentaires | 🟢 Validé |
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
| Chunk Size | 8o | Taille du chunk | 🟢 Validé | Oui |
| Contenu | Variable | Contenu du chunk | 🟢 Validé | Oui |

### Métadonnées field

| Champ | Taille | Description | Statut | Endianness |
|-------|--------|-------------|--------|------------|
| Field Type | 1o | Identifiant numérique du field | 🟢 Validé | Non |
| Field Size | 8o | Taille du field | 🟢 Validé | Oui |
| Contenu | Variable | Contenu du field | 🟢 Validé | Oui |

---

## Hiérarchie

Fichier KPT
│
├── Header (bootstrap)
│
└── Chunks
    │
    ├── Metadata
    │   └── Fields
    │
    ├── Data
    │
    └── Hash

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

- Architecture récursive
    - Modulable

---

## Questions ouvertes

- Taille de la signature ?

- Taille de la version ?

- Format du hash ?

- Les métadonnées sont-elles obligatoires ?

- Chunk Size représente-t-il :
    - la taille totale du Chunk ?
    - la taille du contenu uniquement ?