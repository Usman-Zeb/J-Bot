# Ask J-Bot

**Ask J-Bot** is an AI-powered open-source chatbot developed in-house at **Jazz**, Pakistan’s largest telco and part of the VEON group. Designed to enhance customer experience and streamline support services, Ask J-Bot provides instant access to information about Jazz's packages, offers, data plans, complaints handling, and standard operating procedures (SOPs).

Built on **OpenAI’s GPT-3.5-turbo** API, Ask J-Bot leverages advanced **Natural Language Processing (NLP)** to offer a seamless conversational interface, allowing users to quickly and efficiently obtain the information they need.

## Features

- **Information on Jazz Packages**: Provides up-to-date details on voice, data, and SMS packages tailored to customer needs.
- **Data Offers and Promotions**: Gives instant access to the latest internet bundles, promotional offers, and exclusive deals.
- **Guidance on SOPs**: Clarifies standard operating procedures to help customers navigate services effortlessly.
- **Guidance on Complaints**: Assists customers with various complaints, offering tailored resolutions to enhance overall satisfaction.

## Walkthrough:

[Watch the walkthrough video of Ask J-Bot in action](https://github.com/user-attachments/assets/23605a79-3f30-4acd-920a-e0c2476915c9)

## How It Works

Ask J-Bot uses **LLM (Large Language Model)** technology, specifically **GPT-3.5-turbo**, to generate human-like text responses. The bot processes user queries in real-time, retrieving relevant information about Jazz's services and generating context-aware responses to meet customer needs.

Ask J-Bot also utilizes **RAG (Retrieval-Augmented Generation)**, combining retrieval techniques with generative models. This allows the chatbot to pull relevant data from Jazz’s internal systems and combine it with AI-generated responses to deliver accurate and up-to-date information.

## Cost Breakdown

While Ask J-Bot is free for customers to use, its underlying API incurs charges. The cost of using **OpenAI’s GPT-3.5-turbo API** is as follows:

- **$1.5 per million input tokens**
- **$2 per million output tokens**

### What is a Token?

Tokens are the building blocks of text in **GPT-3.5-turbo** models. A token can represent a word, sub-word segment, punctuation, or character. For example, **4 tokens typically represent one word in English**. The cost for using the API is calculated based on the number of tokens processed:

- **Input Tokens**: These are the tokens provided as part of a user query.
- **Output Tokens**: These are the tokens generated by the model in response to the query.

For example, a 750-word query would be approximately 3,000 tokens, and the response tokens would be charged separately.

## Key Terminologies

- **LLM (Large Language Model)**: AI-based models like GPT-3.5-turbo that generate human-like text based on large-scale training data. Used in chatbots, content generation, and various other NLP applications.
  
- **RAG (Retrieval-Augmented Generation)**: An approach combining retrieval techniques with generative models to produce more context-aware responses by incorporating relevant data from a database or index.

- **Token**: A unit of text used for processing by language models. Approximately 4 tokens make up a word in English.

- **Embedding**: A dense, high-dimensional representation of text, words, or other data, used to compare and retrieve similar text based on context or query.

- **Input**: The data or query provided to the model for processing, measured in tokens.

- **Output**: The response generated by the model, also measured in tokens.

## System Architecture

1. **Frontend**: A user-friendly chat interface allows customers to interact with Ask J-Bot. The chatbot interface is responsive and intuitive, ensuring seamless communication with users.

2. **Backend**: Powered by **GPT-3.5-turbo** for natural language understanding, Ask J-Bot processes customer queries by retrieving relevant information and generating contextually appropriate responses.

3. **Data Source**: **RAG** retrieves information from Jazz’s internal systems, including data on packages, offers, SOPs, and complaint resolutions. This information is processed by the AI to ensure responses are accurate and helpful.

4. **API Integration**: The chatbot interacts with **OpenAI's API**, sending input tokens (user queries) and receiving output tokens (AI-generated responses) based on real-time requests.

## Setup Instructions

To run or contribute to **Ask J-Bot**, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Usman-Zeb/Ask-J-Bot.git
   ```

2. Install the required dependencies:
   ```bash
   npm install
   ```

3. Set up your environment variables:
   - Create a `.env` file with your **OpenAI API key**:
     ```bash
     OPENAI_API_KEY=your_openai_api_key
     ```

4. Run the development server:
   ```bash
   npm start
   ```

5. Access the chatbot interface locally via `http://localhost:3000`.
