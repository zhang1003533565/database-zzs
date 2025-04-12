import pymysql

# MySQL 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'charset': 'utf8mb4'
}

DB_NAME = 'database_test'

def create_database():
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        print(f"✅ 连接成功，MySQL 版本：{conn.get_server_info()}")

        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        print(f"✅ 数据库 `{DB_NAME}` 已创建或已存在。")

        cursor.execute("SHOW DATABASES;")
        print("📦 当前数据库列表：")
        for db in cursor.fetchall():
            print("  -", db[0])

        cursor.close()
        conn.close()

    except pymysql.MySQLError as err:
        print(f"❌ 数据库创建失败: {err}")

if __name__ == '__main__':
    create_database()
