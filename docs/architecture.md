# MyMCP Architecture

This document describes the architecture of the **MyMCP** project using the C4 model.

## 1. System Context Diagram
The **MyMCP** system allows users to interact with... (Context TBD based on deeper requirements, utilizing generic web app context for now).

```mermaid
C4Context
    title System Context for MyMCP
    Person(user, "User", "A user of the MyMCP application")
    System(mymcp, "MyMCP System", "Serverless Web Application hosted on Cloud Run")
    System_Ext(clerk, "Clerk", "Handles User Authentication")
    System_Ext(github, "GitHub", "Hosting and CI/CD")
    Rel(user, mymcp, "Uses", "HTTPS")
    Rel(mymcp, clerk, "Authenticates via", "OIDC/API")
    Rel(github, mymcp, " deploys to", "CI/CD")
```

## 2. Container Diagram
The system consists of a Next.js Frontend and a Serverless Backend.

```mermaid
C4Container
    title Container Diagram for MyMCP
    Person(user, "User", "A user of the application")
    System_Boundary(mymcp, "MyMCP") {
        Container(frontend, "Frontend Web App", "Next.js", "Delivers the UI and handles client-side logic")
        Container(backend, "Backend API", "Python/FastAPI", "Handles core business logic (Serverless)")
        ContainerDb(db, "Database", "Cloud SQL / Firestore", "Stores application data (TBD)")
    }
    System_Ext(clerk, "Clerk", "Identity Provider")
    Rel(user, frontend, "Visits", "HTTPS")
    Rel(frontend, backend, "API Calls", "JSON/HTTPS")
    Rel(frontend, clerk, "Authenticates", "SDK")
    Rel(backend, db, "Reads/Writes", "SQL/NoSQL")
```

## 3. Deployment View (Google Cloud Run)
We use a serverless deployment model.

```mermaid
C4Deployment
    title Deployment Diagram
    Deployment_Node(gcp, "Google Cloud Platform", "Cloud Provider") {
        Deployment_Node(cloud_run, "Cloud Run", "Serverless Container Platform") {
            Container(instance, "MyMCP Instance", "Docker Container", "Next.js + Backend")
        }
    }
    Deployment_Node(github_actions, "GitHub Actions", "CI/CD") {
        Container(runner, "CI Runner", "Ubuntu", "Builds and Deploys")
    }
    Rel(github_actions, cloud_run, "Deploys", "gcloud run deploy")
```
