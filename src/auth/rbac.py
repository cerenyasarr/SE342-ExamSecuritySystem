class RoleBasedAccess:
    def __init__(self):
        self.roles = {
            'Admin': ['create_exam', 'delete_exam', 'manage_users', 'view_reports'],
            'Instructor': ['create_exam', 'upload_seating', 'view_my_reports'],
            'Proctor': ['view_exam_details', 'report_violation', 'override_checkin'],
            'Student': ['check_in', 'view_my_schedule']
        }

    def has_permission(self, role, action):
        """
        Checks if the given role has permission to perform the action.
        """
        if role not in self.roles:
            return False
        return action in self.roles[role]

# Example Usage
# rbac = RoleBasedAccess()
# allowed = rbac.has_permission('Instructor', 'create_exam')
