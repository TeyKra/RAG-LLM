# RAG Tutorial v2

## Prérequis

- **Docker** : Assurez-vous que Docker et Docker Compose sont installés sur votre machine.
- **Accès local** : Les ports suivants doivent être disponibles :
  - Backend : `5002`
  - Frontend : `5003`

---

## Docker

### Construire les images Docker
Pour construire les images nécessaires :
```bash
docker compose build
```

### Démarrer les conteneurs
Pour lancer les conteneurs en mode détaché :
```bash
docker compose up -d
```

### Obtenir les IDs et noms des conteneurs
Pour lister les conteneurs en cours d'exécution :
```bash
docker ps
```

### Accéder à un conteneur
Pour entrer dans un conteneur via bash :
```bash
docker exec -it <container_id> /bin/bash
```
> Remplacez `<container_id>` par l'ID ou le nom du conteneur obtenu avec `docker ps`.

---

## Visualiser les logs de tous les containers en temps réel

```bash
docker-compose logs -f llm
```

---

## Requêtes API avec `curl`

L'API backend est accessible via le port `5002`. Voici les principales requêtes que vous pouvez effectuer :

### 1. **Populate Database**
Réinitialisez et remplissez la base de données :
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"reset": true}' \
     http://127.0.0.1:5002/api/populate
```

### 2. **Query Data**
Effectuez une requête sur les données :
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"query": "What is graph theoretical?"}' \
     http://127.0.0.1:5002/api/query
```

---

## Lancer l'application frontend

Une fois les conteneurs démarrés, accédez à l'application frontend via votre navigateur à l'adresse suivante :
[http://localhost:5003/](http://localhost:5003/)

---

## Terraform : 

### Initialisation
```bash
Terraform init
```

### Validation
```bash
Terraform validate
```

### Planification 
```bash 
Terraform plan
```

### Application

```bash
Terraform apply
```

### Destruction 

```bash
Terraform destroy
```

## Azure 
Se connecter à azure :
az login

update les credentials kub local :
az aks get-credentials --resource-group rg-rag-llm --name aks-rag-llm

vérifier la liste des services :
kubectl get svc

se connecter au frontend via ip publique:
http://52.xx.xx.xx:5003


## Ressources supplémentaires

- [Documentation officielle de Docker](https://docs.docker.com/)

