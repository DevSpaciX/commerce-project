Hello ! In this project, I implemented a simple principle of working with clients who can book any service for a certain time.
To start my project locally you need write some simple commands:

1. Download python 3.10 Windows(https://www.python.org/downloads/release/python-3100/) , Ubuntu (https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/)
2. python -m venv env
3. source env/bin/activate (Windows : venv/Scripts/activate)
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py loaddata fixture_file.json 
7. python manage.py runserver

If you want to create more data just run python manage.py createsuperuser and login by your username/password 
OR you can use fixture superuser : 
username : admin
password : admin

  In .env.sample you have 3 variables : 
- STRIPE_SECRET_KEY ( need to stripe payment work fine ),
- STRIPE_ENDPOINT_SECRET ( need to handle request payment ),
- SECRET_KEY ( that`s your djando secret key to run project ),

To make payment through Stripe work for you:
1. You need to register here : https://dashboard.stripe.com/login_success?redirect=%2F
2. Get your secret and public api keys
3. Configure the Stripe request handler (webhook)  how to do it is described here: https://stripe.com/docs/stripe-cli#install
4. Here is full tutorial if you got problems : https://testdriven.io/blog/django-stripe-tutorial/
5. IMPORTANT! Paste your keys into settings or .env.sample file to load secret information from 
