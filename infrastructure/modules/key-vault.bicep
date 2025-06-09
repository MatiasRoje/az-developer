@description('Location for all resources')
param location string

@description('Key Vault name')
param keyVaultName string

@description('Current user object ID for granting access to Key Vault')
param currentUserObjectId string

@description('PostgreSQL admin password')
@secure()
param postgresAdminPassword string

@description('Tags for the Key Vault')
param tags object

resource keyVault 'Microsoft.KeyVault/vaults@2024-11-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7  // Minimum for cost
    publicNetworkAccess: 'Enabled'  // Development only
  }
  tags: tags
}

// AZ-204 Pattern: Grant current user access to Key Vault
resource currentUserSecretAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, 'current-user', 'Key Vault Secrets User')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '00482a5a-887f-4fb3-b363-3b7fe8e74483') // Key Vault Administrator
    principalId: currentUserObjectId
    principalType: 'User'
  }
}

resource postgresAdminPasswordSecret 'Microsoft.KeyVault/vaults/secrets@2024-11-01' = {
  name: 'postgres-admin-password'
  parent: keyVault
  properties: {
    value: postgresAdminPassword
  }
}

// JWT secret for application
resource jwtSecret 'Microsoft.KeyVault/vaults/secrets@2024-11-01' = {
  name: 'jwt-secret'
  parent: keyVault
  properties: {
    value: 'az-dev-jwt-secret-${uniqueString(resourceGroup().id)}'
  }
}

output keyVaultId string = keyVault.id
output keyVaultUri string = keyVault.properties.vaultUri
output keyVaultName string = keyVault.name
