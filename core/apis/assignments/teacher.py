from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradingSchema
teacher_assignments_resources = Blueprint(
    'teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=["GET"], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(
        teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=["POST"], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Returns list of assignments"""
    # AssignmentGradingSchema().load(incoming_payload)
    grade_assignments_payload = AssignmentGradingSchema().load(incoming_payload)
    grade_assignments = Assignment.grade_assignment(
        _id=grade_assignments_payload.id,
        grade=grade_assignments_payload.grade,
        principal=p
    )
    db.session.commit()
    grade_assignment_dump = AssignmentSchema().dump(grade_assignments)
    return APIResponse.respond(data=grade_assignment_dump)
