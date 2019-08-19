import sqlite3
from sqlite3 import Error

def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file, timeout = 30000)
    return conn
  except Error as e:
    print(e)
  return None


def create_table(conn, create_table_sql):
  try:
    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.commit()
  except Error as e:
    print(e)


def create_database(database_name):
  sql_create_Users_table = """ CREATE TABLE IF NOT EXISTS Users (
                            WUSTL_id integer PRIMARY KEY,
                            Facebook_id text UNIQUE,
                            user_name text NOT NULL
                            ); """
  sql_create_Pages_table = """CREATE TABLE IF NOT EXISTS Pages (
                            page_id text PRIMARY KEY,
                            page_name text NOT NULL,
                            page_link text NOT NULL
                            );"""
  sql_create_Posts_table = """CREATE TABLE IF NOT EXISTS Posts (
                            post_id text PRIMARY KEY,
                            post_text text NOT NULL,
                            post_time text NOT NULL,
                            page_id text NOT NULL,
                            FOREIGN KEY (page_id) REFERENCES Pages (page_id)
                            );"""
  sql_create_Likes_table = """CREATE TABLE IF NOT EXISTS Likes (
                            id integer PRIMARY KEY,
                            post_id text NOT NULL,
                            WUSTL_id integer NOT NULL,
                            FOREIGN KEY (post_id) REFERENCES Posts (post_id),
                            FOREIGN KEY (WUSTL_id) REFERENCES Users (WUSTL_id),
                            CONSTRAINT UQ_Like UNIQUE (post_id, WUSTL_id)
                            );"""
  # create a database connection
  conn = create_connection(database_name)
  if conn is not None:
    # create users table
    create_table(conn, sql_create_Users_table)
    # create pages table
    create_table(conn, sql_create_Pages_table)
    # create pages table
    create_table(conn, sql_create_Posts_table)
    # create pages table
    create_table(conn, sql_create_Likes_table)
  else:
    print("Error! cannot create the database connection.")
  conn.close()

def insert_page(conn, page_data, page_link): 
  sql = ''' INSERT OR IGNORE INTO Pages(page_id, page_name, page_link)
            VALUES(?,?,?) '''
  cur = conn.cursor()
  cur.execute(sql, [page_data['id'], page_data['name'], page_link])
  return cur.lastrowid

def insert_posts(conn, post_data): 
  sql = ''' INSERT OR IGNORE INTO Posts(post_id, post_text, post_time, page_id)
            VALUES(:id, :message, :created_time, :page_id) '''
  cur = conn.cursor()
  cur.executemany(sql, post_data)
  return cur.lastrowid

def insert_likes(conn, like_data):
  cur = conn.cursor()
  cur.executemany('INSERT OR IGNORE INTO Users(WUSTL_id, Facebook_id, user_name) VALUES(:WUSTLID, :id, :name)', like_data)
  cur.executemany('INSERT OR IGNORE INTO Likes(post_id, WUSTL_id) VALUES(:post_id, :WUSTLID)', like_data)
  return cur.lastrowid
