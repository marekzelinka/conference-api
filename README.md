# Conference API

A simple API for managing a tech conference system using **FastAPI**, **SQLModel** for data validation and database models, and **Neon's serverless Postgres** for data storage.

This combination provides a very good foundation for building scalable and efficient web services. FastAPI's speed and ease of use, combined with Pydantic's powerful data validation and Neon's serverless Postgres, make for a formidable tech stack.

## Performance Considerations

**Database Indexing**: We've added indexes to frequently queried fields (id, name, title) in our models. This improves query performance. To learn more about indexing, refer to the Neon documentation.

**Pagination**: The read_speakers and read_talks endpoints include skip and limit parameters for pagination, preventing the retrieval of unnecessarily large datasets.

**Dependency Injection**: By using Depends(get_db), we make sure that database connections are properly managed and closed after each request. This prevents connection leaks and improves performance.

**SQLModels Models**: Using SQLModel's models for request and response models provides automatic data validation and serialization, reducing the need for manual checks.

**Relationships**: We've used SQLModel relationships to efficiently load related data (speakers and their talks) in a single query.

## Prerequisites

Before we begin, make sure of the following:

- This project uses the modern `pyproject.toml` standard for dependency management and requires the `uv` tool to manage the environment.
- **Ensure `uv` is installed** globally on your system. If not, follow the official installation guide for [`uv`](https://docs.astral.sh/uv/).
- A [Neon account](https://console.neon.tech/signup) for serverless Postgres

## Setup

1.  **Install deps**

    ```sh
    uv sync
    ```

2.  **Setup env variables.**

    ```sh
    cp .env.example .env
    ```


3.  **Start app in dev mode**

    ```sh
    uv run uvicorn app.main:app --reload
    ```

4.  **Visit OpenAPI docs in browser**

    ```sh
    open http://localhost:8000/docs
    ```

## Development

1. Setup your editor to work with [ruff](https://docs.astral.sh/ruff/editors/setup/) and [ty](https://docs.astral.sh/ty/editors/).

2. Install the [justfile extension](https://just.systems/man/en/editor-support.html) for your editor, and use the provided `./justfile` to run commands.
