#!/usr/bin/env python2.7
#
# An internal reporting tool that will use information from
# the database to answer several questions
import psycopg2
import sys
import datetime

DBNAME = "news"
# name of the database
TOP_NUMBER = 3
# how many articles are listed in the top


def connect_db(connect_string):
    """Connect to a database."""
    try:
        db = psycopg2.connect(database=connect_string)
    except psycopg2.Error as e:
        print "Unable to connect the database !"
        sys.exit(1)
    else:
        return db


def read_user_choice():
    """Promts the user with the main menu .
    A valid answer must be inserted or 0 to exit the program .
    """
    options = ['0', '1', '2', '3']
    while True:
        response = raw_input("To show the most popular " + str(TOP_NUMBER) +
                             " articles of all time , press 1 ...\nTo " +
                             "show the most popular article authors of " +
                             "all times , press 2 ...\nTo show statistics " +
                             "about request errors , press 3 ...\nTo " +
                             "quit , press 0 ...\nYour choice ? ")
        if response in options:
            return int(response)
        else:
            print "This is not an option ! Please try again !\n"
    return None


def colums_widths(myTable):
    """Calculates the widths of the table's columns .
    The table we are talking about will be filled with information
    taken from our list 'myTable'
    Inputs :
    myTable -- nested list : list of lists of strings
    Outputs :
    widths -- list of table's widths computed based on
    information from 'myTable' ( finding the largest string
    on the list for the corresponding column in the table )
    """
    widths = []
    for index in range(0, len(myTable[0])):
        widths.append(len(myTable[0][index]))
    for indexi in range(1, len(myTable)):
        for indexj in range(0, min(len(myTable[0]), len(myTable[indexi]))):
            widths[indexj] = max(widths[indexj], len(myTable[indexi][indexj]))
    return widths


def build_header(myTable, widths):
    """Build the table's header . Information to make up the
    header is stored in myTable[0] ( list of strings ) .
    Thean a line is drawn .
    Return a string representing the header .
    """
    text = ""
    for index in range(0, len(widths)):
        # centered alignment
        text += ((widths[index] - len(myTable[0][index]))/2 + 1)*" " + \
                myTable[0][index] + ((widths[index] -
                                      len(myTable[0][index]))/2 +
                                     (widths[index] -
                                      len(myTable[0][index])) % 2 + 1)*" "
        if index < len(widths) - 1:
            text += "|"
    text += "\n"
    # draw a line between the header and the rows
    for index in range(0, len(widths)):
        text += (widths[index] + 2)*"-"
        if index < len(widths) - 1:
            text += "+"
    return text + "\n"


def build_rows(myTable, widths):
    """Build the table's rows .
    Return a string adding up the table's rows .
    """
    text = ""
    for indexi in range(1, len(myTable)):
        # left alignment
        for indexj in range(0, min(len(myTable[indexi]), len(myTable[0]) - 1)):
            text += " " + myTable[indexi][indexj] + \
                (widths[indexj] - len(myTable[indexi][indexj]) + 1)*" "
            text += "|"
        if len(myTable[indexi]) < len(myTable[0]):
            for indexj in range(len(myTable[indexi]), len(myTable[0]) - 1):
                text += (widths[indexj]+2)*" " + "|"
        else:
            # align the contents to the right in the last column
            text += (widths[len(myTable[0]) - 1] -
                     len(myTable[indexi][len(myTable[0]) - 1]) + 1)*" " + \
                     myTable[indexi][len(myTable[0]) - 1]
        text += "\n"
    return text


def print_table(myTable):
    """Prints a formatted tzble from information found in the list .
    Inputs : myTable -- the list"""
    formatedTable = ""
    # add table elements to the string
    widths = colums_widths(myTable)
    formatedTable += build_header(myTable, widths)
    formatedTable += build_rows(myTable, widths)
    print formatedTable
    print "\n"


def show_popular_articles(myCursor):
    """Answer the 1st question."""
    sql = "select articles.title, articles_views.views from articles join " + \
          "articles_views on articles.id = articles_views.id order by " + \
          "articles_views.views desc limit " + str(TOP_NUMBER)
    try:
        myCursor.execute(sql)
    except psycopg2.Error as e:
        print "Cannot retrieve data from database !"
        sys.exit(1)
    print "\nThe most popular " + str(TOP_NUMBER) + " articles of all time :"
    print "\n"
    solution = [["title", "views"]]
    for article, views in myCursor.fetchall():
        solution.append([article, str(views)])
    print_table(solution)


def show_popular_authors(myCursor):
    """Answer the 2nd question."""
    sql = "select authors.name, sum(articles_views.views) as total_views " + \
          "from authors, articles, articles_views where authors.id = " + \
          "articles.author and articles.id = articles_views.id group by " + \
          "authors.id order by total_views desc"
    solution = [["author", "views"]]
    try:
        myCursor.execute(sql)
    except psycopg2.Error as e:
        print "Cannot retrieve data from database !"
        sys.exit(1)
    print "\nThe most popular article authors of all time :\n"
    for author, views in myCursor.fetchall():
        solution.append([author, str(views)])
    print_table(solution)


def logs_prompt():
    """Another user prompt for the main menu's 3rd option."""
    options = ['0', '1', '2', '3']
    while True:
        response = raw_input("To print the days when more than 1% of " +
                             "requests lead to errors , press 1 ...\nTo " +
                             "show the percentage of request errors for " +
                             "each day , press 2 ...\nTo show the days " +
                             "with most request errors , press 3 ...\nTo " +
                             "turn back , press 0 ...\nYour choice ? ")
        if response in options:
            return int(response)
        else:
            print "This is not an option ! Please try again !\n"
    return None


def print_error_logs(myCursor, sql):
    """Execute the right querry for the min menu's 3rd option and
    then print the fetched result in a properly fromatted way."""
    solution = [["day", "percentage"]]
    try:
        myCursor.execute(sql)
    except psycopg2.Error as e:
        print "Cannot retrieve data from database !"
        sys.exit(1)
    print "\nError logs ( percentages ) :\n"
    for day, percent in myCursor.fetchall():
        solution.append([day.strftime("%B %d, %Y"),
                         str("%.2f" % round(percent, 2)) + " %"])
        # change the date into the requested format
        # convert the percentage to a 2 decimal points float
    print_table(solution)


def show_error_logs(myCursor):
    """Answer the 3rd question."""
    sql = "select days, percentage from (select errors.day as days, " + \
          "cast(100*(cast(errors.logs as decimal)/cast(totals.logs as " + \
          "decimal)) as decimal) as percentage from (select date(time) " + \
          "as day , count(*) as logs from log group by day) as totals " + \
          "join (select date(time) as day , count(*) as logs from log " + \
          "where not status like '%200%' group by day) as errors on " + \
          "totals.day = errors.day) as err_percent "
    choice = logs_prompt()
    if choice == 1:
        sql += "where percentage > 1"
    elif choice == 2:
        sql += "order by days"
    elif choice == 3:
        sql += "order by percentage desc"
    if choice > 0:
        print_error_logs(myCursor, sql)


def show_logs():
    """The main function."""
    db = connect_db(DBNAME)
    dbCursor = db.cursor()
    while True:
        choice = read_user_choice()
        if choice == 1:
            show_popular_articles(dbCursor)
        elif choice == 2:
            show_popular_authors(dbCursor)
        elif choice == 3:
            show_error_logs(dbCursor)
        else:
            break
    db.close()
    print "\nGoodbye !"


show_logs()
