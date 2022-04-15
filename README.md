Content Management System.

Local Setup -

1. Clone repository 
2. install requiremnet.txt use command as "pip install -r requirements.txt"
3. run command in main project folder as "python manage.py makemigrations"
    - This will create migration file in migrations folder.
4. run command in main project folder as "python manage.py migrate" to apply migrations.
5. Start the server with "python manage.py runserver"


API End Points - 

1. Register new admin/user[POST]
    - http://127.0.0.1:8000/api/auth/register
    - Payload ={'email': 'admin@gmail.com',
                        'password': '123123Aa',
                        'role': '1',
                        'full_name': 'Author Three',
                        'phone': '+919888888888',
                        'address': 'Pune',
                        'city': 'Pune',
                        'state': 'Maharashtra',
                        'country': 'India',
                        'pincode': '415305'
                }

2. Login [POST]
    - http://127.0.0.1:8000/api/auth/login
    - payload = {
                    "email": "admin@gmail.com",
                    "password": "123123Aa"
                    }
3. Get users list [GET]
    - http://127.0.0.1:8000/api/auth/users
4. Create Content [POST]
    - http://127.0.0.1:8000/api/auth/content/create
    - Payload = {'title': 'Author2.2 title',
                'body': 'Author body',
                'summury': 'Author summery',
                'categories': 'Author category'}
                files=[
                ('document',('Invoice-061733D2-0003.pdf',open('/D:/Zeamo/assignment/role_based_auth/django-rest-role-jwt/api/tst_upload_files/Invoice-061733D2-0003.pdf','rb'),'application/pdf'))
                ]
5. Get Content list [GET]
    - http://127.0.0.1:8000/api/auth/contents

6. Get Content with uid [GET]
    - http://127.0.0.1:8000/api/auth/contents/83e3c4c2-a54b-4cc1-a65a-e866bb9c2a3c

7. Update Content with uid [PUT]
    - http://127.0.0.1:8000/api/auth/contents/83e3c4c2-a54b-4cc1-a65a-e866bb9c2a3c
    - Payload = {'title': 'Author2.2.1 title',
                'body': 'Author body',
                'summury': 'Author summery',
                'categories': 'Author category'}
                files=[
                ('document',('Invoice-061733D2-0003.pdf',open('/D:/Zeamo/assignment/role_based_auth/django-rest-role-jwt/api/tst_upload_files/Invoice-061733D2-0003.pdf','rb'),'application/pdf'))
                ]
8. Delete Content with uid [DELETE]
    - http://127.0.0.1:8000/api/auth/contents/80029dbd-8873-4e22-8125-f0cf25510c03

9. Search Content with keywords [GET]
    - http://127.0.0.1:8000/api/auth/search/author1