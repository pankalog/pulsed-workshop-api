from flask import Flask, request, Response
import datetime
import os

app = Flask(__name__)

DATA_FILE = 'database.txt'

def get_new_id():
    max_id = 0
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if fields:
                    try:
                        post_id = int(fields[0])
                        if post_id > max_id:
                            max_id = post_id
                    except ValueError:
                        continue
    return max_id + 1

@app.route('/', methods=['POST'])
def add_post():
    # Read raw data from request body
    username = request.form.get('username')
    title = request.form.get('title')
    text = request.form.get('text')

    # Generate a new ID
    new_id = get_new_id()

    # Get current date
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create the new post line
    new_post = f"{new_id}|{username}|{title}|{text}|{date}\n"

    # Append to the file
    with open(DATA_FILE, 'a') as f:
        f.write(new_post+"\n")

    return f"Post added with id {new_id}", 201

@app.route('/posts', methods=['GET'])
def get_posts():
    username = request.args.get('username')
    id_str = request.args.get('id')

    posts = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 5:
                    continue  # skip invalid lines
                post_id, post_username, title, text, date = fields
                if ((not username or username == post_username) and
                    (not id_str or id_str == post_id)):
                    posts.append(line)

    posts = [post_to_html(post) for post in posts]

    # Return the posts as plain text
    response_data = '\n'.join(posts)
    return Response(response_data, mimetype='text/html')

@app.route('/', methods=['GET', 'POST'])
def get_all_posts():
    posts = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('|')
                if len(fields) != 5:
                    continue  # skip invalid lines
                post_id, post_username, title, text, date = fields
                posts.append(line+"<br>")

    # Return the posts as plain text
    '\n<br>'.join(posts)
    posts = posts + [post_to_html(post) for post in posts]

    form_html = """
    <form action="/" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="title">Title:</label><br>
        <input type="text" id="title" name="title"><br>
        <label for="text">Text:</label><br>
        <textarea id="text" name="text"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    """
    request_form_html = """
        <form action="/posts" method="get">
            <label for="id">Post ID:</label><br>
            <input type="text" id="id" name="id"><br>
            <input type="submit" value="Get Post">
        </form>
    """

    posts.append(form_html)
    posts.append(request_form_html)

    response_data = '\n'.join(posts)
    return Response(response_data, mimetype='text/html')


def post_to_html(post_line):
    """
    Convert a single post line in the format 'id|username|title|text|date' to an HTML string.

    :param post_line: A string representing a single post with fields separated by '|'.
    :return: A string containing the HTML representation of the post.
    """
    fields = post_line.strip().split('|')

    if len(fields) != 5:
        return "<p>Invalid post format</p>"

    post_id, username, title, text, date = fields

    # Create the HTML structure for the post
    html = f"""
    <div class="post">
        <h2>{title} (Post ID: {post_id})</h2>
        <p><strong>Author:</strong> {username}</p>
        <p>{text}</p>
        <small><em>Posted on {date}</em></small>
    </div>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True)