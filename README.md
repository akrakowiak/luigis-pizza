# Luigi's Pizza
Pizzeria

## Requirements
- uv - running the Python backend (port 8000)
- Docker - running PostgreSQL (port 5432) and adminer (port 9000)

## Running
```
docker compose --profile dev up   # Run the containers in dev mode
uv run dev                        # Run backend in dev mode
```

## Contributing
```
uvx pre-commit install            # Install pre-commit hook
```
