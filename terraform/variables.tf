#####################################
# Variables
#####################################

# Nom de l'abonnement Azure
variable "subscription_id" {
  type        = string
  description = "L'ID de l'abonnement Azure où déployer la solution."
}

# Nom du Resource Group
variable "resource_group_name" {
  type        = string
  description = "Le nom du Resource Group à créer."
  default     = "rg-rag-llm"
}

# Localisation (region) Azure
variable "location" {
  type        = string
  description = "Région Azure où créer les ressources."
  default     = "francecentral"
}

# Nom du cluster AKS
variable "aks_cluster_name" {
  type        = string
  description = "Le nom du cluster AKS."
  default     = "aks-rag-llm"
}

# Nombre de noeuds dans le pool par défaut
variable "default_node_count" {
  type        = number
  description = "Nombre de nœuds dans le pool AKS par défaut."
  default     = 2
}

# Type de VM pour les noeuds
variable "default_node_vm_size" {
  type        = string
  description = "Type de VM pour le node pool AKS."
  default     = "Standard_DS2_v2"
}


