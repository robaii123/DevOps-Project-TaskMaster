# 🚀 TaskMaster Pro — Architecture Full-Stack & Pipeline DevSecOps

![CI/CD Pipeline](https://github.com/robaii123/DevOps-Project-TaskMaster/actions/workflows/pipeline.yml/badge.svg)
![Docker](https://img.shields.io/badge/Docker-Non--Root%20%2B%20Healthcheck-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16--Alpine-336791?logo=postgresql&logoColor=white)
![Security](https://img.shields.io/badge/DevSecOps-Trivy%20%2B%20Flake8-27ae60?logo=aquasecurity&logoColor=white)

Application web de gestion de tâches (**Flask + PostgreSQL**) entièrement conteneurisée et déployée automatiquement sur le Cloud (**Render**) via un pipeline **CI/CD/DevSecOps** sous **GitHub Actions**.

---

## 🏗️ Architecture & Points Forts DevOps

Ce projet met en œuvre les bonnes pratiques d'ingénierie DevOps et de sécurité en entreprise :

### 1. Conteneurisation Sécurisée & Orchestration Locale (`Docker` & `Docker Compose`)
* **Sécurité Non-Root (`USER appuser`) :** Le conteneur applicatif exécute Python sous un utilisateur restreint sans privilèges `root` pour limiter la surface d'attaque.
* **Monitoring Intégré (`HEALTHCHECK`) :** Le `Dockerfile` et le `docker-compose.yml` surveillent l'état de santé réel de l'application (`/health`) et de PostgreSQL (`pg_isready`).
* **Démarrage Ordonné (`condition: service_healthy`) :** Le conteneur web attend que le moteur PostgreSQL soit totalement prêt à accepter des connexions avant de démarrer.
* **Persistance des Données :** Utilisation d'un volume Docker dédié (`pgdata`) pour conserver les données SQL.

### 2. Pipeline CI/CD & DevSecOps (`GitHub Actions`)
Le workflow `.github/workflows/pipeline.yml` s'adapte automatiquement à la branche utilisée (`dev` vs `main`) :

| Job | Déclencheur | Actions réalisées |
| :--- | :--- | :--- |
| **1. `quality-test`** | `push` (`dev`, `main`) & `pull_request` (`main`) | • Démarrage d'un **Service Container PostgreSQL** éphémère.<br>• Analyse statique du code Python (**Linter `flake8`**).<br>• Exécution des tests unitaires et d'intégration SQL (**`pytest`**). |
| **2. `build-scan-push`** | `push` sur `main` uniquement (`if:`) | • Build de l'image Docker.<br>• **Double Tagging** (`:latest` + `:${{ github.sha }}` pour la traçabilité et le rollback).<br>• **Scan de vulnérabilités `Trivy`** (`CRITICAL`, `HIGH`) avant publication.<br>• Push sécurisé vers **Docker Hub**. |
| **3. `deploy`** | Après succès du Job 2 sur `main` | • Déclenchement automatique du déploiement Cloud sur **Render** via Webhook sécurisé (`RENDER_DEPLOY_HOOK`). |

---

## 🛠️ Stack Technique

* **Backend & UI :** Python 3.12, Flask, Jinja2 (HTML5/CSS3)
* **Base de données :** PostgreSQL 16 (`psycopg2-binary`)
* **Qualité & Sécurité :** Pytest, Flake8, Aqua Security Trivy
* **Conteneurisation :** Docker, Docker Compose
* **CI/CD & Cloud :** GitHub Actions, Docker Hub, Render (Web Service + Managed PostgreSQL)

---

## 💻 Installation et Lancement en Local

### Prérequis
* **Docker** et **Docker Compose** installés.

### 1. Cloner le projet
```bash
git clone https://github.com/robaii123/DevOps-Project-TaskMaster.git
cd DevOps-Project-TaskMaster
```

### 2. Démarrer la stack complète (Web + PostgreSQL)
```bash
docker compose up -d --build
```

### 3. Vérifier l'état des conteneurs (`healthy`) et la sécurité (`appuser`)
```bash
docker ps
docker compose exec web whoami
```

* 🌐 **Interface Web :** [http://localhost:8080](http://localhost:8080)
* 🩺 **Endpoint de Monitoring (Healthcheck) :** [http://localhost:8080/health](http://localhost:8080/health)

### 4. Arrêter l'environnement local
```bash
docker compose down
```

---

## 🌿 Workflow Git (Branches `dev` & `main`)

1. Développement des nouvelles fonctionnalités sur la branche `dev` :
   ```bash
   git checkout dev
   git add .
   git commit -m "Feat: nouvelle fonctionnalité"
   git push origin dev
   ```
   *(Lance uniquement le job `quality-test` sur GitHub Actions).*

2. Ouverture d'une **Pull Request** de `dev` vers `main` sur GitHub, puis **Merge** après validation des tests :
   *(Déclenche automatiquement `quality-test` ➔ `build-scan-push` ➔ `deploy` en production).*

---

## 🔐 Secrets GitHub Actions Requis

Pour reproduire ce pipeline dans un fork, configurez les secrets suivants dans `Settings > Secrets and variables > Actions` :

* `DOCKER_USERNAME` : Identifiant Docker Hub
* `DOCKER_PASSWORD` : Token d'accès Docker Hub (Read/Write)
* `RENDER_DEPLOY_HOOK` : URL du Webhook de déploiement Render