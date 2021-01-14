from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Staff, Student, Courses, Data, student_courses

def create_app(test_config=None):
    # Create and configure the app 
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    @app.route('/<int:id>')
    def landing_page(id):
        courses_id = Courses.join(student_courses).join(Student).filter(student_courses.c.student_id == id).all()
        courses = Courses.query.filter(Courses.id == courses_id).all()
        return str(courses.format())

    @app.route('/login', methods=['POST'])
    def login():
        body = request.get_json()
        logincode = body.get('logincode', None)
        try:
            if logincode[0] == 'I' or logincode[0] == 'D' or logincode[0] == 'T':
                staff = Staff.query.filter(Staff.logincode == logincode).one()
                identifier = staff.id
            elif logincode[0] == 'S':
                student = Student.query.filter(Student.logincode == logincode).one()
                identifier = student.id
            else:
                abort(401)
            return jsonify({
                'success': True,
                'id': identifier
            }), 200
        except:
            abort(404)

    @app.route('/student/profile/<int:id>', methods=['GET'])
    def retrive_student(id):
        student = Student.query.get(id)
        if not student:
            abort(404)

        return jsonify({
                'success': True,
                'id': student.id,
                'name': student.name,
                'email': student.email,
                'address': student.address,
                'phone': student.phone,
                'gender': student.gender,
                'date_of_birth': student.date_of_birth,
            }), 200


    @app.route('/staff/profile/<int:id>', methods=['GET'])
    def retrive_staff(id):
        staff = Staff.query.get(id)
        if not staff:
            abort(404)

        return jsonify({
                'success': True,
                'id': staff.id,
                'name': staff.name,
                'email': staff.email,
                'address': staff.address,
                'phone': staff.phone,
                'gender': staff.gender,
                'job': staff.job,
                'date_of_birth': staff.date_of_birth,
            }), 200


    @app.route('/student/courses/<int:id>', methods=['GET'])
    def retrive_student_courses(id):
        try:
            courses_id = student_courses.query.filter(student_courses.student_id == id).all()
            courses = Courses.query.filter(Courses.id == courses_id).all()
            return jsonify({
                    'success': True,
                    'courses_details': courses.format(),
                    'length_of_courses': courses.length()
                }), 200
        except:
            abort(404)


    @app.route('/staff/courses/<int:id>', methods=['GET'])
    def retrive_staff_courses(id):
        try:
            course = Staff.courses.query.filter(Staff.courses.student_id == id).all()
            courses_details = Courses.query.filter(Courses.id == courses.courses_id).all()
            return jsonify({
                    'success': True,
                    'courses_details': courses_details,
                    'length_of_courses': courses_details.length()
                }), 200
        except:
            abort(404)


    @app.route('/staff/course/view/<int:id>', methods=['GET'])
    def retrive_course_staff(id):
        try:
            selection = Data.query.filter(Data.staff_id == id).all()
            content = [result.format() for result in selection]
            return jsonify({
                    'success': True,
                    'course_content': content,
                    'length_of_courses': content.length()
                }), 200
        except:
            abort(404)


    @app.route('/student/course/view/<int:id>', methods=['GET'])
    def retrive_course_student(id):
        try:
            selection = Data.query.filter(Data.course_id == id).all()
            content = [result.format() for result in selection]
            return jsonify({
                    'success': True,
                    'course_content': content,
                    'length_of_courses': content.length()
                }), 200
        except:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401
                
            
            
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()


