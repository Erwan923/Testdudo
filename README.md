# Testdudo 🛡️

Outil d'audit automatisé de sécurité basé sur la stratégie de la tortue romaine

## À propos

Testdudo est un outil d'audit de sécurité qui utilise une approche méthodique inspirée de la formation en tortue des légions romaines. L'outil progresse de manière sécurisée, consolidant chaque position avant d'avancer.

## Fonctionnalités

- 🔍 Reconnaissance automatisée (OSINT)
- 🌐 Analyse réseau progressive
- 🔒 Tests de sécurité web
- 🤖 Analyse par IA des résultats
- 🐳 Architecture conteneurisée (Docker + Kubernetes)

## Architecture

```
Testdudo/
├── src/                     # Code source principal
│   ├── core/               # Modules principaux
│   ├── modules/            # Modules spécialisés 
│   └── utils/              # Utilitaires
├── kubernetes/             # Configuration Kubernetes
├── docker/                 # Dockerfiles
├── cheatsheets/           # Fiches techniques markdown
└── config/                # Configuration
```

## Installation

### Option 1 : Installation locale
```bash
# Cloner le dépôt
git clone https://github.com/Erwan923/Testdudo.git
cd Testdudo

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'outil
python testdudo.py setup
```

### Option 2 : Déploiement Kubernetes
```bash
# Appliquer la configuration Kubernetes
kubectl apply -f kubernetes/

# Vérifier le déploiement
kubectl get pods -l app=testdudo
```

## Utilisation

```bash
# Lancer un audit complet
python testdudo.py attack --target example.com

# Mode spécifique
python testdudo.py attack --target example.com --mode recon

# Sans l'analyse IA
python testdudo.py attack --target example.com --no-ai
```

## Structure des Pods

1. **Coordinateur** : Orchestration des attaques
2. **OSINT** : Reconnaissance et collecte d'informations
3. **Network** : Tests réseau
4. **WebApp** : Tests d'applications web

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer des améliorations
- Soumettre une pull request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.