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
