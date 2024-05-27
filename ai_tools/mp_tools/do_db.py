import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

os.chdir(os.path.dirname(os.path.abspath(__file__)))
db_file = "mp1.db"

# 连接到数据库
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

def create_db():
    # 定义创建表的SQL语句
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS mp_articles (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publish_date DATE NOT NULL,
        link TEXT NOT NULL,
        summary TEXT,
        read_count INTEGER DEFAULT 0,
        like_count INTEGER DEFAULT 0
    );
    """

    # 执行创建表命令
    cursor.execute(create_table_sql)

    # 提交事务
    conn.commit()

    # 关闭连接
    cursor.close()
    conn.close()

def create_mysql_db():
    import mysql.connector

    # 连接到MySQL数据库
    conn_mysql = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DB']
    )

    # 创建一个游标对象
    c_mysql = conn_mysql.cursor()

    # 创建mp_articles表
    c_mysql.execute("""
        CREATE TABLE mp_articles (
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

# 增加字段
def add_column(column_name, column_type):
    # 定义增加字段的SQL语句
    add_column_sql = """
    ALTER TABLE mp_articles ADD COLUMN {column_name} {column_type};
    """.format(column_name=column_name, column_type=column_type)

    # 执行增加字段命令
    cursor.execute(add_column_sql)

    # 提交事务
    conn.commit()

    # 关闭连接
    cursor.close()
    conn.close()

def get_articles():
    # 定义查询文章的SQL语句
    get_articles_sql = """
    SELECT * FROM mp_articles;
    """

    # 执行查询文章命令
    cursor.execute(get_articles_sql)

    # 获取查询结果
    articles = cursor.fetchall()

    # 关闭连接
    cursor.close()
    conn.close()

    return articles

def get_article_from_date(date):
    # 定义查询文章的SQL语句
    get_article_sql = """
    SELECT * FROM mp_articles WHERE publish_date = '2024-04-16 00:00:00';
    """

    # 执行查询文章命令
    cursor.execute(get_article_sql)

    # 获取查询结果
    articles = cursor.fetchall()

    # 关闭连接
    cursor.close()
    conn.close()

    return articles

def move_sqlite_to_mysql():
    import mysql.connector

    # 连接到MySQL数据库
    conn_mysql = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DB']

    )

    # 创建一个游标对象
    c_mysql = conn_mysql.cursor()

    # 查询SQLite数据库中的数据
    cursor.execute("SELECT * FROM mp_articles")
    articles = cursor.fetchall()

    # 遍历每一篇文章
    for article in articles:
        # 提取文章信息
        id = article[0]
        title = article[1]
        author = article[2]
        publish_date = article[3]
        link = article[4]
        summary = article[5]
        read_count = article[6]
        like_count = article[7]

        # 插入数据到MySQL数据库
        c_mysql.execute("""
            INSERT INTO mp_articles (id, title, author, publish_date, link, summary, read_count, like_count)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

        """, (id, title, author, publish_date, link, summary, read_count, like_count))

    # 提交事务
    conn_mysql.commit()

    # 关闭连接
    cursor.close()

def get_articles_from_mysql():
    import mysql.connector

    # 连接到MySQL数据库
    conn_mysql = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DB']
    )

    # 创建一个游标对象
    c_mysql = conn_mysql.cursor()

    # 查询最近3天的所有文章
    c_mysql.execute("SELECT * FROM mp_articles WHERE publish_date >= DATE_SUB(NOW(), INTERVAL 5 DAY) ORDER BY publish_date DESC")
    articles = c_mysql.fetchall()

    # 遍历每一篇文章
    for article in articles:
        # 提取文章信息
        id = article[0]
        title = article[1]
        author = article[2]
        publish_date = article[3]
        link = article[4]
        summary = article[5]
        read_count = article[6]
        like_count = article[7]
        
        # 打印文章信息
        print(f"ID: {id}, \nTitle: {title}, \nAuthor: {author}, \nPublish Date: {publish_date}, \nLink: {link}, \nSummary: {summary}, \nRead Count: {read_count}, \nLike Count: {like_count}")

    # 关闭连接
    c_mysql.close()
    conn_mysql.close()
    return articles

def get_authors_from_mysql():
    import mysql.connector

    # 连接到MySQL数据库
    conn_mysql = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DB']
    )

    # 创建一个游标对象
    c_mysql = conn_mysql.cursor()

    # 查询所有作者
    c_mysql.execute("SELECT DISTINCT author FROM mp_articles")
    authors = c_mysql.fetchall()

    # 关闭连接
    c_mysql.close()
    conn_mysql.close()
    return authors


if __name__ == '__main__':
    # create_db()
    # add_column('summary', 'TEXT')
    # articles = get_articles()
    # print(articles)
    # articles = get_article_from_date('2023-04-16 00:00:00')
    # print(articles)
    # create_mysql_db()
    # move_sqlite_to_mysql()
    # get_articles_from_mysql()
    authors = get_authors_from_mysql()
    for author in authors:
        print(author[0])
