
CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS posts
              (ID             SERIAL PRIMARY KEY,
              TITLE           TEXT    NOT NULL,
              CONTENT         TEXT,
              USER_ID         TEXT,
              PUBLISHDAY      date,
              IMG             bytea
                ); '''

CREATE_USER_TABLE = '''CREATE TABLE IF NOT EXISTS users(
              USER_ID         TEXT PRIMARY KEY,
              NAME            TEXT,
              PHONE           TEXT,
              EMAIL           TEXT
                )'''

CREATE_LIKE_TABLE = '''CREATE TABLE IF NOT EXISTS likes(
                    USER_ID            TEXT,
                    POST_ID            TEXT)'''

CREATE_COMMENT_TABLE = '''CREATE TABLE IF NOT EXISTS comments(
                    USER_ID            TEXT,
                    POST_ID            TEXT,
                    COMMENT            TEXT)'''

INSERT_DATA = '''INSERT INTO posts (ID, TITLE, CONTENT, AUTHOR, PUBLISHDAY) VALUES
              ('Blog post number 1', 'My first blog post is all about my blog post and how to write a new post in my blog, you can find it here.','Nofar Levy', '2021-12-18'), 
              ('Blog post number 2', 'My second blog post is all about my blog post', 'Ophir Leron', '2021-12-19')'''

COLOUM_TABLE_USER = '''(USER_ID, NAME, PHONE, EMAIL)'''
COLOUM_TABLE_LIKE = '''(USER_ID, POST_ID)'''
COLOUM_TABLE_COMMENT = '''(USER_ID, POST_ID, COMMENT)'''
COLOUM_TABLE_POST = '''(TITLE, CONTENT, USER_ID, PUBLISHDAY)'''
