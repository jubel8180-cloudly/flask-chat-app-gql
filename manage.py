# ./manage.py
import click

from app import create_app
from flask.cli import FlaskGroup
from app.batch_processing import BatchOperation

app = create_app()

# app.debug = True

# cli = FlaskGroup(app)

# @cli.command("test")
# def test():
#    BatchOperation()

# @cli.command("create-user")
# @click.argument("name")
# def create_user(name):
#    pass

# if __name__ == "__main__":
#     cli()
    
# command example
"""
   run the flask app: $ python3 manage.py run
   run with host: $ python3 manage.py run --host 0.0.0.0 --port 3000
   test command: $ python3 manage.py test
   
"""
