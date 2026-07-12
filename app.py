from App.agents.campus_info_agent import ask_campus_bot

print("Campus Information Chatbot")

while True:
    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    answer = ask_campus_bot(question)

    print("\nAnswer:")
    print(answer)