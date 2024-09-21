from flask import Blueprint
from core.apis import decorators
from core import db
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.libs import assertions
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_graded_assignments(p):
    """Returns a list of submitted and graded assignments"""
    assignments = Assignment.get_assignments_by_teacher()
    assignments_data = AssignmentSchema().dump(assignments, many=True)
    all_work = []
    for work in assignments_data:
        if(work['state'] != "DRAFT"):
            all_work.append(work)


    return APIResponse.respond(data=all_work)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    test = Assignment.get_by_id(grade_assignment_payload.id)
    if(test.state == 'DRAFT'):
        assertions.base_assert(400,"FyleError")
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    
    db.session.commit()

    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

    return APIResponse.respond(data=graded_assignment_dump)