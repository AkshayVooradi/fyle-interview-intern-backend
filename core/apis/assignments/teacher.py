from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum
from core.libs.exceptions import FyleError

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    # assignment_id = incoming_payload.get('id')
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # Ensure the assignment exists, otherwise return 404
    if not assignment:
        raise FyleError(404, "This assignment doesn't exist")

    if assignment.teacher_id != p.teacher_id:
        raise FyleError(400, "You are not allowed to grade this assignment")


    # Ensure the assignment is either SUBMITTED or GRADED, not in DRAFT state
    if assignment.state not in [AssignmentStateEnum.SUBMITTED]:
        return APIResponse.respond(
            {"error": "Invalid assignment state", "message": "Only assignments that are submitted or graded can be graded"}
        ),400
    

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
