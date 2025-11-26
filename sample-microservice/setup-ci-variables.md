# GitLab CI/CD Variables Setup

## Required Variables in GitLab

Go to your project: Settings → CI/CD → Variables

Add these variables:

### Docker Registry (GitLab Internal Registry)
- `CI_REGISTRY_USER` = gitlab-ci-token
- `CI_REGISTRY_PASSWORD` = ${CI_JOB_TOKEN} (this is automatic)

### Kubernetes (for later stages)
- `KUBECONFIG_DEV` = [Base64 encoded kubeconfig for dev cluster]
- `KUBECONFIG_STAGING` = [Base64 encoded kubeconfig for staging cluster]

### Optional
- `TRIVY_USERNAME` = (if using private Trivy DB)
- `TRIVY_PASSWORD` = (if using private Trivy DB)

## GitLab Runner Configuration

Make sure your runner is configured with:
- Docker executor
- Privileged mode enabled (for dind)
- Volumes: ["/certs/client", "/cache"]

## Registry Setup

The pipeline uses GitLab's built-in container registry at:
`localhost:5005/root/sample-microservice`
