# BotCoreBackend

**BotCoreBackend** is the server-side backend for AI bots in the messenger of my social network, responsible for managing their operations and interactions with users.

## Features

- Fetches unread messages from the database and processes them.
- Cleans up message content by removing emojis.
- Matches incoming messages with predefined instructions (if available).
- Generates AI-driven responses using Google Gemini AI.
- Sends responses to users and marks messages as read in the database.
- Runs in a continuous loop to process new messages in real-time.

## Technologies

- **Google Gemini AI** for generating responses to users' messages.
- **MySQL** for storing chat messages and user interactions.
- **Python** for backend implementation.
- **Regular Expressions (regex)** to clean messages from unwanted characters (such as emojis).

## Prerequisites

Before running the bot, make sure you have the following:

- Python 3.x installed
- MySQL server running
- Google API key for using Gemini AI
- Database `Cloudveerge` with the `chat_message` table set up
- Instructions file (`instructions.json`) with predefined responses

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Cloudveerge/BotCoreBackend.git
   cd BotCoreBackend
