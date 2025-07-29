# Deployment Guide: Anime Recommender System with LLMOps

Deploy your Streamlit-based LLM-powered anime recommendation system using Docker, Kubernetes (Minikube), and Google Cloud Platform VM with comprehensive monitoring.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Google Cloud VM Setup](#google-cloud-vm-setup)
4. [Environment Configuration](#environment-configuration)
5. [Docker Installation](#docker-installation)
6. [Kubernetes Setup](#kubernetes-setup)
7. [Application Deployment](#application-deployment)
8. [Access Configuration](#access-configuration)
9. [Monitoring Setup](#monitoring-setup)
10. [Troubleshooting](#troubleshooting)
11. [Cleanup](#cleanup)

---

## Prerequisites

Before starting, ensure you have:

- Google Cloud Platform account with billing enabled
- GitHub repository with your anime recommender code
- GitHub Personal Access Token
- GROQ API Key
- HuggingFace API Token
- Basic knowledge of Docker and Kubernetes

---

## Project Structure

Your project should include these essential files:

```
anime-recommender/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── llmops-k8s.yaml       # Kubernetes deployment
├── values.yaml           # Grafana monitoring config
└── README.md
```
---

## Google Cloud VM Setup

### 1. Create VM Instance

1. Visit: [GCP Console](https://console.cloud.google.com/)
2. Navigate to **Compute Engine** → **VM Instances** → **Create Instance**
3. Configure your instance:

   **Basic Configuration:**
   - **Name:** `anime-llmops-vm`
   - **Region:** Choose closest to your users (e.g., `us-central1`)
   - **Zone:** `us-central1-a`

   **Machine Configuration:**
   - **Machine Type:** `e2-standard-4` (4 vCPU, 16 GB memory)
   - **Architecture:** `x86/64`

   **Boot Disk:**
   - **Operating System:** `Ubuntu`
   - **Version:** `Ubuntu 24.04 LTS`
   - **Boot disk type:** `Balanced persistent disk`
   - **Size:** `100 GB`

   **Firewall:**
   - Allow HTTP traffic
   - Allow HTTPS traffic

4. Click **Create** and wait for the instance to start

### 2. Configure Firewall Rules

Create firewall rule for Streamlit access:

```bash
gcloud compute firewall-rules create allow-streamlit \
    --allow tcp:8501 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow Streamlit access"
```

### 3. SSH into VM

Use the SSH button from GCP Console or:

```bash
gcloud compute ssh anime-llmops-vm --zone=us-central1-a
```

---

## Environment Configuration

### 1. Update System Packages

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl wget git vim htop
```

### 2. Interlink your Github on VSCode and on VM

```bash
git config --global user.name "your-username"
git config --global user.email "your-email@example.com"
```

### 3. Clone Your Repository

```bash
git clone https://github.com/your-username/your-anime-repo.git
cd your-anime-repo
```

When prompted for credentials:
- **Username:** Your GitHub username  
- **Password:** Your GitHub Personal Access Token

> 💡 **Tip:** Generate a token at [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
>  Enable repo, workflow, admin:org, admin:repo_hook, admin:org_hook while generating personal access token.

---

## Docker Installation

### 1. Install Docker Engine

Follow the official Docker installation guide:

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
sudo apt-get update

# Install Docker Engine
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Test Docker installation
sudo docker run hello-world
```

### 2. Configure Docker for Non-Root User

```bash
# Create docker group and add user
sudo groupadd docker
sudo usermod -aG docker $USER

# Apply group membership
newgrp docker

# Enable Docker service
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

### 3. Verify Docker Installation

```bash
docker run hello-world
docker --version
```

If you see the "Hello from Docker!" message, Docker is installed correctly.

---

## Kubernetes Setup

### 1. Install Minikube

```bash
# Download and install Minikube
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

# Verify installation
minikube version
```

### 2. Install kubectl

```bash
# Install kubectl via snap
sudo snap install kubectl --classic

# Verify installation
kubectl version --client
```

### 3. Start Minikube Cluster

```bash
# Start Minikube with sufficient resources
minikube start

# Verify cluster status
minikube status
kubectl cluster-info
kubectl get nodes
```

Expected output should show your cluster is running.

---

##  Application Deployment

### 1. Point Docker to Minikube Registry

```bash
# Configure Docker to use Minikube's Docker daemon
eval $(minikube docker-env)
```

### 2. Build Docker Image

```bash
# Build your application image
docker build -t llmops-app:latest .

# Verify image was built
docker images | grep llmops-app
```

### 3. Create Kubernetes Secrets

```bash
# Create secrets for API keys
kubectl create secret generic llmops-secrets \
  --from-literal=GROQ_API_KEY="your-groq-api-key-here" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="your-huggingface-token-here"

# Verify secrets were created
kubectl get secrets
```

### 4. Deploy to Kubernetes

```bash
# Apply the deployment configuration
kubectl apply -f llmops-k8s.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=llmops-app --timeout=300s
```

### 5. Verify Deployment

```bash
# Check pod logs
kubectl logs -l app=llmops-app

# Check service status
kubectl describe service llmops-service
```

---

## Access Configuration

### Option A: Port Forwarding (Recommended for Development)

```bash
# Forward port 8501 to access the application
kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0
```

Access your application at: `http://YOUR-VM-EXTERNAL-IP:8501`

### Option B: Minikube Tunnel (For LoadBalancer Access)

In a new terminal session:

```bash
# Start tunnel (keep this running)
minikube tunnel
```

In another terminal:

```bash
# Get external IP
kubectl get svc llmops-service
```

### Option C: NodePort Service (Alternative)

Modify your service in `llmops-k8s.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: llmops-service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8501
    nodePort: 30001
  selector:
    app: llmops-app
```

Then access via: `http://YOUR-VM-EXTERNAL-IP:30001`

---

## Monitoring Setup with Grafana Cloud

### 1. Create Monitoring Namespace

```bash
kubectl create namespace monitoring
```

### 2. Install Helm

```bash
# Download and install Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

# Verify installation
helm version
```

### 3. Set Up Grafana Cloud Integration

1. Sign up at [Grafana Cloud](https://grafana.com/products/cloud/)
2. Go to your Grafana Cloud stack
3. Navigate to **Observability** → **Kubernetes** → **Start sending data**
4. Configure the integration:
   - **Cluster name:** `minikube`
   - **Namespace:** `monitoring`
   - Select **Kubernetes** as platform
   - Keep other settings as default
   - Create new access token (name it `minikube-token`) and save it securely

### 4. Create Values File

```bash
# Create and edit the values file
vi values.yaml
```

**Important Steps:**
1. Copy the entire Helm configuration from Grafana Cloud UI
2. **Remove the initial command part** (save it separately for later use):
   ```bash
   # SAVE THIS COMMAND (you'll need it in step 5):
   helm repo add grafana https://grafana.github.io/helm-charts &&
     helm repo update &&
     helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
       --namespace "monitoring" --create-namespace --values - <<'EOF'
   ```
3. **Remove the final `EOF` line** from the values.yaml file
4. Paste only the YAML configuration content into values.yaml
5. Save the file with `:wq!`

### 5. Deploy Grafana Monitoring Stack

Use the saved command from step 4, but modify it to use your values.yaml file:

```bash
# Add Grafana Helm repository and deploy
helm repo add grafana https://grafana.github.io/helm-charts &&
  helm repo update &&
  helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
    --namespace "monitoring" --create-namespace --values values.yaml
```

**Success indicator:** You should see `STATUS: deployed REVISION: 1`

### 6. Verify Deployment

```bash
# Check if all pods are running
kubectl get pods -n monitoring
```

### 7. Access Dashboards

Visit your Grafana Cloud instance to view:
- Kubernetes cluster metrics
- Application performance metrics  
- Resource utilization
- Custom dashboards

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Pod Not Starting

```bash
# Check pod status and events
kubectl describe pod -l app=llmops-app

# Check pod logs
kubectl logs -l app=llmops-app --tail=50
```

#### 2. Image Pull Errors

```bash
# Verify Docker environment is set
eval $(minikube docker-env)

# Rebuild image
docker build -t llmops-app:latest .
```

#### 3. Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints llmops-service

# Verify firewall rules
gcloud compute firewall-rules list --filter="name:allow-streamlit"
```

#### 4. Resource Issues

```bash
# Check resource usage
kubectl top nodes
kubectl top pods

# Scale down if needed
kubectl scale deployment llmops-deployment --replicas=1
```

### Useful Commands

```bash
# Restart deployment
kubectl rollout restart deployment llmops-deployment

# Check cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

# Access pod shell
kubectl exec -it deployment/llmops-deployment -- /bin/bash

# View all resources
kubectl get all -o wide
```

---

## Cleanup

### Stop Services

```bash
# Delete deployment
kubectl delete -f llmops-k8s.yaml

# Delete secrets
kubectl delete secret llmops-secrets

# Delete monitoring (if installed)
helm uninstall grafana-k8s-monitoring -n monitoring
kubectl delete namespace monitoring
```

### Stop Minikube

```bash
# Stop Minikube cluster
minikube stop

# Delete cluster (optional)
minikube delete
```

### Cleanup GCP Resources

```bash
# Delete firewall rule
gcloud compute firewall-rules delete allow-streamlit

# Delete VM instance
gcloud compute instances delete anime-llmops-vm --zone=us-central1-a
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Grafana Cloud Documentation](https://grafana.com/docs/grafana-cloud/)

---
> 💡 **Important:** Remember to monitor your GCP usage to avoid unexpected charges. Consider setting up billing alerts and resource quotas for cost management.
