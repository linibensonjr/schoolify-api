from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from .students.views import students_namespace
from .courses.views import course_namespace
from .auth.views import auth_namespace
from .enrollment.views import enrollment_namespace
from .utils import db
from .models.courses import Course
from .models.users import Student, User
from .models.enrollment import Enrollment
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)
    
    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    api = Api(app)

    api.add_namespace(auth_namespace)
    api.add_namespace(students_namespace)
    api.add_namespace(course_namespace)
    api.add_namespace(enrollment_namespace)

    # db.init_app(app)

    @app.context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Student': Student,
            'Course': Course,
            'Enrollment': Enrollment
        }
    
    return app
