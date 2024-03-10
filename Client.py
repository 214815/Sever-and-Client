import xmlrpc.client

server_url = "http://localhost:8000/"
proxy = xmlrpc.client.ServerProxy(server_url)

def add_note():
    topic = input("Enter topic: ")
    text = input("Enter text: ")
    timestamp = input("Enter timestamp (YYYY-MM-DD): ")
    result = proxy.save_note(topic, text, timestamp)
    print(result)

def get_topic_notes():
    topic = input("Enter topic to retrieve notes: ")
    notes = proxy.get_notes(topic)
    if notes:
        for note in notes:
            print(note)
    else:
        print("No notes found for this topic.")

def search_wikipedia_topic():
    topic = input("Enter topic to search on Wikipedia: ")
    result = proxy.search_wikipedia(topic)
    print(result)

def main():
    while True:
        print("\n1. Add a note\n2. Get notes by topic\n3. Search Wikipedia for a topic\n4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_note()
        elif choice == "2":
            get_topic_notes()
        elif choice == "3":
            search_wikipedia_topic()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
