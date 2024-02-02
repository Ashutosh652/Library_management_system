Library Management System Backend API

### Steps to run this app:

1. Clone it.

2. Open the cloned project and enter the terminal.

3. Create a new virtual environment.
```
python3 -m venv venv
```

4. Activate the virtual environment:
```
source venv/bin/activate #Linux
.\venv\Scripts\activate #Windows
```

5. Install the requirements:
```
pip install -r requirements.txt
```

6. Open pgAdmin4 (Postgres),

7. Create a new database in pgAdmin4 by giving it a name and a password.

8. Create a new file named `.env` in the same level as the file `.env.example`.

9. Open the file `.env.example` and copy its contents into `.env`.

10. Modify the `DATABASE_URL` as specified in the example. If the example is `postgres://<user>:<password>@localhost:5432/<database_name>`, you need to write something like `postgres://username:password@localhost:5432/library_db`. The user, password and database name should be as you specified while creating the database. Make sure to keep the database running.

11. MakeMigrations and Migrate:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
This will create the tables in the database. You can check it in pgAdmin4. If the tables don't show up, make sure to refresh it by right clicking on 'Tables' and selecting refresh.

12. Create a superuser:
In the terminal where the virtual environment is active, enter the following:
```
python3 manage.py createsuperuser
```
This will prompt you to enter an email, first name, last name and password. Enter them. You should see 'Superuser created successfully'.

13. Run the server:
```
python3 manage.py runserver
```
Open up the development server. It will open by default on "http://127.0.0.1:8000".

14. You will see a 'Page Not Found' in the base link. Go to `http://127.0.0.1:8000/api/schema/docs/` to see SwaggerUI for the APIs.

15. Go to `http://localhost:8000/admin/` and login with the email and password of the superuser you just created.

16. In the admin panel, you will see different tables. One of them is `Sessions`. Click on it and you will see one entry in it with session key, session data and expiry date. This entry is there because you just logged in as the admin.

17. Here is the postman collection in json you can use to test the APIs:
`https://api.postman.com/collections/21338538-1f4f02fe-e974-4309-8a66-f2e0071a6803?access_key=PMAT-01HNKTSPCX3SMJP03Y89VD3A90`.
Import the above collection in postman.

18. Make sure your django server is running. Now in the postman collection, open the Logout tab and go to headers. You will see one header `Cookie` that contains a session id. Copy the `Session key` from django admin and replace the sessionid in postman Logout tab. Click on `Send`. You will now be logged out. If you try to access the admin panel again, it will prompt you to login again. You can login again.

19. Create a new user from the 'User Create' tab in postman.

20. Go to Login tab and send request with the new user you just created. After that if you go to adminpanel again, you will see two entries in the sessions table indicating a new user has just logged in. Non of the views require authentication right now since authentication. This is just a simple session authentication because it was an optional task.

21. Check the rest of the endpoints from the postman.