# CITS5505_Group_Project
This project is to develop a web application to create a forms for Computer programming languag

## Overview:
This web application is primarily designed as a learning Q&A platform for students in the UWA, CSSE (Computer Science and Software Engineering) college. Currently, the main platform used by everyone to search for answers to computer-related questions is Stack Overflow. However, this application is too large and general, which results in very low search efficiency, and often the answers are not suitable and cannot solve the problem. Additionally, although each unit has relevant Q&A platforms on Teams or LMS, they are mostly very scattered, brief, lacking categorization and tagging, and students can only see very recent ones, with past records being invisible. Therefore, this application addresses the issues that the above two platforms cannot simultaneously address and can provide questions and answers related to courses under the CSSE college.


## Features:
- **Technical Forum**: Seamlessly search for various topic on many problems faced by students while working on computer programming.
- **Comprehensive Database**: Access a database of technical discussion along with the solution from various members.
- **Interactive Visualizations**: Asthetic Visualization .
- **Contribute to Forum**: Contribute to work by logging in to forum and get the upvote.


### 1. User Account Management
Allow users to create accounts, log in, and log out, manage their profiles, and set preferences.
### 2. Question Posting and Editing
Users can post new questions and edit/update existing ones.
### 3.	Question Categorization and Tagging
Allow questions to be categorized by topic and tagged for more precise classification, making it easier for other users to find relevant questions.
### 4.	Answers and Comments
Enable users to provide answers and comments on questions to share knowledge and experiences.
### 5. Voting and Sorting
Allow users to vote on questions and answers to increase or decrease their priority on the page, helping other users find the most useful information faster.
### 6. Marking Best Answers
Allow question askers to select and mark one answer as the best answer, making it easier for other users to find solutions.
### 7. Search and Filtering
Provide powerful search functionality allowing users to filter and search questions and answers based on keywords, tags, users, etc.
### 8.User Reputation and Badge System
Provide users with a reputation or badge system based on their contributions (such as asking questions, providing answers, voting, etc.) to evaluate their credibility and potentially provide privileges or rewards.
### 9. Community Management Tools
Provide tools and features such as reporting, banning, deleting, etc., to manage inappropriate behavior and content and maintain community order.
### 10. Community Dashboard
Provide a dashboard or homepage that displays the most popular, recent, and unanswered questions, as well as other relevant information to help users navigate the platform.

### 11. Notification and Alerts
Allow users to receive notifications about their questions, answers, and comments to stay informed about relevant activity.

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
### Run the Application
To run the application, run the following command:
```
flask run
```
The application will be running on http://localhost:5000/ by default.

### Linting and Formatting
To lint the code, run the following command, with the option `--show-source` to show the source code of the errors and `--fix` to fix the errors automatically:
```
ruff check .
```
To format the code, run the following command, with the option `--check` to check if the code is formatted correctly and `--diff` to show the differences between the original and formatted code:
```
python -m black .
```
### Testing
To run the test suite, run the following command:
```
pytest
```
To be decided

### Accessing the API Documentation
To be decided

## User Guide
To be decided

## Developer Guide
To be devided

## Contributing
To be decided

## License
To be decided