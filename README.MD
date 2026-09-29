Installation
Prérequis
Docker
Docker Compose
Python 3
pip

## 1. Installer les dépendances Python

Créer éventuellement un environnement virtuel :

python -m venv .venv

Activer l'environnement :

Linux / WSL :

source .venv/bin/activate

Puis installer les dépendances :

pip install -r requirements.txt
2. Démarrer MySQL
docker compose up -d

Vérifier que le conteneur fonctionne :

docker compose ps

3. Créer les tables
docker compose exec -T database mysql \
  -uuser_dteng \
  -pcirilgroupt \
  db_dteng < schema.sql

4. Exécuter le programme
python example.py

Le fichier suivant est alors généré :

data/output.json
Reproductibilité

Le programme peut être exécuté plusieurs fois.

À chaque nouvelle exécution, les données précédemment importées sont supprimées avant le nouvel import afin d'éviter les doublons et de garantir un état cohérent de la base.

Pour repartir complètement d'une nouvelle instance MySQL :

docker compose down -v
docker compose up -d

Puis recréer les tables avec schema.sql.

Résultat

L'import réalisé avec les données fournies produit actuellement :

114 places
10000 personnes
0 personne avec une valeur obligatoire manquante
0 personne avec une date invalide
