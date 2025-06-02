# 🚀 Complete Pet Adoption System - Deployment Guide

This guide covers deploying the complete pet adoption system with frontend, backend, and cloud infrastructure.

## 🏗️ **System Architecture**

### **Frontend (React)**
- Modern React 18 application
- Bootstrap 5 UI framework
- React Query for state management
- Responsive design for all devices

### **Backend (Django REST API)**
- Django 4.2 with REST Framework
- Token-based authentication
- MongoDB/DocumentDB database
- Redis for caching and sessions
- Celery for background tasks

### **Cloud Infrastructure (AWS)**
- ECS Fargate for containerized deployment
- Application Load Balancer
- DocumentDB (MongoDB-compatible)
- ElastiCache (Redis)
- S3 for static files and media
- CloudFront CDN
- Route 53 for DNS

## 📋 **Prerequisites**

### **Development Environment**
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- MongoDB (local development)

### **Production Environment**
- AWS Account with appropriate permissions
- Domain name
- SSL certificate

## 🛠️ **Local Development Setup**

### **1. Backend Setup**
```bash
# Clone repository
git clone <repository-url>
cd pet-adoption-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python populate_sample_data.py
python add_pet_photos.py

# Start development server
python manage.py runserver
```

### **2. Frontend Setup**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### **3. Docker Development**
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ **Cloud Deployment (AWS)**

### **1. Infrastructure Setup**

#### **Deploy CloudFormation Stack**
```bash
# Deploy infrastructure
aws cloudformation create-stack \
  --stack-name pet-adoption-infrastructure \
  --template-body file://aws/cloudformation-template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=production \
               ParameterKey=DomainName,ParameterValue=your-domain.com \
               ParameterKey=DBPassword,ParameterValue=your-secure-password \
  --capabilities CAPABILITY_IAM

# Wait for stack creation
aws cloudformation wait stack-create-complete \
  --stack-name pet-adoption-infrastructure
```

#### **Configure DNS**
```bash
# Get Load Balancer DNS
ALB_DNS=$(aws cloudformation describe-stacks \
  --stack-name pet-adoption-infrastructure \
  --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
  --output text)

# Create Route 53 record (replace with your hosted zone ID)
aws route53 change-resource-record-sets \
  --hosted-zone-id YOUR_HOSTED_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "your-domain.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "'$ALB_DNS'"}]
      }
    }]
  }'
```

### **2. Application Deployment**

#### **Build and Push Docker Image**
```bash
# Build Docker image
docker build -t pet-adoption-app .

# Tag for ECR
docker tag pet-adoption-app:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/pet-adoption-app:latest

# Push to ECR
aws ecr get-login-password --region YOUR_REGION | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com

docker push YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/pet-adoption-app:latest
```

#### **Deploy ECS Service**
```bash
# Create ECS task definition
aws ecs register-task-definition \
  --cli-input-json file://aws/task-definition.json

# Create ECS service
aws ecs create-service \
  --cluster production-pet-adoption-cluster \
  --service-name pet-adoption-service \
  --task-definition pet-adoption-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-xxx", "subnet-yyy"],
      "securityGroups": ["sg-xxx"],
      "assignPublicIp": "ENABLED"
    }
  }' \
  --load-balancers '[{
    "targetGroupArn": "arn:aws:elasticloadbalancing:...",
    "containerName": "pet-adoption-app",
    "containerPort": 8000
  }]'
```

### **3. Database Setup**

#### **Configure DocumentDB**
```bash
# Connect to DocumentDB
mongo --ssl --host YOUR_DOCDB_ENDPOINT:27017 \
  --sslCAFile rds-combined-ca-bundle.pem \
  --username admin --password

# Create database and collections
use pet_adoption_db
db.createCollection("users")
db.createCollection("pets")
db.createCollection("adoptions")
```

#### **Run Migrations**
```bash
# Run Django migrations on ECS
aws ecs run-task \
  --cluster production-pet-adoption-cluster \
  --task-definition pet-adoption-migrate-task \
  --launch-type FARGATE \
  --network-configuration '{
    "awsvpcConfiguration": {
      "subnets": ["subnet-xxx"],
      "securityGroups": ["sg-xxx"],
      "assignPublicIp": "ENABLED"
    }
  }'
```

## 🔧 **Configuration**

### **Environment Variables**

#### **Production (.env)**
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DB_NAME=pet_adoption_db
DB_HOST=your-docdb-endpoint
DB_USER=admin
DB_PASSWORD=your-secure-password

# Redis
REDIS_URL=redis://your-elasticache-endpoint:6379/0

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
AWS_S3_REGION_NAME=us-east-1
USE_S3=True

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery
CELERY_BROKER_URL=redis://your-elasticache-endpoint:6379/0
CELERY_RESULT_BACKEND=redis://your-elasticache-endpoint:6379/0
```

### **Frontend Environment (.env)**
```bash
REACT_APP_API_URL=https://your-domain.com/api/v1
REACT_APP_ENVIRONMENT=production
```

## 📊 **Monitoring & Logging**

### **CloudWatch Setup**
```bash
# Create log groups
aws logs create-log-group --log-group-name /ecs/pet-adoption-app
aws logs create-log-group --log-group-name /ecs/pet-adoption-nginx

# Set up CloudWatch alarms
aws cloudwatch put-metric-alarm \
  --alarm-name "pet-adoption-high-cpu" \
  --alarm-description "High CPU utilization" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

### **Application Monitoring**
- **Health Checks**: `/api/v1/stats/` endpoint
- **Error Tracking**: Sentry integration
- **Performance**: New Relic or DataDog
- **Uptime**: Pingdom or StatusCake

## 🔒 **Security**

### **SSL/TLS Certificate**
```bash
# Request certificate from ACM
aws acm request-certificate \
  --domain-name your-domain.com \
  --subject-alternative-names www.your-domain.com \
  --validation-method DNS

# Update ALB listener for HTTPS
aws elbv2 modify-listener \
  --listener-arn YOUR_LISTENER_ARN \
  --port 443 \
  --protocol HTTPS \
  --certificates CertificateArn=YOUR_CERTIFICATE_ARN
```

### **Security Best Practices**
- Enable WAF on CloudFront
- Use IAM roles with least privilege
- Enable VPC Flow Logs
- Regular security updates
- Database encryption at rest
- Secure environment variables

## 🚀 **CI/CD Pipeline**

### **GitHub Actions Workflow**
```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to ECS
        run: |
          # Build, test, and deploy
          docker build -t pet-adoption .
          # Push to ECR and update ECS service
```

## 📈 **Scaling**

### **Auto Scaling**
- ECS Service Auto Scaling
- Application Load Balancer
- DocumentDB Read Replicas
- ElastiCache Cluster Mode

### **Performance Optimization**
- CloudFront CDN
- Redis caching
- Database indexing
- Image optimization
- Gzip compression

## 🔄 **Backup & Recovery**

### **Database Backups**
- DocumentDB automated backups
- Point-in-time recovery
- Cross-region replication

### **Application Backups**
- S3 versioning
- ECS task definition versions
- Infrastructure as Code

## 📞 **Support & Maintenance**

### **Monitoring Checklist**
- [ ] Application health checks
- [ ] Database performance
- [ ] Error rates and logs
- [ ] SSL certificate expiry
- [ ] Security updates
- [ ] Backup verification

### **Regular Tasks**
- Weekly security updates
- Monthly performance review
- Quarterly disaster recovery testing
- Annual security audit

---

## 🎯 **Quick Start Commands**

### **Local Development**
```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

### **Production Deployment**
```bash
# Deploy infrastructure
aws cloudformation create-stack --stack-name pet-adoption --template-body file://aws/cloudformation-template.yaml

# Build and deploy application
docker build -t pet-adoption .
docker tag pet-adoption YOUR_ECR_REPO
docker push YOUR_ECR_REPO
aws ecs update-service --cluster pet-adoption --service pet-adoption-service --force-new-deployment
```

This deployment guide provides a complete production-ready setup for your pet adoption platform! 🐾
