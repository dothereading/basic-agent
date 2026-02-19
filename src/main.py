from anthropic import Anthropic
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from tools import read_file, write_file, run_bash

load_dotenv() 

@dataclass
class Agent:
    def __init__(self, client, get_user_message, tools: list):
        self.client = client
        self.get_user_message = get_user_message
        self.tools = tools
    
    def _run_inference(self, messages):
        message = self.client.messages.create(
                max_tokens=10000,
                messages=messages,
                model="claude-sonnet-4-6",
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

            while True:
                response = self._run_inference(conversation)
                conversation.append({"role": "assistant", "content": response.content})

                tool_results = []
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
                        elif block.name == "write_file":
                            try:
                                tool_result_content = write_file(**block.input)
                            except Exception as e:
                                tool_result_content = str(e)
                        elif block.name == "run_bash":
                            try:
                                tool_result_content = run_bash(**block.input)
                            except Exception as e:
                                tool_result_content = str(e)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result_content
                        })
                if tool_results:
                    conversation.append({
                        "role":"user",
                        "content":tool_results
                    })
                else:
                    break
        

def main():
    client = Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    def get_user_message():
        print("User: ", end="", flush=True)
        user_message = input()
        return user_message
    
    tools = [
        read_file.to_dict(), 
        write_file.to_dict(),
        run_bash.to_dict()]
    
    agent = Agent(client, get_user_message, tools)
    response = agent.run()
    print("Agent: ", response[0].text)



if __name__ == "__main__":
    main()