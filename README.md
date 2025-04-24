# PES2UG22CS578_596_614_615_LoadBalancedURLShortener

A scalable URL shortener service built with **Flask** and **Redis**, featuring **Kubernetes deployment** and **Horizontal Pod Auto-scaling** (HPA).

---

## Prerequisites

- Docker  
- Minikube  
- kubectl  
- Homebrew (for macOS)

---

## 📁 Project Structure

```
.
├── app/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
└── k8s/
    ├── hpa.yaml
    ├── redis-deployment.yaml
    └── url-shortener-deployment.yaml
```

---

## 🛠️ Week 1: Local Development

### To Run Locally

1. Run Redis container:

   ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```

2. Build the Docker image:

   ```bash
   docker build -t url-shortener ./app
   ```

3. Run the container:

   ```bash
   docker run -d --name url-app --link redis -p 5050:5000 url-shortener
   ```

4. Visit the app at:

   ```
   http://localhost:5050
   ```

> ![URL Shortener Interface](./mdimages/output_week1.png)

### Local Development Setup

1. Copy the environment template:
   ```bash
   cp app/.env.example app/.env
   ```

2. Edit the `.env` file with your configuration

3. Run the application:
   ```bash
   docker-compose up
   ```

---

## Week 2: Kubernetes Deployment

### Setup Steps

1. Start Minikube and configure Docker environment:

   ```bash
   minikube start
   eval $(minikube -p minikube docker-env)
   ```

2. Build and deploy:

   ```bash
   cd app
   docker build -t url-shortener:latest .
   cd ../k8s
   kubectl apply -f redis-deployment.yaml
   kubectl apply -f url-shortener-deployment.yaml
   ```

3. Verify deployment:

   ```bash
   kubectl get pods -l app=redis
   kubectl get pods -l app=url-shortener -w
   kubectl get services
   ```

4. Enable external access:

   - **Terminal 1**:

     ```bash
     minikube tunnel
     ```

   - **Terminal 2**:

     ```bash
     kubectl get service url-shortener-service
     ```

   Access the application at:

   ```
   http://<EXTERNAL-IP>
   ```

---

## Week 3: Auto-scaling Implementation

### Setup Steps

1. Enable HPA:

   ```bash
   minikube addons enable metrics-server
   kubectl apply -f k8s/hpa.yaml
   ```

2. Monitor system:

   ```bash
   kubectl get pods -l app=redis
   kubectl get pods -l app=url-shortener -w
   kubectl get services
   kubectl get hpa
   kubectl top pods
   kubectl get hpa url-shortener-hpa -w
   ```

3. Load testing:

   - Install load testing tool:

     ```bash
     brew install hey
     ```

   - Run test (replace with your actual external IP):

     ```bash
     hey -c 20 -z 60s http://127.0.0.1/
     ```

   - Watch pods scale:

     ```bash
     kubectl get pods -w
     ```
   - Watch cpu get overloaded
     ```bash
     kubectl get hpa url-shortener-hpa -w
     ```

---

## Features

- URL shortening service  
- Redis backend for storage  
- Kubernetes deployment  
- Horizontal Pod Autoscaling (HPA)  
- Load balancing  
- Real-time metrics monitoring

---

## Important Notes

- Keep `minikube tunnel` running in a separate terminal  
- Monitor pod scaling during load tests  
- Ensure `metrics-server` is enabled  
- Use **relative paths** for all K8s YAML files

---

## Troubleshooting

- **Pending pods**:

  ```bash
  kubectl describe pods
  ```

- **HPA issues**:

  ```bash
  kubectl describe hpa url-shortener-hpa
  ```

- **Service access issues**:

  ```bash
  kubectl get events --all-namespaces
  ```

- **Verify metrics server**:

  ```bash
  minikube addons list
  ```
