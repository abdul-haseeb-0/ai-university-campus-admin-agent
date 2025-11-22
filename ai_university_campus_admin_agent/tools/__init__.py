from ai_university_campus_admin_agent.tools.analyst_tools import (
    get_enrollment_statistics,
    get_student_demographics,
    get_financial_reports,
    get_activity_report,
    get_course_performance
    )

from ai_university_campus_admin_agent.tools.course_tools import (
    create_course,
    get_course,
    get_all_courses,
    update_course,
    get_course_enrollments,
    drop_course
)

from ai_university_campus_admin_agent.tools.fee_tools import (
    create_fee_structure,
    get_course_fees,
    calculate_student_fees,
    record_payment,
    get_payment_history,
    get_fee_types
)

from ai_university_campus_admin_agent.tools.registration_tools import (
    create_student,
    get_student,
    update_student,
    delete_student,
    enroll_course,
    get_student_registrations
)