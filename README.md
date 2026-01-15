# ALX Backend Security: IP Tracking

This is a Django project for the ALX Backend Security course. We're tracking IPs, blocking the bad guys, and doing some cool analytics.

## Features

- **IP Logging**: We log every request's IP address, timestamp, and path. Can't hide from us!
- **IP Blacklisting**: Got some haters? Block 'em! We've got a blacklist to keep the riff-raff out.
- **IP Geolocation**: We can see where you're at! We use a free API to get the country and city of each IP.
- **Rate Limiting**: Don't get too crazy. We're limiting requests to keep the server from melting.
- **Anomaly Detection**: We've got a Celery task that sniffs out suspicious IPs and flags them.

## Setup

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/s-pins/alx-backend-security.git
    cd alx-backend-security
    ```

2.  **Create a virtual environment and install dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run migrations**:
    ```bash
    python3 manage.py migrate
    ```

4.  **Run the development server**:
    ```bash
    python3 manage.py runserver
    ```

## Running Celery

To run the anomaly detection task, you'll need to have Redis installed and running. Then, in separate terminals, run the following commands:

**Celery Worker**:
```bash
celery -A alx_backend_security worker -l info
```

**Celery Beat**:
```bash
celery -A alx_backend_security beat -l info
```

## How to Use

- The IP logging and geolocation are done automatically by the middleware.
- To block an IP, use the management command:
  ```bash
  python3 manage.py block_ip <ip_address>
  ```
- The rate limiting is applied to the `/ip/login/` and `/ip/protected/` endpoints.
- Suspicious IPs are flagged automatically by the Celery task.
