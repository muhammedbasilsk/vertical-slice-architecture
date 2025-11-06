# Kubernetes Deployment with Minikube

This guide will help you deploy the Vertical Slice Architecture API to a local Minikube cluster.

## Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed
- [Docker](https://docs.docker.com/get-docker/) installed

## Quick Start

### 1. Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=4096 --driver=docker

# Enable the metrics-server addon (optional, for monitoring)
minikube addons enable metrics-server
```

### 2. Build the Docker Image

Build the application image using Minikube's Docker daemon:

```bash
# Point your shell to Minikube's Docker daemon
eval $(minikube docker-env)

# Build the image (run from project root)
docker build -t vertical-slice-api:latest .

# Verify the image is available
docker images | grep vertical-slice-api
```

### 3. Deploy to Kubernetes

Apply all Kubernetes manifests in order:

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap and Secret
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Create PersistentVolumeClaim
kubectl apply -f k8s/postgres-pvc.yaml

# Deploy PostgreSQL
kubectl apply -f k8s/postgres.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n vertical-slice --timeout=120s

# Deploy API
kubectl apply -f k8s/api.yaml

# Wait for API to be ready
kubectl wait --for=condition=ready pod -l app=api -n vertical-slice --timeout=120s
```

Or apply all manifests at once:

```bash
kubectl apply -f k8s/
```

### 4. Access the Application

Get the Minikube service URL:

```bash
# Get the API service URL
minikube service api -n vertical-slice --url

# Or open in browser
minikube service api -n vertical-slice
```

The API will be accessible at the returned URL. Common endpoints:

- `http://<minikube-ip>:<port>/` - Root endpoint
- `http://<minikube-ip>:<port>/health` - Health check
- `http://<minikube-ip>:<port>/api/docs` - API documentation (Swagger UI)
- `http://<minikube-ip>:<port>/api/v1/users` - Users endpoint
- `http://<minikube-ip>:<port>/api/v1/orders` - Orders endpoint

## Monitoring and Debugging

### Check Pod Status

```bash
# List all pods in the namespace
kubectl get pods -n vertical-slice

# Get detailed pod information
kubectl describe pod <pod-name> -n vertical-slice

# View pod logs
kubectl logs <pod-name> -n vertical-slice

# Follow logs in real-time
kubectl logs -f <pod-name> -n vertical-slice
```

### Check Services

```bash
# List all services
kubectl get svc -n vertical-slice

# Get service details
kubectl describe svc api -n vertical-slice
kubectl describe svc postgres -n vertical-slice
```

### Check Deployments

```bash
# List deployments
kubectl get deployments -n vertical-slice

# Get deployment details
kubectl describe deployment api -n vertical-slice
kubectl describe deployment postgres -n vertical-slice
```

### Check PersistentVolumeClaim

```bash
# List PVCs
kubectl get pvc -n vertical-slice

# Get PVC details
kubectl describe pvc postgres-pvc -n vertical-slice
```

### Execute Commands in Pods

```bash
# Access PostgreSQL shell
kubectl exec -it <postgres-pod-name> -n vertical-slice -- psql -U postgres -d vertical_slice_db

# Access API container shell
kubectl exec -it <api-pod-name> -n vertical-slice -- /bin/bash
```

## Scaling

### Scale API Pods

```bash
# Scale to 3 replicas
kubectl scale deployment api -n vertical-slice --replicas=3

# Verify scaling
kubectl get pods -n vertical-slice -l app=api
```

### Autoscaling (HPA)

```bash
# Create Horizontal Pod Autoscaler
kubectl autoscale deployment api -n vertical-slice --cpu-percent=70 --min=2 --max=5

# Check HPA status
kubectl get hpa -n vertical-slice
```

## Updating the Application

### Update the Image

```bash
# Rebuild the image
eval $(minikube docker-env)
docker build -t vertical-slice-api:latest .

# Restart the deployment to use the new image
kubectl rollout restart deployment/api -n vertical-slice

# Watch the rollout status
kubectl rollout status deployment/api -n vertical-slice
```

## Port Forwarding (Alternative Access Method)

Instead of using Minikube service, you can use port forwarding:

```bash
# Forward API port to localhost
kubectl port-forward -n vertical-slice svc/api 8000:8000

# Access at http://localhost:8000
```

## Cleanup

### Delete All Resources

```bash
# Delete all resources in the namespace
kubectl delete namespace vertical-slice

# Or delete individual resources
kubectl delete -f k8s/
```

### Stop Minikube

```bash
# Stop Minikube
minikube stop

# Delete Minikube cluster (removes all data)
minikube delete
```

## Configuration

### Modifying Database Credentials

To change PostgreSQL credentials:

1. Update `k8s/secret.yaml` with base64-encoded values:
   ```bash
   echo -n "newpassword" | base64
   ```

2. Apply the updated secret:
   ```bash
   kubectl apply -f k8s/secret.yaml
   ```

3. Restart the pods:
   ```bash
   kubectl rollout restart deployment/postgres -n vertical-slice
   kubectl rollout restart deployment/api -n vertical-slice
   ```

### Modifying Application Configuration

Edit `k8s/configmap.yaml` and apply changes:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl rollout restart deployment/api -n vertical-slice
```

## Troubleshooting

### Pods Not Starting

```bash
# Check events
kubectl get events -n vertical-slice --sort-by='.lastTimestamp'

# Check pod logs
kubectl logs <pod-name> -n vertical-slice --previous
```

### Image Pull Errors

If you see `ImagePullBackOff` errors:

1. Ensure you're using Minikube's Docker daemon:
   ```bash
   eval $(minikube docker-env)
   ```

2. Rebuild the image:
   ```bash
   docker build -t vertical-slice-api:latest .
   ```

3. Verify `imagePullPolicy: Never` is set in `k8s/api.yaml`

### Database Connection Issues

```bash
# Check PostgreSQL logs
kubectl logs -l app=postgres -n vertical-slice

# Verify PostgreSQL is ready
kubectl exec -it <postgres-pod-name> -n vertical-slice -- pg_isready -U postgres

# Test database connection from API pod
kubectl exec -it <api-pod-name> -n vertical-slice -- python -c "from shared.database import engine; print(engine.connect())"
```

### Service Not Accessible

```bash
# Check Minikube IP
minikube ip

# Check service endpoints
kubectl get endpoints -n vertical-slice

# Check if Minikube tunnel is needed (for LoadBalancer services)
minikube tunnel
```

## Advanced Configuration

### Using Ingress

To expose the API via Ingress:

1. Enable Ingress addon:
   ```bash
   minikube addons enable ingress
   ```

2. Create an Ingress resource (example in `k8s/ingress.yaml` - to be created if needed)

3. Update your `/etc/hosts` file to map the Ingress hostname to Minikube IP

## Resource Requirements

- **API Pod**: 256Mi-512Mi memory, 250m-500m CPU
- **PostgreSQL Pod**: 256Mi-512Mi memory, 250m-500m CPU
- **Persistent Storage**: 1Gi for PostgreSQL data

## Architecture

```
┌─────────────────────────────────────┐
│         Minikube Cluster            │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  Namespace: vertical-slice    │ │
│  │                               │ │
│  │  ┌─────────┐    ┌──────────┐ │ │
│  │  │   API   │───▶│ Postgres │ │ │
│  │  │  (x2)   │    │   (x1)   │ │ │
│  │  └────┬────┘    └─────┬────┘ │ │
│  │       │               │      │ │
│  │  ┌────▼────┐    ┌─────▼───┐ │ │
│  │  │ Service │    │   PVC   │ │ │
│  │  │NodePort │    │   1Gi   │ │ │
│  │  └─────────┘    └─────────┘ │ │
│  │                               │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

## Next Steps

- Set up Ingress for better routing
- Configure TLS/SSL certificates
- Set up monitoring with Prometheus/Grafana
- Implement CI/CD pipeline
- Configure resource limits and requests based on load testing
- Set up network policies for security
