# AI-Powered Recruitment Chatbot

An interactive recruitment chatbot built with Streamlit that conducts technical interviews and facilitates candidate interactions.

## Features

- Candidate information collection
- Dynamic technical question generation based on candidate's tech stack
- Basic keyword-based answer evaluation
- Interactive chat interface
- Conversation history tracking
- Session state management

## Prerequisites

- Python 3.8+
- Streamlit
- Groq API key


## Installation

1. Clone repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Groq API key in code

## Usage

1. Start application:
   ```bash
   streamlit run app.py
   ```

2. Access at `http://localhost:8501`

3. Follow workflow:
   - Complete candidate information form
   - Answer technical interview questions
   - Engage in general chat
   - Review conversation history

## Project Structure

- `app.py`: Main chatbot logic
- `requirements.txt`: Project dependencies
- `README.md`: Documentation

## Components

### Candidate Information Collection
- Gathers personal details and tech stack
- Generates tech-specific questions

### Technical Question Evaluation
- Keyword-based response assessment

### General Chat
- AI-powered conversations via Groq API
- Interactive chat interface

### Conversation History
- Tracks full session dialogue

## Example Workflow

1. Candidate provides information
2. System asks 3 tech stack-specific questions
3. Open chat session begins
4. Session concludes with farewell

## Future Enhancements

- Advanced NLP answer evaluation
- Enhanced technical question customization
- Multi-step role-specific conversations
- User authentication
