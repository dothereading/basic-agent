from anthropic import beta_tool
import subprocess

@beta_tool
def read_file(path:str) -> str:
    """Reads a file.

    Args:
        path (str): file path
    Returns:
        str: contents of file
    """

    with open(path) as f:
        return f.read()


@beta_tool
def write_file(filename:str, text:str):
    """Writes a file.

    Args:
        filename (str): file path
        text (str): Text to be written to file
    """
    print("Writing file.")
    with open(filename, "w") as f:
        f.write(text)
    print("File written.")

BLOCKED_COMMANDS = [
    "rm -rf /",
    "rm -rf /*",
    "mkfs",
    "dd if=",
    ":(){",          # fork bomb
    "chmod -R 777 /",
    "curl | sh",
    "wget | sh",
    "shutdown",
    "reboot",
    "init 0",
    "init 6",
    "> /dev/sda",
    "mv / ",
    "chmod 000 /",
    "rm ",           # block any rm command
    "unlink",        # block unlink (another way to delete files)
    "shred",         # block shred (secure file deletion)
    "rmdir",         # block directory removal
]

BLOCKED_PATTERNS = [
    "rm -rf /",
    "/dev/sda",
    "/dev/null >",
    ":(){ :|:",      # fork bomb pattern
    "> /etc/passwd",
    "> /etc/shadow",
    r"rm\s+",        # block rm with any arguments
    r"unlink\s+",    # block unlink with any arguments
]

def is_dangerous(command: str) -> bool:
    """Check if a command matches known dangerous patterns."""
    import re
    cmd_lower = command.strip().lower()
    for blocked in BLOCKED_COMMANDS:
        if blocked in cmd_lower:
            return True
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, cmd_lower):
            return True
    return False

@beta_tool
def run_bash(command: str, timeout: int = 30) -> str:
    """Runs a bash command with basic safety filtering.
    Args:
        command (str): bash command to execute
        timeout (int): max seconds before timeout
    Returns:
        str: command output or error message
    """
    if is_dangerous(command):
        return f"Blocked: command matched a dangerous pattern"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = result.stdout + result.stderr
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: command timed out after {timeout}s"
