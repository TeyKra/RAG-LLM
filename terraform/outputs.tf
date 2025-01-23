#####################################
# Outputs
#####################################

# IP publique du Load Balancer attribuée au service frontend
output "frontend_public_ip" {
  description = "Adresse IP publique du frontend exposé"
  value       = kubernetes_service.frontend_svc.status[0].load_balancer[0].ingress[0].ip
}

# Nom du Resource Group
output "resource_group_name" {
  description = "Nom du Resource Group créé"
  value       = azurerm_resource_group.rg.name
}

# Nom du cluster AKS
output "aks_cluster_name" {
  description = "Nom du cluster AKS"
  value       = azurerm_kubernetes_cluster.aks.name
}
