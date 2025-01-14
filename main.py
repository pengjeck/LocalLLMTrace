import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional, Union
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv
from openai import OpenAI

# Langfuse imports
from langfuse import Langfuse
from langfuse import Langfuse

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Langfuse
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

app = FastAPI(title="Local LLM Inspector",
              description="OpenAI-compatible API proxy with LLM trace visualization")

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_API_URL"))

# Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     # allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

class ContentText(BaseModel):
    type: str
    text: str

class ChatMessage(BaseModel):
    role: str
    content: Union[str, List[ContentText]]
    # content: str
    # content: List[ContentText]

class StreamOptions(BaseModel):
    include_usage: bool

class ChatInput(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float]
    stream: bool
    max_tokens: Optional[int] = 4096
    stream_options: Optional[StreamOptions] = None

@app.post("/v1/chat/completions")
@app.post("/chat/completions")
async def chat_completion(request: ChatInput):
    # Validate request
    if not request.model:
        logger.error("Model field is required")
        raise HTTPException(
            status_code=422,
            detail="model field is required"
        )
    if not request.messages:
        logger.error("No messages provided in request")
        for msg in request.messages:
            if not isinstance(msg, role="user"):
                logger.error("Invalid message format in request")
                raise HTTPException(
                    status_code=422,
                    detail="Invalid request: missing required fields"
                )
    
    trace = langfuse.trace(
        name="chat_completion",
        input=request.messages,
        metadata={
            "model": request.model,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": request.stream
        }
    )
    
    span = trace.span(
        name="chat_completion",
        input=request.messages
    )
    
    try:
        if request.stream:
            # Handle streaming response
            async def stream_response():
                try:
                    response = client.chat.completions.create(
                        model=request.model,
                        messages=[msg.model_dump() for msg in request.messages],
                        temperature=request.temperature,
                        max_tokens=request.max_tokens,
                        stream=True
                    )
                    
                    logger.info("Streaming response from OpenAI API")
                    
                    for chunk in response:
                        yield f"data: {chunk.json()}\n\n"
                    
                    # Record streaming completion
                    span.update(
                        output="[streaming completed]",
                        metadata={
                            "status_code": 200
                        }
                    )
                except Exception as e:
                    logger.error(f"Error during streaming: {str(e)}")
                    span.update(
                        output=None,
                        metadata={
                            "error_message": str(e)
                        }
                    )
                    raise
                
            return StreamingResponse(stream_response(), media_type="text/event-stream")
        
        else:
            # Handle non-streaming response
            response = await client.chat.completions.create(
                model=request.model,
                messages=[msg.model_dump() for msg in request.messages],
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            logger.info("Received successful response from OpenAI API")
            
            # Record successful response
            span.update(
                output=response,
                metadata={
                    "status_code": 200
                }
            )
            
            return response
    except Exception as e:
        logger.error(
            f"OpenAI API error: {str(e)}",
            exc_info=True
        )
        
        # Record error details
        span.update(
            output=None,
            metadata={
                "error_message": str(e)
            }
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API error: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)