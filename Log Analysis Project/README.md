Project Title: Log Analysis

Description:
-----------------------

This project is an internal reporting tool for a newspaper site. It uses information from the already built database, to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page.
Using this information, the project will answer questions about the site's user activity such as:
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors? 


Project Design:
---------------
Here is the high level design for the three questions:

Part 1: What are the most popular three articles of all time? 

1. The "path" column in "log" table has a substring that matches with the slug column in articles table.
2. using this info, join the tables "articles" and "log"
3. for each view of the article, a corresponding entry is found in the log table.
4. by counting the number of rows matching the article, we get the total number of views of that particular article.
5. So fetch the "title" from "articles" and count the number of views by aggregating and grouping.
6. Finally order by the host number of views in descending order, and limit to 3 rows to get the 3 top most viewed articles.

Part 2: Who are the most popular article authors of all time?

1. The "path" column in "log" table has a substring that matches with the slug column in articles table.
2. the "id" column in authors table is the foreign key - "author" in "articles" table
3. using these two criteria, join the tables "authors", "articles" and "log"
4. fetch the authors' names and the total number of views of articles authored by those authors by aggregations.
5. Finally order the final output based on the number of views with the most views on top.

Part 3: On which days did more than 1% of requests lead to errors? 

1. Extract the date from the timestamp
2. create a view that has the data about total number of HTTP requests on each day
3. Create a view that has dataabout total number of errors in HTTP requests on each day
4. Then join the two above views and fetch the rows that have more than 1% requests with error code-404

Project Environment setup:
--------------------------
1) Download the source file LogAnalysis.py and store it in the Vagrant folder.
2) ensure that the newsdata.sql is also present in the same folder
3) Vagrant and Virtual box download links:
https://www.vagrantup.com/downloads.html
https://www.virtualbox.org/wiki/Download_Old_Builds_5_1

Project execution:
------------------
This program in this project will run on command line. It won't take any input from user. Instead it will connect to the database, use SQL queries to analyze the log data, and print out the answer to some questions.
(This project is developed on Vagrant VM, whose configuration was provided by Udacity. The file newsdata.sql was provided which had the database set up)

Steps to execute the project: 
-----------------------------
1) Open command prompt, navigate to the "Vagrant" directory
2) Execute the two commands:
	$vagrant ssh
	$cd /vagrant
3) Execute command: $psql -d news
4) Create the following two views by executing the queries:

	create view total_requests as
	select cast(time :: timestamp at time zone 'America/Los_Angeles' as date) as days, count(*) as total_requests
	from log
	group by days;

	create view error_requests as
	select cast(time :: timestamp at time zone 'America/Los_Angeles' as date) as days, count(*) as errors
	from log
	where substr(status,1,3)='404'
	group by days;
5) execute:  \q command to exit from the psql prompt
6) Now execute the python code: $python3 LogAnalysis.py


