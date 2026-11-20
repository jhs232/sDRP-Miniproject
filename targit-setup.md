# F-Klub TARGIT setup on Windows

Use these settings to reproduce the working setup from [targit-setup.pdf](targit-setup.pdf) on the other Windows VM. The dashboard refers to the TARGIT connection by name, so name it exactly `FKlub`.

## 1. PostgreSQL and the warehouse

Use PostgreSQL **16** on the Windows VM. The working database was set up with the native Windows installer.

| Setting | Value |
| --- | --- |
| Host | `localhost` |
| Port | `5432` |
| Database | `fklub_bi` |
| Schema | `public` |
| Login and database owner | `fklub_admin` |
| Login password | `secretpassword` |

For a fresh database, run these two statements as the PostgreSQL administrator, outside a transaction. If the login and database already exist, use those and confirm the settings above.

```sql
CREATE ROLE fklub_admin LOGIN PASSWORD 'secretpassword';
CREATE DATABASE fklub_bi OWNER fklub_admin;
```

From the repo root in PowerShell with Python 3.13 installed, load the supplied F-Klub CSVs:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

The loader runs [schema.sql](schema.sql) and reloads the warehouse tables. On an already-loaded database that only needs the new view, run [schema.sql](schema.sql) as `fklub_admin` in `fklub_bi`. It creates or replaces `public.date_olap` without reloading the warehouse. The view provides the integer `year_month_key` used by the model's **Month** level for chronological sorting.

The working warehouse had **500,060** rows in `public.sale`, covering **1996–2017**. This query checks the data and the view:

```sql
SELECT count(*) FROM public.sale;
SELECT date_id, year_month_key FROM public.date_olap ORDER BY date_id LIMIT 5;
```

## 2. Windows ODBC

Use **psqlODBC 17.00.0010 (64-bit)** and select the **PostgreSQL Unicode(x64)** driver. That version matches both working VMs. Version 18.00.0005 could connect and query rows on this VM, but column discovery through `MSDASQL` failed and the TARGIT Data Model Editor returned HTTP 500. Port 5432 alone did not resolve it. [Official psqlODBC 17.00.0010 installers](https://www.postgresql.org/ftp/odbc/releases/REL-17_00_0010/)

Open **ODBC Data Sources (64-bit)** as administrator. Under **System DSN**, add or configure:

| Field | Value |
| --- | --- |
| Data Source | `FKlub` |
| Database | `fklub_bi` |
| Server | `localhost` |
| Port | `5432` |
| User Name | `fklub_admin` |
| Password for the connection test | `secretpassword` |
| SSL Mode | `disable` |

Click **Test**, then save the DSN. If you replace the driver while TARGIT is running, restart the Windows service **TARGIT Server** (`ANTServer`) so it picks up the driver.

## 3. TARGIT Server and connection

This VM uses TARGIT Decision Suite **2026.Q4, build 26.10.5006**, with **TARGIT Server** and **TARGIT Client** installed. The demo license worked on this VM after the key in the PDF failed validation. Use the existing valid license on the other PC if TARGIT is already installed.

In TARGIT Management, connect to `localhost`, then go to **Connections → Add → Relational Database → Generic**.

| Field | Value |
| --- | --- |
| Connection name | `FKlub` |
| Description | Blank |
| OLE DB provider | Microsoft OLE DB Provider for ODBC Drivers (`MSDASQL.1`) |
| Data source name | `FKlub` |
| User ID | `fklub_admin` |
| Password | `secretpassword` |
| Allow saving password | Checked |
| Initial catalog | Blank. The DSN selects `fklub_bi`. |

The saved connection string on the working server is:

```text
Provider=MSDASQL.1;Password=secretpassword;Persist Security Info=True;User ID=fklub_admin;Data Source=FKlub
```

Run **Test connection on server**, then save. Open **Edit data model** and verify that `public.sale` expands to show columns. This checks column discovery in addition to connectivity.

## 4. Import the matching model and open the dashboard

1. In TARGIT Management, right-click **FKlub → Edit data model → Import**. Select [`targit/fklubdatamodel_7.xml`](targit/fklubdatamodel_7.xml) and save. This export matches the live model and includes **F-Klub Sales**, **Calendar Days**, and the virtual cube **F-Klub Sales Analysis**.
2. Copy [`targit/fklub_bq1.xview`](targit/fklub_bq1.xview) into the other PC's TARGIT **Shared** documents using the Designer client. The repo copy is an earlier save than the current server dashboard. To bring the latest saved version, copy **fklub_bq1** from this VM's Shared documents to your transfer folder first. The live file is also at `C:\ProgramData\TARGIT\ANTServer\VFS\Global\fklub_bq1.xview`. [TARGIT document copy instructions](https://community.targit.com/hc/en-us/articles/13168996401180-Copy-paste-documents-between-client-and-file-system)
3. Open **fklub_bq1** in Designer and confirm the dashboard objects return data. The document uses the `FKlub` connection and refers to the cube names in the imported model.
