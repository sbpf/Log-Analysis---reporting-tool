#!/usr/bin/env python3 for Python 3

# This file contains Log Analysis reporting code
# which analyses the the "news" database,
# that has data about authors,articles and an entry in
# the log table whenever a user views the article

import psycopg2


def get_articles_query():
    """This function returns the query string to fetch the most
    popular articles by aggregating the total number of views
    of all the articles"""

    query = '''select articles.title, count(*) as views
            from log, articles
            where substr(log.path,10)=articles.slug
            group by articles.title
            order by views desc limit 3;'''

    return query


def get_authors_query():
    """ This function returns the query to fetch authors' names
    and lists them down based on their popularity by aggregating
    total number of views of all the articles authored by them respectively"""

    query = '''select authors.name, count(*) as views
            from authors, articles, log
            where authors.id = articles.author
            and substr(log.path,10)=articles.slug
            group by authors.name order by views desc;'''

    return query


def get_errorData_query():
    """This function returns the query to fetch data
    regarding the days when there were more than 1% errors in
    HTTP requests """

    query = '''select total_requests.days, errors*100/total_requests as percentage
            from error_requests, total_requests
            where error_requests.days = total_requests.days
            and (errors*100/total_requests > 1);'''

    return query


def execute_query(query):
    """This function takes a query in string format as input,
    creates a database connection object and passes the query to execute().
    This function returns the results of the query in the form of tuples"""

    db = psycopg2.connect(database="news")
    cursor = db.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()
    db.close()
    return query_result


def print_top_articles(popular_articles):
    """Prints the most viewed articles"""

    print('\nThe three top most articles viewed are:\n')
    for article in popular_articles:
        print(article[0] + '\t-\t' + str(article[1]) + '  views \n')


def print_authors(popular_authors):
    """Prints the list of authors listed in order of the popularity"""

    print('\nThe list of authors being listed as per their popularity:\n')
    for author in popular_authors:
        print(author[0] + '\t-\t' + str(author[1]) + '  views \n')


def print_error_data(error_data):
    """This function prints the days when there were more than 1% errors"""

    print('\nDays when there were more than 1% errors in HTTP :\n')
    for day in error_data:
        print(str(day[0]) + '\t-\t' + str(day[1]) + '% \n')


def generate_report():
    """This function renders the output by generating the final report"""

    # Fetch the top 3 most viewed articles and number of views and print them
    articles_query = get_articles_query()
    popular_articles = execute_query(articles_query)
    print_top_articles(popular_articles)

    # Fetch the most popular authors and print them
    authors_query = get_authors_query()
    popular_authors = execute_query(authors_query)
    print_authors(popular_authors)

    # Print the days when there were more than 1% errors in HTTP requests
    errors_query = get_errorData_query()
    error_data = execute_query(errors_query)
    print_error_data(error_data)


if __name__ == '__main__':
    generate_report()
