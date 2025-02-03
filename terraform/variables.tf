variable "subscription_id" {
  description = "L'ID de l'abonnement Azure"
  type        = string
}

variable "resource_group_name" {
  description = "Nom du groupe de ressources"
  type        = string
  default     = "rg-rag-llm"
}

variable "location" {
  description = "Emplacement Azure"
  type        = string
  default     = "westeurope"
}

variable "vnet_name" {
  description = "Nom du Virtual Network"
  type        = string
  default     = "vnet-rag-llm"
}

variable "subnet_name" {
  description = "Nom du Subnet (utilisé pour AKS)"
  type        = string
  default     = "aks-subnet"
}

variable "aks_cluster_name" {
  description = "Nom du cluster AKS"
  type        = string
  default     = "aks-rag-llm"
}

variable "node_count" {
  description = "Nombre de nœuds dans le pool"
  type        = number
  default     = 1
}

variable "dockerhub_username" {
  description = "Nom d'utilisateur Docker Hub"
  type        = string
}

variable "dockerhub_password" {
  description = "Mot de passe Docker Hub"
  type        = string
  sensitive   = true
}

variable "dockerhub_email" {
  description = "Email associé à Docker Hub"
  type        = string
}

variable "dockerhub_server" {
  description = "Serveur Docker Hub (par défaut : index.docker.io)"
  type        = string
  default     = "https://index.docker.io/v1/"
}
