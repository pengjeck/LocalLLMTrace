# Local LLM Inspector

An OpenAI-compatible API proxy with LLM trace visualization using Langfuse.

## Features

- OpenAI API compatible endpoints
- Streaming and non-streaming responses
- LLM trace visualization
- Integration with Langfuse for observability
- Docker-based deployment

## Requirements

- Python 3.8+
- Docker
- Docker Compose

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pengjeck/LocalLLMTrace
cd LocalLLMTrace
```

2. Create a `.env` file based on `.env-example`:
```bash
cp .env-example .env
```

3. Update the `.env` file with your API keys and configuration:
```bash
# OpenAI/DeepSeek API
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_API_URL=https://api.deepseek.com/v1

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://localhost:3000
```

4. Start the services:
```bash
docker-compose up -d
```

## API Documentation

### POST /v1/chat/completions
### POST /chat/completions

#### Request Body
```json
{
  "model": "string",
  "messages": [
    {
      "role": "string",
      "content": "string"
    }
  ],
  "temperature": "number",
  "stream": "boolean",
  "max_tokens": "number",
  "stream_options": {
    "include_usage": "boolean"
  }
}
```

#### Example Request
```bash
curl -X POST "http://localhost:8000/chat/completions" \
-H "Content-Type: application/json" \
-d '{
  "model": "deepseek-chat",
  "messages": [
    {
      "role": "user",
      "content": "Hello!"
    }
  ],
  "temperature": 0.7,
  "stream": false
}'
```

## Deployment

The project uses Docker Compose for deployment. The following services are included:

- Langfuse Web (port 3000)
- Langfuse Worker (port 3030)
- Postgres (port 5432)
- Redis (port 6379)
- Clickhouse (ports 8123, 9000)
- MinIO (ports 9090, 9091)

To start all services:
```bash
docker-compose up -d
```

To stop all services:
```bash
docker-compose down
```

## Development

1. Create a virtual environment:
```bash
poetry shell
```

2. Install dependencies:
```bash
poetry install
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

## Configuration

The following environment variables are required:

- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `DEEPSEEK_API_URL`: DeepSeek API endpoint
- `LANGFUSE_PUBLIC_KEY`: Langfuse public key
- `LANGFUSE_SECRET_KEY`: Langfuse secret key
- `LANGFUSE_HOST`: Langfuse host URL

## Usage
![image](https://github.com/user-attachments/assets/6a6986c2-3131-46dc-8a1d-2642720e0f6e)
![image](https://github.com/user-attachments/assets/6570cbfb-a154-493f-9eb0-699cd450127d)


## License

MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted...
