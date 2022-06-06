from flask import Flask
from flask import render_template
import psycopg2
from sql_database import get_cursor

app = Flask(__name__)


@app.route("/posts")
def get_posts():
    # SQL to get records from Postgres
    s = "SELECT * FROM posts"
    # Error trapping
    try:
        cursor = get_cursor()
        cursor.execute(s)
        # Retrieve records from Postgres into a Python List
        posts = cursor.fetchall()
        # how to get the database?
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("error.html", t_message=t_message)

    return {'DATA': posts}



# create new post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = int(request.form['content'])
        publishday = request.form['publishday']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO posts (TITLE, CONTENT, AUTHOR, PUBLISHDAY)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, content, author, publishday))
        conn.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


# Show post by id
@app.route('/post/<id>', methods=('GET', 'POST'))
def get_post(id):
    s = 'SELECT * FROM POSTS WHERE ID=%s'
    cursor.excute(s, id)
    res = cursor.fetchall()


if __name__ == '__main__':
    app.run(port=8090)