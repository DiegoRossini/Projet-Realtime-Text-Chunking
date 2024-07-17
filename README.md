# Réalisation d'une étude sur l'utilisation des chunkers pour l'analyse de données écrites en temps réel

## Description
Exploration de l'utilisation des chunkers pour analyser des données textuelles en temps réel.

## Introduction

Dans le cadre de notre projet, nous avons entrepris une étude sur l'utilisation des chunkers pour l'analyse de données écrites en temps réel. Le corpus utilisé est composé de données enregistrées en temps réel, comprenant des informations telles que la position du curseur, les caractères écrits ou supprimés, les espaces et les textes finaux. Ces données présentent des défis spécifiques en raison de leur nature particulière et ont été peu explorées dans le domaine du Traitement Automatique des Langues (TAL).

Notre objectif principal était d'explorer la tâche de chunking appliquée à ces données en temps réel. Le chunking est une technique d'analyse linguistique qui identifie et regroupe des mots en unités plus larges, comme des groupes nominaux ou verbaux. En raison des caractéristiques spécifiques des données en temps réel, cette tâche présente des défis nécessitant une exploration approfondie.

## Objectifs

1. **Explorer l'utilisation des chunkers** pour l'analyse de textes en temps réel.
2. **Évaluer les performances des chunkers** sur des données présentant des caractéristiques spécifiques.
3. **Identifier les défis et opportunités** liés à la segmentation de données en temps réel.

## Méthodologie

1. **Formulation des Hypothèses et Questions de Recherche** : Nous avons formulé des questions pour diriger notre recherche, telles que la capacité des chunkers à segmenter précisément les données et la localisation des pauses par rapport aux groupes de mots.
2. **Analyse du Corpus de Données** : Le corpus était composé de données enregistrées en trois étapes du processus de rédaction : la planification, la formulation et la révision.
3. **Sélection des Chunkers** : Nous avons évalué plusieurs chunkers (SEM, TreeTagger, SpaCy, et NLTK) basés sur leurs performances de rappel, précision et F-mesure.
4. **Collecte et Préparation des Données** : Nous avons reconstruit les textes depuis les enregistrements et créé des bigrammes de phrases pour l'analyse avec les chunkers sélectionnés.
5. **Scraping Intensif** : Nous avons utilisé la librairie Selenium pour automatiser la récupération des données chunkées à partir de SEM, en simulant la navigation humaine sur le site web et en passant en boucle tous les bigrammes de notre liste.
6. **Statistiques** : Nous avons automatisé la collecte de statistiques sur les pauses et leur placement par rapport aux chunks, et analysé les données pour identifier des patterns significatifs.

## Résultats

### Hypothèses et Questions de Recherche
Nous avons confirmé nos hypothèses principales, montrant que les chunkers disponibles peuvent segmenter les données en temps réel avec une certaine précision et que les pauses se produisent fréquemment aux frontières des chunks.

### Performances des Chunkers
- **SEM** : A montré les meilleures performances avec un rappel de 98%, une précision de 94% pour le POS tagging, et une F-mesure de 95% pour le chunking.
- **TreeTagger** : Moins performant en termes de précision et de gestion de la ponctuation.
- **SpaCy** : A rencontré des erreurs dans l'identification des limites des chunks.
- **NLTK** : Nécessite des règles manuelles pour le chunking, limitant son automatisation.

### Statistiques et Analyse
Les résultats ont montré que :
- Les pauses se produisent principalement aux frontières des chunks, surtout entre les groupes prépositionnels et nominaux.
- Les chunks nominaux et prépositionnels sont les plus couramment interrompus par des pauses.

## Conclusion

Notre évaluation des chunkers a révélé que SEM était l'outil le plus efficace pour le corpus de données enregistrées en temps réel. Les pauses se trouvent généralement aux frontières des chunks, indiquant leur rôle essentiel dans la segmentation textuelle. Cette étude souligne l'importance d'utiliser des outils performants tels que SEM pour une analyse linguistique précise et ouvre la voie à des améliorations futures et des recherches supplémentaires.

## Contributeurs

- **Diego Rossini** - [GitHub](https://github.com/DiegoRossini)
- **Sandra Jagodzinska**
- **Sarah Almeida Barreto**
- **Yingzi Liu**
