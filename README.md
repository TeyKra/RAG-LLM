# Infrastructure RAG LLM

---
## Project Demonstration
Watch the demonstration on youtube : 
📹 **[Watch Video](https://youtu.be/J8PcfdjdevA)** 

---

## Table of Contents
- [Project Architecture](#project-architecture)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [1. Deployment using Docker](#1-deployment-using-docker)
  - [2. On-Premises Deployment](#2-on-premises-deployment)
    - [Prerequisites for On-Premises](#prerequisites-for-on-premises)
    - [Deployment Steps](#deployment-steps)
      - [Deploy with k8s (Kubernetes)](#deploy-with-k8s-kubernetes)
      - [Deployment with HELM](#deployment-with-helm)
      - [Destroying the Deployment](#destroying-the-deployment)
  - [3. Cloud Deployment](#3cloud-deployment)

---

## Project Architecture

```bash
📁 RAG-LLM-1        # Root directory of the project
├── 📂 .github      # GitHub Actions for CI/CD automation
│   └── 📂 workflows  
│       └── 📄 ci-cd.yml               # GitHub Actions workflow for CI/CD pipeline
├── 📂 charts       # HELM charts for Kubernetes deployment
│   └── 📂 rag-llm  
│       ├── 📂 charts  
│       │   ├── 📄 grafana-7.0.22.tgz  # Pre-packaged Grafana chart for monitoring
│       │   └── 📄 prometheus-15.0.4.tgz  # Pre-packaged Prometheus chart for monitoring
│       ├── 📂 templates               # Helm templates for Kubernetes resources
│       │   ├── 📄 api-deployment.yaml       # API container deployment definition
│       │   ├── 📄 api-service.yaml          # API service definition
│       │   ├── 📄 chroma-deployment.yaml    # ChromaDB container deployment definition
│       │   ├── 📄 chroma-service.yaml       # ChromaDB service definition
│       │   ├── 📄 frontend-deployment.yaml  # Frontend container deployment definition
│       │   ├── 📄 frontend-service.yaml     # Frontend service definition
│       │   ├── 📄 rag-llm-deployment.yaml   # RAG LLM container deployment definition
│       │   ├── 📄 rag-llm-service.yaml      # RAG LLM service definition
│       ├── 🔒 Chart.lock               # Lock file for Helm dependencies
│       ├── 📄 Chart.yaml               # Helm chart metadata
│       └── 📄 values.yaml              # Configuration values for Helm deployment
├── 📂 chroma       # Vectorial database (ChromaDB) files and configuration
├── 📂 data         # Directory storing datasets used by the model
├── 📂 frontend     # UI files for the frontend
│   ├── 📄 index.html   # Main HTML page
│   ├── 📄 scripts.js   # JavaScript logic for the frontend
│   └── 📄 styles.css   # Styles for the UI
├── 📂 k8s          # Kubernetes deployment configuration files
│   ├── 📄 api-deployment.yaml          # API deployment manifest
│   ├── 📄 api-service.yaml             # API service manifest
│   ├── 📄 chroma-deployment.yaml       # ChromaDB deployment manifest
│   ├── 📄 chroma-service.yaml          # ChromaDB service manifest
│   ├── 📄 frontend-deployment.yaml     # Frontend deployment manifest
│   ├── 📄 frontend-service.yaml        # Frontend service manifest
│   ├── 📄 rag_llm-deployment.yaml      # RAG LLM deployment manifest
│   └── 📄 rag_llm-service.yaml         # RAG LLM service manifest
├── 📂 src          # Source code for the RAG LLM project
│   ├── 📂 __pycache__             # Compiled Python cache files
│   ├── 📄 __init__.py             # Module initialization file
│   ├── 📄 api.py                  # API implementation for handling requests and endpoints
│   ├── 📄 frontend.py             # Frontend service logic
│   ├── 📄 get_embedding.py        # Script for generating vector embeddings
│   ├── 📄 populate_database.py    # Script to populate the ChromaDB vectorial database
│   ├── 📄 query_data.py           # Script to perform queries on the RAG LLM
│   └── 📄 rag_llm_services.py     # Microservice communication logic for the RAG LLM
├── 📂 terraform    # Infrastructure as Code (IaC) using Terraform for cloud deployment
│   ├── 📄 app_gateway.tf       # Deploys an Azure Application Gateway for private frontend access
│   ├── 📄 jumpbox.tf           # Jumpbox VM for administrative tasks
│   ├── 📄 kubernetes.tf        # Deploys AKS (Azure Kubernetes Service) clusters
│   ├── 📄 main.tf              # Main Terraform script including bastion host for network security
│   ├── 📄 outputs.tf           # Defines Terraform outputs for infrastructure information
│   ├── 📄 variables.tf         # Defines Terraform variables
│   └── 📄 terraform.tfvars     # Contains DockerHub credentials and Azure Subscription ID (ignored by .gitignore)
├── 📄 .dockerignore  # Specifies files/folders to exclude from Docker builds
├── 📄 .gitignore     # Specifies files/folders to exclude from Git repository
├── 📄 docker-compose.yml   # Docker Compose configuration for multi-container setup
├── 📄 dockerfile.api       # Dockerfile for building the API container
├── 📄 dockerfile.chroma    # Dockerfile for building the ChromaDB container
├── 📄 dockerfile.frontend  # Dockerfile for building the frontend container
├── 📄 dockerfile.rag_llm   # Dockerfile for building the RAG LLM container
├── 📄 README.md            # Project documentation
└── 📄 requirements.txt     # Python dependencies required for the project
```

---

## Prerequisites

Ensure you have the following installed before running this project:

- **Python 3.10 / 3.11 / 3.12**: [Installation guide](https://www.python.org/downloads/)
- **Docker and Docker Desktop**: [Installation guide](https://www.docker.com/products/docker-desktop/)
- **Kubernetes**: [Installation guide](https://kubernetes.io/docs/setup/)
- **Kubectl** : [Installation guide](https://kubernetes.io/docs/tasks/tools/)
- **Minikube**: [Installation guide](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download)
- **Helm**: [Installation guide](https://helm.sh/docs/helm/helm_install/)
- **Terraform**: [Installation guide](https://developer.hashicorp.com/terraform/install)
- **Azure CLI**: [Installation guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli/)
- **Git**: [Installation guide](https://git-scm.com/downloads)

Make sure you have an account:
- **GitHub**: [Usage guide](https://github.com/)
- **DockerHub**: [Usage guide](https://hub.docker.com/)

---

## Usage

This project allows you to deploy your **RAG LLM container services** in different environments.

---

### 1. Deployment using Docker

You can deploy the project using **Docker & Docker Desktop** only.  
**Don't forget to adapt the code (dockerfile, docker-compose) to your own settings.**

#### Steps:

1. Ensure **Python, Docker, and Docker Desktop** are installed on your machine.  
2. Open the project directory and start **Docker Desktop**.  
3. Open a terminal and run the following commands to build and start the containers:

   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```

4. Wait until the container is deployed and ready to use. You can verify its status with:

   ```bash
   docker ps
   ```

5. Open a second terminal and check the logs of the LLM container:

   ```bash
   docker-compose logs -f llm
   ```

6. You can now start using the solution:

   - **Using CURL**:
     - **Reset and populate the database**:
       ```bash
       curl -X POST -H "Content-Type: application/json" \
            -d '{"reset": true}' \
            http://127.0.0.1:5002/api/populate
       ```
     - **Make a query on the dataset**:
       ```bash
       curl -X POST -H "Content-Type: application/json" \
            -d '{"query": "What is graph theoretical?"}' \
            http://127.0.0.1:5002/api/query
       ```

   - **Access the frontend**: [http://localhost:5003/](http://localhost:5003/)

7. If you need to enter any container, you can use:  
   ```bash
   docker exec -it <container_id> /bin/bash
   ```

---

### 2. On-Premises Deployment

You can deploy the project using **GitHub, Docker, DockerHub, Kubernetes, and HELM**.  
**Don't forget to adapt the code (dockerfile, docker-compose, k8s yaml scripts, charts/rag-llm/templates scripts, .github/workflows/ci-cd.yml) to your own settings.**

#### Prerequisites for On-Premises

Before starting, ensure you have:

- A **GitHub account** with a repository ready for use.
- A **DockerHub account** with a repository ready for use.
- The following dependencies installed:
  - `python`
  - `kubernetes`
  - `kubectl`
  - `minikube`
  - `docker`
  - `helm`
  - `git`


#### Deployment Steps

##### Deploy with k8s (Kubernetes)

1. **Configure Your GitHub Repository**  
   1. Navigate to the `.github/workflows` folder.  
   2. Modify the configuration files with your own settings.  
   3. Push the updated configuration to your GitHub repository.

2. **Build and Push the Docker Image**  
   1. Once the new configuration is pushed, GitHub Actions will trigger the CI/CD pipeline.  
   2. Wait for the pipeline to complete (it will build and push the container to DockerHub).

3. **Start Minikube and Set Up Kubernetes**  
   1. Open a terminal and start Minikube:
      ```bash
      minikube start
      ```
   2. Log in to your Docker account:
      ```bash
      docker login
      ```
   3. Create a Kubernetes registry secret:
      ```bash
      kubectl create secret generic my-registry-secret \
          --from-file=.dockerconfigjson=$HOME/.docker/config.json \
          --type=kubernetes.io/dockerconfigjson
      ```
   4. Apply the Kubernetes deployment configuration:
      ```bash
      kubectl apply -f k8s
      ```
   5. Check the status of the Kubernetes pods:
      ```bash
      kubectl get pods
      ```
   6. Access the frontend service:
      ```bash
      minikube service frontend
      ```

##### Deployment with HELM

You can also deploy this solution using **Helm** instead of **k8s** :

1. **Configure Your GitHub Repository**  
   1. Navigate to the `.github/workflows` folder.  
   2. Modify the configuration files with your own settings.  
   3. Push the updated configuration to your GitHub repository.

2. **Build and Push the Docker Image**  
   1. Once the new configuration is pushed, GitHub Actions will trigger the CI/CD pipeline.  
   2. Wait for the pipeline to complete (it will build and push the container to DockerHub).

3. Navigate to the `rag-llm` Helm chart folder:
   ```bash
   cd charts/rag-llm
   ```
4. Deploy the container:
   ```bash
   helm install rag-llm .
   ```
5. Check the status of the Kubernetes pods:
   ```bash
   kubectl get pods
   ```
6. Access the frontend service:
   ```bash
   minikube service frontend
   ```
7. Add **Prometheus** and **Grafana** for monitoring:
   ```bash
   kubectl port-forward service/rag-llm-grafana 3000:80
   kubectl port-forward service/rag-llm-prometheus-server 9090:80
   ```
   - Open Grafana at: [http://localhost:3000/login](http://localhost:3000/login)  
   - Open Prometheus at: [http://localhost:9090](http://localhost:9090)

##### Destroying the Deployment

If you want to remove all deployments, use:

```bash
kubectl delete --all all
minikube delete
```

---

### 3. Cloud Deployment

You can deploy the project on the **Azure Cloud** using **GitHub, Docker, DockerHub, Terraform and Azure**.  
**Don't forget to adapt the code to your own settings.**

#### Prerequisites for On-Premises

Before starting, ensure you have:

- A **GitHub account** with a repository ready for use.
- A **DockerHub account** with a repository ready for use.
- The following dependencies installed:
  - `python`
  - `terraform`
  - `azure`
  - `docker`
  - `git`

1. **Configure Your GitHub Repository**  
   1. Navigate to the `.github/workflows` folder.  
   2. Modify the configuration files with your own settings.  
   3. Push the updated configuration to your GitHub repository.

2. **Build and Push the Docker Image**  
   1. Once the new configuration is pushed, GitHub Actions will trigger the CI/CD pipeline.  
   2. Wait for the pipeline to complete (it will build and push the container to DockerHub).

3. **Create and Configure `terraform.tfvars`**  
   1. Open a terminal, go to the `terraform` folder.  
   2. Create a `terraform.tfvars` file and add your credentials:
      ```bash
      dockerhub_username = ""
      dockerhub_password = ""
      dockerhub_email    = ""
      subscription_id    = ""
      ```
4. **Adapt the `kubernetes.tf` script with your own DockerHub images path information.**

5. **Initialize Terraform**  
   ```bash
   terraform init
   ```

6. **Check the Deployment Plan**  
   ```bash
   terraform plan
   ```
   - Ensure there are no errors.

7. **Deploy Your Solution**  
   ```bash
   terraform apply
   ```
   - Confirm when prompted.

8. **Wait for Deployment to Complete**  
   - Ensure Terraform finishes deploying all resources.

8. **Access the Frontend Services**  
   1. In the Azure Portal, navigate to the resource group **`rg_rg_llm`**.  
   2. Locate the **`app_gateway`** resource and find its **public IP**.  
   3. Copy the public IP and paste it into your web browser to access the frontend services.
