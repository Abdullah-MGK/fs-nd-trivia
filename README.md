# Flask Trivia

## QuickStart

### Requirements
- PostgreSQL
- Python3
- Node

### Installation
Clone or download the repository.

#### Backend Setup
1. Run `cd backend`
2. Run `pip install -r requirements.txt`, to install the required dependencies under your favorite virtual environment.
3. Run `pg_ctl -D <your DB Server Name> start`, to start your DB server.
4. Run `createdb trivia`, to create a DB with a name, trivia here.
5. Run `psql trivia < trivia.psql`, to populate tables with some data. 
6. Go `models.py` and set the following variables:
```
database_name = "trivia"
database_path = "postgresql://{}/{}".format('localhost:5432', database_name)
#db_url follows '[dialec]+[DBAPI(optional)]://[username]:[password(optional)]@[host]:[port]/[database_name]'
```
7. Run `FLASK_APP=flaskr FLASK_DEBUG=true FLASK_ENV=development flask run`

#### Frontend Setup
1. Run `cd frontend`
2. Run `npm install`, to install the required dependencies.
3. Run `npm start`
4. Open your browser and type `http://localhost:3000`
5. You made it! You should be able to use the application now.

#### Testing Setup
1. Run `cd backend`
2. To run the tests, run
```
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Endpoints

#### GET /categories
- request: N/A
- response: `success` `categories`
- example:
```
{
    'success':true,
    'categories': {
        "1": "Science",
        "2": "Art",
        "3": "Geography"
    }
}
```

#### GET /questions
- request: `?page=<page_number>`
- response: `success` `questions` `totalQuestions` `categories` `currentCategory`
- note: this returns 10 question per page
- note: this returns first page questions if page is not provided
- example:
```
{
    "success": true,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography"
    },
    "currentCategory": "",
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "totalQuestions": 2
}
```

#### DELETE /questions/<question_id>
- request: N/A
- response: `success` `deleted_question`
- example:
```
{
    "success": true,
    "deleted_question": 1
}
```

#### POST /questions
- request: `question` `answer` `category` `difficulty`
- response: `success` `question`
- example:
```
{
    "success": true,
    "question": {
        "id": 50,
        "question": "What is my name?"
        "answer": "Abdullah",
        "category": 1,
        "difficulty": 1
    }
}
```

#### POST /questions/search
- request: `searchTerm`
- response: `success` `questions` `totalQuestions` `categories` `currentCategory`
- example:
```
{
    "success": true,
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "totalQuestions": 2,
    "categories": [
        1,
        2
    ]
    "currentCategory": ""
}
```

#### GET /categories/<category_id>/questions
- request: N/A
- response: `success` `questions` `totalQuestions` `currentCategory`
- example:
```
{
    "success": true,
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "totalQuestions": 2,
    "currentCategory": 6
}
```

#### POST /quizzes
- request: `previous_questions` `quiz_category`
- response: `success` `question`
- note: this returns empty question when there is no more questions
- example:
```
{
    "success": true,
    "question": {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer Wor`ld Cup tournament?"
    }
}
```

### Error Handling

* 400: Bad Request
* 404: Not Found
* 422: Unprocessable Request
* 500: Internal Server Error

#### Response
`success` `error` `message`

exmaple
```
{
    "success": false,
    "error": 400,
    "message": "Bad Request"
}
```
