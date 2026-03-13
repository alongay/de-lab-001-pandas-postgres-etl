# Metabase Setup Guide: Connecting to the Warehouse

To finalize **Lab 7**, follow these steps to connect Metabase to your production data.

## 1. Access Metabase
Open your browser and navigate to: [http://localhost:3010](http://localhost:3010)

## 2. Initial Setup
1. Click **Let's get started**.
2. Create your admin account (e.g., `admin@pde.lab`).
3. When asked to **Add your data**, select **PostgreSQL**.

## 3. Connection Details (The Warehouse)
Use the following settings to connect to the main platform warehouse:

| Field | Value |
| :--- | :--- |
| **Name** | `PDE Warehouse` |
| **Host** | `postgres` (internal Docker hostname) |
| **Port** | `5432` |
| **Database** | `de_workshop` |
| **Username** | `de_user` |
| **Password** | `de_password` |

> [!NOTE]
> We use the hostname `postgres` because both Metabase and the Postgres container are sharing the `pde_platform_net` network.

## 4. Troubleshooting
If Metabase cannot reach the database:
- Run `.\task.ps1 platform-status` to ensure the `pde_postgres_15` container is healthy.
- Ensure the `platform_net` (pde_platform_net) hasn't been accidentally deleted.
