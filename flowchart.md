graph TD
    A[Start] --> B{Chatbot: Greeting message}
    B -->|Greeting| C[Chitchat]
    C --> D[End]
    
    B -->|Ask for Weather| E{Location}
    E --> F{Today/Tomorrow/2 Day/3 Day}
    F --> G{Overall/Temp/Humidity/Wind/UV}
    G --> H[End]