# 没有跑通
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('openai')

base_url = "http://127.0.0.1:8000"
# base_url = "https://api.deepseek.com"

class OpenAIClient:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            api_key="any_key",
            base_url=base_url)

    def chat_completion(self, system_message, user_message, **kwargs):
        print("Starting chat completion request...")
        try:
            print("Creating API request...")
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                stream=True,
                **kwargs
            )
            print("API request successful, processing stream...")
            return self._process_stream(response)
        except Exception as e:
            print(f"Error in chat completion: {str(e)}")
            print(f"API Key: {self.client.api_key}")
            print(f"Base URL: {self.client.base_url}")
            return None

    def _process_stream(self, response):
        print("Starting stream processing...")
        try:
            for chunk in response:
                print(f"Received chunk: {chunk}")
                yield chunk.model_dump()
        except Exception as e:
            print(f"Error processing stream: {e}")
            raise

if __name__ == "__main__":
    client = OpenAIClient()
    for chunk in client.chat_completion(
        system_message="You are a helpful assistant",
        user_message="Hi",
        temperature=0.5,
        max_tokens=1024
    ):
        print(chunk)


