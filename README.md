# Basic AI Agent

A simple command-line AI agent built with Python and the Anthropic SDK. This agent can chat with you and has the ability to read local files using a custom tool. Inspired by [Amp's blogpost](https://ampcode.com/notes/how-to-build-an-agent) about building a simple agent in Go. 

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

- **Interactive Chat**: Conversational loop with Claude 4.5 Sonnet.
- **Tool Use**: Can read files from your local directory upon request.
- **Context Awareness**: Maintains conversation history.
