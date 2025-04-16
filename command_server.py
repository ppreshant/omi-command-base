from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import subprocess
from typing import Optional

app = FastAPI()

# Temporary directory to store uploaded files
TEMP_DIR = "/tmp/uploaded_files"

# Ensure the temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/v1/commands")
async def run_command_with_file(
    command: str = Form(...),  # Changed from query parameter to Form
    file: UploadFile = File(...),
    working_directory: Optional[str] = Form(None)
):
    """
    Run a command with an uploaded file.
    """
    print(f"Received command: {command}")
    print(f"Received file: {file.filename}")
    
    # Save the uploaded file temporarily
    try:
        # Create a temp file
        temp_file_path = os.path.join(TEMP_DIR, file.filename)
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Run the command
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        stdout, stderr = result.stdout, result.stderr
        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": result.returncode
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e}")