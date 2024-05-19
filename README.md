# CITS5505_Group_Project
This project is to develop a web application to create a forms for Computer programming language

## Overview:
This web application is primarily designed as a learning Q&A and career preparation platform for students in the UWA, CSSE (Computer Science and Software Engineering) college. Currently, the main platform used by everyone to search for answers to computer-related questions is something like Stack Overflow. However, Stack Overflow is too large and general, which results in very low search efficiency, and often the answers are not suitable and cannot solve the problem. Additionally, although each unit has relevant Q&A platforms on Teams or LMS, they are mostly very scattered, brief, lacking categorization and tagging, and students can only see very recent ones, with past records being invisible. Therefore, this application addresses the issues that the above two platforms cannot simultaneously address and can provide questions and answers related to courses under the CSSE college.Besides, they can also exchange the experiences about career preparation.

## Group Members:
| UWA ID     | Name         | Github Username |
|------------|--------------|-----------------|
| 23737198   | Jinsen Lou       | Jinsen_Lou |
| 22917174   | Raman Datta      | ramandatta87 |
| 23242469   | Qian Zhang       | zhangqianalone |

## Features
### Question Posting and Management
- **Create, Categorize, and Manage Questions:** Users can utilize a detailed form to post questions, select categories (Unit or Career Preparation), tag, and save drafts.
- **User Dashboard:** Manage and view posted questions, drafts, and favorite entries from a personalized dashboard.

### Interactive Post Viewing
- **View and Interact with Posts:** Each question on the platform is presented with details like title, tags, author, and date, accompanied by functionalities to add and view replies.

### Advanced Search Capabilities
- **Robust Search Functionality:** Supports keyword and tag-based searches to efficiently find relevant questions. Users can perform searches using simple keywords or a combination of tags and keywords.

### Detailed Response System
- **Engage with Detailed Discussions:** Offers a detailed view of each question where users can read and contribute responses, fostering an interactive dialogue environment.

### Navigational Ease
- **Streamlined Sidebar Navigation:** Easily access different sections such as 'All Posts', 'Tags', 'Career Preparation', and 'Unit Preparation' through the sidebar, enhancing user experience and content discovery.

## Getting Started
### Requirements
- [Python 3.9 or newer](https://www.python.org/downloads/)
- [Pip 21.1 or newer](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/downloads)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (Optional)

### Virtual Environment
It is recommended to use a virtual environment to run this project. To create a virtual environment, follow the instructions in the [Getting Started](./docs/Getting-Started.md) section. If you are using a virtual environment, make sure to activate it before installing the dependencies.

### Clone the Repository
To clone the repository, run the following command:
```
git clone https://github.com/ramandatta87/CITS5505_UWA_Group_Project.git
```
### Install Dependencies
To install all the dependencies, run the following command:
```
cd CITS5505_UWA_Group_Project
pip install -r requirements.txt
```
### Database initialization(if not already initialized)
Database setup using flask-migrate
- Initialize the migration repository (if not already initialized)
```
flask db init
```
- Generate the initial migration script 
```
flask db migrate -m
```
- Apply the migration to create the database and tables
```
flask db upgrade
```

### Run the Application
To run the application, run the following command:
```
flask run
```
The application will be running on http://localhost:5000/ by default.

### Testing
To run the test suite, run the following command:
```
pytest
```