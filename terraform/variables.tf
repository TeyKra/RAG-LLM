variable "subscription_id" {
  description = "The Azure subscription ID"    # The ID of your Azure subscription.
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"      # The name for the Azure resource group.
  type        = string
  default     = "rg-rag-llm"
}

variable "location" {
  description = "Azure location"                  # The Azure region where resources will be deployed.
  type        = string
  default     = "westeurope"
}

variable "vnet_name" {
  description = "Name of the Virtual Network"     # The name for the Virtual Network.
  type        = string
  default     = "vnet-rag-llm"
}

variable "subnet_name" {
  description = "Name of the Subnet (used for AKS)"  # The name for the subnet used by the AKS cluster.
  type        = string
  default     = "aks-subnet"
}

variable "aks_cluster_name" {
  description = "Name of the AKS cluster"          # The name for the Azure Kubernetes Service (AKS) cluster.
  type        = string
  default     = "aks-rag-llm"
}

variable "node_count" {
  description = "Number of nodes in the pool"       # The number of nodes in the AKS node pool.
  type        = number
  default     = 1
}

variable "dockerhub_username" {
  description = "Docker Hub username"              # Your Docker Hub username.
  type        = string
}

variable "dockerhub_password" {
  description = "Docker Hub password"              # Your Docker Hub password.
  type        = string
  sensitive   = true                                 # Marked sensitive to hide its value in logs.
}

variable "dockerhub_email" {
  description = "Email associated with Docker Hub" # The email address associated with your Docker Hub account.
  type        = string
}

variable "dockerhub_server" {
  description = "Docker Hub server (default: index.docker.io)"  # The Docker Hub server URL.
  type        = string
  default     = "https://index.docker.io/v1/"
}
