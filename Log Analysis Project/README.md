About this project:
-----------------------

This project is an internal reporting tool for a newspaper site. It uses information from the already built database, to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page.
Using this information, the project will answer questions about the site's user activity such as:
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors? 

Project execution:
------------------
This program in this project will run on command line. It won't take any input from user. Instead it will connect to the database, use SQL queries to analyze the log data, and print out the answer to some questions.
(This project is developed on Vagrant VM, whose configuration was provided by Udacity. The file newsdata.sql was provided which had the database set up)

Project Environment setup:
--------------------------
1) Download the source file LogAnalysis.py and store it in the Vagrant folder.
2) ensure that the newsdata.sql is also present in the same folder

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

