output "resource_group_name" {
  description = "The name of the resource group"   # Description of the output.
  value       = azurerm_resource_group.rg.name       # Outputs the name of the resource group.
}

output "aks_cluster_name" {
  description = "The name of the AKS cluster"         # Description of the output.
  value       = azurerm_kubernetes_cluster.aks.name    # Outputs the name of the AKS cluster.
}

output "kube_config" {
  description = "Kube config for AKS"                  # Description of the output.
  value       = azurerm_kubernetes_cluster.aks.kube_config_raw  # Outputs the raw kubeconfig for the AKS cluster.
  sensitive   = true                                   # Marks the output as sensitive, so it will not be displayed in logs.
}

output "bastion_public_ip" {
  description = "Public IP address of the Bastion Host"  # Description of the output.
  value       = azurerm_public_ip.bastion.ip_address       # Outputs the public IP address of the Bastion Host.
}
