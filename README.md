# Development Process

## Planning and Analysis

### Project Initiation

The project is aim to design a real world application that perform sentiment analysis and market research base on social media data. 

The goals are increase the productivity of individuals and SMEs by reducing the resources they need for product and market research.

For the timelines, there are 3 stages of the project. First, research and implementation of LLM for sentiment analysis .Second, develop the high level architecture of the platform, including UX and UI design. Third, implementation and testing of the platform.

Regarding the stakeholders and corresponding role, Jeffery responds for market LLM research, Hayden responds for UX and UI design and Chevy responds implementation.

### Feasibility Study

## Tech Stack

### Overview

- Backend: Flask, SQLAlchemy
- Frontend: HTML, CSS, JavaScript, Apex Charts
- Database: SQLite
- Machine Learning: Hugging Face Transformers (RoBERTa)
- Containerization: Docker

## System Overview

The high-level architecture of the platform, is receiving product or subject input from user, then we collect social media data regarding the product/subject, finally generate sentiment analysis and metric. 

![Platform workflow.png](attachment:ef9906e9-3548-440b-8aaf-28d26b3c8ee4:Platform_workflow.png)

For the search function design, the platform will send a check request to the database first before collecting data from internet, in order to shorten the response time. 

Here’s the search and report page of the platform

![Individual Search Page(1).jpg](attachment:2ec0d0fc-e5cb-490f-8402-b17bece84acf:Individual_Search_Page(1).jpg)

![Individual Report Page.jpg](attachment:82ecfd08-4720-4f85-9bd2-b2ed15441eb1:Individual_Report_Page.jpg)

![SMEs Quick Search Site.png](attachment:8edf659a-e1d3-40aa-93c3-ec7c238e015d:SMEs_Quick_Search_Site.png)

![Product Sentiment Table.jpg](attachment:f3e78d0d-a47c-438a-8a27-70ab6bd54d8b:Product_Sentiment_Table.jpg)

## Development Process

### Backend Development

1. Set up Flask and Blueprint for modularity
2. Implement models for Search, Product, and Sentiment_table using SQLAlchemy
3. Implement the data_collector class that collect social media posts and comments and pass to the analyst class.
4. Implement the analyst class that integrate the RoBERTs model for sentiment analysis with the data collected from data_collector class and save the result as sentiment_table model in the database
5. Develop the presenter class to process and format data for visulization.

### Frontend Development

1. Designed the UI using HTML and CSS
2. Used ApexCharts for interactive visualizations (e.g. sentiment bar chart, time series trends).
3. Styled the navigation bar and sidebar for a clean and responsive layout.

![image.png](attachment:d13a2bc9-624f-4ad8-b788-0963dc9ad569:image.png)

### Database

1. Used SQLite for local development
2. Created relationships between User, Search,  Product, and Sentiment_table models.

![drawSQL-image-export-2025-04-08.png](attachment:669f5f34-d949-4af8-ae22-af0309d1b8b1:drawSQL-image-export-2025-04-08.png)

## System Design

There are three main classes: the analyst class, data collector class, and presenter class.

The analyst class receives product objects from the search function and passes them to the data collector class to gather social media data.

The data collector class handles the logic of data collection, including data limits and time periods, to optimize the platform's response time.

The presenter class formats data for visualization.

The presenter class queries the database for product data and reshapes it for HTML rendering.

![Platform workflow.png](attachment:305f7ec1-a550-46f8-b99c-f7780f8b7434:Platform_workflow.png)
