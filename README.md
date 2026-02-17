AI-Enabled Claim Status API on Amazon EKS
1. Overview
    This project implements a GenAI-enabled Claim Status API deployed on Amazon EKS (EC2 worker nodes) with full CI/CD automation, IAM role-based security (IRSA), and AI-powered summarization using Amazon Bedrock.
    The solution demonstrates enterprise-grade Kubernetes deployment patterns while integrating GenAI into a business workflow.
    This implementation follows outcome-driven architectural design principles under controlled service constraints.

2. Architecture Overview
    High-Level Flow
    
   Client
     ↓
 Kubernetes Service (EKS)
     ↓
 FastAPI Application
     ↓
 DynamoDB (Claim Data)
     ↓
 Amazon Bedrock (AI Summarization)
 CI/CD:
 GitHub → CodePipeline → CodeBuild → ECR → EKS Deployment
 Security:
 IRSA → IAM Role → Bedrock + DynamoDB permissions

3. AWS Services Used
Service	Purpose
Amazon EKS	Kubernetes control plane
Amazon EC2	Worker nodes
Amazon ECR	Container image repository
Amazon DynamoDB	Claim status data store
Amazon Bedrock	AI summarization
AWS CodePipeline	CI/CD orchestration
AWS CodeBuild	Build + image publish + deploy
IAM (IRSA)	Pod-level permissions
CloudWatch	Logs and metrics

4. Functional Endpoints
1️⃣ Create Claim
     POST /claims


    Creates a new claim record in DynamoDB.
    
    Request:
    
    {
      "user": "John Doe",
      "amount": 250.00,
      "status": "Pending"
    }
    
    
    Response:
    
    {
      "message": "Claim created",
      "claimId": "uuid"
    }
    
    2️⃣ Get Claim
    GET /claims/{claim_id}
    
    
    Fetches claim details from DynamoDB.
    
    3️⃣ Analyze Claim (GenAI)
    POST /analyze
    
    
    Request:
    
    {
      "text": "Customer reported broken screen and is requesting refund."
    }
    
    
    This endpoint:
    
    Invokes Amazon Bedrock (Claude model)
    
    Generates structured AI guidance
    
    Returns summarized next-step recommendations

5. GenAI Integration
    Amazon Bedrock (Claude model) is invoked using:
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    The model is used for:
    Claim text summarization
    Recommendation generation
    Decision support guidance
    The integration uses IRSA for secure credential injection.

6. Security Model
    IAM Roles for Service Accounts (IRSA)
    The Kubernetes service account is mapped to:
    claim-api-irsa-role
    Attached Policies:
    AmazonBedrockFullAccess
    AmazonDynamoDBFullAccess
    Custom IRSA policy
    This ensures:
    No static credentials
    The Least privilege access
    Pod-level IAM isolation

7. CI/CD Pipeline

    Pipeline Stages:
    Source – GitHub
    Build – CodeBuild
    Docker image build
    Push to ECR
    Kubernetes deployment update
    Pipeline ensures:
    Automated image builds
    Versioned deployments
    Repeatable release process

8. Kubernetes Deployment

    Deployment includes:
    2 replicas
    Readiness probe
    LoadBalancer service exposure
    Image from private ECR
    Example:
    
    replicas: 2
    readinessProbe:
      httpGet:
        path: /docs
        port: 8080

9. Observability

    Application logs streamed to CloudWatch
    Kubernetes pod health checks
    Load balancer monitoring
    Bedrock invocation metrics available via AWS console

10. Trade-offs and Design Decisions
    
    Decision	Rationale
    Used LoadBalancer instead of API Gateway	Reduced complexity for lab timeline
    Direct text summarization instead of S3	Simplified GenAI flow
    Used AWS-managed policies	Faster secure setup
    Used EKS EC2 instead of Fargate	Meets lab constraint

11. Lessons Learned

    DynamoDB requires Decimal type for numeric fields
    
    IRSA trust relationship must include sub condition
    
    Bedrock models require first-time use-case approval
    
    NAT gateways incur hidden cost if not cleaned
    
    Image tags must be updated on deployment

12. Cleanup Procedure

    To avoid unnecessary cost:
    
    Delete EKS cluster
    
    Delete NAT Gateway
    
    Delete Load Balancers
    
    Delete ECR repository
    
    Delete DynamoDB table
    
    Delete IAM roles

13. Repository Structure
    
    src/              Application source
    k8s/              Kubernetes manifests
    pipelines/        CI/CD configs
    Dockerfile        Container definition
    requirements.txt  Python dependencies

14. How to Run Locally

    uvicorn main:app --reload


Docker:

    docker build -t claim-api .
    docker run -p 8080:8080 claim-api