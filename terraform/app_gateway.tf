# Create an Azure Application Gateway resource
resource "azurerm_application_gateway" "appgw" {
  name                = "appgw"                           # Name of the Application Gateway
  location            = azurerm_resource_group.rg.location  # Location (region) from the resource group
  resource_group_name = azurerm_resource_group.rg.name        # Name of the resource group where the gateway will reside

  sku {
    name     = "Standard_v2"    # SKU name for the gateway (Standard_v2)
    tier     = "Standard_v2"    # SKU tier (Standard_v2)
    capacity = 2                # Number of instances (scaling capacity)
  }

  # Define the IP configuration for the gateway
  gateway_ip_configuration {
    name      = "appGatewayIpConfig"           # Name for the IP configuration
    subnet_id = azurerm_subnet.appgw.id         # Subnet ID where the gateway will be deployed
  }

  # Define a frontend port for the gateway (HTTP port)
  frontend_port {
    name = "httpPort"         # Name of the frontend port
    port = 80                 # Port number to listen on
  }

  # Configure the frontend IP of the gateway using a public IP address
  frontend_ip_configuration {
    name                 = "appGatewayFrontendIP"          # Name of the frontend IP configuration
    public_ip_address_id = azurerm_public_ip.appgw.id      # ID of the public IP resource to attach
  }

  # Define the backend address pool containing the IP addresses of the backend servers
  backend_address_pool {
    name         = "appGatewayBackendPool"       # Name of the backend pool
    ip_addresses = ["10.0.1.100"]                # List of IP addresses for the backend servers
  }

  # Define the HTTP settings for backend communication
  backend_http_settings {
    name                  = "appGatewayBackendHttpSettings"  # Name of the backend HTTP settings
    cookie_based_affinity = "Disabled"                       # Disable cookie-based affinity
    port                  = 5003                             # Port on which the backend service is listening
    protocol              = "Http"                           # Protocol used (HTTP)
    request_timeout       = 60                               # Timeout (in seconds) for backend requests
  }

  # Configure the HTTP listener that receives incoming traffic
  http_listener {
    name                           = "appGatewayHttpListener"         # Name of the HTTP listener
    frontend_ip_configuration_name = "appGatewayFrontendIP"           # Reference to the frontend IP configuration
    frontend_port_name             = "httpPort"                       # Reference to the frontend port configuration
    protocol                       = "Http"                           # Protocol used for listening (HTTP)
  }

  # Define a basic request routing rule that links the listener to the backend pool and settings
  request_routing_rule {
    name                       = "appGatewayRoutingRule"              # Name of the routing rule
    rule_type                  = "Basic"                              # Rule type (Basic routing rule)
    http_listener_name         = "appGatewayHttpListener"             # Reference to the HTTP listener
    backend_address_pool_name  = "appGatewayBackendPool"              # Reference to the backend address pool
    backend_http_settings_name = "appGatewayBackendHttpSettings"      # Reference to the backend HTTP settings
    priority                   = 100                                  # Priority of the rule (lower values have higher priority)
  }

  # Tags to organize and categorize resources (here, marking the environment as Production)
  tags = {
    Environment = "Production"
  }

  # Specify dependencies to ensure the public IP and subnet resources are created before this resource
  depends_on = [
    azurerm_public_ip.appgw,
    azurerm_subnet.appgw
  ]
}
