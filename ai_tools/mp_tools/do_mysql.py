from ai_tools.mp_tools.db_connection import get_mysql_connection, close_mysql_connection

def create_mysql_db():
    conn_mysql = get_mysql_connection()
    c_mysql = conn_mysql.cursor()
    try:
        c_mysql.execute("""
            CREATE TABLE IF NOT EXISTS mp_articles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                publish_date DATETIME NOT NULL,
                link VARCHAR(255) NOT NULL,
                summary TEXT NOT NULL,
                read_count INT DEFAULT 0,
                like_count INT DEFAULT 0
            )
        """)
        conn_mysql.commit()
    finally:
        c_mysql.close()
        close_mysql_connection(conn_mysql)

def add_column(column_name, column_type):
    conn_mysql = get_mysql_connection()
    c_mysql = conn_mysql.cursor()
    try:
        add_column_sql = """
        ALTER TABLE mp_articles ADD COLUMN {column_name} {column_type};
        """.format(column_name=column_name, column_type=column_type)
        c_mysql.execute(add_column_sql)
        conn_mysql.commit()
    finally:
        c_mysql.close()
        close_mysql_connection(conn_mysql)

def get_articles_from_mysql():
    conn_mysql = get_mysql_connection()
    c_mysql = conn_mysql.cursor()
    try:
        c_mysql.execute("SELECT * FROM mp_articles WHERE publish_date >= DATE_SUB(NOW(), INTERVAL 3 DAY) ORDER BY publish_date DESC")
        articles = c_mysql.fetchall()
        for article in articles:
            id = article[0]
            title = article[1]
            author = article[2]
            publish_date = article[3]
            link = article[4]
            summary = article[5]
            read_count = article[6]
            like_count = article[7]
            print(f"ID: {id}, \nTitle: {title}, \nAuthor: {author}, \nPublish Date: {publish_date}, \nLink: {link}, \nSummary: {summary}, \nRead Count: {read_count}, \nLike Count: {like_count}")
        return articles
    finally:
        c_mysql.close()
        close_mysql_connection(conn_mysql)

def get_authors_from_mysql():
    conn_mysql = get_mysql_connection()
    c_mysql = conn_mysql.cursor()
    try:
        c_mysql.execute("SELECT DISTINCT author FROM mp_articles")
        authors = c_mysql.fetchall()
        return authors
    finally:
        c_mysql.close()
        close_mysql_connection(conn_mysql)

def check_link_exist(link):
    conn_mysql = get_mysql_connection()
    c_mysql = conn_mysql.cursor()
    try:
        check_link_sql = "SELECT COUNT(*) FROM mp_articles WHERE link = %s"
        c_mysql.execute(check_link_sql, (link,))
        result = c_mysql.fetchone()
        exist = result[0] > 0
        return exist
    finally:
        c_mysql.close()
        close_mysql_connection(conn_mysql)

def add_article(article_dict):
    conn_mysql = get_mysql_connection()
    c_mysql = conn_mysql.cursor()
    try:
        add_article_sql = """
        INSERT INTO mp_articles (title, author, publish_date, link, summary)
        VALUES (%s, %s, %s, %s, %s)
        """
        c_mysql.execute(add_article_sql, (article_dict['title'], article_dict['author'], article_dict['publish_date'], article_dict['link'], article_dict['summary']))
        conn_mysql.commit()
    finally:
        c_mysql.close()
        close_mysql_connection(conn_mysql)