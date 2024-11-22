# Copyright (c) 2024, pankaj@360ithub.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeadFollowUp(Document):
    def before_insert(self):
        lead_id = self.lead_id
        lead = frappe.get_doc("Lead", lead_id)

        if lead and lead.followed_up != 1:
            lead.followed_up = 1
            lead.status = "Follow-Up"
            lead.save(ignore_permissions=True)  # Update the lead's followed_up field
            #frappe.msgprint(_("Lead {0} marked as followed up.").format(lead_id))

