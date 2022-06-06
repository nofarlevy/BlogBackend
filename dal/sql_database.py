import psycopg2
from typing import List, Tuple, Union, Dict
from datetime import date
from consts import database_consts
from model.user import User

cursor = None
conn = psycopg2.connect(user="postgres",
                        password="nofar0544",
                        host="127.0.0.1",
                        port="5432",
                        database="nofarlevy")


def get_cursor():
    global cursor
    global conn
    if cursor is None:
        cursor = conn.cursor()
        print("PostgreSQL server information")
        print(conn.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
    return cursor


def delete_table(table_name: str):
    cursor = get_cursor()
    drop_table_stmt = f"DROP TABLE {table_name}"
    cursor.execute(drop_table_stmt)


def get_posts_from_database():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM posts;")
    return cursor.fetchall()


def get_users_from_database():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()


def get_posts_by_user_id(user_id):
    cursor = get_cursor()
    try:
        get_data_by_user = f"SELECT * FROM posts WHERE AUTHOR_ID={user_id}"
        cursor.execute(get_data_by_user)
        return cursor.fetchall()
    except psycopg2.errors.CaseNotFound as error:
        print(error)


def format_data_for_sql(data):
    """
    :param data: JSON:
    {
        "ID" : "DEFAULT",
        "TITLE" : "MILO MY LOVE ",
        "CONTENT" : "milo celebrate 8 years old."
    }
    :return: ("DEFAULT","MILO MY LOVE", "milo celebrate 8 years old")
    """
    result = "("
    for colum in data.values():
        if colum is None:
            colum = ""
        result = result + "'" + colum + "',"
    res = result[:-1]
    return res + ")"


def add_the_current_date(data: str):
    today = date.today().strftime("%Y-%m-%d")
    return data[:-1] + ",'" + today + "')"


def insert_data(table_name: str, column_names: Union[Tuple, List], data: Dict[str, str]) -> bool:
    cursor = get_cursor()
    new_data = format_data_for_sql(data)
    new_data = add_the_current_date(new_data)
    insert_data_st = f"INSERT INTO {table_name} {column_names} VALUES {new_data}"
    cursor.execute(insert_data_st)
    conn.commit()
    return True


def create_table():
    cursor = get_cursor()
    try:
        cursor.execute(database_consts.CREATE_TABLE)
        print("ALL in POSTS: ", cursor.fetchall())
        conn.commit()
    except (psycopg2.errors.DuplicateTable, psycopg2.ProgrammingError) as error:
        print(error)


def edit_post(data):
    post_id = int(data.get("ID"))
    new_title = "'" + data.get("TITLE") + "'"
    new_content = "'" + data.get("CONTENT") + "'"
    cursor = get_cursor()
    if new_title is not None:
        query = f"UPDATE posts SET TITLE = {new_title} WHERE ID = {post_id};"
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError as error:
            print(error)
    if new_content is not None:
        query = f"UPDATE posts SET CONTENT = {new_content} WHERE ID = {post_id};"
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError as error:
            print(error)


def create_users_table():
    cursor = get_cursor()
    create_table = database_consts.CREATE_USER_TABLE
    try:
        cursor.execute(create_table)
        conn.commit()
    except psycopg2.errors.DuplicateTable as error:
        print(error)


def query_to_str(json_data: List[List]):
    posts = json_data
    posts_formatted_list = []
    for post in posts:
        post_query_str = f"""("{'","'.join(post)}")"""
        posts_formatted_list.append(post_query_str)
    result = ",".join(posts_formatted_list)
    return result


def insert_to_users(data: str):
    cursor = get_cursor()
    insert_query = f'''INSERT INTO users {database_consts.COLOUM_TABLE_USER} VALUES {data}'''
    try:
        cursor.execute(insert_query)
        conn.commit()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(users)
    except (psycopg2.errors.UndefinedColumn, psycopg2.errors.UniqueViolation) as error:
        print(error)


def get_phone_of_post_author(post_id):
    cursor = get_cursor()
    query = f'SELECT PHONE FROM users JOIN posts ON posts.USER_ID = USERS.USER_ID WHERE posts.ID = {post_id}'
    try:
        cursor.execute(query)
        phone = cursor.fetchall()
        return phone[0][0]
    except psycopg2.DatabaseError as error:
        print(error)


def delete_from_user(user_id: str):
    cursor = get_cursor()
    delete_query = f'''DELETE FROM users WHERE USER_ID={user_id};'''
    cursor.execute(delete_query)
    conn.commit()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print(users)
    return


def query_by_date(date: str):
    select_query = f'''SELECT * FROM posts WHERE PUBLISHDAY = {date};'''
    try:
        cursor.execute(select_query)
        posts_by_user_date = cursor.fetchall()
        return posts_by_user_date
    except psycopg2.errors.CaseNotFound as error:
        print(error)


"""
SELECT * FROM posts WHERE (title LIKE %milo% OR content LIKE %milo% image LIKE %milo%)
or
SELECT * FROM posts WHERE {col} LIKE {pattern}
or
SELECT * FROM posts WHERE {col} LIKE {pattern}

"""


def search_data_in_posts(data: str):
    pattern = f"'%{data}%'"
    select_query = f'''SELECT * FROM posts WHERE (TITLE LIKE {pattern} OR CONTENT LIKE {pattern} );'''
    try:
        cursor.execute(select_query)
        posts_by_user_date = cursor.fetchall()
        return posts_by_user_date
    except psycopg2.errors.CaseNotFound as error:
        print(error)


def add_like(user_id, post_id):
    cursor = get_cursor()
    data = "(" + user_id + ", " + post_id + ")"
    insert_query = f'''INSERT INTO likes {database_consts.COLOUM_TABLE_LIKE} VALUES {data}'''
    try:
        cursor.execute(insert_query)
        conn.commit()
    except (psycopg2.errors.UndefinedColumn, psycopg2.errors.UniqueViolation) as error:
        print(error)


def likes_by_post(post_id):
    cursor = get_cursor()
    select_query = f'''SELECT * FROM likes WHERE POST_ID = {post_id};'''
    try:
        cursor.execute(select_query)
        likes = cursor.fetchall()
        return likes
    except psycopg2.errors.CaseNotFound as error:
        print(error)


def comment_by_post(post_id):
    cursor = get_cursor()
    select_query = f'''SELECT * FROM comments WHERE POST_ID = {post_id};'''
    try:
        cursor.execute(select_query)
        likes = cursor.fetchall()
        return likes
    except psycopg2.errors.CaseNotFound as error:
        print(error)


def delete_like(user_id, post_id):
    cursor = get_cursor()
    delete_query = f'''DELETE FROM likes WHERE USER_ID={user_id} AND POST_ID={post_id} ;'''
    cursor.execute(delete_query)
    conn.commit()


def add_comment(data: Dict[str, str]) -> bool:
    cursor = get_cursor()
    new_data = format_data_for_sql(data)
    insert_data_st = f"INSERT INTO comments {database_consts.COLOUM_TABLE_COMMENT} VALUES {new_data}"
    try:
        cursor.execute(insert_data_st)
        conn.commit()
        return True
    except (psycopg2.errors.UndefinedColumn, psycopg2.errors.UniqueViolation) as error:
        print(error)


def delete_comment(user_id, post_id):
    cursor = get_cursor()
    delete_query = f'''DELETE FROM comment WHERE USER_ID={user_id} AND POST_ID={post_id} ;'''
    cursor.execute(delete_query)
    conn.commit()


def count_likes_of_post(post_id):
    cursor = get_cursor()
    query = f'''SELECT COUNT(*) FROM likes WHERE POST_ID={post_id}'''
    cursor.execute(query)
    return cursor.fetchall()


def count_comments_of_post(post_id):
    cursor = get_cursor()
    query = f'''SELECT COUNT(*) FROM comments WHERE POST_ID={post_id}'''
    cursor.execute(query)
    return cursor.fetchall()


def update_phone_number(user_id: str, new_phone: str):
    cursor = get_cursor()
    query = f'UPDATE users SET PHONE = {new_phone} WHERE USER_ID = {user_id}'
    cursor.execute(query)
    conn.commit()


def update_phone_number(user_id: str, new_phone: str):
    cursor = get_cursor()
    query = f'UPDATE users SET PHONE = {new_phone} WHERE USER_ID = {user_id}'
    cursor.execute(query)
    conn.commit()


def update_user_id(user_id: str, new_user_id: str):
    cursor = get_cursor()
    query = f'UPDATE users SET USER_ID = {new_user_id} WHERE USER_ID = {user_id}'
    cursor.execute(query)
    conn.commit()


if __name__ == '__main__':
    # # got data from UI
    cursor = get_cursor()
    # cursor.execute("SELECT * FROM POSTS")
    # b = cursor.fetchall()
    #
    # data = [
    #     ["1", 'Blog post number 1', 'My first blog post is all.....', 'Nofar', '29-09-1997'],
    #     ["3", 'Blog post number 3', 'My third......', 'Nufar', '29-09-2002']
    # ]
    # query_to_str(data)
    # insert_query = '''INSERT INTO users (id, name) VALUES
    #           (208937938, 'Ophir Leron')'''
    # cursor.execute(insert_query)
    # cursor.commit()
    # create_table()
    # insert_to_users(("319042907", "Nofar Levy", "0546377149", "nofar@via-events.co.il"))
    # insert_to_users(("208937939", "Ophir Leron", "0544849351", "ophirleron@gmail.com"))
    # print(format_data_for_sql({
    # "ID" : "DEFAULT",
    # "TITLE" : "MILO MY LOVE ",
    # "CONTENT" : "milo celebrate 8 years old."
    # create_users_table()
    # delete_from_user(319024907)
    # insert_to_users((DEFAULT, 'Nofar Levy'))

    #
    # cursor.execute("SELECT * FROM posts")
    # users = cursor.fetchall()
    # print(users)
    # cursor.execute("DROP TABLE posts;")
    # cursor.execute(database_consts.CREATE_LIKE_TABLE)
    # cursor.execute(database_consts.CREATE_COMMENT_TABLE)
    # conn.commit()
    #update_phone_number("'319024907'", "'+972546377149'")
    # update_user_id("'319042907'", "'319024907'")
