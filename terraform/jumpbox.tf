// Dedicated subnet for the jumpbox
resource "azurerm_subnet" "jumpbox" {
  name                 = "jumpbox-subnet"                          // Name of the subnet dedicated to the jumpbox
  resource_group_name  = azurerm_resource_group.rg.name            // Reference to the resource group's name
  virtual_network_name = azurerm_virtual_network.vnet.name         // Reference to the virtual network's name
  address_prefixes     = ["10.0.3.0/24"]                           // IP address range for the subnet
  depends_on           = [azurerm_virtual_network.vnet]            // Ensure the virtual network is created before this subnet
}

// Network interface for the jumpbox
resource "azurerm_network_interface" "jumpbox_nic" {
  name                = "jumpbox-nic"                             // Name of the network interface
  location            = azurerm_resource_group.rg.location        // Location where the NIC is deployed
  resource_group_name = azurerm_resource_group.rg.name            // Resource group for the NIC

  ip_configuration {
    name                          = "internal"                   // Name of the IP configuration
    subnet_id                     = azurerm_subnet.jumpbox.id    // Reference to the jumpbox subnet ID
    private_ip_address_allocation = "Dynamic"                    // Allocate a private IP address dynamically
  }
}

// Linux virtual machine (jumpbox)
resource "azurerm_linux_virtual_machine" "jumpbox" {
  name                = "jumpbox-vm"                              // Name of the jumpbox virtual machine
  resource_group_name = azurerm_resource_group.rg.name            // Resource group for the VM
  location            = azurerm_resource_group.rg.location        // Location where the VM is deployed
  size                = "Standard_B1s"                            // VM size (Standard_B1s is a small instance)
  admin_username      = "azureuser"                               // Administrator username for the VM
  network_interface_ids = [
    azurerm_network_interface.jumpbox_nic.id,                   // Associate the network interface created above
  ]

  os_disk {
    caching              = "ReadWrite"                         // Disk caching mode
    storage_account_type = "Standard_LRS"                      // Storage account type for the OS disk
  }

  source_image_reference {
    publisher = "Canonical"                                     // Publisher of the OS image
    offer     = "UbuntuServer"                                  // Offer (Ubuntu Server)
    sku       = "18.04-LTS"                                     // SKU (Ubuntu 18.04 LTS)
    version   = "latest"                                        // Use the latest version of the image
  }

  admin_ssh_key {
    username   = "azureuser"                                    // Administrator username for SSH access
    public_key = file("C:/Users/morga/Desktop/morgankey.pub")   // Path to the public SSH key file
  }

  disable_password_authentication = true                      // Disable password authentication (use SSH keys only)
}
