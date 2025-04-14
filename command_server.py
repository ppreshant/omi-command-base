from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Dict, Optional
import asyncio
from datetime import datetime
import uuid

app = FastAPI()

# In-memory store for command executions
command_store: Dict[str, dict] = {}

class CommandRequest(BaseModel):
    command: str
    working_directory: Optional[str] = None

class CommandStatus(BaseModel):
    command_id: str
    status: str
    exit_code: Optional[int] = None
    start_time: datetime
    end_time: Optional[datetime] = None

class CommandOutput(BaseModel):
    command_id: str
    stdout: str
    stderr: str

async def execute_command_async(command_id: str, command: str, working_dir: Optional[str] = None):
    try:
        start_time = datetime.now()
        command_store[command_id]["status"] = "running"
        command_store[command_id]["start_time"] = start_time
        
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_dir,
            shell=True
        )
        
        stdout, stderr = await process.communicate()
        
        end_time = datetime.now()
        command_store[command_id].update({
            "status": "completed" if process.returncode == 0 else "failed",
            "exit_code": process.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "end_time": end_time
        })
    except Exception as e:
        command_store[command_id].update({
            "status": "failed",
            "stderr": str(e),
            "end_time": datetime.now()
        })

@app.post("/api/v1/commands")
async def create_command(command: CommandRequest):
    command_id = str(uuid.uuid4())
    command_store[command_id] = {
        "command": command.command,
        "status": "pending",
        "start_time": datetime.now()
    }
    
    # Start command execution in background
    asyncio.create_task(execute_command_async(
        command_id,
        command.command,
        command.working_directory
    ))
    
    return {"command_id": command_id, "status": "pending"}

@app.get("/api/v1/commands/{command_id}/status")
async def get_command_status(command_id: str):
    if command_id not in command_store:
        raise HTTPException(status_code=404, detail="Command not found")
    
    cmd = command_store[command_id]
    return CommandStatus(
        command_id=command_id,
        status=cmd["status"],
        exit_code=cmd.get("exit_code"),
        start_time=cmd["start_time"],
        end_time=cmd.get("end_time")
    )

@app.get("/api/v1/commands/{command_id}/output")
async def get_command_output(command_id: str):
    if command_id not in command_store:
        raise HTTPException(status_code=404, detail="Command not found")
    
    cmd = command_store[command_id]
    if cmd["status"] not in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="Command execution not finished")
    
    return CommandOutput(
        command_id=command_id,
        stdout=cmd.get("stdout", ""),
        stderr=cmd.get("stderr", "")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
