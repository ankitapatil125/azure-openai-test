from openai import AzureOpenAI

# Configuration
api_key = "5hVXsB3VruO9HkglBLZIhrumjBzb4ZxL2NVRKmineokod0JmmEBtJQQJ99BHACfhMk5XJ3w3AAAAACOGI8ai"
endpoint = "https://ankit-me34krax-swedencentral.openai.azure.com/"
deployment_name = "gpt-35-turbo"
api_version = "2024-12-01-preview"

# Initialize the client
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=api_version,
)

# Start conversation loop
print("🔹 Azure OpenAI Chatbot (GPT-3.5 Turbo)\nType 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.strip().lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        ai_response = response.choices[0].message.content.strip()
        print("AI:", ai_response)

    except Exception as e:
        print("❌ Error:", e)
