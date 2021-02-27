# FastAPI demo

For start demo:
1. Create virtual environment and make `pip install -r requirements.txt`
2. Change DNS in `config.py` as you needs. Or simply create in local Postgres db with name `test_db`, user `test_user` and password `test_pass`
3. Run command in terminal: `python server.py`
4. Visit http://127.0.0.1:8000 (start page) or http://127.0.0.1:8000/docs (for the documentation)

In this demo you can find following:
- CRUD examples
- Filtering with validation of input and output fields in API
- Offset and limits available for entities list
- Connection to Postgres DB using sessions and ORM
- Password hashing
- Requests for handy usage in Pycharm Pro or VSCode
- Example of one-to-many relations between Visitor and Log entities
- Separate routers for different entities 
- JWT authentication and defence API methods from unauthorized access

#### When using in production please generate new SECRET_KEY at token.py using `openssl rand -hex 32`