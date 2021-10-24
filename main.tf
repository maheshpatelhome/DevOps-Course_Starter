terraform {
 required_providers {
  azurerm = {
  source = "hashicorp/azurerm"
  version = ">= 2.49"
  }
 }
 backend "azurerm" {
        resource_group_name  = "CreditSuisse2_MaheshPatel_ProjectExercise"
        storage_account_name = "maheshpateltfstate"
        container_name       = "tfstate"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
 features {}
}

data "azurerm_resource_group" "main" {
 name = "CreditSuisse2_MaheshPatel_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
 name = "${var.prefix}-terraformed-asp"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 kind = "Linux"
 reserved = true
 sku {
  tier = "Basic"
  size = "B1"
 }
}

resource "azurerm_app_service" "main" {
 name = "${var.prefix}-MaheshsTerraFormToDoApp"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 app_service_plan_id = azurerm_app_service_plan.main.id
 site_config {
  app_command_line = ""
  linux_fx_version = "DOCKER|maheshpatelhome/todo-app-prod:latest"
 }
 app_settings = {
  "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
  "FLASK_APP"="todo_app/app"
	"FLASK_ENV"="development"
	"SECRET_KEY"="TODO_APP_SECRET_KEY"
	"GITHUB_CLIENT_ID"=var.GITHUB_CLIENT_ID
	"GITHUB_SECRET"=var.GITHUB_SECRET
	"OAUTHLIB_INSECURE_TRANSPORT"="1"
  "COSMOS_CONNECTION_STRING"="mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000" 
	"DEFAULT_DATABASE"="To_Do_App"
	"BOARD_NAME"="To Do List"
 }
}

resource "azurerm_cosmosdb_account" "main" {
  name = "${var.prefix}-mahesh-terraform-cosmosdb-account"
  location = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type = "standard"
  kind = "MongoDB"
  capabilities {
    name = "EnableServerless"
  }
  capabilities {
    name = "EnableMongo"
  }
  geo_location {  
    location = data.azurerm_resource_group.main.location
    failover_priority = "0"
  }
  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }
  #lifecycle {prevent_destroy = true}
}

# Error: waiting on create/update future for Cosmos Mongo Database "mahesh-terraform-db" (Account: "mahesh-terraform-cosmosdb-account"): Code="BadRequest" Message="Throughput may not be defined for databases or collections in this account because Serverless Offer is enabled.\r\nActivityId: 69db0bf1-12d7-462d-a5c0-89994c9c5632, Microsoft.Azure.Documents.Common/2.14.0, Microsoft.Azure.Documents.Common/2.14.0, Microsoft.Azure.Documents.Common/2.14.0, Microsoft.Azure.Documents.Common/2.14.0"
resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-mahesh-terraform-db"
  resource_group_name = resource.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = resource.azurerm_cosmosdb_account.main.name
  # throughput          = 400
}


output "primary_key" {
  value = azurerm_cosmosdb_account.main.primary_key
  sensitive = true
}

output "connection_strings" {
  value = azurerm_cosmosdb_account.main.connection_strings
  sensitive = true
}
