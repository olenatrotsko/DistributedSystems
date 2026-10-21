# Project Setup

## 1. Run with Docker Compose

Build the images and start all services:

```bash
docker compose up --build
```

To run the services in the background:

```bash
docker compose up --build -d
```

To stop the services:

```bash
docker compose down
```

## 2. Set Up a Python Virtual Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

**Linux / macOS**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

## 3. Install Dependencies

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## 4. Run Tests

Run all tests using pytest:

```bash
pytest
```

To run tests with detailed output:

```bash
pytest -v
```
