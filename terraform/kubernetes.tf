provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
}

resource "kubernetes_secret" "dockerhub" {
  metadata {
    name      = "dockerhub-secret"
    namespace = "default"
  }

  data = {
    ".dockerconfigjson" = jsonencode({
      auths = {
        "${var.dockerhub_server}" = {
          username = var.dockerhub_username
          password = var.dockerhub_password
          email    = var.dockerhub_email
          auth     = base64encode("${var.dockerhub_username}:${var.dockerhub_password}")
        }
      }
    })
  }

  type = "kubernetes.io/dockerconfigjson"
}

# Déploiement du service LLM
resource "kubernetes_deployment" "llm_service" {
  metadata {
    name = "llm"
    labels = {
      app = "llm"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "llm"
      }
    }

    template {
      metadata {
        labels = {
          app = "llm"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "llm"
          image = "mgn94/infrastructure-rag-llm:llm-service-latest"
          port {
            container_port = 5001
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "llm_service" {
  metadata {
    name = "llm"
  }

  spec {
    selector = {
      app = "llm"
    }

    port {
      port        = 5001
      target_port = 5001
    }

    type = "ClusterIP"
  }
}

# Déploiement du service API
resource "kubernetes_deployment" "api_service" {
  metadata {
    name = "api"
    labels = {
      app = "api"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "api"
      }
    }

    template {
      metadata {
        labels = {
          app = "api"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "api"
          image = "mgn94/infrastructure-rag-llm:api-service-latest"
          port {
            container_port = 5002
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_service" {
  metadata {
    name = "api"
  }

  spec {
    selector = {
      app = "api"
    }

    port {
      port        = 5002
      target_port = 5002
    }

    type = "ClusterIP"
  }
}

# Déploiement du service Chroma
resource "kubernetes_deployment" "chroma_service" {
  metadata {
    name = "chroma"
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
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "chroma"
          image = "mgn94/infrastructure-rag-llm:chroma-service-latest"
          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "chroma_service" {
  metadata {
    name = "chroma"
  }

  spec {
    selector = {
      app = "chroma"
    }

    port {
      port        = 8000
      target_port = 8000
    }

    type = "ClusterIP"
  }
}

# Déploiement du Frontend avec LoadBalancer interne (IP statique)
resource "kubernetes_deployment" "frontend_service" {
  metadata {
    name = "frontend"
    labels = {
      app = "frontend"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "frontend"
      }
    }

    template {
      metadata {
        labels = {
          app = "frontend"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "frontend"
          image = "mgn94/infrastructure-rag-llm:frontend-service-latest"
          port {
            container_port = 5003
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "frontend_service" {
  metadata {
    name = "frontend"
    annotations = {
      "service.beta.kubernetes.io/azure-load-balancer-internal"         = "true"
      "service.beta.kubernetes.io/azure-load-balancer-internal-subnet"     = "aks-subnet"
      "service.beta.kubernetes.io/azure-load-balancer-resource-group"      = azurerm_kubernetes_cluster.aks.node_resource_group
    }
  }

  spec {
    selector = {
      app = "frontend"
    }

    port {
      port        = 5003
      target_port = 5003
    }

    type             = "LoadBalancer"
    load_balancer_ip = "10.0.1.100"  # IP statique dans le subnet "aks-subnet"
  }

  depends_on = [azurerm_kubernetes_cluster.aks]
}
