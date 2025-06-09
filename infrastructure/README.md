Az-Developer Infrastructure

Instructions:

```bash
# Create infrastructure ()
az deployment sub create \
  --location "West Europe" \
  --template-file infrastructure/main.bicep \
  --parameters postgresAdminPassword=".env.POSTGRES_ADMIN_PASSWORD" currentUserObjectId="$(az ad signed-in-user show --query id -o tsv)"

# Destroy infrastructure
az group delete --name rg-az-developer --yes
```
