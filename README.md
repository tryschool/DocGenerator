# Documentation de l'API de Génération de Documents

## Introduction

Cette API permet de générer des documents PDF en utilisant un modèle `.odt` et des données JSON fournies. Elle utilise un script Python en arrière-plan pour convertir le document en PDF.

## Pré-requis

- **Python 3** : Pour exécuter le script Python.
- **Node.js et npm** : Pour exécuter l’API.
- **LibreOffice** : Pour la conversion du document `.odt` en PDF.

## Installation

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/Elania-Marvers/DocGenerator
   cd DocGenerator
   ```

2. **Installer les dépendances Python** :
   Exécutez le script `install.sh` pour installer les dépendances nécessaires en Python.

   ```bash
   ./install.sh
   ```

3. **Installer les dépendances Node.js** :
   Installez les dépendances Node.js pour l’API.

   ```bash
   npm install
   ```

4. **Ajouter LibreOffice au PATH** :
   Assurez-vous que LibreOffice est bien ajouté au `PATH` de votre système pour permettre la conversion en PDF. Vérifiez avec la commande suivante :
   ```bash
   libreoffice --version
   ```

## Lancer l’API

Pour démarrer l'API en mode développement avec `nodemon` (si configuré) ou en mode normal :

```bash
npm run dev
```

## Endpoints

### POST `/generate`

Cet endpoint génère un document PDF à partir d’un modèle `.odt` et de données JSON fournies.

- **URL** : `http://localhost:3000/generate`
- **Méthode** : `POST`
- **Body** : `multipart/form-data`

#### Paramètres du Body

| Paramètre     | Type            | Description                               |
|---------------|-----------------|-------------------------------------------|
| `template`    | `File (.odt)`   | Le fichier modèle au format `.odt`        |
| `data`        | `Text (JSON)`   | Les données JSON pour remplir le modèle   |

#### Exemple de données JSON pour `data`

```json
{
    "lastname": "Doe",
    "firstname": "John",
    "period_array": [
        {
            "start_period": "01-01-2024",
            "end_period": "31-01-2024",
            "period_project": "Project A"
        },
        {
            "start_period": "01-02-2024",
            "end_period": "28-02-2024",
            "period_project": "Project B"
        }
    ]
}
```

#### Exemple de Requête avec Postman

1. **Ouvrez Postman** et créez une nouvelle requête `POST`.
2. **URL** : `http://localhost:3000/generate`
3. **Body** : Sélectionnez `form-data`
   - **template** : Mettez un fichier `.odt` comme modèle.
   - **data** : Collez les données JSON dans ce champ.

4. **Envoyez la requête**. L'API renverra le fichier `.pdf` généré en réponse.

### Réponse

Si la requête est réussie, l’API renvoie un fichier `.pdf` généré avec les données fournies.

#### Exemple de réponse

Un fichier PDF nommé `generated_document.pdf` qui peut être téléchargé et visualisé.

### Gestion des Erreurs

Si une erreur survient lors de la génération, l’API retourne une réponse avec un code d'erreur 500.

#### Exemple d'erreur JSON

```json
{
    "error": "Erreur lors de la génération du document"
}
```

## Code et Structure

### Structure de l’API

- **`src/app.js`** : Point d'entrée de l'API, configure le serveur et les routes.
- **`src/controllers/document.controller.js`** : Contrôleur qui gère la logique des requêtes pour l'endpoint `/generate`.
- **`src/services/document.service.js`** : Service qui exécute le script Python `main.py` pour générer le PDF.
- **`main.py`** : Script Python qui gère l'extraction du contenu XML, le remplacement des variables, et la conversion en PDF.