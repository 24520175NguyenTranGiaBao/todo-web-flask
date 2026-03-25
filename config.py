import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mat-khau-du-phong'
    DB_PATH = os.path.join(BASE_DIR, 'todos.db')