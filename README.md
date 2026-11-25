# Asystent-Poczty

## Run with Docker Compose

Start the API and Streamlit dashboard:

```sh
docker compose up --build
```

Open the dashboard at <http://localhost:8501> or the API at <http://localhost:8000>.
The SQLite database is stored in the `email_data` Docker volume and survives container
recreation.