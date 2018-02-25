# This file contains Log Analysis reporting code
# which analyses the the "news" database,
# that has data about authors,articles and an entry in
# the log table whenever a user views the article

import psycopg2


def get_popularArticles():
    """This function queries the datsbase and fetches the most
    popular articles by aggregating the total number of views
    of all the articles"""

    db = psycopg2.connect(database="news")
    cursor = db.cursor()
    query = '''select articles.title, count(*) as views
            from log, articles
            where substr(log.path,10)=articles.slug
            group by articles.title
            order by views desc limit 3;'''
    cursor.execute(query)
    articlesData = cursor.fetchall()
    db.close()
    return articlesData


def get_popularAuthors():
    """ This function queries the datsbase and fetches the authors' names
    and lists them down based on their popularity by aggregating
    total number of views of all the articles authored by them respectively"""

    db = psycopg2.connect(database="news")
    cursor = db.cursor()
    query = '''select authors.name, count(*) as views
            from authors, articles, log
            where authors.id = articles.author
            and substr(log.path,10)=articles.slug
            group by authors.name order by views desc;'''
    cursor.execute(query)
    authorsData = cursor.fetchall()
    db.close()
    return authorsData


def get_errorData():
    """This function queries the news database and fetches the data
    regarding the days when there were more than 1% errors in
    HTTP requests """
    db = psycopg2.connect(database="news")
    cursor = db.cursor()
    query = '''select total_requests.days, errors*100/total_requests as percentage
            from error_requests, total_requests
            where error_requests.days = total_requests.days
            and (errors*100/total_requests > 1);'''
    cursor.execute(query)
    errorData = cursor.fetchall()
    db.close()
    return errorData


def generate_report():
    """This function generates the final report by calling the above
    three functions and renders the output by formatting the report"""
    # Fetch the top 3 most viewed articles and number of views
    popular_articles = get_popularArticles()
    print('\nThe three top most articles viewed are:\n')
    for article in popular_articles:
        print(article[0] + '\t-\t' + str(article[1]) + '  views \n')

    # Fetch the most popular authors
    popular_authors = get_popularAuthors()
    print('\nThe list of authors being listed as per their popularity:\n')
    for author in popular_authors:
        print(author[0] + '\t-\t' + str(author[1]) + '  views \n')

    # Fetch the days when there were more than 1% errors in HTTP requests
    print('\nDays when there were more than 1% errors in HTTP :\n')
    error_data = get_errorData()
    for day in error_data:
        print(str(day[0]) + '\t-\t' + str(day[1]) + '% \n')


generate_report()
