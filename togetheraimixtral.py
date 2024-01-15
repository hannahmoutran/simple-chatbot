from openai import OpenAI
import datetime
import os

def get_log_filename():
    # Create a unique log file name using the current timestamp
    return "mixtralchat-" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"

def log_api_call(question, response, log_filename):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_entry = f"{current_time}:\nQuestion: {question}\nResponse:\n{response}\n\n"
    with open(log_filename, "a") as file:
        file.write(formatted_entry)

def format_conversation_history(conversation_history):
    formatted_history = []
    for message in conversation_history:
        if isinstance(message['content'], str):
            formatted_history.append(message)
        else:
            formatted_history.append({
                'role': message['role'],
                'content': str(message['content'])
            })
    return formatted_history

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('TOGETHER_API_KEY'),
  base_url='https://api.together.xyz',)

# Generate a unique log file name for this session
log_filename = get_log_filename()

conversation_history = []
while True:
    user_question = input("Enter your question (or 'exit' to quit): ")
    if user_question.lower() == 'exit':
        break

    # Add user question to conversation history
    conversation_history.append({"role": "user", "content": user_question})

    # Format the conversation history properly
    formatted_history = format_conversation_history(conversation_history)

    # Include the entire conversation history in the request
    completion = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=formatted_history
    )

    assistant_response = completion.choices[0].message.content
    print("Response:", assistant_response)

    # Add LLM response to conversation history
    conversation_history.append({"role": "assistant", "content": assistant_response})

    # Log the API call to the unique log file for this session
    log_api_call(user_question, assistant_response, log_filename)
