# MCP Server Process Documentation

This document visualizes the workflow and architecture of the deployed MCP (Model Context Protocol) Server.

## 1. High-Level Communication Flow (Sequence Diagram)

This diagram shows how a client (like Gemini CLI or a Python script) interacts with the hosted MCP Server.

```mermaid
sequenceDiagram
    participant User as User / CLI
    participant Client as Gemini Client (Local)
    participant CloudRun as Cloud Run (HTTPS Load Balancer)
    participant Server as MCP Server (FastMCP)

    Note over User, Client: One-time Setup
    User->>Client: Configure settings.json & Auth
    Client->>CloudRun: Connect to SSE Endpoint (/sse)
    CloudRun->>Server: Forward Connection Request
    Server-->>Client: SSE Connection Established (Event Stream)

    Note over User, Server: Interactive Session
    User->>Client: "Calculate 40 * 2"
    Client->>Client: Analyze Prompt & Select Tool

    par Tool Execution
        Client->>CloudRun: POST /messages (call_tool: multiply)
        CloudRun->>Server: Invoke 'multiply' function
        Server->>Server: Validate Arguments (a=40, b=2)
        Server->>Server: Execute Logic (40 * 2)
        Server-->>CloudRun: Return Result (80)
        CloudRun-->>Client: Return JSON Result
    end

    Client->>User: Display Result ("80")
```

## 2. Request Processing Logic (Flowchart)

This diagram details the internal logic when the MCP Server receives a request.

```mermaid
flowchart TD
    A[Incoming Request] --> B{Request Type?}

    B -- SSE Connect --> C[Establish Event Stream]
    C --> D[Keep Alive / Push Updates]

    B -- POST /messages --> E[Parse JSON Payload]
    E --> F{Method Type}

    F -- tools/list --> G[Return List of Tools]
    G --> G1[add, subtract, multiply]

    F -- tools/call --> H[Identify Tool Name]
    H --> I{Tool Exists?}

    I -- No --> J[Return Error: ToolNotFound]
    I -- Yes --> K[Validate Arguments (Pydantic)]

    K -- Invalid --> L[Return Error: ValidationError]
    K -- Valid --> M[Execute Python Function]

    M --> N{Execution Success?}
    N -- No --> O[Return Error: ExecutionFailed]
    N -- Yes --> P[Wrap Result in CallToolResult]
    P --> Q[Return JSON Response]
```

## 3. Deployment Architecture

```mermaid
graph LR
    User[User Laptop] -- HTTPS --> lb[Google Cloud Load Balancer]
    lb --> Service[Cloud Run Service: mcp-server]

    subgraph Google Cloud Project: mymcp-antigravity-prod
        Service --> Container[Docker Container]
        Container --> Process[uvicorn running FastMCP]
    end
```
