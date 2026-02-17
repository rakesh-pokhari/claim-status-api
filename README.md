Claim Processing API – EKS + DynamoDB + Bedrock
 Overview

This project is a cloud-native claim processing microservice built using:

FastAPI (Python)

Amazon EKS (Kubernetes)

Amazon DynamoDB

Amazon Bedrock (Claude 3 Haiku)

Amazon ECR

AWS CodePipeline + CodeBuild (CI/CD)

IRSA (IAM Roles for Service Accounts)

The system allows:

Creating insurance claims

Storing them in DynamoDB

Running AI-based claim analysis using Amazon Bedrock

🏗 Architecture
Client (curl / Swagger UI)
        ↓
Application Load Balancer
        ↓
Kubernetes Service (EKS)
        ↓
FastAPI Pod
        ↓
IRSA Role (Secure IAM Access)
        ↓
DynamoDB (Claims Storage)
        ↓
Amazon Bedrock (AI Analysis)

📦 Features
1️⃣ Create Claim

POST /claims

Stores claim in DynamoDB table claims.

Example request:

{
  "user": "Test",
  "amount": 1000,
  "status": "Pending"
}

2️⃣ Analyze Claim (AI Powered)

POST /analyze

Uses Amazon Bedrock (Claude 3 Haiku) to analyze claim text.

Example:

{
  "text": "Customer reported broken screen and is requesting refund."
}


Returns AI-generated analysis.

🔐 Security Design

This project follows AWS best practices:

✅ IRSA (IAM Roles for Service Accounts)

Pods assume a dedicated IAM role:

Access to DynamoDB

Access to Bedrock

No static AWS credentials stored anywhere.

✅ Private Container Registry

Images stored in:

Amazon ECR

✅ CI/CD Pipeline

Source: GitHub

Build: CodeBuild

Push: ECR

Deploy: Kubernetes rolling update

🛠 Deployment Steps
1️⃣ Build Docker Image
docker build -t claim-status-api .

2️⃣ Push to ECR
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/claim-status-api:latest

3️⃣ Deploy to EKS
kubectl apply -f deployment.yml
kubectl apply -f service.yml

4️⃣ Get Load Balancer URL
kubectl get svc


Access:

http://<load-balancer-url>/docs

🗄 DynamoDB Table

Table name: claims

Primary Key:

claim_id (String)

🤖 Bedrock Model Used

Model:

Claude 3 Haiku (Serverless)

Used for:

Claim reasoning

Refund eligibility guidance

Structured AI output
