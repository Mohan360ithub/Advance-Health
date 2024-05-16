from frappe.model.document import Document
import frappe
 
class AdmissionForm(Document):
    # def on_update(self):
    #     self.create_user()
 
    # def after_save(self):
    #     self.send_email_after_create()   
 
 
 
 
    def create_user(self):
        existing_user = frappe.get_all('User', filters={'email': self.email_id}, fields=['name'])
        
        if existing_user:
            return  # User already exists, so return without further action
        else:
            user_doc = {
                'doctype': 'User',
                'email': self.email_id,
                'first_name': self.name_of_applicant if self.name_of_applicant else 'DefaultFirstName',
                'contact_no': self.contact_no,
                'send_welcome_email': False,
                'module_profile': 'No'  # Setting module_profile to 'No'
            }
 
            user = frappe.get_doc(user_doc)
 
            # Set the contact number as the password
            user.new_password = self.contact_no
 
            # Assign role
            role = frappe.get_all('Role', filters={'name': 'Advance Health Customer'}, fields=['name'])
            if role:
                user.add_roles(role[0]['name'])
                user.save()
                return  # User created successfully, so return without further action
            else:
                frappe.throw("Role 'Advance Health Customer' not found.")
 
 
 
    @frappe.whitelist()
    def send_email_before_create(self):
        # Retrieve the customer_name and mobile number from the Customer doctype
        customer_name = frappe.get_value("Customer", self.customer_id, "customer_name")
        mobile_no = frappe.get_value("Customer", self.customer_id, "mobile_no")
        
        # Retrieve the URL for the Before Treatment form
        before_treatment_url = f"/before-treatment/new?customer_id={self.customer_id}&form_id={self.name}&customer_name={customer_name}&custom_contact_no={mobile_no}"
        
        # Construct the HTML message body with user details and the link to Before Treatment form
        message = f"""<html>
            <body>
                <p>Dear {customer_name},</p>
                <p>In order to provide you with the best possible care, we kindly request you to fill out the <a href="{before_treatment_url}">Before Treatment form</a> with accurate information. Your responses will help us understand your specific needs and tailor our services accordingly.</p>
                <p>Best regards,</p>
                <p>drravi@idealcure4u.com,</p>
                <p>Mobile No: 9373101813,</p>
                <p>Advanced Health Team</p>
            </body>
            </html>"""
 
 
        subject = "Before Treatment Form"
        recipients = self.email_id
        
        # Send email using Frappe's email function
        frappe.sendmail(recipients=recipients, subject=subject, message=message)
        
        return "Email sent successfully."
    
    @frappe.whitelist()
    def send_email_after_create(self):
        # Retrieve the customer_name and mobile number from the Customer doctype
        customer_name = frappe.get_value("Customer", self.customer_id, "customer_name")
        mobile_no = frappe.get_value("Customer", self.customer_id, "mobile_no")
        
        # Retrieve the URL for the After Treatment form
        after_treatment_url = f"/after-treatment/new?customer_id={self.customer_id}&form_id={self.name}&customer_name={customer_name}&custom_contact_no={mobile_no}"
        
        # Construct the HTML message body with user details and the link to After Treatment form
        message = f"""<html>
            <body>
                <p>Dear {customer_name},</p>
                <p>In order to provide you with the best possible care, we kindly request you to fill out the <a href="{after_treatment_url}">After Treatment form</a> with accurate information. Your responses will help us understand your specific needs and tailor our services accordingly.</p>
                <p>Best regards,</p>
                <p>drravi@idealcure4u.com,</p>
                <p>Mobile No: 9373101813,</p>
                <p>Advanced Health Team</p>
            </body>
            </html>"""
 
        subject = "After Treatment Feed Back Form"
        recipients = self.email_id
        
        # Send email using Frappe's email function
        frappe.sendmail(recipients=recipients, subject=subject, message=message)
        
        return "Email sent successfully."
 
# eval:doc.which_treatment_plan_have_you_joined == 'Others'
