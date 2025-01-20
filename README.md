# Local LLM Inspector

An OpenAI-compatible API proxy with LLM trace visualization using Phoenix and OpenInference.

## Features

- OpenAI API compatible endpoints
- Streaming and non-streaming responses
- LLM trace visualization using Phoenix
- Lightweight local deployment
- OpenTelemetry-based instrumentation

## Requirements

- Python 3.9 - 3.12
- Poetry (for dependency management)

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

3. Update the `.env` file with your API keys:
```bash
# OpenAI/DeepSeek API
OPENAI_API_KEY=your-api-key
OPENAI_API_URL=https://api.deepseek.com
```

4. Install dependencies:
```bash
poetry install
```

5. Start the development server:
```bash
poetry run uvicorn main:app --reload
```

6. Start Phoenix tracing UI:
```bash
phoenix serve
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

## Development

### Using Supervisor for Process Management

1. Install Supervisor:
```bash
pip install supervisor
```

2. Start services:
```bash
supervisord -c supervisord.conf
```

3. Check service status:
```bash
supervisorctl -c supervisord.conf status
```

4. Common commands:
```bash
# Restart a service
supervisorctl -c supervisord.conf restart [service_name]

# Stop all services
supervisorctl -c supervisord.conf shutdown

# View logs
tail -f /tmp/phoenix_out.log
tail -f /tmp/main_out.log
```

### Manual Development

1. Install dependencies:
```bash
poetry install
```

2. Start the development server:
```bash
poetry run uvicorn main:app --reload
```

3. Start Phoenix tracing UI:
```bash
poetry run phoenix
```

## Configuration

The following environment variables are required:

- `OPENAI_API_KEY`: Your DeepSeek API key
- `OPENAI_API_URL`: DeepSeek API endpoint

## License

MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted...
