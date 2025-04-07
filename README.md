# E-Commerce Sales Report

## Introduction
Welcome to the **E-Commerce Sales Report** project! This project is designed and developed to create an efficient ETL (Extract, Transform, Load) pipeline for processing e-commerce sales data. The primary goal is to ingest, transform, and analyze sales data to provide meaningful insights that support exploratory data analysis and decision-making. By leveraging modern data engineering tools and techniques, this project offers a robust, scalable, and automated solution for managing and visualizing e-commerce sales data effectively.

## Stack
The project is built using a powerful stack of technologies to handle data ingestion, storage, transformation, orchestration, and visualization. The key components include:

- **Python**: Used for implementing the data ingestion process, extracting raw data from e-commerce sources.
- **PostgreSQL**: Serves as the data warehouse to store structured sales data in an organized and accessible format.
- **dbt (Data Build Tool)**: Applied for transforming raw data into actionable insights through cleaning, aggregation, and enrichment.
- **Apache Airflow**: Employed for workflow orchestration and automated scheduling of the ETL pipeline.
- **Apache Superset**: Utilized to develop an interactive dashboard for visualizing data and supporting exploratory analysis.

## Architecture Overview
<img width="956" alt="Ảnh màn hình 2025-04-06 lúc 00 11 32" src="https://github.com/user-attachments/assets/4d55f396-f6da-4129-8496-d05f110d0739" />

The architecture of the **E-Commerce Sales Report** project is designed to ensure a seamless flow of data from ingestion to visualization. The system consists of the following components:

1. **Data Ingestion**:  
   - Raw e-commerce sales data is extracted using Python scripts (represented as the "Data Loader" in the architecture).  
   - The ingested data is loaded into a PostgreSQL database, where it is stored as structured raw data.

2. **Data Storage**:  
   - **PostgreSQL** acts as the central data warehouse, storing both raw and transformed data. It is depicted as a large blue barrel with an elephant logo, highlighting its role as the core storage component.

3. **Data Transformation**:  
   - **dbt** connects to the PostgreSQL database to transform raw data into meaningful insights.  
   - This process involves cleaning, aggregating, and enriching the data, with the transformed results stored back in PostgreSQL (shown as a "Transformed Data" section).

4. **Workflow Orchestration**:  
   - **Apache Airflow** manages the entire ETL pipeline, scheduling and automating tasks such as ingestion and transformation.  
   - It ensures that the workflow runs smoothly and on a predefined schedule, potentially deployed within a Docker container.

5. **Visualization and Reporting**:  
   - **Apache Superset** connects to the PostgreSQL database to access transformed data.  
   - It provides an interactive dashboard (illustrated with graphs) for users to perform exploratory data analysis and generate sales reports.

The overall flow starts with data ingestion via Python, moves through storage and transformation in PostgreSQL with dbt, and ends with visualization in Superset, all orchestrated by Airflow. This architecture ensures scalability, automation, and ease of use.

## Set up
To set up and run the **E-Commerce Sales Report** project locally, follow these step-by-step instructions:

1. **Prerequisites**:   
   - Install **Docker**.  

2. **Clone the Repository**:  
   ```bash
   git clone https://github.com/your-username/e-commerce-sale.git
   cd e-commerce-sale
   ```
2. **Configure Environment**:  
   - Create an `.env` file and add your credentials:  
     ```
     POSTGRES_HOST=host
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=secret
     POSTGRES_DB=database
     SUPERSET_ADMIN=admin
     SUPERSET_PASSWORD=admin
     SUPERSET_SECRET_KEY=secret
     ```
3. **Build Container**:  
   - Run these following command:  
     ```bash
     docker-compose up -d
     ```  

4. **Verify and Explore**:
   - Access the Airflow web UI at `http://localhost:8080` and configure the ETL pipeline DAGs.
   - Check the PostgreSQL database to ensure data is ingested and transformed.  
   - Explore the Superset dashboard to visualize sales insights and generate reports.
<img width="1427" alt="Ảnh màn hình 2025-04-06 lúc 00 22 23" src="https://github.com/user-attachments/assets/61cc218b-4f41-4328-979b-179fb6fbc773" />
<img width="1438" alt="Ảnh màn hình 2025-04-07 lúc 19 21 26" src="https://github.com/user-attachments/assets/eac83738-9fae-4854-9a08-82328a505d4d" />
