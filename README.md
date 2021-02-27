# FastAPI demo

For start demo:
1. Create virtual environment and make `pip install -r requirements.txt`
2. Change DNS in `config.py` as you needs. Or simply create in local Postgres db with name `test_db`, user `test_user` and password `test_pass`
3. Run command in terminal: `python server.py`
4. Visit http://127.0.0.1:8000 (start page) or http://127.0.0.1:8000/docs (for the documentation)

In this demo you can find following:
- CRUD examples
- Connection to Postgres DB using sessions and ORM
- Prepared requests for handy usage in Pycharm Pro or VSCode
