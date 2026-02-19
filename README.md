# Basic AI Agent

A simple command-line AI agent built with Python and the Anthropic SDK. This agent can chat with you and has the ability to read/write local files and run bash commands using custom tools. Inspired by [Amp's blogpost](https://ampcode.com/notes/how-to-build-an-agent) about building a simple agent in Go. 

## Prerequisites

- Python 3.10+
- An Anthropic API Key

## Setup

1.  **Clone the repository**

2.  **Install dependencies**
    ```bash
    pip install anthropic python-dotenv
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory and add your API key:
    ```
    ANTHROPIC_API_KEY=your_api_key_here
    ```

## Usage

Run the agent from the project root:

```bash
python src/main.py
```

## Features

- **Interactive Chat**: Conversational loop with Claude Sonnet 4.6.
- **Tool Use**: Can read files, write files, and run bash commands upon request.
- **Safety Filtering**: Bash commands are checked against a list of blocked commands and patterns before execution to prevent dangerous operations.
- **Context Awareness**: Maintains conversation history.

## Tools

The agent has access to the following tools, defined in `src/tools.py`:

- **`read_file(path)`**: Reads and returns the contents of a local file.
- **`write_file(filename, text)`**: Writes text content to a local file.
- **`run_bash(command, timeout)`**: Executes a bash command with a configurable timeout (default: 30s) and basic safety filtering.
