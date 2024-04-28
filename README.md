# install requirements
pip install -r requirements.txt

# run django
activate environment
copy env vars from .env.sample file; create a .env file and update your db credentials 

- ./manage.py migrate
- ./manage.py runserver


used postman for testing my api endpoints

### USER ###
# registration
http://127.0.0.1:8000/api/users/register/(method post)
# login
http://127.0.0.1:8000/api/users/login/ (method post)
# user list
http://127.0.0.1:8000/api/users/ (method get)
# user detail
http://127.0.0.1:8000/api/users/id/ (method get)

### RIDES ###
# status update
http://127.0.0.1:8000/api/rides/id/update_status/ (method put)
# ride create
http://127.0.0.1:8000/api/rides/ (method post)
# accept ride
http://127.0.0.1:8000/api/rides/id/accept_ride/ (method put)
