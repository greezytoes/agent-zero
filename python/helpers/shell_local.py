import subprocess
import time
import sys
import asyncio
from typing import Optional, Tuple
import io

class LocalInteractiveSession:
    def __init__(self):
        self.process = None
        self.full_output = ''

    async def connect(self):
        # Start a new subprocess with the appropriate shell for the OS
        if sys.platform.startswith('win'):
            # Windows
            self.process = await asyncio.create_subprocess_shell(
                'cmd.exe',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            # macOS and Linux
            self.process = await asyncio.create_subprocess_shell(
                '/bin/bash',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

    def close(self):
        if self.process:
            self.process.terminate()

    def send_command(self, command: str):
        if not self.process or not self.process.stdin:
            raise Exception("Shell not connected")
        self.full_output = ""
        # For Windows, we need to add echo on and cls to ensure proper output
        if sys.platform.startswith('win'):
            command = f"echo on\ncls\n{command}\n"
        self.process.stdin.write(command.encode() + b'\n')
        asyncio.create_task(self.process.stdin.drain())
 
    async def read_output(self, timeout: float = 0, reset_full_output: bool = False) -> Tuple[str, Optional[str]]:
        if not self.process or not self.process.stdout:
            raise Exception("Shell not connected")

        if reset_full_output:
            self.full_output = ""

        partial_output = ''
        
        try:
            # Read from stdout in a non-blocking way
            while True:
                try:
                    chunk = await asyncio.wait_for(self.process.stdout.read(1024), 0.1)
                    if not chunk:
                        break
                    text = chunk.decode()
                    partial_output += text
                    self.full_output += text
                except asyncio.TimeoutError:
                    break
                except Exception as e:
                    print(f"Error reading output: {e}")
                    break

            # Read from stderr
            try:
                chunk = await asyncio.wait_for(self.process.stderr.read(1024), 0.1)
                if chunk:
                    text = chunk.decode()
                    partial_output += text
                    self.full_output += text
            except (asyncio.TimeoutError, Exception):
                pass

        except Exception as e:
            print(f"Error in read_output: {e}")

        if not partial_output:
            return self.full_output, None
        
        return self.full_output, partial_output