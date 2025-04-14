# Command Server Setup and Security Guide

## 1. Running the Internal Command Server

### Prerequisites
- Python 3.8+
- Install dependencies:
  ```sh
  pip install fastapi uvicorn pydantic
  ```

### Starting the Server
- From the `omi-command-base` directory, run:
  ```sh
  uvicorn command_server:app --host 0.0.0.0 --port 8000
  ```
- The server will be accessible at `http://internal-command-server:8000` if your DNS or Docker network resolves that hostname.
- For local access, you may need to add an entry to your hosts file:
  - **Windows:** `C:\Windows\System32\drivers\etc\hosts`
  - **Linux/macOS:** `/etc/hosts`
  - Example entry:
    ```
    127.0.0.1 internal-command-server
    ```

## 2. Security: Adding API Key Authentication

By default, the command server does **not** require authentication. For production or internal use, you should enable authentication.

### Example: API Key Authentication (FastAPI)

1. **Set an environment variable for your API key:**
   ```sh
   export COMMAND_SERVER_API_KEY=your-strong-api-key
   # On Windows (PowerShell):
   $env:COMMAND_SERVER_API_KEY="your-strong-api-key"
   ```

2. **Modify `command_server.py` to require the API key:**
   Add the following at the top:
   ```python
   import os
   from fastapi import Security
   from fastapi.security.api_key import APIKeyHeader

   API_KEY = os.getenv("COMMAND_SERVER_API_KEY", "changeme")
   api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

   def get_api_key(api_key: str = Security(api_key_header)):
       if api_key != API_KEY:
           raise HTTPException(status_code=403, detail="Invalid or missing API Key")
   ```

   Then, add `Depends(get_api_key)` to each route:
   ```python
   @app.post("/api/v1/commands")
   async def create_command(command: CommandRequest, api_key: str = Depends(get_api_key)):
       ...
   # Repeat for other endpoints
   ```

3. **Client Requests:**
   - Include the header `X-API-Key: your-strong-api-key` in all requests.

---

## 3. Additional Recommendations
- Rotate API keys regularly.
- Use HTTPS in production environments.
- Restrict network access to trusted hosts if possible.

---

**For further customization or to implement OAuth2 or JWT, see the [FastAPI Security documentation](https://fastapi.tiangolo.com/advanced/security/).**
