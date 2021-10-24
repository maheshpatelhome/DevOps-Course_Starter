variable "prefix" {
    description = "The prefix used for all resources in this environment"
    default="test"
}

variable "location" {
    description = "The Azure location where all resources in this deployment should be created"
    default = "uksouth"
}

variable "GITHUB_CLIENT_ID" {
    description = "The github client ID"
}

variable "GITHUB_SECRET"  {
    description = "The github client secret"
}

	