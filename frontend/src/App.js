import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [currentStage, setCurrentStage] = useState('start');
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState(null);
  const [selectedInfoType, setSelectedInfoType] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const districts = ['Central', 'Wan Chai', 'Causeway Bay', 'Tai Po', 'Shatin', 'Tuen Mun', 'Yuen Long'];
  const forecastPeriods = ['Today', 'Tomorrow', '2-day forecast', '3-day forecast'];
  const infoTypes = ['Overall weather', 'Temperature', 'Humidity', 'Wind', 'UV index'];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const formatMessage = (text) => {
    return text.split('\n').map((line, index) => (
      <div key={index} className="message-line">
        {line}
      </div>
    ));
  };

  const sendMessage = async (message) => {
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/chat', { message });
      setMessages(prev => [...prev, 
        { text: message, isUser: true }, 
        { text: response.data.message, isUser: false, formatted: formatMessage(response.data.message) }
      ]);
      
      if (response.data.needs_location) {
        setCurrentStage('district');
      } else if (response.data.needs_forecast_period) {
        setCurrentStage('forecast_period');
        setSelectedDistrict(response.data.selected_location);
      } else if (response.data.needs_info_type) {
        setCurrentStage('info_type');
        setSelectedDistrict(response.data.selected_location);
        setSelectedPeriod(response.data.selected_period);
      } else {
        setCurrentStage('start');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, 
        { text: message, isUser: true }, 
        { text: "Sorry, I encountered an error. Please try again.", isUser: false }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDistrictSelect = (district) => {
    setSelectedDistrict(district);
    sendMessage(`What's the weather like in ${district}?`);
  };

  const handleForecastPeriodSelect = (period) => {
    setSelectedPeriod(period);
    const periodText = period.toLowerCase().replace(' forecast', '');
    const message = `Show me the ${periodText} weather forecast for ${selectedDistrict}`;
    sendMessage(message);
  };

  const handleInfoTypeSelect = (type) => {
    setSelectedInfoType(type);
    const cleanType = type.toLowerCase().replace(' weather', '');
    const periodText = selectedPeriod.toLowerCase().replace(' forecast', '');
    const message = `Show me the ${cleanType} for ${selectedDistrict} ${periodText} forecast`;
    sendMessage(message);
  };

  const handleOptionSelect = (option) => {
    if (option === 'Weather Query') {
      setCurrentStage('district');
    } else {
      sendMessage(option);
    }
  };

  const getWeatherIcon = (type) => {
    switch(type) {
      case 'Weather Query':
        return '🌤️';
      case 'Today':
        return '☀️';
      case 'Tomorrow':
        return '🌤️';
      case '2-day forecast':
        return '⛅';
      case '3-day forecast':
        return '🌥️';
      case 'Overall weather':
        return '🌡️';
      case 'Temperature':
        return '🌡️';
      case 'Humidity':
        return '💧';
      case 'Wind':
        return '💨';
      case 'UV index':
        return '☀️';
      default:
        return '🌤️';
    }
  };

  const LoadingIndicator = () => (
    <div className="message bot loading">
      <span></span>
      <span></span>
      <span></span>
    </div>
  );

  return (
    <div className="App">
      <header className="App-header">
        <h1>Weather Chatbot 🌤️</h1>
      </header>
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.isUser ? 'user' : 'bot'}`}>
              {msg.formatted || msg.text}
            </div>
          ))}
          {isLoading && <LoadingIndicator />}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="buttons-container">
          {currentStage === 'start' && (
            <div className="button-group">
              <button onClick={() => sendMessage('Hi')}>
                {getWeatherIcon('Weather Query')} Greet
              </button>
              <button onClick={() => handleOptionSelect('Weather Query')}>
                {getWeatherIcon('Weather Query')} Weather Query
              </button>
            </div>
          )}

          {currentStage === 'district' && (
            <div className="button-group">
              {districts.map(district => (
                <button key={district} onClick={() => handleDistrictSelect(district)}>
                  {getWeatherIcon('Weather Query')} {district}
                </button>
              ))}
            </div>
          )}

          {currentStage === 'forecast_period' && (
            <div className="button-group">
              {forecastPeriods.map(period => (
                <button key={period} onClick={() => handleForecastPeriodSelect(period)}>
                  {getWeatherIcon(period)} {period}
                </button>
              ))}
            </div>
          )}

          {currentStage === 'info_type' && (
            <div className="button-group">
              {infoTypes.map(type => (
                <button key={type} onClick={() => handleInfoTypeSelect(type)}>
                  {getWeatherIcon(type)} {type}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 