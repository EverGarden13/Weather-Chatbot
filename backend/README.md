# Weather Chatbot Backend

This is the backend service for the Weather Chatbot application, built with Flask.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with the following variables:
```
PORT=5000
```

## Running the Application

To run the Flask application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

- `GET /api/health`: Health check endpoint
- `POST /api/chat`: Chat endpoint for weather queries

### Chat Endpoint

The chat endpoint accepts POST requests with the following format:
```json
{
    "message": "What's the weather like in Central?"
}
```

The response will be in the following format:
```json
{
    "message": "The current temperature in Central is 25°C",
    "status": "success",
    "needs_district": false
}
```

### Supported Queries

The chatbot supports the following types of queries:
- Greetings (hi, hello, hey)
- Goodbyes (bye, goodbye)
- Weather queries:
  - Temperature
  - Rainfall
  - UV index
  - Weather warnings
  - General weather forecast

### Hong Kong Districts

The chatbot recognizes the following Hong Kong districts:
- Central
- Wan Chai
- Causeway Bay
- Tai Po
- Shatin
- Tuen Mun
- Yuen Long 