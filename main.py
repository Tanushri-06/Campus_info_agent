from App.services.rag_service import RAGService

def main():
    print("=" * 60)
    print("🎓 Interactive Campus Information Chatbot")
    print("Type 'exit' or 'quit' to end the chat.")
    print("=" * 60)

    rag = RAGService()

    while True:
        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            print("\nChatbot: Thank you! Have a great day.")
            break

        if not question.strip():
            continue

        try:
            answer = rag.query(question)
            print(f"\nChatbot: {answer}")

        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()