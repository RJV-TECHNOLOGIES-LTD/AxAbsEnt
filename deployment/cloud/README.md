# Super_SQL Cloud Deployment

This directory contains setup files for:

- Kubernetes cluster deployments
- Docker containerization
- Docker Compose for local cloud simulation
- Future Terraform scripts for AWS/GCP/Azure

> Deploying to Kubernetes:
kubectl apply -f kubernetes/deployment.yaml

> Running with Docker Compose:
docker-compose up --build

> To prepare cloud registry:
docker tag super_sql_image:latest your-registry/super_sql:latest
docker push your-registry/super_sql:latest
