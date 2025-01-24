output "resource_group_name" {
  description = "Le nom du groupe de ressources"
  value       = azurerm_resource_group.rg.name
}

output "aks_cluster_name" {
  description = "Le nom du cluster AKS"
  value       = azurerm_kubernetes_cluster.aks.name
}

output "kube_config" {
  description = "Kube config pour AKS"
  value       = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive   = true
}
