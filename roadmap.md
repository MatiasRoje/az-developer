# Azure Developer Certification Suite - Learning Roadmap
**Target**: AZ-204 (Developer Associate) + AZ-400 (DevOps Engineer Expert)

## Phase 1: Frontend Foundation
**Objective**: Deploy production-ready React frontend with Infrastructure as Code
- React application with TypeScript and ES modules
- Azure Static Web Apps deployment with custom domain
- **ARM Templates**: Learn JSON structure, functions, and conditions
- **Bicep Templates**: Modern IaC for Static Web Apps infrastructure
- GitHub Actions CI/CD pipeline
- Basic authentication UI components

## Phase 2: Serverless Microservices
**Objective**: Build event-driven backend architecture
- Azure Functions (Python) for core services:
  - Authentication service with JWT handling
  - Image upload service with validation
  - Image processing service with triggers
- Azure Service Bus for async messaging
- Azure Blob Storage for image storage (hot/cool tiers)
- Azure Key Vault for secrets management
- Managed Identity for service-to-service authentication
- Azure Cosmos DB integration for user data
- Event Grid for event-driven workflows

## Phase 3: API & Monitoring Layer
**Objective**: Production-ready API management and observability
- Azure API Management with policies and rate limiting
- Application Insights with custom telemetry
- Azure Monitor dashboards and alerts
- Log Analytics queries for troubleshooting
- Performance monitoring and optimization
- Health checks and availability tests

## Phase 4: Containerization
**Objective**: Container-based deployments and orchestration
- Docker containerization of all services
- Azure Container Registry with security scanning
- Azure Container Apps deployment (serverless containers)
- Azure Kubernetes Service (AKS) with Helm charts
- Container networking and security
- Auto-scaling policies

## Phase 5: Advanced DevOps
**Objective**: Production-grade CI/CD and deployment strategies
- Multi-stage Azure DevOps YAML pipelines
- **Infrastructure testing**: ARM template validation, Bicep linting
- SAST/DAST security scanning integration
- Blue-green and canary deployment strategies
- Feature flags and progressive rollouts
- Automated rollback mechanisms

## Phase 6: Production Readiness
**Objective**: Enterprise-grade security, performance, and reliability
- Load testing with Azure Load Testing
- Disaster recovery and backup strategies
- Network security with Private Link and NSGs
- Cost optimization and resource governance
- Compliance and audit logging
- Performance tuning and optimization

## Cost Management Strategy
- **Free Tier Services**: Functions (1M executions), Static Web Apps (100GB), Cosmos DB (1000 RU/s)
- **12-Month Free**: Blob Storage (5GB), Service Bus (13M operations), Key Vault (10K ops)
- **Always Free**: Event Grid (100K ops), API Management (1M calls), Container Apps (180K vCPU-sec)
- **Target**: $0-5/month for entire learning environment

## 🎓 Certification Mapping

### AZ-204 Coverage (100%)
**Compute Services**
- Azure Functions (triggers, bindings, scaling)
- App Service (deployment slots, configuration)
- Static Web Apps (CI/CD integration, custom domains)

**Storage & Data**
- Blob Storage (access tiers, lifecycle policies, SAS tokens)
- Cosmos DB (consistency levels, partitioning, change feed)
- Azure SQL Database (serverless, elastic pools)

**Security & Identity**
- Key Vault (secrets, certificates, access policies)
- Managed Identity (system-assigned, user-assigned)
- Azure AD B2C (custom policies, user flows)

**Integration & Messaging**
- Service Bus (queues, topics, dead letter queues)
- Event Grid (custom topics, event schemas, handlers)
- API Management (policies, rate limiting, versioning)

**Monitoring & Troubleshooting**
- Application Insights (custom telemetry, availability tests)
- Azure Monitor (metrics, alerts, dashboards)

**Infrastructure as Code**
- **ARM Templates**: Functions, conditions, loops, linked templates
- **Bicep**: Modern syntax, modules, strong typing

### AZ-400 Preparation (100%)
**Infrastructure as Code**
- ARM/Bicep template development and testing
- Infrastructure validation and compliance
- Template versioning and governance

**CI/CD Pipelines**
- Multi-stage YAML pipelines with approvals
- Automated testing integration
- Artifact management and versioning

**Security Integration**
- SAST/DAST scanning in pipelines
- Dependency vulnerability scanning
- Secrets management in DevOps

**Release Management**
- Blue-green and canary deployment patterns
- Feature flags and progressive rollouts
- Automated rollback strategies

**Monitoring & Feedback**
- Infrastructure monitoring and alerting
- Application performance monitoring
- Configuration management with drift detection