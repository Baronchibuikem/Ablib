
This is an online course web application where a teacher/author can create a course content and split them into modules and subject for other users to learn from.


To run this project
Please create a virtual environment
            python -m venv ./myenv
Activate the environment, if you are using bash
        source myenv/Scripts/activate
        
At this point you should have 2 folders in your main folder
            myenv
            eduflex
            
Next 
            cd eduflex
            pip install -r requirements.txt
This will install all the packages needed to run this application
            python manage.py makemigrations
            python manage.py migrate
            python manage.py createsuperuser
            python manage.py runserver
            
And you should be good to go.
To see a demo of this project, check chibyk.pythonanywhere.com
