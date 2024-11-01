# GitHubAnalyzer

GitHubAnalyzer est un script Python puissant qui analyse les dépôts GitHub en récupérant des informations essentielles, telles que le nombre de commits, les contributeurs et un résumé du fichier README.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [License](#license)

## Fonctionnalités

- **Analyse complète des dépôts GitHub** : Récupération des informations de base, y compris le nombre de commits et de contributeurs.
- **Résumé automatique des README** : Utilisation du modèle BART pour créer des résumés pertinents des fichiers README.
- **Exportation des résultats** : Sauvegarde des analyses dans un fichier CSV pour une consultation facile.
- **Interface utilisateur simple** : Éditez un fichier Excel pour spécifier les dépôts à analyser.

## Prérequis

Avant d'exécuter le script, assurez-vous que les éléments suivants sont installés sur votre système :

- **Python** : Version 3.6 ou supérieure.
- **pip** : Le gestionnaire de paquets Python.

## Installation

1. **Clonez le dépôt :**

   ```bash
   git clone https://github.com/your_username/GitHubAnalyzer.git
   cd GitHubAnalyzer
   ```

2. **Installez les dépendances :**

   Exécutez la commande suivante pour installer les bibliothèques nécessaires :

   ```bash
   pip install requests transformers pandas
   ```

## Configuration

1. **Générer un Token GitHub :**

   - Allez sur [GitHub](https://github.com).
   - Accédez à `Settings` > `Developer settings` > `Personal access tokens`.
   - Cliquez sur `Generate new token`, donnez-lui un nom, sélectionnez les permissions nécessaires et copiez le token généré.

2. **Modifier le script :**

   Ouvrez le fichier principal du script (`analyze.py`) et modifiez la ligne suivante :

   ```python
   GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"
   ```

   Assurez-vous de remplacer `"YOUR_GITHUB_TOKEN_HERE"` par votre vrai token GitHub.

## Utilisation

1. **Remplissez le fichier Excel :**

   Ouvrez le fichier Excel (nommé `urls.xlsx`), puis dans la colonne `url`, indiquez les URLs des dépôts GitHub que vous souhaitez analyser.

   Exemple de contenu du fichier `urls.xlsx` :

   | url                              |
   |----------------------------------|
   | https://github.com/user/repo1    |
   | https://github.com/user/repo2    |

2. **Exécutez le script :**

   Exécutez le script pour analyser les dépôts et générer un fichier CSV avec les résultats :

   ```bash
   python analyze.py
   ```

3. **Consultez le fichier CSV :**

   Après l'exécution du script, un fichier CSV sera généré (nommé `results.csv` par exemple) contenant les résultats de l'analyse.

## Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez contribuer à ce projet, veuillez suivre ces étapes :

1. Fork le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/YourFeature`).
3. Commitez vos changements (`git commit -m 'Add some feature'`).
4. Poussez votre branche (`git push origin feature/YourFeature`).
5. Ouvrez une pull request.

## License

Ce projet est sous licence MIT. Pour plus de détails, veuillez consulter le fichier [LICENSE](LICENSE).
