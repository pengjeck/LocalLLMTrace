curl http://localhost:8000/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer testkey" \
-d '{
  "messages": [
    {
      "role": "system",
      "content": "You are a test assistant."
    },
    {
      "role": "user",
      "content": "Testing. Just say hi and nothing else."
    }
  ],
  "model": "deepseek-chat"
}'