# Ycombinator website scraper

This is a program to gather company information from the Y Combinator website using Selenium and save it into sqlite database using Sqlalchemy. 
<br>

## Why did I create this program?

Well, the reason is simple, because I need the data from the company in ycombinator.com, and I willingly share the code with you

## So, how to use this program?
<ol>
<li>First of all, you must have the latest Python, SQLite database, and a terminal on your device.</li> 
<li>Next, create a virtual environment to keep your environment clean.</li>

```
  python -m venv .venv
```

<li>Don't forget to activate it with:</li>
  <br>

__Windows__

``.venv\Scripts\activate``

__Linux & MacOS__

```
source venv/bin/activate
```
<li>Let's install all required dependency</li> 

```
  pip install -r requirements.txt
```

<li>After all dependencies got installed, you can run</li>

```
   main.py
```
</ol>

### When main.py is running, there will be 3 options

1. Scrape Company
2. Export database
3. Exit
   <br>

<ul>
<li> Scrape Company </li>
<p>As the option's name suggests, you will scrape the company's information from this option. To scrape a company's information, 
you need to fill several parameters, which include the URL, the number of companies to scrape, and the table name</p>

<ol>
• Url 
<p> Take a look at the picture below </p>

![Screenshot 2025-01-07 114134](https://github.com/user-attachments/assets/a0ccc873-5c9c-4d1e-987d-daf7af1682b4)

<ol>
<p> 1. Use the filter to decide what kind of company you're looking for </p>
<p> 2. Copy the URL after choosing the filter and pass it into the URL form</p>
</ol>

<br>
• Number of companies
<p> In this form, you need to fill in the quantity of the company to scrape </p>

<br>
• Table Name
<p> This is a table to save the result inside the database. You can use the existing table, and the program will append to the latest 
column automatically. If you enter a new tablename, the program will use it </p>
<br>

</ol>
<li>
Export database
<p> To perform this option, you will need to fill Table name, File name, Sheet title, and Sheet description. The result will be saved as an Excel and a CSV file in </p>

```
C:\Users\[your_storage_name]\Downloads\Documents
``` 
<ol>
<br>

• Table Name

<p> Table name must be a table that exists in the database</p>

• File name (Optional)

<p> Fill this form with the name you want, or leave it empty and the file's name will be created automatically</p>

• Sheet title and sheet description (Optional)

![ycombinator - Copy](https://github.com/user-attachments/assets/9bf180c6-ecb0-4f3b-9b14-8af6cf9ca0f8)

<p> You can add a title and description according to your needs. If you leave it blank, the program will use the default title 
and description</p>

</ol>
</li>
<li>
Exit
<p> Close the program </p>
<p> You can type exit in any form to close the program</p>
</li>
</ul>


## What does this program collected ?

This program will scrape company name, batch, sector, region, company description, founding date, founders, incubator,
source url and company url. You can save it in a database only or as an Excel and Csv file too. The previous scraping
database result will stay, in case you lose the Excel file and need to save it
