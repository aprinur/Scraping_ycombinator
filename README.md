# Ycombinator website scraper
This is a program to scrape company information from ycombinator website using selenium and save it into sqlite database using Sqlalchemy
<br>

## Why I create this program ?

Well the reason is simple, because I need the data of company in y combinator, and i willingly share the code to you

## So, how to use this program ?

- First of all you must have python installed in your device, and then activate venv ( **Optional** ). 
- Next install dependencies from requirement.txt file
```
  pip install -r requirements.txt
```

- After all dependencies got installed you can run
```
    main.py
```
- When main.py is running, there will be 3 options

1. Scrape Company
2. Export database into xlsx and csv file
3. Exit
<br>

<ul>
<li> Scrape Company </li>
<p>As the option's name, you will scrape the company's information from this option. To scrape company's information 
you need to fill several parameters which is Url, Number of company to scrape and Table name</p>

<ol>
• Url 
<p> Take a look on the picture below </p>

![Screenshot 2025-01-07 114134](https://github.com/user-attachments/assets/a0ccc873-5c9c-4d1e-987d-daf7af1682b4)
<ol>
<p> 1. Use the filter to decide what kind of company you're loking for </p>
<p> 2. Copy the url after choosing the filter and pass it into Url form</p>
</ol>

<br>
• Number of company
<p> In this form you need to fill amount of company to scrape </p>

<br>
• Table Name
<p> This is a table to save the result inside database, you can use existing table and the program will append to latest 
column automatically </p>
<br>

</ol>
<li>
Export database into xlsx and csv file 
<p> To perform this option you will need to fill Table name, File name, Sheet title and Sheet description</p>
<ol>
<br>

• Table Name
<p> Table name must be a table that exist in the database</p>

• File name ( __Optional__ )
<p> Fill this form with the name you want or leave it empty and the file's name will created automatically</p>

• Sheet title and sheet description ( __Optional__ ) 

![ycombinator - Copy](https://github.com/user-attachments/assets/9bf180c6-ecb0-4f3b-9b14-8af6cf9ca0f8)

<p> You can add a title and description according your needs. If you leave it blank, the program will use the default title 
and description</p>

</ol>
</li>
<li>
Exit
<p> Close the program </p>
</li>
</ul>

## What does this program collected ?

This program will scrape company name, batch, sector, region, company description, founding date, founders, incubator, 
source url and company url. You can save it in a database only or as an Excel and Csv file too. The previous scraping 
database result will stay, in case you lose the Excel file and need to save it 
