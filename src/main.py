from anthropic import Anthropic
from collections import dataclass
import os

@dataclass
class Agent:
    def __init__(self, client, get_user_message):
        self.client = client
        self.get_user_message = get_user_message
    
    def run(self):
        message = self.client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": self.get_user_message(),
                }
            ],
            model="claude-sonnet-4-5",
        )

        return message.content
        

def main():
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    def get_user_message():
        print("User: ", end="", flush=True)
        user_message = input()
        return user_message
    
    agent = Agent(client, get_user_message)
    response = agent.run()
    print("Agent: ", response)

    