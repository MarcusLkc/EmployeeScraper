# Inspirarion

This Webscraper was requested by a Friend of mine named Brian.
It solves an age old problem that still occurs today...
People did not automate tasks before the script
their would be an employee visiting this website:
https://appext20.dos.ny.gov/lcns_public/roster_cursor?p_record_id=11000080984&p_display_start=47&

and would have to copy links by hand page by page to create an excel database of the companies employees
and this was done regularly because of the constantly updating website

This webscraper shortens that job from weeks to minuites
Here is a demo!

![workingscript](https://user-images.githubusercontent.com/26131181/48509839-2a3c6a00-e820-11e8-9149-250553e4a8a4.gif)

# How to Use

To use this application just run the main.py file and it will run through the entire process grab every link
from all individual pages then use those links to generate dynamic URL for Scraping Employee table
data then save it to a file called 'employees.xlsx'
Usage:

```python
python main.py
```

# Changing Departments

The script by default is set to my friends department and the base Url of that department
If you would like to use a different department feel free
to edit the base_url of the IdCollector class after initialization

example:

```python
id_collector = IdCollector(base_url=[your_base_url])
links = id_collector.collect_data()
employee_records = EmployeeRecords(links)
employee_records.collect_data()
employee_records.save()
```
