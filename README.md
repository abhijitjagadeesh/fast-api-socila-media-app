What's implemented ? A social media (ish) type API
- Creating/getting Users
- User must be able to create, get, update, delete posts
- Users must be able to vote/like posts
- Users Authentication
- Scheme Validation

Tech stack:
Python
Framework - FastAPI
- Built in documentation powered by swagger UI
- Performance - Fast
- Built to build the APIs
Database - Postgress (why not ?? ;) )
ORM - sqlalchemy

Testing:
Postman
built in API docs from browser

Schema validation:
Pydantic

password encryption:
passlib, bcrypt

Typing:
typing library (obviously!!)

To run the dev server:
uvicorn app.main_with_orm:app --reload

TODO
stress test (why not ?) using Auto canon ? or may be something else lets see when we get there