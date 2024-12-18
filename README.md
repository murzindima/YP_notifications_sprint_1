# Sprint 10

[![Formatters and Linters](https://github.com/murzindima/notifications_sprint_1/actions/workflows/checks.yml/badge.svg)](https://github.com/murzindima/notifications_sprint_1/actions/workflows/checks.yml)
[![Tests](https://github.com/murzindima/notifications_sprint_1/actions/workflows/tests.yml/badge.svg)](https://github.com/murzindima/notifications_sprint_1/actions/workflows/tests.yml)

## Repository Link

https://github.com/murzindima/notifications_sprint_1

## Description

The project is a monorepo with multiple services.
The services are:

- notifications api
- notifications worker
- auth api
- postgres for auth api
- postgres for notifications api
- rabbitmq
- NGINX

The infrastructure is set up using Docker Compose:

```bash
docker-compose up --build
```

All ports but NGINX are not exposed to the host. The services are only accessible through the NGINX proxy.
Configuration made by .env files. Each service has its own .env file in the root of the service directory.

## About the repo structure

notifications_api is a FastAPI service for notifications.
notifications_worker is a Celery worker for notifications.
auth_api is a FastAPI service for authentication and authorization.
nginx is the NGINX proxy.

so, you can find the .env.example file in auth_api_service, notifications_api_service, notifications_admin_panel_service, and notifications_worker_service directories.

About the NGINX hosts. The NGINX is set up to listen to the following hosts:

- notifications-api
- auth-api

You must add the following line to your /etc/hosts file:

```bash
127.0.0.1 auth-api notifications-api
```

The services are accessible through the following URLs:

- auth-api: http://auth-api:8080/api/openapi
- notifications-api: http://notifications-api:8080/api/openapi

## How to prepare the databases

The databases are created automatically. But you must create tables and so on manually.

To create the tables for the auth service, you must run the following command:

```bash
docker exec -it auth_service_spr10 alembic upgrade head
docker exec -it auth_service_spr10 python src/tools/init_db.py create-permissions
docker exec -it auth_service_spr10 python src/tools/init_db.py create-roles
docker exec -it auth_service_spr10 python src/tools/init_db.py assign-permissions-to-roles
docker exec -it auth_service_spr10 python src/tools/init_db.py create-admin a@b.com 123qwe Joe Doe
```

To create the tables for the notifications service, you must run the following command:

```bash
docker exec -it notifications_api_spr10 alembic upgrade head
```

## About the authorization and authentication

Services are authenticated by the auth service. So, you must create a user in the auth service

You can create a local user or use the OAuth2 flow to get the access and refresh tokens.
