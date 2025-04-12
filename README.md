# Django 项目部署指南（基于 Windows + GitHub + MySQL）

## 1. 生成 SSH 密钥并配置 GitHub

1. **生成密钥对（使用你自己的 GitHub 邮箱）**

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

2. **进入密钥目录**

   ```bash
   cd ~/.ssh
   ```

3. **查看公钥内容**

   ```bash
   cat id_rsa.pub
   ```

4. **将公钥复制到 GitHub 的 SSH 设置中**  
   如果不清楚如何操作，可以使用 AI 或百度搜索“GitHub 添加 SSH 密钥”。

---

## 2. 克隆项目

### ✅ 如果已经配置 SSH 密钥

```bash
git clone git@github.com:zhang1003533565/database-zzs.git
```

### ❌ 如果没有配置 SSH 密钥（使用 HTTPS）

```bash
git clone https://github.com/zhang1003533565/database-zzs.git
```

---

## 3. 配置 Python 虚拟环境

1. **创建虚拟环境**

   ```bash
   python -m venv venv
   ```

2. **激活虚拟环境**

   ```bash
   venv\Scripts\activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

---

## 4. 初始化数据库

```bash
python init_db.py
```

---

## 5. 进入 Django 项目并初始化模型

1. **进入项目目录**

   ```bash
   cd myproject
   ```

2. **生成迁移文件**

   ```bash
   python manage.py makemigrations
   ```

3. **迁移数据库**

   ```bash
   python manage.py migrate
   ```

4. **创建超级管理员**

   ```bash
   python manage.py createsuperuser
   ```

   - 用户名：admin  
   - 邮箱：直接回车跳过  
   - 密码：admin123  
   - 如果提示密码过弱，输入 `yes` 确认

---

## 6. 启动服务

```bash
python manage.py runserver
```

---

## 7. 最后执行 SQL 插入语句（如有）

至此项目环境搭建完毕 ✅