# Hello World to MinIO


## How to Run

Start MinIO with Docker Compose:

``` bash
docker-compose up -d
```

-   MinIO S3 endpoint: http://localhost:9000\
-   MinIO console: http://localhost:9001 (login with `admin` /
    `admin123`)

## Running the Python Example

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run the app:

``` bash
python app.py
```

Expected output:

    Objects in bucket:
    - hello.txt
    Downloaded content: Hello MinIO!

