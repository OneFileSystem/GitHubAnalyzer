<div style="display: flex; align-items: center; white-space: nowrap; gap: 10px;">
    <img src="https://image.noelshack.com/fichiers/2024/44/6/1730568505-37bfb2bb-301d-48f8-8d71-3d9b0e636132.jpg" alt="Logo" width="60" vertical-align: middle;/>
    <h1 style="margin: 0; font-size: 24px;">GitHubAnalyzer</h1>
</div>

**GitHubAnalyzer** permet d'analyser des dépôts GitHub en récupérant des informations clés et en les présentant de manière concise. Il utilise l'API GitHub et des modèles de traitement du langage naturel pour générer des résumés et des rapports détaillés sur chaque dépôt.

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation des dépendances](#installation-des-dépendances)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Remarques](#remarques)
- [Exemple de sortie](#exemple-de-sortie)
- [Auteurs](#auteurs)
- [License](#license)

## Fonctionnalités

- **Analyse de dépôts GitHub** : Récupère des données d'analyse pour n'importe quel dépôt public.
- **Résumé de README** : Génère un résumé du contenu du fichier README.
- **Informations sur le dépôt** : Affiche le nom, le propriétaire, la description et le langage du dépôt.
- **Statistiques** : Fournit le nombre de stars, forks, commits, problèmes ouverts et pull requests.
- **Gestion des erreurs** : Gère les erreurs lors de la récupération des données GitHub.
- **Compatibilité avec TensorFlow** : Crée un modèle TensorFlow pour des tâches de machine learning.
- **Export des résultats** : Enregistre les résultats d'analyse dans un fichier CSV.
- **Interface utilisateur riche** : Utilise la bibliothèque Rich pour une sortie console attrayante.

## Prérequis

Avant de commencer, assurez-vous d'avoir **Python 3** installé sur votre machine. Vous aurez également besoin des bibliothèques suivantes :

- **numpy** : Pour les calculs numériques.
- **pandas** : Pour la manipulation et l'analyse de données.
- **python-dotenv** : Pour charger les variables d'environnement à partir d'un fichier `.env`.
- **requests** : Pour effectuer des requêtes HTTP.
- **transformers** : Pour utiliser des modèles de traitement de langage naturel.
- **tensorflow** : Pour la création et l'entraînement de modèles de machine learning.
- **rich** : Pour une sortie console colorée et stylisée.

### Installation des dépendances

Vous pouvez installer toutes ces dépendances en utilisant `pip`. Exécutez la commande suivante dans votre terminal :

```bash
pip install numpy pandas python-dotenv requests transformers tensorflow rich
```

## Configuration

1. Clonez le dépôt et accédez au dossier :

   ```bash
   git clone https://github.com/OneFileSystem/GitHubAnalyzer.git
   cd GitHubAnalyzer
   ```

2. Créez un fichier `.env` dans le répertoire principal du projet avec le contenu suivant :

   ```plaintext
   GITHUB_TOKEN=votre_token_gitHub
   ```

## Utilisation

1. Vous disposez d'un fichier `urls.xlsx` contenant une feuille appelée `urls` avec une colonne intitulée `url`. Remplissez cette colonne avec les URLs des dépôts GitHub que vous souhaitez analyser. Par exemple :

| url                                   |
|---------------------------------------|
| https://github.com/user/repo1        |
| https://github.com/user/repo2        |
| https://github.com/user/repo3        |

2. Exécutez le script Python pour analyser les dépôts et générer le rapport. Assurez-vous que le fichier Excel est présent dans le même répertoire que le script.

```bash
python analyze.py
```

3. Après l'exécution, vous verrez un rapport d'analyse dans la console et un fichier CSV nommé `results.csv` dans le répertoire `CSV/`.

## Remarques

- Assurez-vous que l'URL est correctement formatée et présente dans votre fichier `urls.xlsx`.
- Assurez-vous que le token GitHub que vous utilisez a les permissions nécessaires pour accéder aux dépôts.
- Les informations récupérées dépendront des paramètres de confidentialité des dépôts GitHub analysés.

## Exemple de sortie

Le script générera un rapport contenant des informations telles que :

| Nom du dépôt   | Propriétaire | Étoiles | Forks | Commits | Dernier commit | Langage  | Problèmes ouverts | Pull requests |
|----------------|--------------|---------|-------|---------|----------------|----------|-------------------|----------------|
| repo1          | user         | 10      | 2     | 5       | 2023-01-01     | Python   | 1                 | 0              |
| repo2          | user         | 20      | 5     | 10      | 2023-01-10     | JavaScript | 0                 | 1              |

## Auteurs

- [OneFileSystem](https://github.com/OneFileSystem)

## License

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](./LICENSE) pour plus de détails.
