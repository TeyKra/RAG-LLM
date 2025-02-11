# Configure the AzureRM provider with the specified subscription.
provider "azurerm" {
  features {}                              # Enables all required features.
  subscription_id = var.subscription_id      # Subscription ID provided via variable.
}

# Create an Azure Resource Group.
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name        # Name of the resource group (from variable).
  location = var.location                     # Location/region for the resource group.
}

# Create a Virtual Network (VNet) for your resources.
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name           # Name of the VNet (from variable).
  address_space       = ["10.0.0.0/16"]           # Address space for the VNet.
  location            = azurerm_resource_group.rg.location  # Inherit the location from the resource group.
  resource_group_name = azurerm_resource_group.rg.name      # Resource group where the VNet is created.
  depends_on          = [azurerm_resource_group.rg]           # Ensure the resource group is created first.
}

# Subnet dedicated to the AKS nodes.
resource "azurerm_subnet" "subnet" {
  name                 = var.subnet_name         # Name of the subnet (from variable).
  resource_group_name  = azurerm_resource_group.rg.name  # Resource group name.
  virtual_network_name = azurerm_virtual_network.vnet.name  # VNet name.
  address_prefixes     = ["10.0.1.0/24"]         # Address prefix for this subnet.
  depends_on           = [azurerm_virtual_network.vnet]  # Ensure the VNet is created first.
}

# Subnet dedicated to Bastion (the name must be "AzureBastionSubnet" for Bastion Host to work).
resource "azurerm_subnet" "bastion" {
  name                 = "AzureBastionSubnet"    # Must be named "AzureBastionSubnet" for Azure Bastion.
  resource_group_name  = azurerm_resource_group.rg.name  # Resource group name.
  virtual_network_name = azurerm_virtual_network.vnet.name  # VNet name.
  address_prefixes     = ["10.0.2.0/27"]         # Address prefix for the Bastion subnet.
  depends_on           = [azurerm_virtual_network.vnet]  # Ensure the VNet is created first.
}

# Subnet dedicated to the Application Gateway.
resource "azurerm_subnet" "appgw" {
  name                 = "appgw-subnet"          # Name of the subnet for the Application Gateway.
  resource_group_name  = azurerm_resource_group.rg.name  # Resource group name.
  virtual_network_name = azurerm_virtual_network.vnet.name  # VNet name.
  address_prefixes     = ["10.0.4.0/24"]         # Address prefix for the Application Gateway subnet.
  depends_on           = [azurerm_virtual_network.vnet]  # Ensure the VNet is created first.
}

# Create an Azure Kubernetes Service (AKS) cluster.
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_cluster_name     # Name of the AKS cluster (from variable).
  location            = azurerm_resource_group.rg.location  # Location inherited from the resource group.
  resource_group_name = azurerm_resource_group.rg.name      # Resource group name.
  dns_prefix          = "aks-rag-llm"            # DNS prefix for the cluster.

  default_node_pool {
    name            = "default"                  # Name of the default node pool.
    node_count      = var.node_count             # Number of nodes (from variable).
    vm_size         = "Standard_DS3_v2"          # VM size for each node.
    os_disk_size_gb = 30                         # OS disk size in GB.
    vnet_subnet_id  = azurerm_subnet.subnet.id   # Subnet ID where the nodes will be deployed.
  }

  identity {
    type = "SystemAssigned"                      # Enable system-assigned managed identity.
  }

  network_profile {
    network_plugin    = "azure"                   # Network plugin to use.
    load_balancer_sku = "standard"                # Load Balancer SKU.
    service_cidr      = "10.1.0.0/16"             # CIDR block for Kubernetes services.
    dns_service_ip    = "10.1.0.10"               # DNS service IP.
  }

  sku_tier = "Standard"                          # SKU tier for the cluster.

  tags = {
    Environment = "Production"                  # Tag to indicate the environment.
  }

  depends_on = [azurerm_subnet.subnet]           # Ensure the subnet is created before the cluster.
}

# Assign the "Network Contributor" role to the AKS cluster's managed identity on the VNet.
resource "azurerm_role_assignment" "aks_vnet_assignment" {
  scope                = azurerm_virtual_network.vnet.id  # Scope of the role assignment (the VNet).
  role_definition_name = "Network Contributor"            # Role to assign.
  principal_id         = azurerm_kubernetes_cluster.aks.identity.0.principal_id  # Principal ID of the AKS cluster's managed identity.
  depends_on           = [azurerm_kubernetes_cluster.aks]    # Ensure the AKS cluster is created first.
}

# Public IP resource for Bastion.
resource "azurerm_public_ip" "bastion" {
  name                = "bastion-pip"             # Name of the Bastion public IP.
  location            = azurerm_resource_group.rg.location  # Location inherited from the resource group.
  resource_group_name = azurerm_resource_group.rg.name      # Resource group name.
  allocation_method   = "Static"                  # Use static IP allocation.
  sku                 = "Standard"                # SKU for the public IP.
}

# Create an Azure Bastion Host.
resource "azurerm_bastion_host" "bastion" {
  name                = "bastion-host"            # Name of the Bastion host.
  location            = azurerm_resource_group.rg.location  # Location from the resource group.
  resource_group_name = azurerm_resource_group.rg.name      # Resource group name.
  sku                 = "Standard"                # Bastion host SKU.
  
  ip_configuration {
    name                 = "configuration"         # Name of the IP configuration.
    subnet_id            = azurerm_subnet.bastion.id  # Subnet ID dedicated to Bastion.
    public_ip_address_id = azurerm_public_ip.bastion.id  # Public IP associated with Bastion.
  }

  depends_on = [
    azurerm_subnet.bastion,                        # Ensure Bastion subnet is created.
    azurerm_public_ip.bastion                      # Ensure Bastion public IP is created.
  ]
}

# Create a Public IP for the Application Gateway.
resource "azurerm_public_ip" "appgw" {
  name                = "appgw-public-ip"         # Name of the Application Gateway public IP.
  location            = azurerm_resource_group.rg.location  # Location from the resource group.
  resource_group_name = azurerm_resource_group.rg.name      # Resource group name.
  allocation_method   = "Static"                  # Use static IP allocation.
  sku                 = "Standard"                # SKU for the public IP.
}
