# Read in our SQL saving functions
from SQLSaver import *

# Create a new database
create_database('Test.db')

# Open a connection to the database
conn = create_connection('Test.db')

# Generate our data
my_page = {'name': 'PythonCourse2019', 'id': 12345}
my_link = 'www.github.com/RydenButler/PythonCourse2019'

# Enter our page data into the database
insert_page(conn, my_page, my_link)
# Commit the change
conn.commit()

# Generate some more data
## Note that this is a list of dictionaries
my_posts = [{'id': 1, 'message': 'Hello world!', 'created_time': '11:18AM', 'page_id': 12345}, 
{'id': 2, 'message': 'Hello again, world!', 'created_time': '12:20PM', 'page_id': 12345}]

# Enter our posts data into the database
insert_posts(conn, my_posts)
# Before you commit this, SELECT * FROM Posts in SQL
## Now commit the change and try again
### Commit early and often when scraping
conn.commit()

# Generate our likes data
my_post_likes = [{'id': 12345, 'name': 'Ryden Butler', 'WUSTLID': 901, 'post_id': 2},
{'id': 23456, 'name': 'Jeremy Siow', 'WUSTLID': 902, 'post_id': 2},
{'id': 34567, 'name': 'Ipek Sener', 'WUSTLID': 903, 'post_id': 2},
{'id': 45678, 'name': 'Ben Noble', 'WUSTLID': 904, 'post_id': 2},
{'id': 12345, 'name': 'Ryden Butler', 'WUSTLID': 901, 'post_id': 1},
{'id': 23456, 'name': 'Jacob Montgomery', 'WUSTLID': 006, 'post_id': 1}]

# Enter it into the database
insert_likes(conn, my_post_likes)
# Commit the final change
conn.commit()
# And close the connection
## If we want to add more data we'll need to run create_connection again
conn.close()