# Shopify Developer Winter 2021 Challenge

Challenge Link: https://docs.google.com/document/d/1ZKRywXQLZWOqVOHC4JkF3LqdpO3Llpfk_CkZPR8bjak/edit.
This image repository is built using Django. 

# Deployment
This project has been deployed to Google Kubernetes Engine (GKE). The project is live and can be accessed from [here](http://34.75.147.217:8000/login): 

All the images uploaded by admin (username: admin - password: leo123456) are public and would always be visible. Images by any other user would be privately visible to only that user.

# Installation and Setup
Using pyenv:
```bash
git clone https://github.com/saileshnankani/Shopify-Challenge.git
cd Shopify-Challenge
pyenv virtualenv 3.7.6 Shopify-Challenge
source activate Shopify-Challenge
pip install -r requirements.txt 
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations repository
python manage.py migrate repository
python manage.py runserver
```

# Endpoints
- /gallery
- /login 
- /upload
- /signup
- /graphql
- /admin

Once authenticated, you can also query the data using graphql by using the in-built tool at /graphql endpoint. 

```graphql
query getUsers {
  users {
    id
    username
  }
}

query getImages {
  images {
    id
    imageName
  }
}
```