# Project Created by HUNG CHI MING (24125591G)

# Weather Chatbot

An AI-powered weather information system that combines expert system concepts with real-time weather data to provide intelligent weather forecasts and recommendations.

## Project Description

The Weather Chatbot is an intelligent system that provides weather information through a conversational interface. It integrates with the Hong Kong Observatory (HKO) Open Data API to fetch real-time weather data and uses expert system rules to process and present this information in a user-friendly manner.

### Key Features

- **Intelligent Chat Interface**: Natural language processing for understanding weather-related queries
- **Comprehensive Weather Data**: Access to current weather and forecasts
- **Expert System Rules**: Intelligent processing of weather data to provide meaningful insights
- **Multiple Weather Parameters**: Temperature, humidity, wind conditions, and UV index
- **Location-based Services**: Weather information for specific locations
- **User-friendly Interface**: Clean and intuitive design for easy interaction

## System Architecture

The project consists of two main components:

1. **Frontend**: React-based user interface
2. **Backend**: Flask server with expert system implementation

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- npm or yarn
- pip

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

## Running the Application

### Start the Backend Server

1. Navigate to the backend directory
2. Activate the virtual environment (if not already activated)
3. Run the Flask server:
   ```bash
   python app.py
   ```

### Start the Frontend Development Server

1. Navigate to the frontend directory
2. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```

The application will be available at `http://localhost:3000`

## Usage

1. Open the application in your web browser
2. The chatbot will greet you with a welcome message
3. You can ask questions about:
   - Current weather conditions
   - Weather forecasts (today, tomorrow, or next few days)
   - Specific weather parameters (temperature, humidity, wind, UV index)
   - Weather for specific locations

### Example Queries

- "What's the weather like today?"
- "Will it rain tomorrow?"
- "What's the temperature in Central?"
- "Is the UV index high today?"
- "How windy is it right now?"

## API Documentation

The system uses the HKO Open Data API for weather information. For detailed API documentation, refer to the `HKO_Open_Data_API_Documentation.pdf` file in the project root.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hong Kong Observatory for providing the weather data API
- All contributors who have helped in the development of this project