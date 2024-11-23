from flask import Flask, request, Response
import datetime
import os

app = Flask(__name__)

DATA_FILE = 'database.txt'


def read_posts_from_file():
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
                post_id, username, title, text, date = fields
                post = {
                    'id': post_id,
                    'username': username,
                    'title': title,
                    'text': text,
                    'date': date
                }
                posts.append(post)
    return posts


def get_new_id():
    posts = read_posts_from_file()

    max_id = -1
    for post in posts:
        post_id, post_username, title, text, date = post.values()
        post_id = int(post_id)
        if max_id < post_id:
            max_id = post_id

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
        f.write(new_post)

    return f"Post added with id {new_id}", 201


@app.route('/posts', methods=['GET'])
def get_posts():
    username = request.args.get('username')
    id_str = request.args.get('id')

    posts = read_posts_from_file()

    correct_posts = []

    for post in posts:
        post_id, post_username, title, text, date = post.values()
        if((username and username == post_username) or
                (id_str and int(id_str) == post_id)):
            correct_posts.append(post)

    print(correct_posts)

    # [print(post["id"]) for post in posts]

    correct_posts = [post_to_html(line_from_parsed(post)) for post in correct_posts]

    # Return the posts as plain text
    response_data = '\n'.join(correct_posts)
    return Response(response_data, mimetype='text/html')


@app.route('/', methods=['GET', 'POST'])
def get_all_posts():
    posts_from_file = read_posts_from_file();

    posts = []

    for post in posts_from_file:
        post_id, post_username, title, text, date = post.values()
        posts.append(f"{post_id}|{post_username}|{title}|{text}|{date}<br>")

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
            <label for="username">User's username:</label><br>
            <input type="text" id="username" name="username"><br>
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
    print(post_line)
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


def line_from_parsed(post):
    post_id, username, title, text, date = post.values();
    return f"{post_id}|{username}|{title}|{text}|{date}<br>"


if __name__ == '__main__':
    app.run(debug=True)
