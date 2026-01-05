# Bookstore API - Deployment Guide

Flask REST API for BOOKSTORE database on Azure Cosmos DB (MongoDB API) deployed on Azure Kubernetes Service (AKS).

## Prerequisites

- Azure account with active subscription
- Azure CLI, Docker, kubectl installed
- Python 3.11+

## Step 1: Create Azure Cosmos DB

```bash
RESOURCE_GROUP="rg-bookstore-aks"
COSMOS_ACCOUNT="bookstore-cosmos-$(date +%s | cut -c1-10)"
LOCATION="centralus"

az group create --name $RESOURCE_GROUP --location $LOCATION

az cosmosdb create \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --kind MongoDB \
  --default-consistency-level Session \
  --locations regionName=$LOCATION failoverPriority=0 isZoneRedundant=False

az cosmosdb keys list \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --type connection-strings \
  --query "connectionStrings[0].connectionString" -o tsv
```

**Azure Portal:** Create database `BOOKSTORE` and collection `books` (400 RU/s minimum).

## Step 2: Local Testing

```bash
cd app
cp .env.example .env

pip install -r requirements.txt

cd ../scripts
python seed.py

cd ../app
python app.py

cd ../scripts
python crud_test.py
```

## Step 3: Docker Build

```bash
cd app
docker build -t bookstore-api:latest .
```

## Step 4: Azure Container Registry (ACR)

```bash
ACR_NAME="bookstoreacr$(date +%s | cut -c1-8)"
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true \
  --location $LOCATION

az acr login --name $ACR_NAME

ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
docker tag bookstore-api:latest $ACR_LOGIN_SERVER/bookstore-api:latest
docker push $ACR_LOGIN_SERVER/bookstore-api:latest
```

**Note:** Build for amd64 platform: `docker buildx build --platform linux/amd64 -t $ACR_LOGIN_SERVER/bookstore-api:latest --push .`

## Step 5: Create AKS Cluster

```bash
AKS_NAME="bookstore-aks"
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $AKS_NAME \
  --node-count 2 \
  --attach-acr $ACR_NAME \
  --location $LOCATION \
  --node-vm-size Standard_D2s_v3 \
  --generate-ssh-keys

az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_NAME
kubectl get nodes
```

## Step 6: Deploy MongoDB on AKS

```bash
kubectl apply -f k8s/mongo/namespace.yaml
kubectl apply -f k8s/mongo/secret.yaml
kubectl apply -f k8s/mongo/pvc.yaml
kubectl apply -f k8s/mongo/statefulset.yaml
kubectl apply -f k8s/mongo/service.yaml

kubectl wait --for=condition=ready pod -l app=mongo -n bookstore --timeout=300s
```

## Step 7: Deploy Flask API on AKS

```bash
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
sed -i.bak "s|<ACR_IMAGE_PLACEHOLDER>|$ACR_LOGIN_SERVER/bookstore-api:latest|g" k8s/api/deployment.yaml

# Deploy
kubectl apply -f k8s/api/configmap.yaml
kubectl apply -f k8s/api/secret.yaml
kubectl apply -f k8s/api/deployment.yaml
kubectl apply -f k8s/api/service.yaml
```

## Step 8: Apply NetworkPolicy

```bash
kubectl apply -f k8s/network/networkpolicy.yaml
```

## Step 9: Testing

```bash
EXTERNAL_IP=$(kubectl get svc bookstore-api-service -n bookstore -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

curl http://$EXTERNAL_IP/health
curl http://$EXTERNAL_IP/books

curl -X POST http://$EXTERNAL_IP/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","author":"Author","isbn":"123","price":29.99}'
```

## API Endpoints

- `GET /health` - Health check
- `POST /books` - Create book
- `GET /books` - List all books
- `GET /books/<id>` - Get book by ID
- `PUT /books/<id>` - Update book
- `DELETE /books/<id>` - Delete book

## Environment Variables

- `MONGO_URI` - MongoDB connection string (preferred)
- `MONGO_HOST`, `MONGO_PORT`, `MONGO_USER`, `MONGO_PASS` - Individual components (fallback)
- `MONGO_DB` - Database name (default: BOOKSTORE)
- `MONGO_COLLECTION` - Collection name (default: books)

## Logging

```bash
kubectl logs -l app=bookstore-api -n bookstore
kubectl logs -l app=mongo -n bookstore
```

## Cleanup

```bash
az aks delete --resource-group $RESOURCE_GROUP --name $AKS_NAME --yes
az cosmosdb delete --name $COSMOS_ACCOUNT --resource-group $RESOURCE_GROUP --yes
az acr delete --name $ACR_NAME --resource-group $RESOURCE_GROUP --yes
az group delete --name $RESOURCE_GROUP --yes
```
