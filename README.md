# 🚀 Django 项目部署指南  

基于 **Windows + GitHub + MySQL + Docker + Vue**

---

## 🧩 1. 生成 SSH 密钥并配置 GitHub

1. 生成密钥对（替换为你自己的 GitHub 邮箱）：

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

2. 进入密钥目录：

   ```bash
   cd ~/.ssh
   ```

3. 查看公钥内容：

   ```bash
   cat id_rsa.pub
   ```

4. 将公钥复制到 GitHub 的「SSH and GPG keys」中。

---

## 🧬 2. 克隆项目代码

- 使用 SSH（推荐）：

  ```bash
  git clone git@github.com:zhang1003533565/database-zzs.git
  ```

- 如果未配置 SSH，可使用 HTTPS：

  ```bash
  git clone https://github.com/zhang1003533565/database-zzs.git
  ```

---

## 🐳 3. 启动 Docker（MySQL + Adminer）

1. 检查 Docker 是否安装成功：

   ```bash
   docker --version
   ```

2. 启动容器服务：

   ```bash
   docker compose up
   ```

3. 浏览器访问 Adminer 可视化管理界面：

   ```
   http://localhost:7070
   ```

---

## 🐍 4. 配置 Python 虚拟环境

1. 创建虚拟环境：

   ```bash
   python -m venv venv
   ```

2. 激活虚拟环境（Windows）：

   ```bash
   venv\Scripts\activate
   ```

3. 安装项目依赖：

   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠️ 5. 初始化数据库（可选）

```bash
python init_db.py
```

---

## ⚙️ 6. 初始化 Django 模型

1. 进入 Django 项目目录：

   ```bash
   cd myproject
   ```

2. 创建迁移文件：

   ```bash
   python manage.py makemigrations
   ```

3. 执行迁移：

   ```bash
   python manage.py migrate
   ```

4. 创建超级管理员：

   ```bash
   python manage.py createsuperuser
   ```

   - 用户名：admin  
   - 邮箱：可回车跳过  
   - 密码：admin123  
   - 密码强度提示时输入 `yes`

---

## 🌐 7. 启动 Django 服务

```bash
python manage.py runserver
```

访问地址：

```
http://127.0.0.1:8000
```

---

## 💾 8. 执行 SQL 插入语句（如有）

可在 Adminer、Django Admin、或 Django Shell 中执行数据初始化语句。

---

## 🌈 9. 启动前端 Vue 项目

1. 全局安装 Vue CLI：

   ```bash
   npm install -g @vue/cli
   ```

2. 进入前端目录并安装依赖：

   ```bash
   cd frontend
   npm install
   npm install element-plus axios vue-router @element-plus/icons-vue
   ```

3. 启动前端项目：

   ```bash
   npm run serve
   ```

---

✅ 至此，**Django + MySQL + Docker + Vue 项目部署已完成！**