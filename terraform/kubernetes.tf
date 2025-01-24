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
    # On met directement la sortie de `jsonencode` (sans base64encode)
    ".dockerconfigjson" = jsonencode({
      auths = {
        # vous pouvez laisser var.dockerhub_server comme clé
        # ou la mettre en dur "https://index.docker.io/v1/" si vous préférez
        "${var.dockerhub_server}" = {
          username = var.dockerhub_username
          password = var.dockerhub_password
          email    = var.dockerhub_email
          # Ici on peut garder base64encode pour le champ "auth" lui-même 
          auth     = base64encode("${var.dockerhub_username}:${var.dockerhub_password}")
        }
      }
    })
  }

  type = "kubernetes.io/dockerconfigjson"
}


resource "kubernetes_deployment" "llm_service" {
  metadata {
    name = "llm-service"
    labels = {
      app = "llm-service"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "llm-service"
      }
    }

    template {
      metadata {
        labels = {
          app = "llm-service"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "llm-service"
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
    name = "llm-service"
  }

  spec {
    selector = {
      app = "llm-service"
    }

    port {
      port        = 5001
      target_port = 5001
    }

    type = "ClusterIP"
  }
}

# Répétez les ressources de déploiement et de service pour les autres services (api, frontend, chroma)

# Exemple pour le service API
resource "kubernetes_deployment" "api_service" {
  metadata {
    name = "api-service"
    labels = {
      app = "api-service"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "api-service"
      }
    }

    template {
      metadata {
        labels = {
          app = "api-service"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "api-service"
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
    name = "api-service"
  }

  spec {
    selector = {
      app = "api-service"
    }

    port {
      port        = 5002
      target_port = 5002
    }

    type = "ClusterIP"
  }
}

# Exemple pour le service Chroma
resource "kubernetes_deployment" "chroma_service" {
  metadata {
    name = "chroma-service"
    labels = {
      app = "chroma-service"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "chroma-service"
      }
    }

    template {
      metadata {
        labels = {
          app = "chroma-service"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "chroma-service"
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
    name = "chroma-service"
  }

  spec {
    selector = {
      app = "chroma-service"
    }

    port {
      port        = 8000
      target_port = 8000
    }

    type = "ClusterIP"
  }
}

# Déploiement du Frontend avec LoadBalancer
resource "kubernetes_deployment" "frontend_service" {
  metadata {
    name = "frontend-service"
    labels = {
      app = "frontend-service"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "frontend-service"
      }
    }

    template {
      metadata {
        labels = {
          app = "frontend-service"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "frontend-service"
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
    name = "frontend-service"
  }

  spec {
    selector = {
      app = "frontend-service"
    }

    port {
      port        = 5003
      target_port = 5003
    }

    type = "LoadBalancer"
  }
}
