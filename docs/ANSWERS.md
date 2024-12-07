# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

_Inscrire la documentation technique_

### Etape 1:

Pour ce test, j'utilise **conda** pour créer l'environnement et l'activer.

### Commandes utilisées (en se positionnant à la racine du projet `\technical-test-data-engineer-develop`) :


conda create -n moovai python=3.9 -y
conda activate moovai
conda install -r requirements.txt


### Etape 2:
En se pointant sur le dossier src\moovitamix_fastapi, on execute la commande "python -m uvicorn main:app", ceci démarre l'API sur le serveur local http://127.0.0.1:8000
Pour automatiser la récupération quotidienne des données, nous avons plusieurs possibilités à explorer:

1. **Cron Jobs** : Utilisation d’un planificateur de tâches intégré au système pour exécuter un script à intervalles réguliers. Idéal pour les environnements Linux/Unix.
2. **Task Scheduler (Windows)** : Planificateur similaire pour Windows, permettant d'exécuter des scripts Python de manière planifiée.
3. **Bibliothèques Python comme APScheduler** : Solution intégrée dans le code Python, permettant une grande portabilité et une gestion fine des tâches.
4. **Fonctions Serverless** : Utilisation de services comme AWS Lambda ou Google Cloud Functions pour exécuter des tâches périodiques sans gérer d’infrastructure.
5. **Pipelines CI/CD** : Automatisation via des outils comme GitHub Actions pour exécuter des scripts selon un calendrier défini.
6. **Docker et Kubernetes** : Conteneurisation des scripts et gestion des exécutions planifiées via des CronJobs Kubernetes ou d'autres outils similaires.


## **Choix pour ce projet**

Pour simplifier la tâche, je vais utiliser une approche combinant des bibliothèques comme requests pour les appels API et APScheduler pour la planification des tâches quotidiennes. Cette méthode est facile à implémenter, portable, et permet une intégration directe dans un script Python unique sans dépendances lourdes.

Du coup je procède a installer les dépendances "requests" et "APScheduler" en utilisant la commande ```pip install requests apscheduler```
Ensuite, je crée un script ```python python fetch_data.py``` sur le même dossier courant pour automatiser les appels quotidiens à l'API

Je me suis conformé aux instructions du test et aux bonnes pratiques du développement de code en intégrant les test des edge cases et le logging lors de l'implémentation du script

### Etape 3:
Je vais m'assurer que les différentes parties du code du pipeline fonctionnent correctement. Donc, je vais me concentrer sur les éléments essentiels du flux de données, à savoir :

1. **La fonction api_request** : pour vérifier que les appels API fonctionnent correctement, en tenant compte des succès et des erreurs possibles.
2. **La fonction save_to_file** : pour garantir que les données sont correctement enregistrées dans un fichier JSON.
3. **Le pipeline global run_pipeline** : pour tester l'exécution complète du flux de données, en simulant l'appel des différents endpoints et l'enregistrement des données.

Je tiendrais en compte les cas d'erreurs et de succès possible pour m'assurer que tout fonctionne comme prévu, et je me limiterai sur les test du endpoint /tracks pour ne pas faire des test exhaustives
Pour ce faire, je crée un script "unit_tests.py" dans le même dossier courant et je l'éxécute en utilisant la commande ```python -m unittest unit_tests.py```



## Questions (étapes 4 à 7)

### Étape 4

_votre réponse ici_
## **Conception du schéma**

### **1. Table : `users`**
Stocke les informations détaillées des utilisateurs

| Colonne           | Type              | Contraintes                   | Description                            |
|-------------------|-------------------|-------------------------------|----------------------------------------|
| `id`              | INT               | PRIMARY KEY, AUTO_INCREMENT   | Identifiant unique pour chaque utilisateur. |
| `first_name`      | VARCHAR(255)      | NOT NULL                      | Prénom de l'utilisateur.               |
| `last_name`       | VARCHAR(255)      | NOT NULL                      | Nom de famille de l'utilisateur.       |
| `email`           | VARCHAR(255)      | NOT NULL, UNIQUE              | Adresse email de l'utilisateur.        |
| `gender`          | VARCHAR(50)       |                               | Genre de l'utilisateur (homme, femme, etc.). |
| `favorite_genres` | TEXT              |                               | Genres musicaux favoris de l'utilisateur. |
| `created_at`      | TIMESTAMP         | DEFAULT CURRENT_TIMESTAMP     | Date de création de l'utilisateur.     |
| `updated_at`      | TIMESTAMP         | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Dernière mise à jour. |

---

### **2. Table : `tracks`**
Stocke les informations détaillées des pistes musicales.

| Colonne        | Type              | Contraintes                   | Description                            |
|----------------|-------------------|-------------------------------|----------------------------------------|
| `id`           | INT               | PRIMARY KEY, AUTO_INCREMENT   | Identifiant unique pour chaque piste.  |
| `name`         | VARCHAR(255)      | NOT NULL                      | Titre de la piste musicale.            |
| `artist`       | VARCHAR(255)      |                               | Artiste associé à la piste.            |
| `songwriters`  | VARCHAR(255)      |                               | Auteurs de la chanson.                 |
| `duration`     | VARCHAR(10)       |                               | Durée de la piste (ex : "03:45").      |
| `genres`       | TEXT              |                               | Genres musicaux associés à la piste.   |
| `album`        | VARCHAR(255)      |                               | Album contenant la piste.              |
| `created_at`   | TIMESTAMP         | DEFAULT CURRENT_TIMESTAMP     | Date de création de l'enregistrement.  |
| `updated_at`   | TIMESTAMP         | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Dernière mise à jour. |

---

### **3. Table : `listen_history`**
Associe les utilisateurs aux pistes qu'ils ont écoutées, en utilisant une liste des identifiants de pistes pour un utilisateur donné.

| Colonne         | Type              | Contraintes                   | Description                            |
|-----------------|-------------------|-------------------------------|----------------------------------------|
| `id`            | INT               | PRIMARY KEY, AUTO_INCREMENT   | Identifiant unique de l'historique.    |
| `user_id`       | INT               | FOREIGN KEY (`users.id`)      | Identifiant de l'utilisateur.          |
| `track_ids`     | JSON              |                               | Liste des identifiants de pistes.      |
| `created_at`    | TIMESTAMP         | DEFAULT CURRENT_TIMESTAMP     | Date de création de l'historique.      |
| `updated_at`    | TIMESTAMP         | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Dernière mise à jour. |

---

## **Recommandation du Système de Base de Données**

### **Système Recommandé : PostgreSQL**
#### Raisons :
1. **Fiabilité et robustesse** : PostgreSQL est une base de données relationnelle très fiable avec des fonctionnalités avancées pour gérer des données complexes.
2. **Gestion des relations complexes** : La structure des données (relations entre `users`, `tracks`, et `listen_history`) est adaptée à un SGBDR tel que PostgreSQL.
3. **Extensibilité** : PostgreSQL permet d'ajouter des fonctionnalités spécifiques grâce à des extensions, ce qui est utile si des analyses avancées ou des données semi-structurées sont nécessaires.
5. **Support communautaire** : PostgreSQL est bien documenté et dispose d'une large communauté d'utilisateurs.

---

## **Avantages du Schéma**
- **Scalabilité** : Chaque table est découplée, permettant une extension facile des données ou des relations futures.
- **Facilité d'analyse** : Les relations bien définies permettent des requêtes analytiques efficaces sur les habitudes d'écoute, les utilisateurs actifs, etc.
- **Maintenance simplifiée** : Les contraintes de base (clés primaires, étrangères, unicité) garantissent l'intégrité des données.


### Étape 5

_votre réponse ici_
# Méthode de Surveillance du Pipeline de Données

### **1. Outils de Surveillance**
- **Système de Logs Centralisé** : Utilisation d’outils du Cloud Logging comme (AWS CloudWatch, Google Cloud Logging).
- **Dashboards de Monitoring** : Outils comme Grafana pour visualiser les métriques en temps réel.
- **Alertes Automatiques** : Mise en place de notifications via email en cas d’échec.

### **2. Métriques Clés à Suivre**
#### **Étapes du Pipeline**
- **Taux de succès/échec des tâches** : Pourcentage des tâches exécutées avec succès.
- **Durée d’exécution** : Temps moyen pour chaque étape du pipeline.
- **Latence** : Temps écoulé entre l’ingestion et la disponibilité des données.
- **Volume des données traitées** : Nombre de lignes ou taille des fichiers ingérés quotidiennement.


---
### Étape 6

_votre réponse ici_

### **1. Automatisation du Calcul des Recommandations**
#### **Architecture Proposée**
1. **Pipeline de Données**
   - Ingestion quotidienne des nouvelles interactions utilisateur.
   - Nettoyage et préparation des données.
2. **Module de Calcul**
   Algorithme de recommandation basé sur un modèle prédéfini (filtrage collaboratif, basé sur le contenu, ou hybride), un modèle de ML comme ALS (Alternating Least Squares), KNN (K-Nearest Neighbors), ou Deep Learning est utilisé pour générer les recommandations.

#### **Fréquence**
- **Batch Processing** : Calcul des recommandations toutes les 24 heures.
- **Approche Temps Réel** (si nécessaire) : Utilisation de Kafka pour les flux en temps réel avec Spark Streaming.

### Étape 7

_votre réponse ici_
### Automatisation du Réentraînement du Modèle de Recommandation

---

### **Étapes pour Automatiser le Réentraînement du Modèle de Recommandation**

#### 1. **Collecte et Préparation des Données**
- **Pipeline de données** : Un pipeline robuste est essentiel pour ingérer, nettoyer et transformer ces données dans un format adéquat pour le modèle de recommandation. Des outils comme Apache Airflow, Kubeflow ou des scripts personnalisés peuvent être utilisés pour automatiser cette étape.

#### 2. **Détection des Modifications de Données**
- **Fréquence de réentraînement** : Définir une fréquence pour vérifier si de nouvelles données sont disponibles et déterminer si le modèle nécessite un réentraînement. Cela pourrait être quotidien, hebdomadaire, ou basé sur un seuil de nouvelles données.

#### 3. **Réentraînement du Modèle**
- **Planification du réentraînement** : Le réentraînement automatique peut être géré avec des outils comme **Kubeflow**, **Apache Airflow**, ou **MLflow**. Ces outils permettent de créer des workflows programmés qui réexécutent le processus de réentraînement à intervalles réguliers ou lorsque des conditions spécifiques sont remplies.
- **Sélection de l'algorithme** : Selon le type de système de recommandation (par exemple, filtrage collaboratif, basé sur le contenu, ou hybride), l'algorithme approprié doit être choisi. Par exemple, pour un modèle de filtrage collaboratif, vous pourriez utiliser des matrices de similarité ou des modèles comme **ALS (Alternating Least Squares)**. Pour un modèle basé sur le contenu, des techniques comme TF-IDF ou des réseaux de neurones peuvent être appliquées.
#### 4. **Automatisation et Déploiement**
- **Automatisation avec des outils CI/CD** : L'intégration continue et le déploiement continu (CI/CD) permettent de déployer automatiquement le modèle réentrainé dans l’environnement de production. Ces outils (comme Jenkins, GitLab CI, ou CircleCI) peuvent automatiser l’ensemble du processus de réentraînement, y compris la mise à jour du modèle sur les serveurs de production.
- **Monitoring post-déploiement** : Une fois le modèle déployé, il est important de suivre ses performances en temps réel. Des outils de monitoring comme **Prometheus** ou **Grafana** peuvent être utilisés pour surveiller l'impact des nouvelles recommandations sur l'expérience utilisateur.

---