from anthropic import Anthropic
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from tools import read_file

load_dotenv() 

@dataclass
class Agent:
    def __init__(self, client, get_user_message, tools: list):
        self.client = client
        self.get_user_message = get_user_message
        self.tools = tools
    
    def _run_inference(self, messages):
        print("_run inference")
        print("messages:", messages)
        message = self.client.messages.create(
                max_tokens=1024,
                messages=messages,
                model="claude-sonnet-4-5",
                tools=self.tools
            )

        return message

    def run(self):
        print("Chat with Claude. Ctrl-c to quit.")
        conversation = []
        
        while True:
            try: 
                user_message = self.get_user_message()

            except (EOFError, KeyboardInterrupt): 
                print("\nGoodbye!")
                break

            conversation.append({"role": "user", "content": user_message})

            response = self._run_inference(conversation)
            
            conversation.append({"role": "assistant", "content": response.content})

            for block in response.content:
                if block.type == "text":
                    print("Agent response: ", block.text)
                
                elif block.type == "tool_use":
                    print("Tool use: ", block.name, " with input: ", block.input)

                    tool_result_content = ""
                    if block.name == "read_file":
                        try:
                            tool_result_content = read_file(**block.input)
                        except Exception as e:
                            tool_result_content = str(e)

                    conversation.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": tool_result_content
                            }
                        ]
                    })

                    final_response = self._run_inference(conversation)
                    print(f"Agent: {final_response.content[0].text}")
                    conversation.append(final_response.content)
    

def main():
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    def get_user_message():
        print("User: ", end="", flush=True)
        user_message = input()
        return user_message
    
    tools = [read_file.to_dict()]
    
    agent = Agent(client, get_user_message, tools)
    response = agent.run()
    print("Agent: ", response[0].text)



if __name__ == "__main__":
    main()