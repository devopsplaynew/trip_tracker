import os
from datetime import datetime
import requests

class WhatsAppNotifier:
    def __init__(self):
        # Using CallMeBot API (Free WhatsApp notifications)
        # Sign up at: https://www.callmebot.com/blog/free-api-whatsapp-messages/
        self.api_key = os.environ.get("CALLMEBOT_API_KEY", "")  # Get from CallMeBot
        self.phone_number = os.environ.get("WHATSAPP_PHONE", "")  # Your phone with country code
        self.enabled = bool(self.api_key and self.phone_number)
    
    def send_message(self, message):
        """Send WhatsApp message using CallMeBot API (Free)"""
        if not self.enabled:
            print("WhatsApp notifications not configured")
            return False
        
        try:
            # CallMeBot API endpoint
            url = f"https://api.callmebot.com/whatsapp.php"
            params = {
                "phone": self.phone_number,
                "text": message,
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                print("WhatsApp notification sent successfully")
                return True
            else:
                print(f"Failed to send WhatsApp notification: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending WhatsApp notification: {str(e)}")
            return False
    
    def notify_new_transaction(self, name, trans_type, amount, place):
        """Send notification for new transaction"""
        emoji = "💰" if trans_type == "Income" else "💸"
        message = f"""
🆕 *New Transaction Added*
{emoji} *{name}* added {trans_type}
📍 {place}
💵 Amount: ₹{amount:,.2f}
📅 Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}
        """.strip()
        return self.send_message(message)
    
    def notify_transaction_approved(self, name, trans_type, amount, place):
        """Send notification for approved transaction"""
        emoji = "✅"
        message = f"""
{emoji} *Transaction Approved*
👤 *{name}* - {trans_type}
📍 {place}
💵 Amount: ₹{amount:,.2f}
📅 Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}
Status: ✅ Approved
        """.strip()
        return self.send_message(message)
    
    def notify_transaction_deleted(self, name, trans_type, amount, place, deleted_by):
        """Send notification for deleted transaction"""
        message = f"""
🗑️ *Transaction Deleted*
👤 *{name}* - {trans_type}
📍 {place}
💵 Amount: ₹{amount:,.2f}
Deleted by: {deleted_by}
📅 Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}
        """.strip()
        return self.send_message(message)
    
    def send_trip_summary(self, summary_data):
        """Send trip summary via WhatsApp"""
        total_income = summary_data['total_income']
        total_expense = summary_data['total_expense']
        balance = total_income - total_expense
        
        message = f"""
📊 *Trip Expense Summary*
📅 {datetime.now().strftime('%d-%m-%Y %H:%M')}

💰 Total Income: ₹{total_income:,.2f}
💸 Total Expense: ₹{total_expense:,.2f}
⚖️ Net Balance: ₹{balance:,.2f}

👥 *Per Person:*
        """.strip()
        
        for person in summary_data['per_person']:
            message += f"\n• {person['Name']}: Income ₹{person['Income_Raw']:,.2f} | Expense ₹{person['Expense_Raw']:,.2f}"
        
        return self.send_message(message)
