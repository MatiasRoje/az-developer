# AZ-204 Focused Learning Roadmap

**Target**: Pass AZ-204 (Azure Developer Associate) first, then enhance for AZ-400

## 🎯 AZ-204 Exam Strategy: Local → Azure → Serverless

**Philosophy**: Build working microservices locally, then adapt to Azure patterns

---

## Phase 1: Local Microservices Foundation

**Objective**: Working microservices system with exam-relevant patterns

### 1.1 Core Services Setup

- **Auth Service** (Python FastAPI + PostgreSQL)
  - JWT token generation/validation
  - User registration/login
  - PostgreSQL connection patterns
- **Image Service** (Python FastAPI)
  - File upload handling
  - Image processing workflows
  - Storage abstraction layer
- **Gateway Service** (Python FastAPI)
  - Route aggregation
  - Authentication middleware
  - Rate limiting patterns

### 1.2 Infrastructure (minikube)

```bash
# PostgreSQL container
# RabbitMQ container
# Redis container (caching patterns)
# All services containerized
```

### 1.3 Frontend Integration

- React SPA with TypeScript
- Authentication flows
- File upload components
- API integration patterns

**AZ-204 Exam Points Covered**:

- Container deployment patterns
- Database connection strings
- Authentication flows
- API design patterns

---

## Phase 2: Azure Services Integration

**Objective**: Replace local services with Azure equivalents

### 2.1 Database Migration

- **Local PostgreSQL** → **Azure PostgreSQL Flexible Server**
- Connection string management
- Firewall configuration
- SSL/TLS requirements
- Key Vault integration

### 2.2 Storage Implementation

- **Azure Blob Storage** integration
- Hot/Cool/Archive tiers
- SAS token generation
- Lifecycle policies
- CDN integration

### 2.3 Messaging System

- **RabbitMQ** → **Azure Service Bus**
- Queue vs Topic patterns
- Dead letter queue handling
- Message sessions
- Duplicate detection

### 2.4 Security Implementation

- **Azure Key Vault** for secrets
- **Managed Identity** configuration
- **Azure AD** integration
- RBAC patterns

**AZ-204 Exam Points Covered**:

- Azure service configuration
- Security best practices
- Service integration patterns
- Cost optimization strategies

---

## Phase 3: Serverless Adaptation

**Objective**: Convert microservices to Azure Functions

### 3.1 Function Apps Development

- **HTTP Triggered Functions** (API endpoints)
- **Blob Triggered Functions** (image processing)
- **Timer Triggered Functions** (cleanup jobs)
- **Service Bus Triggered Functions** (message processing)

### 3.2 Serverless Patterns

- Function chaining
- Durable Functions workflows
- Event-driven architecture
- Cold start optimization

### 3.3 Monitoring Integration

- **Application Insights** setup
- Custom telemetry
- Performance monitoring
- Error tracking
- Log Analytics queries

**AZ-204 Exam Points Covered**:

- Azure Functions development
- Trigger and binding patterns
- Serverless architecture
- Monitoring and diagnostics

---

## Phase 4: Production Patterns

**Objective**: Enterprise-ready deployment patterns

### 4.1 API Management

- **Azure API Management** setup
- Policy implementation
- Rate limiting
- API versioning
- Developer portal

### 4.2 Container Deployment

- **Azure Container Apps** deployment
- **AKS** comparison and setup
- Scaling policies
- Health checks
- Blue-green deployments

### 4.3 Static Web Apps

- **Azure Static Web Apps** deployment
- Custom domains
- CI/CD integration
- API integration
- Authentication providers

**AZ-204 Exam Points Covered**:

- API gateway patterns
- Container orchestration
- Static web hosting
- CI/CD integration

---

## Phase 5: Infrastructure as Code

**Objective**: Automated deployment and management

### 5.1 Bicep Templates

- Resource group templates
- Parameter files
- Module development
- Template validation
- Deployment automation

### 5.2 CI/CD Pipeline

- **GitHub Actions** setup
- Automated testing
- Infrastructure deployment
- Application deployment
- Environment management

**AZ-204 Exam Points Covered**:

- Infrastructure as Code
- Deployment automation
- Environment configuration
- Resource management

---

## 🎓 AZ-204 Exam Readiness Checklist

### Compute Services ✅

- [ ] Azure Functions (HTTP, Timer, Blob triggers)
- [ ] Container Apps (deployment, scaling)
- [ ] Static Web Apps (CI/CD, custom domains)

### Storage & Data ✅

- [ ] Blob Storage (tiers, SAS, lifecycle)
- [ ] PostgreSQL (connection, firewall, SSL)
- [ ] Cosmos DB (consistency, partitioning)

### Security & Identity ✅

- [ ] Key Vault (secrets, certificates)
- [ ] Managed Identity (system/user assigned)
- [ ] Azure AD (authentication, authorization)

### Integration & Messaging ✅

- [ ] Service Bus (queues, topics, sessions)
- [ ] Event Grid (custom topics, handlers)
- [ ] API Management (policies, versioning)

### Monitoring & Troubleshooting ✅

- [ ] Application Insights (telemetry, queries)
- [ ] Azure Monitor (metrics, alerts)
- [ ] Log Analytics (KQL queries)

### Infrastructure as Code ✅

- [ ] Bicep templates (resources, modules)
- [ ] ARM templates (functions, conditions)
- [ ] Deployment patterns (validation, testing)

---

## 💰 Cost Management (AZ-204 Learning)

### Free Tier Services

- **Azure Functions**: 1M executions/month
- **Static Web Apps**: 100GB bandwidth/month
- **PostgreSQL**: 12 months free (B1ms)
- **Blob Storage**: 5GB for 12 months
- **Service Bus**: 13M operations for 12 months
- **Key Vault**: 10K operations/month

### Learning Strategy

1. **Deploy** → Test specific exam scenario → **Delete**
2. **Document** learnings and exam points
3. **Repeat** with different configurations
4. **Practice** deployment automation

**Target Cost**: $0-5/month during learning phase

---

## 🚀 Next Phase: AZ-400 Enhancement (After AZ-204)

Once AZ-204 is passed, enhance the same codebase for AZ-400:

- Advanced CI/CD pipelines
- Security scanning integration
- Infrastructure testing
- Release management strategies
- Production monitoring
- Compliance and governance

**Focus**: Keep the same application, add DevOps engineering practices
