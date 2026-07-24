# Journal Kryptos

## Recap

### Ce que j'ai appris

- Un ordinateur manipule des octets, pas du texte.
- Les `bytes` sont différents des `str`.
- XOR est réversible.
- Les formats de fichiers contiennent des métadonnées.
- Chiffrement avec XOR
- Conception de format
- Conteneur binaire orienté blocs
- Endianness

### Décisions prises

- Le projet utilisera Git.
- Une RFC décrira le format `.kpt`.
- Le format `.kpt` sera un conteneur binaire orienté blocs avec un header de 8 octets

### Questions restantes

- Comment transmettre une clé ?
- À quoi sert réellement un hash ?
- Comment fonctionne un salt ?

### Idées

Créer un format suffisamment générique pour pouvoir supporter plusieurs algorithmes.