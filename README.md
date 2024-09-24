# Overview
Analytical Model supporting the strategic expansion of PropTech company Prello by identifying optimal locations in France for the deployment of property hunters. Built using SQL, Python (incl. NumPy, Pandas and Scikit-Learn) and Power BI.

# Context
Prello, founded in 2021, is a pioneering proptech company specializing in the sale and management of second homes. With a mission to transform the second home market, Prello offers options for both co-purchase and single purchase, along with comprehensive services such as legal support, renovations, Airbnb rental management, and co-owner collaboration. To strategically expand their reach, Prello aims to identify optimal areas for deploying property hunters.

My goal is to devise a scoring system for French towns, ranking them from most to least attractive for Prello’s operations, using abundant open-source data from France to build the analytical model.

# Data Structure
The database structure consists of 6 tables, with a combined 4,738,212 total records.

The primary key for each table is "municipality_code".

![2024-09-24 (1)](https://github.com/user-attachments/assets/f2181293-ffcb-4e80-8cdd-7f760910c099)

Data Lineage:

![2024-09-24 (7)](https://github.com/user-attachments/assets/b368faf5-71cd-473f-9caa-a33361fd493d)


# KPIs
The rankings were calculated based on 3 KPIs:
- Profitability (Average Sale Price): Prello charges 8% on property or share value, so high-end areas more profitable for the company
- Housing Stress Level: Areas with unaffordable rent or living conditions / high default rates are penalised
- Tourism "Score": Quantifying the number and importance of tourist sites in the area. Higher tourism demand increases rental opportunities

The KPIs were then weighted and tested to fine tune the model until results matched intuitions regarding optimal locations for second homes

![2024-09-24 (5)](https://github.com/user-attachments/assets/9227df17-a032-450d-abad-bcee3820917e)

# Insights

- Sharp decline from top scores, suggesting there are small percentage of locations significantly more optimal with respect to the KPI criteria
- Majority of top ranking locations situated on the coast, fitting with general intuitions about second homes

![2024-09-24 (6)](https://github.com/user-attachments/assets/a9ff708a-0e65-408c-bc9c-44326ca9d53c)







