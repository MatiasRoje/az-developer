@description('Location for all resources')
param location string

@description('PostgreSQL server name')
param serverName string

@description('PostgreSQL administrator login')
param postgresAdminLogin string

@description('PostgreSQL admin password')
@secure()
param postgresAdminPassword string

@description('Key Vault resource ID')
param keyVaultId string

@description('Tags for the PostgreSQL server')
param tags object

// Reference existing Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2024-11-01' existing = {
  name: last(split(keyVaultId, '/'))
}

// PostgreSQL using Key Vault secrets via getSecret() function
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: serverName
  location: location
  sku: {
    name: 'Standard_B1ms'  // FREE TIER
    tier: 'Burstable'
  }
  properties: {
    // AZ-204 Exam Pattern: Use secure parameters directly
    administratorLogin: postgresAdminLogin
    administratorLoginPassword: postgresAdminPassword
    storage: {
      storageSizeGB: 32    // FREE: 32GB
    }
    backup: {
      backupRetentionDays: 7  // FREE: 7 days
      geoRedundantBackup: 'Disabled'
    }
    version: '15'
  }

  tags: tags
}

// Allow all IPs (development only)
resource firewallRule 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2024-08-01' = {
  name: 'AllowAllIps'
  parent: postgresServer
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '255.255.255.255'
  }
}

// Create database
resource authDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2024-08-01' = {
  name: 'authdb'
  parent: postgresServer
}

// Store complete connection string in Key Vault
resource connectionString 'Microsoft.KeyVault/vaults/secrets@2024-11-01' = {
  name: 'postgres-connection-string'
  parent: keyVault
  properties: {
    // AZ-204 Pattern: Build connection string using getSecret()
    value: 'postgresql://${postgresAdminLogin}:${postgresAdminPassword}@${postgresServer.properties.fullyQualifiedDomainName}:5432/authdb?sslmode=require'
  }
}

output serverFqdn string = postgresServer.properties.fullyQualifiedDomainName
output databaseName string = authDatabase.name
