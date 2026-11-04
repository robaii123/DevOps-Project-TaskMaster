# 🚀 TaskMaster Pro — Architecture 3-Tiers & Pipeline DevSecOps

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Multi--Stage_Alpine-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Security](https://img.shields.io/badge/Trivy_Scan-0_Vulnerabilities-00C853?style=for-the-badge&logo=aquasecurity&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11_%7C_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16--Alpine-336791?style=for-the-badge&logo=postgresql&logoColor=white)

Application web de gestion de tâches déployée selon les standards d'ingénierie **DevSecOps** de production : architecture conteneurisée à 3 tiers isolés, serveur WSGI multi-workers, construction Docker Multi-Stage ultra-légère et pipeline CI/CD automatisé avec portes de sécurité strictes.

---

## 🏗️ Architecture Système (3-Tiers Isolés)

L'application ne publie jamais le serveur Python directement sur l'extérieur. Seul le **Reverse Proxy Nginx** est exposé sur le port `8080`, routant le trafic via le réseau privé interne de Docker :

```text
[ Client / Navigateur (:8080) ]
              │
              ▼
┌─────────────────────────────┐
│  Conteneur NGINX (:80)      │ ◄── Reverse Proxy (nginx:alpine - ~2.5 Mo RAM)
└─────────────┬───────────────┘
              │ (Réseau interne Docker - Port 5000)
              ▼
┌─────────────────────────────┐
│  Conteneur WEB (:5000)      │ ◄── Gunicorn 22.0.0 (4 Workers WSGI) + Flask 3.0.3
│  User: appuser (Non-Root)   │     Image Multi-Stage Python 3.12-alpine (26.7 Mo)
└─────────────┬───────────────┘
              │ (Réseau interne Docker - Port 5432)
              ▼
┌─────────────────────────────┐
│  Conteneur DB (:5432)       │ ◄── PostgreSQL 16-alpine + Volume persistant (pgdata)
└─────────────────────────────┘
```

---

## 📊 Métriques d'Optimisation & DevSecOps

| Indicateur | Avant Optimisation (Standard) | Après Optimisation (Production-Grade) | Gain / Impact |
| :--- | :--- | :--- | :--- |
| **Image de base** | `python:3.11-slim` (Debian) | `python:3.12-alpine` (Multi-Stage) | Surface d'attaque minimale |
| **Taille de l'image** | ~214 MB (58 MB compressée) | **110 MB (26.7 MB compressée)** | **-54 % de poids réseau** |
| **Failles (CRITICAL / HIGH)** | 44 vulnérabilités OS | **0 vulnérabilité (Trivy Gate)** | **100 % remédié (`exit-code: 1`)** |
| **Serveur Web** | Serveur de dev Flask (1 thread) | **Gunicorn WSGI (4 Workers)** | Haute concurrence & résilience |
| **Privilèges Conteneur** | `root` (par défaut) | **`appuser` (Non-Root)** | Isolation contre l'escalade de privilèges |

---

## ⚙️ Pipeline CI/CD (`.github/workflows/pipeline.yml`)

Le pipeline s'exécute automatiquement sur les branches `dev` et `main` (avec filtrage `paths-ignore` sur la documentation pour économiser les ressources CI) :

1. **Job 1 — `quality-test` (Intégration Continue & Matrice) :**
   * **Matrix Strategy :** Exécution parallèle des tests sur **Python `3.11` et `3.12`**.
   * **Service Container :** Base de données éphémère `postgres:16-alpine` avec vérification de santé (`pg_isready`).
   * **Pip Caching & Séparation :** Mise en cache des dépendances et séparation stricte entre `requirements.txt` (Prod) et `requirements-dev.txt` (Tests/Linter).
   * **Qualité & Tests :** Analyse statique du code avec `flake8` et tests d'intégration SQL avec `pytest`.

2. **Job 2 — `build-scan-push` (DevSecOps & Livraison) :**
   * *Déclenché uniquement sur `main` après validation de la matrice de tests.*
   * **Docker BuildKit Cache :** Construction Multi-Stage accélérée grâce au cache natif GitHub Actions (`type=gha,mode=max`).
   * **Double Tagging :** Versionnement immuable avec `:latest` et `:${{ github.sha }}`.
   * **Security Gate (Trivy) :** Scan de l'image avant publication. Le pipeline est **bloqué automatiquement** (`exit-code: '1'`) si une faille `HIGH` ou `CRITICAL` est détectée.
   * **Publication :** Push sécurisé vers Docker Hub.

3. **Job 3 — `deploy` (Continuous Deployment avec Approbation) :**
   * Protégé par l'environnement GitHub **`production`** avec règle **Required Reviewers** (*Manual Approval Gate*).
   * Déclenchement du déploiement Cloud sur **Render** via Webhook sécurisé.

---

## 🛠️ Stack Technique & Versions

* **Backend :** Python `3.12`, Flask `3.0.3`, Psycopg2-binary `2.9.9`
* **Serveur WSGI :** Gunicorn `22.0.0` (4 workers synchrones)
* **Reverse Proxy :** Nginx (`nginx:alpine`)
* **Base de données :** PostgreSQL `16` (`postgres:16-alpine`)
* **Qualité & Sécurité :** Pytest, Flake8, Aqua Security Trivy
* **Conteneurisation & CI/CD :** Docker (Multi-Stage + `/opt/venv`), Docker Compose, GitHub Actions, Render Cloud

---

## 🚀 Démarrage Rapide en Local

### 1. Cloner le dépôt
```bash
git clone [https://github.com/TON_PSEUDO_GITHUB/DevOps-Project-TaskMaster.git](https://github.com/TON_PSEUDO_GITHUB/DevOps-Project-TaskMaster.git)
cd DevOps-Project-TaskMaster
```

### 2. Lancer l'architecture 3-Tiers complète
```bash
docker compose up -d --build
```

### 3. Vérifier l'état des services et des Healthchecks
```bash
docker ps
```
* **Application Web (via Nginx) :** [http://localhost:8080](http://localhost:8080)
* **Endpoint de santé (Healthcheck) :** [http://localhost:8080/health](http://localhost:8080/health)

### 4. Exécuter les tests en local
```bash
docker compose exec web pytest
```

---

## 📂 Structure du Projet

```text
├── .github/workflows/
│   └── pipeline.yml         # Pipeline CI/CD (Matrix, Buildx Cache, Trivy, Deploy Gate)
├── app.py                   # Application Flask & routes API (/health, CRUD tâches)
├── test_app.py              # Suite de tests d'intégration Pytest
├── Dockerfile               # Multi-Stage Build (builder /opt/venv -> production alpine)
├── .dockerignore            # Exclusion des fichiers de test/config de l'image finale
├── docker-compose.yml       # Orchestration 3-Tiers (nginx + web + db) & Healthchecks
├── nginx.conf               # Configuration du Reverse Proxy Nginx -> http://web:5000
├── requirements.txt         # Dépendances de production (Flask, Psycopg2, Gunicorn)
└── requirements-dev.txt     # Dépendances de CI/Test (Pytest, Flake8)
```