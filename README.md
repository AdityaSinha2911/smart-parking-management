# Cloud-Native Smart Parking Management System

A practical cloud-native Smart Parking Management System built to demonstrate how a normal web application can evolve into a containerized, microservices-based application and then be managed with Kubernetes.

The project is intentionally kept understandable. The main goal is not to build a huge parking platform, but to demonstrate **Docker, microservices, API Gateway, Kubernetes, service discovery, scaling, CI/CD, monitoring, configuration management and security**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [How the System Works](#how-the-system-works)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Authentication](#authentication)
- [Docker Compose](#docker-compose)
- [Run Locally with Docker](#run-locally-with-docker)
- [Run Directly on PC](#run-directly-on-pc)
- [Kubernetes](#kubernetes)
- [Autoscaling](#autoscaling)
- [Monitoring](#monitoring)
- [CI/CD](#cicd)
- [Configuration and Security](#configuration-and-security)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Development Journey](#development-journey)
- [INT363 Concepts Covered](#int363-concepts-covered)
- [Current Scope](#current-scope)
- [Future AWS Evolution](#future-aws-evolution)

---

## Project Overview

The **Cloud-Native Smart Parking Management System** is a web-based application for managing users, vehicles, parking slots and bookings.

The project was developed progressively instead of trying to build a cloud-native system from the beginning:

```text
Simple Application
       ↓
Monolithic Backend
       ↓
Docker
       ↓
Microservices
       ↓
API Gateway
       ↓
Kubernetes
       ↓
HPA / Autoscaling
       ↓
CI/CD
       ↓
Monitoring & Security
```

The idea is to understand not only **how** each technology works, but also **why** it is being introduced.

---

# Features

### User

- Create an account
- Login using email and password
- JWT-based authentication
- View dashboard
- View parking availability
- Book available parking slots
- View bookings
- Logout

### Parking

- View parking slots
- View available/occupied status
- Book available slots
- Backend-driven parking information

### Booking

- Create bookings
- View bookings
- Use the existing Booking API/database

### Cloud-Native Features

- Docker containers
- Docker Compose
- Microservices
- API Gateway
- Kubernetes Deployments
- Kubernetes Services
- ConfigMaps
- Secrets
- Ingress
- Horizontal Pod Autoscaling
- Metrics Server
- GitHub Actions CI
- Logs and monitoring

---

# Architecture

The application has two important layers: the main FastAPI application and the separated microservice architecture.

```text
                         ┌─────────────────────┐
                         │      Frontend       │
                         │ HTML/CSS/JavaScript │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
              FastAPI Backend                API Gateway
                 :8000                         :9000
                     │                             │
                     │                    ┌────────┼────────┐
                     │                    │        │        │
                     │                    ▼        ▼        ▼
                     │                 User    Parking   Booking
                     │                Service   Service   Service
                     │                 :8001     :8002     :8003
                     │
                     └──────────────┐
                                    ▼
                              PostgreSQL
```

The microservices are independently containerized and can be deployed separately.

---

# How the System Works

## Frontend

The frontend uses:

- HTML5
- CSS3
- Vanilla JavaScript
- Fetch API

It communicates with the backend using HTTP REST APIs.

The main frontend pages are:

```text
Login
Create Account
Dashboard
Parking
Bookings
Services
Logout
```

---

## Backend

The main backend is built with **FastAPI**.

Its internal structure separates:

```text
Routes
   ↓
Schemas
   ↓
Services
   ↓
Models
   ↓
Database
```

The backend handles authentication and database-backed application operations.

---

## Microservices

### User Service

Handles user-related operations.

```text
User Service
     ↓
User information
```

### Parking Service

Handles parking-slot operations.

```text
Parking Service
      ↓
Slots
Availability
Status
```

### Booking Service

Handles booking-related operations.

```text
Booking Service
      ↓
Reservations
Bookings
```

---

# API Gateway

The API Gateway provides a common entry point for the microservices.

```text
Client
  ↓
API Gateway :9000
  │
  ├── /users
  │      ↓
  │   User Service :8001
  │
  ├── /parking
  │      ↓
  │   Parking Service :8002
  │
  └── /bookings
         ↓
      Booking Service :8003
```

Inside Docker, services communicate using Docker service names:

```text
http://user-service:8001
http://parking-service:8002
http://booking-service:8003
```

This demonstrates container networking and loose coupling.

---

# Database

The project uses **PostgreSQL**.

The core data is organized around:

```text
Users
Vehicles
Parking Slots
Bookings
```

A simplified relationship is:

```text
User
 │
 ├── Vehicles
 │
 └── Bookings
          │
          ▼
     Parking Slot
```

PostgreSQL is run as a Docker container in the Compose environment.

A named Docker volume is used for PostgreSQL data persistence.

---

# Authentication

Authentication uses JWT.

The login flow is:

```text
Email + Password
       ↓
POST /auth/login
       ↓
FastAPI
       ↓
Find user
       ↓
Verify password hash
       ↓
Generate JWT
       ↓
Return access token
       ↓
Frontend stores token
```

Authenticated requests use:

```text
Authorization: Bearer <token>
```

Passwords are hashed rather than stored as plain text.

---

# Project Structure

```text
smartParkingManagement/
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── database/
│       ├── models/
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       ├── main.py
│       ├── security.py
│       └── dependencies.py
│
├── services/
│   ├── user-service/
│   ├── parking-service/
│   ├── booking-service/
│   └── api-gateway/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── k8s/
│   ├── namespace.yaml
│   ├── user-service.yaml
│   ├── parking-service.yaml
│   ├── booking-service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | FastAPI |
| Language | Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Hashing | pwdlib |
| API | REST |
| Containers | Docker |
| Local Orchestration | Docker Compose |
| Orchestration | Kubernetes |
| Ingress | ingress-nginx |
| Autoscaling | Kubernetes HPA |
| CI/CD | GitHub Actions |

---

# Docker Compose

Docker Compose is used to run the complete application locally.

The main containers are:

```text
Backend          :8000
API Gateway      :9000
User Service     :8001
Parking Service  :8002
Booking Service  :8003
PostgreSQL       :5433 → container 5432
```

Architecture:

```text
                 Docker Compose
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
   Backend         API Gateway       PostgreSQL
    :8000             :9000
                        │
                 ┌──────┼──────┐
                 ▼      ▼      ▼
               User   Parking Booking
               :8001   :8002   :8003
```

---

# Run Locally with Docker

## Prerequisites

Install:

- Docker Desktop
- Git

Check:

```powershell
docker --version
docker compose version
```

## Clone

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd smartParkingManagement
```

## Start everything

```powershell
docker compose up -d
```

## Check containers

```powershell
docker compose ps
```

All required services should be running.

## Test FastAPI

Open:

```text
http://localhost:8000/docs
```

## Test API Gateway

Open:

```text
http://localhost:9000
```

## Start frontend

Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Then open:

```text
http://localhost:5500
```

Using an HTTP server is preferable to opening `index.html` directly because it gives the browser a normal HTTP origin.

## Stop

```powershell
docker compose down
```

## Stop and delete volumes

```powershell
docker compose down -v
```

**Warning:** `-v` removes the PostgreSQL Docker volume and therefore deletes the stored database data.

---

# Run Directly on PC

Docker Compose is recommended, but the backend can also be run directly with Python.

## Requirements

- Python 3.12
- PostgreSQL
- Git

Check:

```powershell
python --version
```

## Create virtual environment

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
```

## Install dependencies

```powershell
pip install -r requirements.txt
```

## Configure PostgreSQL

Create a database named:

```text
parking
```

Then configure the database connection expected by the backend.

Example:

```text
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5433/parking
```

Use the actual username, password and port of your PostgreSQL installation.

## Start backend

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## Start frontend

```powershell
cd frontend
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

# Kubernetes

The project includes Kubernetes manifests for the microservices.

Kubernetes demonstrates:

- Cluster
- Node
- Pods
- Deployments
- ReplicaSets
- Services
- Service discovery
- Load balancing
- ConfigMaps
- Secrets
- Ingress
- Horizontal Pod Autoscaling

---

# Kubernetes Prerequisites

Recommended:

- Docker Desktop
- Kubernetes enabled in Docker Desktop
- kubectl

Check:

```powershell
kubectl version --client
kubectl config current-context
kubectl get nodes
```

The local Docker Desktop context should normally be:

```text
docker-desktop
```

---

# Deploy to Kubernetes

## 1. Namespace

```powershell
kubectl apply -f k8s/namespace.yaml
```

Check:

```powershell
kubectl get namespaces
```

The project uses:

```text
parking
```

## 2. Configuration

```powershell
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
```

## 3. Deploy services

```powershell
kubectl apply -f k8s/user-service.yaml
kubectl apply -f k8s/parking-service.yaml
kubectl apply -f k8s/booking-service.yaml
```

Check:

```powershell
kubectl get deployments -n parking
kubectl get pods -n parking
kubectl get services -n parking
```

---

# Kubernetes Service Discovery

Kubernetes Services provide stable network endpoints for Pods.

Instead of using a Pod IP:

```text
Pod IP → unstable
```

the application can use:

```text
user-service
parking-service
booking-service
```

The Service automatically routes traffic to the available Pods.

```text
Service
   │
   ├── Pod 1
   └── Pod 2
```

If a Pod is replaced, the Service continues providing the stable endpoint.

---

# Kubernetes Replicas

The microservices use multiple replicas.

For example:

```text
User Service
     │
 ┌───┴───┐
 ▼       ▼
Pod 1   Pod 2
```

This improves availability and allows Kubernetes to distribute traffic between Pods.

---

# Ingress

The project uses nginx Ingress.

Check:

```powershell
kubectl get ingressclass
```

You should see:

```text
nginx
```

Apply:

```powershell
kubectl apply -f k8s/ingress.yaml
```

Check:

```powershell
kubectl get ingress -n parking
```

For local Docker Desktop testing:

```powershell
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80
```

Then test the configured route, for example:

```text
http://localhost:8080/users
```

Ingress provides a single external entry point and forwards requests to Kubernetes Services.

---

# Autoscaling with HPA

The project contains:

```text
k8s/hpa.yaml
```

The Horizontal Pod Autoscaler monitors CPU utilization and adjusts the number of Pods.

Conceptually:

```text
Normal Load
     ↓
2 Pods
```

When load increases:

```text
Higher CPU
     ↓
HPA detects target
     ↓
More Pods
     ↓
Traffic distributed
```

Check:

```powershell
kubectl get hpa -n parking
```

The HPA currently targets the `user-service` deployment.

---

# Metrics Server

HPA requires resource metrics.

Check:

```powershell
kubectl top nodes
kubectl top pods -n parking
```

If these commands return CPU and memory values, Metrics Server is working.

For the local Docker Desktop Kubernetes environment, Metrics Server may need:

```text
--kubelet-insecure-tls
```

because local kubelet certificates may not contain the expected IP SAN.

This is a local-development workaround, not a general production security recommendation.

---

# Monitoring

Useful Kubernetes monitoring commands:

### Pods

```powershell
kubectl get pods -n parking
```

### Deployments

```powershell
kubectl get deployments -n parking
```

### Services

```powershell
kubectl get services -n parking
```

### Logs

```powershell
kubectl logs -n parking deployment/user-service
kubectl logs -n parking deployment/parking-service
kubectl logs -n parking deployment/booking-service
```

### Resource usage

```powershell
kubectl top pods -n parking
kubectl top nodes
```

### Events

```powershell
kubectl get events -n parking --sort-by=.lastTimestamp
```

These commands provide basic operational visibility without requiring a large monitoring stack.

---

# CI/CD

The project contains:

```text
.github/workflows/ci.yml
```

The workflow runs on pushes and pull requests involving `main`.

The current CI process:

```text
Developer
   ↓
git push
   ↓
GitHub
   ↓
GitHub Actions
   ↓
Checkout
   ↓
Python setup
   ↓
Install dependencies
   ↓
Backend validation
```

This demonstrates the basic idea of Continuous Integration: every change can be automatically checked.

---

# Configuration and Security

Do not commit:

```text
.env
venv/
__pycache__/
*.pyc
```

Never commit:

- database passwords
- JWT secrets
- API keys
- personal credentials

The project also demonstrates Kubernetes:

```text
ConfigMap
Secret
```

ConfigMaps are intended for normal configuration.

Secrets are intended for sensitive configuration.

For production systems, secrets should be managed using a proper secret-management solution rather than treating a repository file as a secure vault.

---

# Testing the Complete Application

A simple end-to-end test:

```text
Create Account
      ↓
Login
      ↓
Dashboard
      ↓
Parking
      ↓
View availability
      ↓
Book slot
      ↓
Check Bookings
      ↓
Logout
```

### Start backend

```powershell
docker compose up -d
```

### Verify

```powershell
docker compose ps
```

### Start frontend

```powershell
cd frontend
python -m http.server 5500
```

### Open

```text
http://localhost:5500
```

Then test the application through the UI.

---

# Useful Commands

## Docker

```powershell
docker compose up -d
docker compose ps
docker compose logs
docker compose logs backend
docker compose down
```

## Kubernetes

```powershell
kubectl get nodes
kubectl get pods -n parking
kubectl get deployments -n parking
kubectl get services -n parking
kubectl get ingress -n parking
kubectl get hpa -n parking
kubectl top nodes
kubectl top pods -n parking
```

---

# Troubleshooting

## "Cannot reach the backend"

Check:

```powershell
docker compose ps
```

Then:

```powershell
docker compose logs backend
```

Test:

```text
http://localhost:8000/docs
```

---

## Database connection error

Check PostgreSQL:

```powershell
docker compose logs database
```

Remember:

```text
Inside Docker:
database:5432

From your PC:
localhost:5433
```

These are different because Docker uses its internal network.

---

## CORS error

Run the frontend through:

```powershell
python -m http.server 5500
```

instead of opening:

```text
file://...
```

Then make sure the backend/API Gateway allows the frontend origin.

---

## Kubernetes Pod failure

```powershell
kubectl get pods -n parking
```

Then:

```powershell
kubectl describe pod <pod-name> -n parking
```

And:

```powershell
kubectl get events -n parking --sort-by=.lastTimestamp
```

---

## HPA shows unknown metrics

Run:

```powershell
kubectl top nodes
```

If that fails, check the Metrics Server.

---

## Ingress returns 404

Check:

```powershell
kubectl get ingress -n parking
kubectl get ingressclass
kubectl get pods -n ingress-nginx
```

Then:

```powershell
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80
```

---

# Development Journey

The project was intentionally developed step by step.

## Stage 1 — Basic application

The first goal was simply to get the Smart Parking application working with:

- FastAPI
- PostgreSQL
- Users
- Vehicles
- Parking
- Bookings

## Stage 2 — Authentication

JWT authentication and password hashing were added.

```text
Register
   ↓
Login
   ↓
JWT
   ↓
Authenticated requests
```

## Stage 3 — Docker

The application was containerized so that the application environment becomes reproducible.

Docker solves the classic:

> "It works on my machine."

problem by packaging the application and its dependencies together.

## Stage 4 — Docker Compose

Multiple containers were connected with Docker Compose.

One command can now start the local environment:

```powershell
docker compose up -d
```

## Stage 5 — Microservices

The application was separated into:

```text
User Service
Parking Service
Booking Service
```

This introduces independent service boundaries and independent deployment/scaling.

## Stage 6 — API Gateway

The gateway provides a common entry point to the microservices.

## Stage 7 — Kubernetes

The services were deployed using Kubernetes.

This introduced:

- Pods
- Deployments
- Services
- Service discovery
- Replicas
- ConfigMaps
- Secrets
- Ingress

## Stage 8 — HPA

Horizontal Pod Autoscaling was added to demonstrate automatic scaling based on resource utilization.

## Stage 9 — CI/CD

GitHub Actions was added for automated backend validation.

## Stage 10 — Monitoring

Kubernetes logs, metrics and events were used to observe and troubleshoot the system.

---

# INT363 Concepts Covered

This project provides practical demonstrations of:

### Architecture

- Monolith vs Microservices
- Service boundaries
- Loose coupling
- API Gateway
- REST APIs

### Docker

- Dockerfile
- Docker image
- Container
- Port mapping
- Volumes
- Networking
- Docker Compose

### Kubernetes

- Cluster
- Node
- Pod
- Deployment
- ReplicaSet
- Service
- Service discovery
- Load balancing
- ConfigMap
- Secret
- Ingress
- HPA

### DevOps

- Git
- GitHub
- GitHub Actions
- CI/CD

### Security

- Password hashing
- JWT
- Authorization headers
- Configuration/secrets separation

### Operations

- Health checks
- Logs
- Resource metrics
- Kubernetes events
- Autoscaling

---

# Current Scope

This is primarily an academic cloud-native project.

The focus is on understanding architecture and deployment rather than implementing every production-grade feature.

Production systems would additionally require things such as:

- HTTPS/TLS
- Production secret management
- Centralized logging
- Distributed tracing
- Advanced monitoring
- Database migrations
- High-availability PostgreSQL
- Production ingress/domain configuration
- Stronger authorization/RBAC
- Automated production deployment
- Cloud-managed infrastructure

These are outside the minimum scope of the current implementation.

---

# Future AWS Evolution

The same application can later be moved from the local Docker/Kubernetes environment to AWS.

A possible evolution is:

```text
                         AWS
                          │
                         VPC
                          │
                 ┌────────┴────────┐
                 │                 │
                ALB               S3
                 │
                EC2
                 │
          Application Services
          ┌──────┼──────┐
          ▼      ▼      ▼
        User   Parking Booking
          │      │      │
          └──────┼──────┘
                 ▼
                RDS
             PostgreSQL
```

Potential AWS services for the next stage include:

- VPC
- EC2
- RDS
- S3
- Application Load Balancer
- Auto Scaling Groups
- CloudWatch
- Lambda
- Cognito
- CloudFormation

The important idea is that AWS becomes the **next evolution of the same application**, not a separate project.

---

# Final Note

The main lesson of this project is not memorizing commands such as:

```text
docker build
docker compose up
kubectl apply
kubectl get pods
```

The important part is understanding the progression:

```text
Why Docker?
    ↓
Why Microservices?
    ↓
Why API Gateway?
    ↓
Why Kubernetes?
    ↓
Why Services?
    ↓
Why Replicas?
    ↓
Why HPA?
    ↓
Why CI/CD?
    ↓
Why Monitoring?
```

Each technology solves a specific problem.

That is the core idea behind this **Cloud-Native Smart Parking Management System**.

---

## Author

**Aditya Kumar Sinha**

Cloud-Native Smart Parking Management System

Academic project focused on cloud-native application development, containerization, microservices, Kubernetes, CI/CD and scalable system design.
