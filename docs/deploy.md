# Live Demo Deployment (AWS EC2 + Nginx + Gunicorn + MySQL)

This project is deployed on a single AWS EC2 instance using a classic “Flask + Gunicorn + Nginx” stack, with MySQL running locally for persistence.

> Note: The demo was previously deployed via Render and Aiven, however free tier had limits where it would stop the instance after long periods of inactivity. This was okay for dev work, but EC2 is a more long-term for production-level applications.

## **Infrastructure**

- Launched an Ubuntu-based AWS EC2 instance and attached an Elastic IP so the server has a stable public address.
- Installed core packages: `nginx`, `mysql-server`, `python3`, `python3-venv`, `pip`, and any required system dependencies.
- Created separate MySQL databases and users for each backend app to keep concerns isolated.

## **Flask backend**

- Copied the Flask project to `/home/ubuntu/apps/indigenous-library-flask` and set up a Python virtual environment.
- Installed dependencies from `requirements.txt` and ran the app via Gunicorn using the Flask app factory (`project:create_app()`).
- Configured environment variables for `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, and `MYSQL_PORT` so the Flask app reads DB credentials via its existing config helper.
- Created a `systemd` service (`indigenous-library-flask.service`) that:
  - Runs Gunicorn from the virtual environment,
  - Binds to `127.0.0.1:8001`,
  - Restarts on failure and starts automatically on boot.

## **Nginx reverse proxy**

- Configured Nginx’s default server block to act as a reverse proxy:
  - `location /` proxies all HTTP traffic to `http://127.0.0.1:8001`,
  - Passes through headers (`Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`) so Flask sees correct request metadata.
- Verified locally (`curl 127.0.0.1:8001/...`) and externally (`curl ELASTIC_IP/...`) that routes work end-to-end through Nginx.

## **Domain and HTTPS**

- Registered a custom domain and pointed an `A` record at the EC2 Elastic IP using DNS.
- Updated Nginx’s `server_name` to the new domain and confirmed HTTP requests resolve correctly.
- Installed Certbot with the Nginx plugin and obtained a free Let’s Encrypt SSL certificate for the domain.
- Let Certbot automatically update the Nginx configuration to serve HTTPS and optionally redirect HTTP → HTTPS, so all Flask auth traffic is now encrypted in transit.

---

## Deploying the Indigenous Library App (AWS EC2 + Nginx + Gunicorn + MySQL)

This guide walks through how to redeploy the Indigenous Library Flask app on a fresh Ubuntu EC2 instance. It assumes basic familiarity with SSH, Git, and AWS.

---

### 1. Provision and prepare the EC2 instance

1. Launch an **Ubuntu** EC2 instance (t2.micro or similar).
2. Attach an **Elastic IP** so the server’s public IP is stable.
3. SSH into the instance:

```bash
ssh ubuntu@YOUR_ELASTIC_IP
```

4. Update packages and install core tools:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip nginx mysql-server git
```

Check:

```bash
python3 --version
nginx -v
mysql --version
```

5. Enable and start Nginx and MySQL:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl enable mysql
sudo systemctl start mysql
```

Verify the default Nginx page at `http://YOUR_ELASTIC_IP/` in a browser.

---

### 2. Configure MySQL for this app

1. Secure MySQL (answer prompts reasonably, e.g. remove anonymous users, disallow remote root):

```bash
sudo mysql_secure_installation
```

2. Log into MySQL:

```bash
sudo mysql
```

3. Create a database and user for this app:

```sql
CREATE DATABASE indigenous_library_db;
CREATE USER 'indigenous_user'@'localhost' IDENTIFIED BY 'StrongIndigenousPass123!';
GRANT ALL PRIVILEGES ON indigenous_library_db.* TO 'indigenous_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

4. Test the credentials:

```bash
mysql -h 127.0.0.1 -u indigenous_user -p indigenous_library_db
```

If login works, the DB is ready.

---

### 3. Clone the project and set up the virtualenv

1. Create app folders:

```bash
mkdir -p ~/apps
cd ~/apps
git clone GIT_REPO_URL indigenous-library-flask
cd indigenous-library-flask
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

---

### 4. Configure environment variables and app settings

The project uses an **app factory** (`create_app`) in the `project` package and reads DB config from either `config.py` or environment variables.

For production on EC2:

1. Comment out or remove any line like:

```python
app.config["MYSQL_SSL_CA"] = "..."
```

in the app factory (local MySQL on the same EC2 instance does not need this).

2. Ensure the app reads:

- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`
- `MYSQL_PORT`
- `RESET_SECRET` (for the demo reset endpoint)

These will be provided via the systemd service.

---

### 5. Test the Flask app with Gunicorn

From the project root:

```bash
cd ~/apps/indigenous-library-flask
source venv/bin/activate
gunicorn --bind 127.0.0.1:8001 'project:create_app()'
```

- If there are no errors, visit:

```bash
curl http://127.0.0.1:8001/
curl http://127.0.0.1:8001/catalogue
```

Both should return HTML. Stop Gunicorn with `Ctrl+C`.

---

### 6. Create a systemd service for the Flask app

1. Create the unit file:

```bash
sudo nano /etc/systemd/system/indigenous-library-flask.service
```

2. Paste (adjust paths if necessary):

```ini
[Unit]
Description=Gunicorn service for indigenous-library-flask
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/apps/indigenous-library-flask
Environment="PATH=/home/ubuntu/apps/indigenous-library-flask/venv/bin"
Environment="MYSQL_HOST=127.0.0.1"
Environment="MYSQL_USER=indigenous_user"
Environment="MYSQL_PASSWORD=StrongIndigenousPass123!"
Environment="MYSQL_DB=indigenous_library_db"
Environment="MYSQL_PORT=3306"
Environment="RESET_SECRET=test123"
ExecStart=/home/ubuntu/apps/indigenous-library-flask/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8001 'project:create_app()'
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Reload and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable indigenous-library-flask
sudo systemctl start indigenous-library-flask
sudo systemctl status indigenous-library-flask --no-pager
```

4. Verify again:

```bash
curl http://127.0.0.1:8001/
curl http://127.0.0.1:8001/catalogue
```

If there are issues, check logs:

```bash
journalctl -u indigenous-library-flask -n 100 --no-pager
```

---

### 7. Configure Nginx as a reverse proxy

1. Edit the default Nginx site:

```bash
sudo nano /etc/nginx/sites-available/default
```

2. Replace contents with:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Test and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

4. Check via browser:

- `http://YOUR_ELASTIC_IP/`
- `http://YOUR_ELASTIC_IP/catalogue`

Routes should now work through Nginx.

---

### 8. Attach a domain and enable HTTPS (optional but recommended)

1. Register a domain and create an **A record** pointing to the EC2 Elastic IP.
2. Update Nginx `server_name`:

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name library.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Install Certbot:

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
```

4. Request a Let’s Encrypt certificate:

```bash
sudo certbot --nginx -d library.yourdomain.com
```

5. Confirm renewal:

```bash
sudo certbot renew --dry-run
```

6. Visit:

- `https://library.yourdomain.com`

You should see a valid HTTPS connection.

---

### 9. Demo reset automation (optional)

If using the demo reset endpoint:

1. Ensure `/admin/reset-demo` in Flask checks `RESET_SECRET` from env and the `X-Reset-Key` header.
2. A GitHub Actions workflow can periodically call:

```bash
curl -sf -X POST "${{ secrets.DEMO_APP_URL }}/admin/reset-demo" \
  -H "X-Reset-Key: ${{ secrets.RESET_SECRET }}"
```

Set `DEMO_APP_URL` to your domain and `RESET_SECRET` to match the env set in the systemd service.

---
