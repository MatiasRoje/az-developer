targetScope = 'subscription'

@description('Location for all resources')
param location string = 'West Europe'

@description('Current user object ID for granting access to Key Vault')
param currentUserObjectId string = ''

@description('PostgreSQL administrator login')
param postgresAdminLogin string = 'azdevpostgresuser'

@description('PostgreSQL administrator password (will be stored in Key Vault)')
@secure()
param postgresAdminPassword string

@description('Enable PostgreSQL deployment')
param deployPostgreSQL bool = true

// Define common tags as variable
var standardTags = {
  Project: 'AZ-204'
  Environment: 'Development'
  Owner: 'rojechi@gmail.com'
  CreatedBy: 'Bicep'
}


// Main resource group
resource rg 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: 'rg-az-developer'
  location: location
  tags: standardTags
}

// Key Vault (deployed first)
module keyVault 'modules/key-vault.bicep' = {
  name: 'key-vault'
  scope: rg
  params: {
    location: location
    keyVaultName: 'kv-az-developer'
    currentUserObjectId: currentUserObjectId
    postgresAdminPassword: postgresAdminPassword
    tags: standardTags
  }
}

// PostgreSQL (using getSecret to retrieve from Key Vault)
module postgres 'modules/postgres.bicep' = if (deployPostgreSQL) {
  name: 'postgres'
  scope: rg
  params: {
    location: location
    serverName: 'postgres-az-developer'
    keyVaultId: keyVault.outputs.keyVaultId
    postgresAdminLogin: postgresAdminLogin
    postgresAdminPassword: postgresAdminPassword
    tags: standardTags
  }
}

// Useful outputs for testing
output keyVaultName string = keyVault.outputs.keyVaultName
output postgresServerFqdn string = deployPostgreSQL ? postgres.outputs.serverFqdn : ''
output postgresDatabase string = deployPostgreSQL ? postgres.outputs.databaseName : ''

