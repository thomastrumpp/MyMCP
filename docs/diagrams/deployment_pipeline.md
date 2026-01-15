# Deployment Pipeline (CI/CD)

This diagram illustrates the modern Infrastructure as Code and Deployment workflow.

```mermaid
flowchart TD
    subgraph Local [Local Development]
        Dev[Developer]
        Code[Source Code]
        Terraform[Terraform Config]
        Tests[Unit Tests (pytest)]
    end

    subgraph Github [GitHub Actions]
        Lint[Linting (Ruff)]
        Test_CI[Run Tests]
        Build[Build Docker Image]
        Push[Push to Artifact Registry]
        Deploy[Deploy to Cloud Run]
    end

    subgraph GCP [Google Cloud Platform]
        AR[Artifact Registry]
        CR[Cloud Run Service]
        IAM[IAM & Workload Identity]
    end

    Dev -->|Commit & Push| Code
    Code -->|Trigger| Lint
    Terraform -->|Apply (Local/CI)| IAM

    Lint --> Test_CI
    Test_CI --> Build
    Build -->|Push Image| AR
    AR -->|Pull Image| Deploy
    Deploy -->|Update Service| CR

    IAM -.->|OIDC Auth| Github
```
