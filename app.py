def main():
    print("Hello! Dreamer AI is ready to assist you.")
    while True:
        user_input = input("> ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        else:
            # Placeholder for AI processing
            print(f"Processing your request: {user_input}")

if __name__ == "__main__":
    main()
