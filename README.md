# Gestion de la santé avec un chatbot IA

Ce projet est une application web développée en Python avec **FastAPI**, intégrant un **chatbot intelligent** pour le suivi de l'IMC (Indice de Masse Corporelle). Il a été réalisé dans le cadre d’un mini-projet universitaire (Licence MIASI – 2024).

---

## Fonctionnalités

- Création de compte utilisateur (nom, âge, taille, poids, etc.)
- Connexion sécurisée avec gestion des sessions via cookies
- Calcul dynamique de l'IMC
- Chatbot intégré utilisant **Google Gemini API** pour fournir :
  - Des recommandations personnalisées sur la santé
  - Des réponses aux questions des utilisateurs
- Interface utilisateur fluide et réactive (HTML/CSS/JS)

---

## Stack technique

- **Backend** : Python, FastAPI
- **Base de données** : SQLite
- **Frontend** : HTML, CSS, JavaScript
- **IA** : API Gemini (Google Generative AI)

---

## Structure du projet
project/ 
│ ├── main.py # Backend FastAPI 
  ├── users.db # Base de données SQLite 
  ├──templates/ # Pages HTML (signup, login, home) 
  ├── static/ # Fichiers CSS et images 
  └──README.md # Ce fichier

