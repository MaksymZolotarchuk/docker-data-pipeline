variable "resource_group_location" {
  type        = string
  default     = "francecentral"
  description = "Location of the resource group."
}

variable "resource_group_name_prefix" {
  type        = string
  default     = "rg-devops-lab-v3"
  description = "Prefix of the resource group name."
}

variable "admin_username" {
  type        = string
  default     = "azureuser"
  description = "The username for the local administrator account."
}
