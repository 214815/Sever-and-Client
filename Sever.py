from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests
import threading

# Initialize or load the XML database
db_file = "E:\学习资料归纳\db.xml"
try:
    tree = ET.parse(db_file)
    root = tree.getroot()
except Exception as e:
    root = ET.Element("notes")
    tree = ET.ElementTree(root)


def save_note(topic, text, timestamp):
    """Save a note to the XML database."""
    for topic_element in root.findall('topic'):
        if topic_element.get('name') == topic:
            ET.SubElement(topic_element, "note", timestamp=timestamp).text = text
            tree.write(db_file)
            return "Note added to existing topic."

    new_topic = ET.SubElement(root, "topic", name=topic)
    ET.SubElement(new_topic, "note", timestamp=timestamp).text = text
    tree.write(db_file)
    return "New topic and note added."


def get_notes(topic):
    """Retrieve notes for a given topic."""
    for topic_element in root.findall('topic'):
        if topic_element.get('name') == topic:
            return [note.text for note in topic_element.findall('note')]
    return []


def search_wikipedia(topic):
    """Search Wikipedia for a given topic and append the first result link to the topic."""
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={topic}&limit=1&namespace=0&format=json"
    response = requests.get(url)
    data = response.json()

    if data[1]:  # If there is at least one result
        wiki_topic, wiki_link = data[1][0], data[3][0]
        save_note(topic, f"Wikipedia link: {wiki_link}", "Wikipedia API")
        return f"Added Wikipedia link to topic {topic}: {wiki_link}"
    return "No Wikipedia results found."


def run_server(host="localhost", port=8000):
    with SimpleXMLRPCServer((host, port), allow_none=True) as server:
        server.register_introspection_functions()
        server.register_function(save_note, "save_note")
        server.register_function(get_notes, "get_notes")
        server.register_function(search_wikipedia, "search_wikipedia")

        print(f"Server running on {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    threading.Thread(target=run_server).start()
