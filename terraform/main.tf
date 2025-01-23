#####################################
# Provider AzureRM
#####################################
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.57"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }

  required_version = ">= 1.3.0"
}

provider "azurerm" {
  features {}
  # Vous pouvez aussi utiliser l'authentification via Azure CLI ou un service principal
  # tenant_id       = "xxx"
  # client_id       = "xxx"
  # client_secret   = "xxx"
  # subscription_id = var.subscription_id
}

#####################################
# Création du Resource Group
#####################################
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

#####################################
# Création du cluster AKS
#####################################
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_cluster_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.aks_cluster_name}-dns"

  default_node_pool {
    name       = "default"
    node_count = var.default_node_count
    vm_size    = var.default_node_vm_size
  }

  identity {
    type = "SystemAssigned"
  }
}

#####################################
# Récupération des credentials du cluster
#####################################
data "azurerm_kubernetes_cluster" "cluster" {
  name                = azurerm_kubernetes_cluster.aks.name
  resource_group_name = azurerm_resource_group.rg.name
}

#####################################
# Configuration du provider Kubernetes
#####################################
provider "kubernetes" {
  host                   = data.azurerm_kubernetes_cluster.cluster.kube_config.0.host
  client_certificate     = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate)
  client_key             = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate)
}

#####################################
# Création d'un Namespace
#####################################
resource "kubernetes_namespace" "rag_llm_namespace" {
  metadata {
    name = "rag-llm-namespace"
  }
}

################################################################################
# Déploiement du service 'chroma'
################################################################################
resource "kubernetes_deployment" "chroma" {
  metadata {
    name      = "chroma"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name

    labels = {
      app = "chroma"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "chroma"
      }
    }
    template {
      metadata {
        labels = {
          app = "chroma"
        }
      }
      spec {
        container {
          name  = "chroma-container"
          image = "mgn94/infrastructure-rag-llm:chroma-service-latest"

          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "chroma" {
  metadata {
    name      = "chroma-svc"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name
  }

  spec {
    type = "ClusterIP"
    selector = {
      app = "chroma"
    }
    port {
      name        = "http"
      port        = 8000
      target_port = 8000
    }
  }
}

################################################################################
# Déploiement du service 'llm' (rag_llm_services.py)
################################################################################
resource "kubernetes_deployment" "rag_llm" {
  metadata {
    name      = "rag-llm"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name

    labels = {
      app = "rag-llm"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "rag-llm"
      }
    }
    template {
      metadata {
        labels = {
          app = "rag-llm"
        }
      }
      spec {
        container {
          name  = "rag-llm-container"
          image = "mgn94/infrastructure-rag-llm:llm-service-latest"

          port {
            container_port = 5001
          }
          # Si vous avez besoin de variables d'environnement
          # env {
          #   name  = "PYTHONPATH"
          #   value = "/app"
          # }
        }
      }
    }
  }
}

resource "kubernetes_service" "rag_llm_svc" {
  metadata {
    name      = "rag-llm-svc"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name
  }

  spec {
    type = "ClusterIP"
    selector = {
      app = "rag-llm"
    }
    port {
      name        = "http"
      port        = 5001
      target_port = 5001
    }
  }
}

################################################################################
# Déploiement du service 'api' (api.py)
################################################################################
resource "kubernetes_deployment" "api" {
  metadata {
    name      = "rag-llm-api"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name

    labels = {
      app = "rag-llm-api"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "rag-llm-api"
      }
    }
    template {
      metadata {
        labels = {
          app = "rag-llm-api"
        }
      }
      spec {
        container {
          name  = "rag-llm-api-container"
          image = "mgn94/infrastructure-rag-llm:api-service-latest"

          port {
            container_port = 5002
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_svc" {
  metadata {
    name      = "rag-llm-api-svc"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name
  }

  spec {
    type = "ClusterIP"
    selector = {
      app = "rag-llm-api"
    }
    port {
      name        = "http"
      port        = 5002
      target_port = 5002
    }
  }
}

################################################################################
# Déploiement du service 'frontend' (frontend.py)
################################################################################
resource "kubernetes_deployment" "frontend" {
  metadata {
    name      = "rag-llm-frontend"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name

    labels = {
      app = "rag-llm-frontend"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "rag-llm-frontend"
      }
    }
    template {
      metadata {
        labels = {
          app = "rag-llm-frontend"
        }
      }
      spec {
        container {
          name  = "rag-llm-frontend-container"
          image = "mgn94/infrastructure-rag-llm:frontend-service-latest"

          port {
            container_port = 5003
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "frontend_svc" {
  metadata {
    name      = "rag-llm-frontend-svc"
    namespace = kubernetes_namespace.rag_llm_namespace.metadata[0].name
  }

  spec {
    type = "LoadBalancer" # Pour l'exposer publiquement
    selector = {
      app = "rag-llm-frontend"
    }
    port {
      name        = "http"
      port        = 80       # Port public d'accès
      target_port = 5003     # Port dans le conteneur
    }
  }
}
