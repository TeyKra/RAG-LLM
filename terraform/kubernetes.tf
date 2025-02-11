# Configure the Kubernetes provider using the AKS cluster's kubeconfig.
provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
}

# Create a Kubernetes secret for Docker Hub credentials.
resource "kubernetes_secret" "dockerhub" {
  metadata {
    name      = "dockerhub-secret"   # Name of the secret.
    namespace = "default"            # Namespace where the secret will be created.
  }

  data = {
    ".dockerconfigjson" = jsonencode({
      auths = {
        "${var.dockerhub_server}" = {
          username = var.dockerhub_username
          password = var.dockerhub_password
          email    = var.dockerhub_email
          # Encode the "username:password" pair in Base64.
          auth     = base64encode("${var.dockerhub_username}:${var.dockerhub_password}")
        }
      }
    })
  }

  type = "kubernetes.io/dockerconfigjson"  # Specify the secret type for Docker credentials.
}

# -------------------------------
# Deployment of the LLM service
# -------------------------------
resource "kubernetes_deployment" "llm_service" {
  metadata {
    name = "llm"    # Name of the deployment.
    labels = {
      app = "llm"   # Label to identify pods belonging to the LLM service.
    }
  }

  spec {
    replicas = 1    # Number of pod replicas.

    selector {
      match_labels = {
        app = "llm"  # Selector to match pods with label "app: llm".
      }
    }

    template {
      metadata {
        labels = {
          app = "llm"  # Labels applied to the pod template.
        }
      }

      spec {
        # Reference the Docker Hub secret for pulling images.
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "llm"  # Name of the container.
          image = "mgn94/infrastructure-rag-llm:llm-service-latest"  # Container image.
          port {
            container_port = 5001  # Port exposed by the container.
          }
        }
      }
    }
  }
}

# Service to expose the LLM deployment internally within the cluster.
resource "kubernetes_service" "llm_service" {
  metadata {
    name = "llm"   # Name of the service.
  }

  spec {
    selector = {
      app = "llm"  # Select pods with label "app: llm".
    }

    port {
      port        = 5001  # Port on which the service is exposed.
      target_port = 5001  # Port on the pod to which traffic is forwarded.
    }

    type = "ClusterIP"  # Internal cluster IP service.
  }
}

# -------------------------------
# Deployment of the API service
# -------------------------------
resource "kubernetes_deployment" "api_service" {
  metadata {
    name = "api"   # Name of the deployment.
    labels = {
      app = "api"  # Label to identify pods belonging to the API service.
    }
  }

  spec {
    replicas = 1  # Number of pod replicas.

    selector {
      match_labels = {
        app = "api"  # Selector to match pods with label "app: api".
      }
    }

    template {
      metadata {
        labels = {
          app = "api"  # Labels applied to the pod template.
        }
      }

      spec {
        # Use the Docker Hub secret for image pulling.
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "api"  # Name of the container.
          image = "mgn94/infrastructure-rag-llm:api-service-latest"  # Container image.
          port {
            container_port = 5002  # Port exposed by the container.
          }
        }
      }
    }
  }
}

# Service to expose the API deployment internally.
resource "kubernetes_service" "api_service" {
  metadata {
    name = "api"  # Name of the service.
  }

  spec {
    selector = {
      app = "api"  # Select pods with label "app: api".
    }

    port {
      port        = 5002  # Port on which the service is exposed.
      target_port = 5002  # Port on the pod to which traffic is forwarded.
    }

    type = "ClusterIP"  # Internal cluster IP service.
  }
}

# -------------------------------
# Deployment of the Chroma service
# -------------------------------
resource "kubernetes_deployment" "chroma_service" {
  metadata {
    name = "chroma"   # Name of the deployment.
    labels = {
      app = "chroma"  # Label to identify pods belonging to the Chroma service.
    }
  }

  spec {
    replicas = 1  # Number of pod replicas.

    selector {
      match_labels = {
        app = "chroma"  # Selector to match pods with label "app: chroma".
      }
    }

    template {
      metadata {
        labels = {
          app = "chroma"  # Labels applied to the pod template.
        }
      }

      spec {
        # Use the Docker Hub secret for image pulling.
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "chroma"  # Name of the container.
          image = "mgn94/infrastructure-rag-llm:chroma-service-latest"  # Container image.
          port {
            container_port = 8000  # Port exposed by the container.
          }
        }
      }
    }
  }
}

# Service to expose the Chroma deployment internally.
resource "kubernetes_service" "chroma_service" {
  metadata {
    name = "chroma"  # Name of the service.
  }

  spec {
    selector = {
      app = "chroma"  # Select pods with label "app: chroma".
    }

    port {
      port        = 8000  # Port on which the service is exposed.
      target_port = 8000  # Port on the pod to which traffic is forwarded.
    }

    type = "ClusterIP"  # Internal cluster IP service.
  }
}

# -------------------------------
# Deployment of the Frontend service with an internal LoadBalancer
# -------------------------------
resource "kubernetes_deployment" "frontend_service" {
  metadata {
    name = "frontend"  # Name of the deployment.
    labels = {
      app = "frontend"  # Label to identify pods belonging to the Frontend service.
    }
  }

  spec {
    replicas = 1  # Number of pod replicas.

    selector {
      match_labels = {
        app = "frontend"  # Selector to match pods with label "app: frontend".
      }
    }

    template {
      metadata {
        labels = {
          app = "frontend"  # Labels applied to the pod template.
        }
      }

      spec {
        # Use the Docker Hub secret for image pulling.
        image_pull_secrets {
          name = kubernetes_secret.dockerhub.metadata[0].name
        }

        container {
          name  = "frontend"  # Name of the container.
          image = "mgn94/infrastructure-rag-llm:frontend-service-latest"  # Container image.
          port {
            container_port = 5003  # Port exposed by the container.
          }
        }
      }
    }
  }
}

# Service to expose the Frontend deployment externally using an internal LoadBalancer.
resource "kubernetes_service" "frontend_service" {
  metadata {
    name = "frontend"  # Name of the service.
    annotations = {
      # Annotation to designate an internal Azure Load Balancer.
      "service.beta.kubernetes.io/azure-load-balancer-internal"         = "true"
      # Specify the subnet within which the load balancer should be provisioned.
      "service.beta.kubernetes.io/azure-load-balancer-internal-subnet"     = "aks-subnet"
      # Specify the resource group where the AKS node resources reside.
      "service.beta.kubernetes.io/azure-load-balancer-resource-group"      = azurerm_kubernetes_cluster.aks.node_resource_group
    }
  }

  spec {
    selector = {
      app = "frontend"  # Select pods with label "app: frontend".
    }

    port {
      port        = 5003  # Port on which the service is exposed.
      target_port = 5003  # Port on the pod to which traffic is forwarded.
    }

    type             = "LoadBalancer"  # Expose the service using a LoadBalancer.
    load_balancer_ip = "10.0.1.100"      # Assign a static IP from the "aks-subnet" for the load balancer.
  }

  depends_on = [azurerm_kubernetes_cluster.aks]  # Ensure the AKS cluster is created before this service.
}
