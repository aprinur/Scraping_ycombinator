# Y Combinator Website Scraper

This program gathers company information from the Y Combinator website using Selenium and saves it into a SQLite database with SQLAlchemy.  
I made it because I needed the data myself, and I’m happy to share the code with you.

---

## Why did I create this program?

Simple: I needed company data from ycombinator.com, and I thought, why not make the scraper and share it so others can benefit too?

---

## How to use this program

1. **Install Python, SQLite, and a terminal**  
   Make sure you have the latest Python installed, SQLite database available, and a working terminal.

2. **Create a virtual environment** (to keep your environment clean)
   ```
   python -m venv .venv
   ```

3. **Don't forget to activate it with:**

   __Windows__
   
   ```
   .venv\Scripts\activate
   ```
   
   __Linux & MacOS__
   
   ```
   source venv/bin/activate
   ```
4. Let's install all required dependency

   ```
     pip install -r requirements.txt
   ```
   
5. After all dependencies got installed, you can run

   ```
      python main.py
   ```


## Program menu

When you run `main.py`, you will see 3 options:

<ol>
<li>Scrape Company</li>

   <p>As the name suggests, this option scrapes company information. You will be asked for:</p>

<ul>
<li>Url</li> 
<p> Go to the Y Combinator site, apply the filters you want, then copy the resulting URL and paste it here.</p>
<p>Example: </p>

![Screenshot 2025-01-07 114134](https://github.com/user-attachments/assets/a0ccc873-5c9c-4d1e-987d-daf7af1682b4)

<br>
<li>Number of companies</li> 
<p> How many companies you want to scrape.</p>


<li>Table Name</li>
<p> If the table exists, the data will be appended. If it’s new, a new table will be created. </p>
<br>
</ul>


<li>Export database</li>
<p> To perform this option, you will need to fill Table name, File name, Sheet title, and Sheet description. The result will be saved as an Excel and a CSV file in </p>

```
C:\Users\[your_storage_name]\Downloads\Documents
```
<br>

<ul>

<li>Table Name</li>

<p> Table name must be a table that exists in the database</p>

<li>File name (Optional)</li>
<p> Fill this form with the name you want, or leave it empty and the file's name will be created automatically</p>

<li>Sheet title and sheet description (Optional)</li>

![ycombinator - Copy](https://github.com/user-attachments/assets/9bf180c6-ecb0-4f3b-9b14-8af6cf9ca0f8)

<p> You can add a title and description according to your needs. If you leave it blank, the program will use the default title 
and description</p>

</ul>


<li>Exit</li>
<p>Close the program.</p>
<em>(Tip: you can also type exit in any form to quit immediately.)</em>
</ol>


## What does this program collected ?

<p>The scraper collects:</p>
<ul>
<li>Company name</li>

<li>Batch</li>

<li>Sector</li>

<li>Region</li>

<li>Description</li>

<li>Founding date</li>

<li>Founders</li>

<li>Incubator</li>

<li>Source URL</li>

<li>Company URL</li>
</ul>

<p>You can store the data in the database only, or export it as Excel/CSV as well.
Previous database entries are kept, so even if you lose the exported file, you can re-export it.</p>

## Notes on Console Output

<p>When running this scraper, you might see messages like:</p>

```DevTools listening on ....```
<p>and</p> 

```WARNING: All log messages before absl::InitializeLog() is called are written to STDERR ... ```

<p>These are **not errors**.</p>
They come from Chrome/Chromium’s internal machine learning and speech processing modules, which load automatically when Selenium starts Chrome.
They have no effect on your scraping process and can be safely ignored.



