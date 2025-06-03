targetScope = 'subscription'

@description('Location for all resources')
param location string = 'West Europe'

@description('GitHub repository URL')
param repositoryUrl string  = 'https://github.com/MatiasRoje/az-developer'

@description('GitHub repository branch')
param branch string = 'main'

@description('GitHub personal access token')
@secure()
param githubToken string

@description('Create a resource group')
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-swa-az-developer-matiasroje'
  location: location
  tags: {
    Environment: 'Production'
    Owner: 'Matias Roje'
    Project: 'az-developer'
  }
}

@description('Create a static web app with GitHub integration')
module swa 'br/public:avm/res/web/static-site:0.3.0' = {
  name: 'client'
  scope: rg
  params: {
    name: 'swa-az-developer-matiasroje'
    location: location
    sku: 'Free'

    // GitHub integration
    repositoryUrl: repositoryUrl
    branch: branch
    repositoryToken: githubToken

    // Build configuration for Vite 
    buildProperties: {
      appLocation: '/frontend'
      outputLocation: '/frontend/dist'
      appBuildCommand: 'npm run build'
    }
  }
}

@description('Output the URL of the static web app')
output appUrl string = 'https://${swa.outputs.defaultHostname}'

@description('Output the static web app name')
output staticWebAppName string = swa.outputs.name
