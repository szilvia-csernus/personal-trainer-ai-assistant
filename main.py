# https://platform.openai.com/docs/assistants/overview

import openai
from dotenv import load_dotenv
from typing_extensions import override
from openai import AssistantEventHandler

load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo"

# Create our Assistant

# assistant = client.beta.assistants.create(
#   name="Personal Trainer",
#   instructions="You are a highly knowledgable personal trainer and nutritionist.",
#   tools=[{"type": "code_interpreter"}],
#   model=model,
# )

# assistant_id = assistant.id
# print(assistant_id)

assistant_id = "asst_52gGnQcKtZjnF9Zs2oBp8QK4"

# Create a Thread

# thread = client.beta.threads.create()

# thread_id = thread.id
# print(thread_id)

thread_id = "thread_z4PtZKiN2ueAFCBQX5D2qe7m"

# Create a Message

# message = client.beta.threads.messages.create(
#   thread_id=thread_id,
#   role="user",
#   content="How do I get started working out to lose fat and build muscles?"
# )

# Run the Assistant

# https://platform.openai.com/docs/assistants/overview#streaming-response
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.
 
with client.beta.threads.runs.stream(
  thread_id=thread_id,
  assistant_id=assistant_id,
  instructions="Please address the user in a professional tone.",
  event_handler=EventHandler(),
) as stream:
  stream.until_done()