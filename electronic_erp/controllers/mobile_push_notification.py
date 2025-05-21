import frappe
import requests
import json

@frappe.whitelist()
def enqueue_mobile_push_notification(message_content):
    frappe.enqueue(
        "electronic_erp.controllers.mobile_push_notification.send_mobile_push_notification",
        enqueue_after_commit=True,
        message_content=message_content,
        start=0
    )

def send_mobile_push_notification(message_content, start = 0):
    message = frappe.get_doc("Message Content")
    if message is None:
        return

    number_of_users = 100
    users = frappe.db.get_list("User",
        fields=['name', 'full_name'],
        start=start,
        page_length=number_of_users,
        as_list=True
    )

    if not users:
        return
    
    to = []
    for user in users:
        message = frappe.new_doc("Message")
        message.message_content = message_content
        message.recipient = user.name
        message.recipient_name = user.full_name
        message.status = "Unread"
        message.title = message_content.title
        message.content = message_content.content
        message.save()

        mobile_push_settings = frappe.get_list("Mobile Push Settings", 
            filters={
                "user": user.name,
                "app": "tender"
            },
            fields=["expo_push_token"]
        )
        if mobile_push_settings:
            to.append(mobile_push_settings[0].expo_push_token)
    
    request_data = {
        "to": to,
        "body": message_content.content,
        "title": message_content.title
    }
    try:
        response = requests.post(
            "https://exp.host/--/api/v2/push/send",
            data=json.dumps(request_data),
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
    except Exception as e:
        frappe.log_error(
            title="Error Send Mobile Push Notification",
            message=f"error send message content[{message_content.name}]: {str(e)}"
        )

    frappe.enqueue(
        "electronic_erp.controllers.mobile_push_notification.send_mobile_push_notification",
        enqueue_after_commit=True,
        message_content=message_content,
        start=start + number_of_users
    )
