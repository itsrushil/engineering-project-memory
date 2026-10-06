# Demo Engineering Project Memory

## Project Overview
The project uses a web client, FastAPI backend, service layer and PostgreSQL database.

## Database Decision
The team selected PostgreSQL because the application contains relational users, orders and payments. Transactions and foreign-key constraints are important.

## Authentication
Authentication is implemented in `auth_service.py` and exposed through `routes/auth.py`. Passwords are hashed before storage and a session is created after successful login.

## Registration Flow
A user submits registration details. The backend validates the request, hashes the password, stores the user in PostgreSQL and returns a successful registration response.

## Payment Module
The payment service is called by the order service. Payment status is associated with orders.

## Architecture
The client sends requests to FastAPI. FastAPI routes requests to service modules. Services communicate with PostgreSQL. Authentication and payment are separate service modules.

## Engineering Decision
The team selected RAG for project memory because retrieval reduces irrelevant context and allows source-aware answers.

## Meeting Notes
The team agreed that project decisions should be stored in Markdown meeting notes so future developers can ask why a technology or architecture choice was made.
