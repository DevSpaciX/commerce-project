Hello ! In this project, I implemented a simple principle of working with clients who can book any service for a certain time. To make payment through Stripe work for you:
1. You need to register here : https://dashboard.stripe.com/login_success?redirect=%2F
2. Get your secret and public api keys
3. Configure the Stripe request handler (webhook)  how to do it is described here: https://stripe.com/docs/stripe-cli#install
4. Here is full tutorial if you got problems : https://testdriven.io/blog/django-stripe-tutorial/