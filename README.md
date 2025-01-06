# Ycombinator website scraper

---

This is a program to scrape company information from ycombinator website using selenium and save it into sqlite database using Sqlalchemy
<br>

## Why I create this program ?

---
Well the reason is simple, because I need the data of company in y combinator 

## So, how to use this program ?

---
- First of all you must have python installed in your device, and activate venv (optional). 
- Next install dependencies from requirement.txt file
```
  pip install -r requirements.txt
```

- After all dependencies got installed you can run
```
    main.py
```

## What is collected by this program ?

---
This program will scrape company name, batch, sector, region, company description, founding date, founders, incubator, 
source url and company url. You can save it in a database only or as an Excel and Csv file too. The previous scraping 
database result will stay, in case you lose the Excel file and need to save it 
