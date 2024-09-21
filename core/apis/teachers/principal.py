from flask import Blueprint
from core.apis import decorators
from core.models.principals import Principal
from core.apis.responses import APIResponse
from core.apis.teachers.schema import TeacherSchema,Teacher

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    print("called")
    teachers = Teacher.get_all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)  