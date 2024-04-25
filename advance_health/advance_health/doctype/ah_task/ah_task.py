import frappe
from frappe.model.document import Document
 
class AHTask(Document):
    def before_save(self):
        assigned_users = self.assign_to_user or []
 
        # If the document is being created for the first time, save it first
        if not self.is_new():
            # Share the document with each assigned user
            for user in assigned_users:
                print("Sharing with User:", user.user)
 
                # Share the document with read and write access
                frappe.share.add('AH Task', self.name, user.user, read=1, write=1)
 
            # Remove access for users who are not in the updated list
            current_users = [user.user for user in assigned_users]
            previous_users = frappe.share.get_users('AH Task', self.name)
            previous_user_ids = [user['user'] for user in previous_users] if previous_users else []
            users_to_remove = list(set(previous_user_ids) - set(current_users))
 
            for user_to_remove in users_to_remove:
                print("Removing access for User:", user_to_remove)
                frappe.share.remove('AH Task', self.name, user_to_remove)
 
    def after_insert(self):
        # After the document is inserted, if it's a new task, share it with assigned users
        if self.is_new():
            self.share_with_assigned_users()
 
    def share_with_assigned_users(self):
        assigned_users = self.assign_to_user or []
        
        # Share the document with each assigned user
        for user in assigned_users:
            print("Sharing with User:", user.user)
 
            # Share the document with read and write access
            frappe.share.add('AH Task', self.name, user.user, read=1, write=1)
