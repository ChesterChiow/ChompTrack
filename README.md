# ChompTrack

Welcome to the official repository for NTU SC2006 Software Engineering group project **_ChompTrack_**.

<p align='center'>
  <img src="/ChompTrack/client/src/static/img/ChomptrackLogo.png" width=150 />
</p>

ChompTrack is your one-stop meal planner website, designed to make healthy eating and budgeting easy. With a vast selection of easy-to-follow recipes, users can conveniently plan daily meals while tracking their nutrition intake to ensure they meet their dietary goals. ChompTrack also reflects grocery prices, allowing users to manage their food budget efficiently. Built with Flask on the backend and HTML/CSS on the frontend, ChompTrack leverages several controllers for a streamlined user experience in nutrition tracking and meal planning.


<details>
<summary>Demo Video</summary>
<br>

[![SC2006 Demo Video](https://img.youtube.com/vi/clYcb9vEWFk/0.jpg)](https://youtu.be/clYcb9vEWFk)

</details>


<details>
<summary>Supporting Documentations</summary>
<br>

1. [Functional and Non-Functional Requirements](https://github.com/ChesterChiow/ChompTrack/blob/main/Supporting%20Documents/Functional%20%26%20Non-Functional%20Requirements.pdf)
2. [Use Case Model: Use Case Diagram and Descriptions](https://github.com/ChesterChiow/ChompTrack/tree/main/Supporting%20Documents/Use%20Case%20Model)
3. [User Interface Mockups](https://github.com/ChesterChiow/ChompTrack/blob/main/Supporting%20Documents/UI%20Mockup.pdf)
4. [Data Dictionary](https://github.com/ChesterChiow/ChompTrack/blob/main/Supporting%20Documents/Data%20Dictionary.pdf)
5. [Live Demo Presentation Slides](https://github.com/ChesterChiow/ChompTrack/blob/main/Supporting%20Documents/Live%20Demonstration%20Slides.pdf)
6. [Pydoc](https://github.com/ChesterChiow/ChompTrack/tree/main/pydoc)
7. [Test Cases and Testing Results](https://github.com/ChesterChiow/ChompTrack/blob/main/Supporting%20Documents/Test%20Cases%20and%20Testing%20Results.pdf)

</details>

<details>
<summary>Diagrams</summary>
<br>

1. [Use Case Diagram](https://github.com/ChesterChiow/ChompTrack/blob/main/Supporting%20Documents/Use%20Case%20Model/Use%20Case%20Diagram.jpg)
2. [Architecture Diagram](https://github.com/ChesterChiow/ChompTrack/blob/main/Diagrams/System%20Architecture.jpg)
3. [Class Diagram](https://github.com/ChesterChiow/ChompTrack/blob/main/Diagrams/Class%20Diagram.jpg)
4. [Sequence Diagrams](https://github.com/ChesterChiow/ChompTrack/tree/main/Diagrams/Sequence%20Diagrams)
5. [Dialog Map](https://github.com/ChesterChiow/ChompTrack/blob/main/Diagrams/Dialog%20Map.jpg)
6. [Key Boundary and Control Class Diagram](https://github.com/ChesterChiow/ChompTrack/blob/main/Diagrams/Key%20Boundary%20and%20Control%20Class%20Diagram.jpg)

</details>



<details>
<summary>Software Requirements Specification</summary>
<br>

1. [Software Requirements Specification](https://github.com/softwarelab3/2006-SCS2-44/blob/main/Lab5/Software%20Requirements%20Specification.pdf)

</details>

<br>

## Table of Contents

1. [Project Goals](#project-goals)
2. [Key Features](#key-features)
3. [Setup Instructions](#setup-instructions)
4. [Usage](#usage)
5. [App Design](#app-design)
   - [Frontend](#frontend)
   - [Backend](#backend)
   - [Tech Stack](#tech-stack)
   - [Design Tools](#design-tools)
6. [Design Patterns](#design-patterns)
7. [SOLID Principles](#solid-principles)
---

## Project Goals

Throughout the development of ChompTrack, we gained valuable insights into creating an effective, user-centered application for dietary tracking and meal planning. The project allowed us to explore the following areas:

- **Backend-Frontend Integration**: Implementing Flask as the backend framework provided experience in structuring API calls effectively and managing data flow between the client and server, ensuring a smooth and cohesive user experience.

- **Handling User-Specific Data**: Integrating features like dietary preferences, restrictions, and personalized meal plans taught us the importance of organizing and securing user data, enhancing functionality while safeguarding privacy.

- **API Utilization and Efficiency**: Leveraging the Spoonacular API, we gained insights into external data integration, managing recipe and ingredient data effectively, and optimizing performance through caching to minimize redundant requests.

- **Performance Optimization**: Implementing lazy loading for resource-heavy components and caching frequently accessed data allowed us to optimize performance, reduce load times, and improve the client-side experience.

- **Enhanced User Engagement**: Developing intuitive navigation using Flask routes and creating user-friendly interfaces for grocery and recipe tracking highlighted the importance of seamless user experience to drive sustained engagement.

This project provided a comprehensive experience in creating a practical, user-centered application to simplify meal planning.

## Key Features

- **Authentication**:
  - Login
  - Register
- **Profile Creation**:
  - Calculate suggested daily nutrition intake
- **Nutrition Tracking**
- **Meal Planning**
  - Add meal plan
  - Complete meal plan
  - Remove meal plan  
- **Recipe Selection**
  - View recipe list
  - Filter recipe list
- **Past Recipes View**:
  - Search past recipes by name
  - Filter past recipes by date.
- **Grocery List**:
  - Strikethrough an ingredient.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourUsername/ChompTrack.git
   cd 2006-SCS2-44/ChompTrack
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install & Setup Database (MySQL Workbench):**
   Installation & setup guide: https://youtu.be/u96rVINbAUI?si=j21IOXyq6zhWA5g4

   Retrieve the database credentials, and create the following file:
   
   - `server/DatabaseCtrl/credentials.py`:
   ```python
   SQL_CREDENTIALS = {
    'user':'',
    'password':'',
    'database':'ChompTrack',
    'host':'localhost',
    'port':3306
   }
   SPOONACULAR_API_KEY = 'your_api_key_here'
   ```

5. **API Key Setup**
   This project uses the Spoonacular API for recipe and ingredient data. Obtain an API key from [Spoonacular](https://spoonacular.com/food-api), and update the following file with the 
   API key:

   - `server/DatabaseCtrl/credentials.py`:
   ```python
   SPOONACULAR_API_KEY = 'your_api_key_here'
   ```

## Usage

1. **Run the Application:** Start the Flask server.
   ```bash
   python app.py
   ```
2. **Access the Application:** Visit [http://localhost:5000](http://localhost:5000) in your browser.


## App Design

### Frontend

The frontend is organized to provide a clean and modular structure for developing and maintaining the user interface. The main files and folders include:

- **`/pages`** - Contains the HTML files for various pages of the application. Each page represents a different screen or functionality within ChompTrack, such as meal planning, ingredient tracking, and user profile management.
  
- **`/static`** - Houses all static assets used by the frontend, organized as follows:
  - **`/css`** - Contains the stylesheets for the application, ensuring a cohesive design and responsive layout across all pages.
  - **`/img`** - Stores images, icons, and other graphical assets used within the application’s UI.
  - **`/js`** - Contains JavaScript files that control frontend logic and interactions, handling functionalities like form validation, user interactions, and dynamic content updates.

### Backend

The backend is developed in Python, following a modular approach to handle various responsibilities within the application. Below is an outline of key backend components:

- **`📁 DatabaseCtrl/`**
  - Contains database controllers that manage data storage and retrieval operations.
- **`📁 controllers/`**
  - Implements the application’s core logic and handles request processing.
- **`📁 entity/`**
  - Defines the entities (data models) for ChompTrack, structured to maintain data consistency.
- **`📁 enums/`**
  - Stores enumerations and constants for use across different backend components.

This structure supports a clean separation of concerns, enabling efficient data management and reducing complexity in business logic.

### Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: MySQL
- Version Control: Git, GitHub

### Design Tools

- [Figma](https://www.figma.com/design/pQxXAVn36epCdS9owHQtzl/lab1-UI-Mockup?node-id=0-1&node-type=canvas)

## Design Patterns

1. **`Factory Pattern`**
  - DBFactory: Simplifies database management by centralizing query type object creation through a single DBFactory class. Each entity only needs to reference DatabaseQueries to handle database interactions, which keeps our system clean and reduces dependencies.
  - FilterFactory: Dynamically creates specific filter objects at runtime based on the user's selected filter, and the object proceeds to execute its corresponding functions to apply the desired filter.

2. **`Facade Pattern`**
  - We applied the Facade pattern in our control classes, such as the RecipeCtrl class, to simplify interactions and reduce complexity. By instantiating Recipe and IngredientCtrl within the RecipeCtrl class and invoking their methods, we make the code more understandable and easier to maintain.

## SOLID Principles

1. **`Single Responsibility Principle (SRP)`**
- Different packages containing specific classes are created. Each class is responsible for a specific logic or task
2. **`Open-Closed Principle (OCP)`**
- The system is open to extension through the use of Factory pattern, which leverage abstraction.
3. **`Dependency Inversion Principle (DIP)`**
- High level and low level modules depend on abstractions through the use of interfaces

