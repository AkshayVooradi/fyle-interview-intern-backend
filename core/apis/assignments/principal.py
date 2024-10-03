from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema,TeacherSchema
from core.models.teachers import Teacher
from core import db
from core.libs.exceptions import FyleError

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)
principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of submitted and graded assignments"""
    assignments = Assignment.query.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    teachers = Teacher.query.all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)
    


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""

    assignment_id = incoming_payload.get('id')
    grade = incoming_payload.get('grade')

    assignment = Assignment.get_by_id(assignment_id)
    if not assignment:
        return APIResponse.respond({"error": "Assignment not found"}),404
    

    if assignment.state not in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]:
        raise FyleError(400, "only a graded or submitted assignment can be graded")
    

    assignment.grade = grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump),200