# Copyright (c) 2023, Mohan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AdvanceHealthUser(Document):
    def after_save(self):
        print(self.advance_health_crm)

    def on_submit(self):
        core_user = frappe.get_doc({
            "doctype": "User",
            "enabled":self.enabled,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "gender": self.gender,
            "birth_date": self.date_of_birth,
            "send_welcome_email": self.send_welcome_email,
            "mobile_no": self.mobile_no,
            "new_password": self.password,
            "module_profile":"No"
        })

        # Save the user
        core_user.insert()

        # Assign roles to the user using the add_roles method
        self.update_roles(core_user)

        # Save the user again to update roles
        core_user.save()

    def before_update_after_submit(self):
        core_user = frappe.get_all("User", filters={"email": self.email})
        if core_user:
            core_user = frappe.get_doc("User", core_user[0].name)
            core_user.new_password = self.password
            core_user.enabled = self.enabled
            core_user.birth_date = self.date_of_birth
            core_user.gender = self.gender
            core_user.mobile_no = self.mobile_no
            # Uncomment and customize the following lines if you want to update other fields in the User document
            # core_user.first_name = self.first_name
            # core_user.last_name = self.last_name
            # core_user.middle_name = self.middle_name
            # core_user.gender = self.gender
            # core_user.birth_date = self.date_of_birth
            # core_user.mobile_no = self.mobile_no
            # core_user.role_profile_name = self.role_profile

            # Update roles when the document is updated
            self.update_roles(core_user)

            core_user.save()

    def update_roles(self, user_doc):
        # Mapping between checkbox values and corresponding roles
        checkbox_role_mapping = {
            "advance_health_crm": "Advance Health CRM",
            "advance_health_admin": "Advance Health Admin",
            "advance_health_front_desk": "Advance Health Front Desk",
            "advance_health_accounts": "Advance Health Accounts",
            "advance_health_counceller": "Advance Health Counceller",
            "advance_health_digital_team": "Advance Health Digital Team",
        }

        # Clear existing roles
        user_doc.roles = []

        # Assign roles to the user using the add_roles method
        for checkbox_field, role_name in checkbox_role_mapping.items():
            if getattr(self, checkbox_field) == 1 and frappe.get_all("Role", filters={"role_name": role_name}):
                user_doc.add_roles(role_name)


    def on_trash(self):
        # Get the corresponding user document and delete it
        user = frappe.get_all("User", filters={"email": self.email})
        if user:
            frappe.delete_doc("User", user[0].name)