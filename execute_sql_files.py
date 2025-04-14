import pymysql
import os

# MySQL 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'database': 'database_test',
    'charset': 'utf8mb4'
}

# SQL 文件目录（将路径改成你的）
SQL_FILES_DIR = './sql语句'  # 假设所有 SQL 文件放在这个文件夹里

def execute_sql_file(cursor, filepath):
    print(f"📄 正在执行文件: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        sql = f.read()
        # 分割多个语句，防止多条语句同时提交报错
        for statement in sql.split(';'):
            stmt = statement.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print(f"⚠️ 执行语句失败：{stmt[:50]}...，原因：{e}")

def run():
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # 按文件名排序执行
        sql_files = sorted([f for f in os.listdir(SQL_FILES_DIR) if f.endswith('.sql')])

        for sql_file in sql_files:
            filepath = os.path.join(SQL_FILES_DIR, sql_file)
            execute_sql_file(cursor, filepath)

        conn.commit()
        print("✅ 所有 SQL 文件执行完毕。")

        cursor.close()
        conn.close()

    except pymysql.MySQLError as e:
        print(f"❌ MySQL 连接或执行失败: {e}")

if __name__ == '__main__':
    run()
