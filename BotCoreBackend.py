import google.generativeai as genai
import mysql.connector
from time import sleep
import re
import json

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

db_config = {
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'host': 'localhost',
    'database': 'Cloudveerge'
}

bot_id = 8
instructions_file = 'instructions.json'

def load_instructions(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in {file_path}.")
        return {}

instructions = load_instructions(instructions_file)

def fetch_unread_messages():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chat_message WHERE `For` = %s AND `Viewed` = 0", (bot_id,))
        messages = cursor.fetchall()
        cursor.close()
        connection.close()
        return messages
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []

def clean_message(text):
    emoji_pattern = re.compile(
        "["  
        "\U0001F600-\U0001F64F" 
        "\U0001F300-\U0001F5FF"  
        "\U0001F680-\U0001F6FF"  
        "\U0001F1E0-\U0001F1FF"  
        "\U00002700-\U000027BF"  
        "\U0001F900-\U0001F9FF"  
        "\U0001FA70-\U0001FAFF"  
        "\U00002600-\U000026FF"  
        "\U00002B50-\U00002B55"  
        "]",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub("", text)
    return text.strip()

def find_instruction(message_text):
    for key, data in instructions.get("instructions", {}).items():
        if data["question"] in message_text.lower():
            return data["answer"]
    return None

def generate_response(message_text):
    instruction_response = find_instruction(message_text)
    if instruction_response:
        return instruction_response

    prompt = f"You are a bot for a social network, respond to the following question: {message_text}"
    try:
        response = model.generate_content(prompt)
        if response:
            return clean_message(response.text)
    except Exception as e:
        print(f"Error generating response: {e}")
    return "Sorry, I couldn't generate a response."

def save_response_message(chat_id, message_text):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO chat_message (`From`, `For`, `Message`, `Viewed`, `Date`) VALUES (%s, %s, %s, %s, NOW())",
            (bot_id, chat_id, message_text, 1)
        )
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Database error while saving response: {e}")

def mark_message_as_read(message_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("UPDATE chat_message SET `Viewed` = 1 WHERE `ID` = %s", (message_id,))
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Database error while marking message as read: {e}")

def bot_loop():
    while True:
        try:
            messages = fetch_unread_messages()
            for message in messages:
                user_id = message['From']
                message_text = message['Message']
                response_text = generate_response(message_text)

                print(f"Sending message to user {user_id}: {response_text}")

                save_response_message(user_id, response_text)
                mark_message_as_read(message['ID'])
            
            sleep(5)
        except Exception as e:
            print(f"Error occurred in bot loop: {e}")
            sleep(1)

if __name__ == "__main__":
    bot_loop()
