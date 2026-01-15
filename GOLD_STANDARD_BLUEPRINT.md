# 🏆 The Antigravity Gold Standard Blueprint

This document acts as the definitive template for starting high-quality, modern software projects. It consolidates best practices for development, infrastructure, security, automation, and documentation.

---

## 1. 🛠️ Development Environment & Tooling

**Goal**: Zero-setup time ("clone & run") and strict consistency.

- **Virtual Environments**: Use `venv` (std lib) or `poetry`.
- **Dependency Management**:
  - `requirements.txt`: Production dependencies (locked versions).
  - `requirements-dev.txt`: Development tools (linters, test frameworks).
- **Code Quality (The "Holy Trinity")**:
  - **Ruff**: Ultra-fast Linter & Formatter. Replaces `flake8`, `black`, `isort`.
  - **Mypy**: Static Type Checking. Mandatory for robust Python code.
  - **Pre-commit**: Git hooks that enforce quality _before_ code enters the repo.
- **Version Control**:
  - **Conventional Commits**: Standardized commit messages (e.g., `feat: add user login`, `fix: handle timeout`) to enable automated changelogs.

## 2. 🧪 360° Testing Strategy

**Goal**: Confidence in every change, at every layer.

- **Unit Tests (`pytest`)**:
  - Test individual functions in isolation.
  - Mock external dependencies (databases, APIs).
  - **Coverage**: Target > 80% with `pytest-cov`.
- **Integration Tests**:
  - Test interactions between components (e.g., API <-> DB) locally.
  - Use `test_client.py` pattern for verification.
- **End-to-End (E2E) Tests**:
  - Verify the _deployed_ system (`test_remote.py`).
  - Validate real-world scenarios.
- **Load Testing** (Advanced):
  - Use **Locust** or **k6** to verify performance under stress.
- **Infrastructure Tests**:
  - **TFLint** / `terraform validate`: Ensure IaC is correct.

## 3. 🏗️ Infrastructure as Code (IaC)

**Goal**: Immutable, reproducible infrastructure. No "ClickOps".

- **Tool**: **Terraform** (Industry Standard).
- **State Management**: Remote backend (GCS/S3) with looking enabled.
- **Resource Management**:
  - **Import Existing**: Use `terraform import` to bring legacy resources under control.
  - **Least Privilege**: Atomic Service Accounts for each service.
- **Security Scanning**:
  - **tfsec** / **Trivy**: Scan Terraform code for misconfigurations (e.g., open firewalls) _before_ deploy.

## 4. 📝 Documentation as Code (DaC)

**Goal**: Documentation is living, versioned, and tested with the code.

- **Framework**: **MkDocs** (with Material theme) or **Sphinx**.
  - Write docs in Markdown.
  - Build static sites automatically in CI/CD.
- **Diagrams as Code**:
  - **Mermaid.js**: Define flowcharts and sequence diagrams in text (embedded in Markdown).
  - **C4 Model**: Structure architecture docs (Context, Container, Component, Code).
- **Architecture Decision Records (ADRs)**:
  - Document _why_ major technical decisions were made (`docs/adr/001-use-fastmcp.md`).
- **API Documentation**:
  - Auto-generated OpenAPI (Swagger) specs from code (FastAPI/FastMCP standards).

## 5. 🚀 CI/CD Pipeline (GitHub Actions)

**Goal**: Automate the path from Commit to Production.

- **Authentication**: **Workload Identity Federation** (OIDC). No long-lived JSON keys!
- **Pipeline Stages**:
  1.  **Code Quality**: `ruff`, `mypy`, `pre-commit` (Blocker).
  2.  **Test**: `pytest` (Blocker).
  3.  **Security Scan**: `trivy` (Container scan), `tfsec` (IaC scan).
  4.  **Build**: Docker build (Multi-stage, distroless/slim images).
  5.  **Deploy**: Terraform Apply -> Cloud Run Deploy.
  6.  **Release**: Automated Release Draft based on Conventional Commits.

## 6. 🛡️ Security & Observability

**Goal**: Secure by design and full visibility.

- **Dependencies**: **Dependabot** / **Renovate** to auto-update libraries.
- **Container Security**: Scan images for CVEs in the registry.
- **Observability**:
  - **Structured Logging**: JSON logs for machine parsing.
  - **Tracing**: OpenTelemetry for request flows across microservices.
  - **Error Tracking**: Sentry or Google Cloud Error Reporting.

---

## ⚡ Generic Project Structure

```text
my-awesome-project/
├── .github/
│   ├── workflows/          # CI/CD
│   └── dependabot.yml      # Dependency Updates
├── docs/                   # Documentation as Code
│   ├── adr/                # Decision Records
│   ├── diagrams/           # Mermaid/PlantsUML
│   └── index.md
├── terraform/              # Infrastructure
│   ├── main.tf
│   └── security.tf
├── src/                    # Application Code
├── tests/                  # Pytest Bundle
│   ├── unit/
│   └── integration/
├── .pre-commit-config.yaml # Quality Gates
├── mkdocs.yml              # Doc Config
├── pyproject.toml          # Tool Config
├── Dockerfile              # Container Def
└── README.md               # Entry Point
```
