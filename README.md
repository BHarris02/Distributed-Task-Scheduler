# Distributed Task Scheduler

## Overview
The Distributed Task Scheduler is a microservices-based system for scheduling, managing, and monitoring tasks across distributed worker nodes

## Features
- RESTful API for task scheduling and monitoring
- Distributed worker nodes for task execution
- Scalable and cloud-deployable architecture

## Technologies
- Python (Flask/FastAPI) for Scheduler Service
- Java (Spring Boot) for Worker Nodes
- MySQL for task metadata storage
- RabbitMQ for message queuing
- AWS, Terraform, Ansible for cloud deployment and configuration

## Architecture
The system consists of:
1. A Scheduler Service (Python) for task management
2. Worker Nodes (Java) for task execution
3. A MySQL database for storing task details
4. A Message Queue (RabbitMQ) for dispatching tasks

## Getting Started
### Prerequisites
- Python 3.x, Java 11+, MySQL, RabbitMQ
- Docker (optional for containerized development)

### Clone the Repository
```bash
git clone https://github.com/your-username/distributed-task-scheduler.git
cd distributed-task-scheduler
