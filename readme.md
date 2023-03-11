**My site LIVE : https://commerce-pwjx.onrender.com/**

Hello ! In this project, I implemented a simple principle of working with clients who can book any service for a certain time.
To start my project locally you need write some simple commands:
## Features:
- Stripe payment
- Statistic in admin panel of all payments
- Chained dropdown list of available training time
## Installing using GitHub:
```python
python3 -m venv env
source env/bin/activate (Windows : venv/Scripts/activate)
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```
If you want to create more data just login by this superuser data :
username : admin
password: admin 
## Env variables:
  In .env.sample you have 3 variables : 
- STRIPE_SECRET_KEY ( need to stripe payment work fine ),
- STRIPE_ENDPOINT_SECRET ( need to handle request payment ),
- SECRET_KEY ( that`s your djando secret key to run project ),
## Stripe:
To make payment through Stripe work for you:
- You need to register here : https://dashboard.stripe.com/login_success?redirect=%2F
- Get your secret and public api keys
- Configure the Stripe request handler (webhook)  how to do it is described here: https://stripe.com/docs/stripe-cli#install
- Here is full tutorial if you got problems : https://testdriven.io/blog/django-stripe-tutorial/
IMPORTANT! Paste your stripe keys and SECRET_KEY (that`s your djando secret key to run project ) into settings or .env.sample file to load secret information from AND RENAME FILE TO .env !
- To create test payment just use this card number: 4242 4242 4242 4242

## Screenshots
![image](https://user-images.githubusercontent.com/102595649/224473708-01f94820-4fe9-43e1-9146-7e22465e2d19.png)
![image](https://user-images.githubusercontent.com/102595649/224473846-78befcec-963f-4e37-af8b-b377b280d264.png)
![image](https://user-images.githubusercontent.com/102595649/224473870-e8cf82f3-b257-4f95-8a0b-0391b59ba537.png)
![image](https://user-images.githubusercontent.com/102595649/224473900-663c1cf5-1ddc-43de-b182-53742df2eecb.png)
![image](https://user-images.githubusercontent.com/102595649/224473923-26c265b2-fc70-47d6-82f6-caf9c387003d.png)

