# Multi-Tenant Python Service Execution Platform

## Overview
This platform is a dynamic, multi-tenant Python service execution framework. It allows different tenants to deploy and execute their own services independently while sharing a common runtime framework. Services are loaded dynamically at runtime using Python’s `importlib` and can be executed either synchronously or asynchronously via a background executor.

The architecture cleanly separates the shared execution engine from tenant-owned business logic, enabling flexibility without compromising stability.

## CI/CD with GitHub Actions
Each tenant uses a GitHub Actions pipeline to build its deployable artifact. The pipeline flow is as follows:

1. Checkout tenant service repository
2. Checkout shared framework repository at a pinned version
3. Install shared + tenant dependencies
4. Copy tenant services and configuration into the framework runtime
5. Build a single consolidated Docker image

## Security Model

Identity and access management is enforced using a sidecar-based approach. The sidecar intercepts inbound requests and applies security policies before the requests reach the service execution framework.

### Fine-Grained Authorization (Optional)
Fine-grained authorization can be enabled through LDAP integration. When enabled:

* The sidecar authenticates incoming requests
* User and group information is resolved via LDAP
* Authorization policies are evaluated per tenant, per service, and per operation
* Only authorized service executions are forwarded to the framework

