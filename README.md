# Azure Developer Certification Suite - AZ-204 Focus

**Goal**: Master AZ-204 (Azure Developer Associate) through hands-on microservices development, then proceed to AZ-400.

## 🎯 AZ-204 Exam Coverage Strategy

**Local Development First → Azure Adaptation → Azure Native**

### Microservices Architecture (AZ-204 Focus)

- **Auth Service**: JWT authentication with PostgreSQL
- **Image Service**: Upload/processing with Azure Blob Storage
- **Gateway Service**: Custom API gateway patterns
- **Frontend**: React SPA with Azure Static Web Apps
- **Messaging**: RabbitMQ (local) → Azure Service Bus (cloud)

### Azure Services Covered (100% AZ-204 Exam Objectives)

- ✅ **Compute**: Azure Functions, Container Apps, Static Web Apps
- ✅ **Storage**: Blob Storage (hot/cool tiers, SAS tokens, lifecycle policies)
- ✅ **Database**: PostgreSQL Flexible Server (free tier, connection patterns)
- ✅ **Security**: Key Vault, Managed Identity, Azure AD integration
- ✅ **Integration**: Service Bus (queues/topics), Event Grid patterns
- ✅ **API**: API Management (policies, versioning, rate limiting)
- ✅ **Monitoring**: Application Insights, Azure Monitor, custom telemetry
- ✅ **IaC**: Bicep templates for all infrastructure

## 🏗️ Development Phases

- Phase 1: Local Microservices (minikube)

- Phase 2: Azure Functions Adaptation

- Phase 3: Azure Container Deployment

## 💰 Cost Strategy (AZ-204 Learning)

- **Local Development**: $0 (minikube + Docker)
- **Azure Testing**: Free tier only (~$0-2/month)
- **Immediate Deletion**: Test → Learn → Delete → Repeat

## 🎓 Exam Preparation Strategy

**Current Focus: AZ-204 ONLY**

- All code demonstrates specific exam scenarios
- Every Azure service includes exam-focused explanations
- Practice questions integrated into development workflow
- Real-world patterns that appear in exam questions

**Next Phase: AZ-400** (after passing AZ-204)

- Advanced CI/CD pipelines
- Production-ready security patterns
- Infrastructure testing and validation
- Enterprise DevOps practices

## 🚀 Quick Start (AZ-204 Learning Path)

```bash
# 1. Local development
# Build and start all services (production frontend)
docker compose up --build

# For development with hot reload
# Run frontend locally with hot reload
cd frontend
npm run dev
# Run backend services in containers
docker compose up -d postgres auth-service gateway-service

# 2. Azure adaptation
az login
az deployment sub create --template-file infrastructure/main.bicep

# 3. Test, learn, delete
az group delete --name rg-az-developer --yes
```

**Ready for AZ-204 exam upon completion of all phases.**
