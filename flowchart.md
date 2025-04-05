graph TD
    A[Start] --> B{weather query?}
    B -->|yes| C{query contains HK district?}
    B -->|no| D{user input}
    
    D -->|greet| E[say hello]
    D -->|bye| F[say bye]
    D -->|other| G[chitchat/optional]
    
    E --> H[reset values: district, time, weather type]
    F --> End
    G --> End
    
    C -->|no| I[ask district]
    C -->|yes| J{forecasting time known?<br/>[current, today, tomorrow]}
    
    I --> K[Tell generic weather<br/>currently in district]
    K --> End
    
    J -->|no| K
    J -->|yes| L{specific query?<br/>[temperature, humidity,<br/>rainfall, UV index, warnings]}
    
    L -->|no| M[Tell generic weather info:<br/>- Current: temp, humidity, rain, UV, warnings<br/>- Today/Tomorrow: temp range, humidity range,<br/>weather description, rain probability,<br/>general situation]
    L -->|yes| N[Tell specific weather info:<br/>- Current: exact value for parameter<br/>- Today/Tomorrow: forecast range/probability<br/>for specific parameter]
    
    M --> End
    N --> End