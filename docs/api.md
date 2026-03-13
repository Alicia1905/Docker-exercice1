**Documentation des API**
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/users` | Lister tous les utilisateurs |
| GET | `/users/{id}` | Détail d'un utilisateur |
| POST | `/users` | Créer un utilisateur |
| PUT | `/users/{id}` | Modifier un utilisateur |
| DELETE | `/users/{id}` | Supprimer un utilisateur |
| POST | `/users/login` | Authentification simple |
| GET | `/health` | Healthcheck |


| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/products` | Lister tous les produits |
| GET | `/products/{id}` | Détail d'un produit |
| POST | `/products` | Créer un produit |
| PUT | `/products/{id}` | Modifier un produit |
| DELETE | `/products/{id}` | Supprimer un produit |
| GET | `/health` | Healthcheck |

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/orders` | Lister toutes les commandes |
| GET | `/orders/{id}` | Détail d'une commande |
| POST | `/orders` | Créer une commande |
| GET | `/orders/user/{user_id}` | Commandes d'un utilisateur |
| GET | `/health` | Healthcheck |