import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [currentStage, setCurrentStage] = useState('start');
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [selectedTime, setSelectedTime] = useState(null);
  const [selectedWeatherType, setSelectedWeatherType] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const districts = ['Central', 'Wan Chai', 'Causeway Bay', 'Tai Po', 'Shatin', 'Tuen Mun', 'Yuen Long'];
  const timePeriods = ['Current', 'Today', 'Tomorrow'];
  const weatherTypes = ['Temperature', 'Rainfall', 'UV Index', 'Warnings', 'General Forecast'];

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
      
      if (response.data.needs_district) {
        setCurrentStage('district');
      } else if (response.data.options && response.data.options.length > 0) {
        setCurrentStage('options');
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
    setCurrentStage('time');
    sendMessage(`What's the weather like in ${district}?`);
  };

  const handleTimeSelect = (time) => {
    setSelectedTime(time);
    setCurrentStage('weather_type');
    sendMessage(`What's the weather like in ${selectedDistrict} ${time.toLowerCase()}?`);
  };

  const handleWeatherTypeSelect = (type) => {
    setSelectedWeatherType(type);
    const message = `What's the ${type.toLowerCase()} in ${selectedDistrict} ${selectedTime.toLowerCase()}?`;
    sendMessage(message);
  };

  const handleOptionSelect = (option) => {
    if (currentStage === 'start') {
      if (option === 'Weather Query') {
        setCurrentStage('district');
      } else {
        sendMessage(option);
      }
    } else if (currentStage === 'options') {
      sendMessage(option);
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
        <h1>Weather Chatbot</h1>
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
              <button onClick={() => sendMessage('Hi')}>Greet</button>
              <button onClick={() => handleOptionSelect('Weather Query')}>Weather Query</button>
            </div>
          )}

          {currentStage === 'district' && (
            <div className="button-group">
              {districts.map(district => (
                <button key={district} onClick={() => handleDistrictSelect(district)}>
                  {district}
                </button>
              ))}
            </div>
          )}

          {currentStage === 'time' && (
            <div className="button-group">
              {timePeriods.map(time => (
                <button key={time} onClick={() => handleTimeSelect(time)}>
                  {time}
                </button>
              ))}
            </div>
          )}

          {currentStage === 'weather_type' && (
            <div className="button-group">
              {weatherTypes.map(type => (
                <button key={type} onClick={() => handleWeatherTypeSelect(type)}>
                  {type}
                </button>
              ))}
            </div>
          )}

          {currentStage === 'options' && (
            <div className="button-group">
              {messages[messages.length - 1]?.options?.map(option => (
                <button key={option} onClick={() => handleOptionSelect(option)}>
                  {option}
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