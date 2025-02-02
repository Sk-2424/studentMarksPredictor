# AWS CI-CD Pipeline using Github Actions for Deploying Streamlit App

## Overview
This project demonstrates two approaches to deploying a Streamlit application:
1. **AWS CI/CD Pipeline** using GitHub Actions, Docker, and AWS services.
2. **Streamlit Cloud Deployment** for quick and easy deployment.

---

## Approach 1: AWS CI-CD Pipeline
### Steps to Deploy on AWS

### 1. Create a Dockerfile
Create a `Dockerfile` in the root of your project:
```dockerfile
# Use official Python 3.9 image as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the entire project in app directory
COPY . /app

# Install dependencies
RUN apt update -y && apt install awscli -y

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 unzip -y && pip install -r requirements.txt

# Expose the Streamlit default port (8501)
EXPOSE 8501

# Set the default command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
```

### 2. Build a Docker Image
Run the following command to build the Docker image:
```bash
docker build -t my-streamlit-app .
```

### 3. Setup GitHub Actions for CI/CD
1. Create a `.github/workflows/` folder in your repository.
2. Add a YAML config file for automation.

### 4. Create an IAM User in AWS
- Go to **AWS IAM Console** → Create User
- Assign permissions:
  - `AWSEC2ContainerRegistryFullAccess`
  - `AWSEC2FullAccess`
- Generate **Access Key** and **Secret Key**, then store them securely.

### 5. Create a Repository in AWS Elastic Container Registry (ECR)
- Open **AWS ECR** and create a repository (Public or Private).
- Copy the repository URL for future use.

### 6. Launch an EC2 Instance
- Select **Ubuntu** as the OS.
- Choose **free-tier** options.
- Create a **key pair** (if not already created).
- Launch the instance.

### 7. Configure EC2 Security Group for Streamlit
- Go to **EC2** → **Security Groups**.
- Edit **Inbound Rules** → Add Rule:
  - Protocol: `Custom TCP`
  - Port: `8501`
  - Source: `0.0.0.0/0` (open to all, for testing purposes)

### 8. Connect to EC2 and Setup Docker
Run the following commands to install Docker:
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

### 9. Set Up GitHub Self-Hosted Runner
- Go to **GitHub → Settings → Actions → Runners → Linux**
- Run the following commands:
```bash
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.321.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.321.0/actions-runner-linux-x64-2.321.0.tar.gz
echo "ba46ba7ce3a4d7236b16fbe44419fb453bc08f866b24f04d549ec89f1722a29e actions-runner-linux-x64-2.321.0.tar.gz" | shasum -a 256 -c
tar xzf ./actions-runner-linux-x64-2.321.0.tar.gz
```
- Configure the runner:
```bash
./config.sh --url https://github.com/Sk-2424/studentMarksPredictor --token YOUR_GITHUB_RUNNER_TOKEN
```
- Name the runner as `self-hosted`.
- ./run.sh

### 10. Add Secrets in GitHub
- Go to **GitHub → Settings → Security → Actions**
- Add AWS secrets:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
  - `ECR_REPOSITORY_URL`

### 11. Test CI/CD Pipeline
- Make a change in the code, commit, and push.
- The GitHub runner should trigger and deploy the app automatically.

---

## Approach 2: Deploy on Streamlit Cloud
For a simpler deployment, use Streamlit Cloud:

### Steps to Deploy
1. Push your code to **GitHub**.
2. Go to [Streamlit Cloud](https://share.streamlit.io/).
3. Click **New App** → Connect GitHub Repository.
4. Select the repository and branch.
5. Click **Deploy**.
6. The app will be accessible at: [Student Performance Predictor](https://studentperformancesk.streamlit.app/)

---

## Conclusion
- **AWS CI/CD Pipeline** is useful for enterprise-level deployment with scalability.
- **Streamlit Cloud** is great for quick and easy deployments.

