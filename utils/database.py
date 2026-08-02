import json
import os
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self, filepath="data/transactions.json"):
        self.filepath = filepath
        self._ensure_data_directory()
        self._ensure_data_file()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
    
    def _ensure_data_file(self):
        """Create data file if it doesn't exist"""
        if not os.path.exists(self.filepath):
            self._save_data([])
    
    def _load_data(self):
        """Load transactions from JSON file"""
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, transactions):
        """Save transactions to JSON file"""
        with open(self.filepath, 'w') as f:
            json.dump(transactions, f, indent=2)
    
    def add_transaction(self, name, place, amount, trans_type, comments="", date=None, added_by=None):
        """Add a new transaction (pending approval)"""
        transactions = self._load_data()
        
        # Generate new ID
        new_id = 1
        if transactions:
            new_id = max(t.get("id", 0) for t in transactions) + 1
        
        # Use provided date or current date
        if date is None:
            date = datetime.now().strftime("%d-%m-%Y")
        
        transaction = {
            "id": new_id,
            "name": name.strip().title(),
            "place": place.strip().title(),
            "amount": float(amount),
            "type": trans_type,
            "comments": comments.strip(),
            "date": date,
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "added_by": added_by or "unknown",
            "approved": False,  # Pending approval
            "approved_by": None,
            "approved_date": None
        }
        
        transactions.append(transaction)
        self._save_data(transactions)
        return transaction
    
    def approve_transaction(self, transaction_id, approved_by):
        """Approve a transaction"""
        transactions = self._load_data()
        
        for trans in transactions:
            if trans.get("id") == transaction_id:
                trans["approved"] = True
                trans["approved_by"] = approved_by
                trans["approved_date"] = datetime.now().strftime("%d-%m-%Y %H:%M")
                break
        
        self._save_data(transactions)
        return True
    
    def delete_transaction(self, transaction_id, deleted_by=None):
        """Delete a transaction by ID (admin only)"""
        transactions = self._load_data()
        deleted_trans = None
        
        for trans in transactions:
            if trans.get("id") == transaction_id:
                deleted_trans = trans
                break
        
        transactions = [t for t in transactions if t.get("id") != transaction_id]
        self._save_data(transactions)
        return deleted_trans
    
    def get_all_transactions(self, include_pending=True):
        """Get all transactions sorted by newest first"""
        transactions = self._load_data()
        if not include_pending:
            transactions = [t for t in transactions if t.get("approved", False)]
        return sorted(transactions, key=lambda x: x.get("id", 0), reverse=True)
    
    def get_pending_transactions(self):
        """Get only pending transactions"""
        transactions = self._load_data()
        return sorted(
            [t for t in transactions if not t.get("approved", False)],
            key=lambda x: x.get("id", 0),
            reverse=True
        )
    
    def get_summary(self, only_approved=True):
        """Get summary statistics"""
        transactions = self._load_data()
        
        # Only include approved transactions for summary
        if only_approved:
            transactions = [t for t in transactions if t.get("approved", False)]
        
        if not transactions:
            return None
        
        df = pd.DataFrame(transactions)
        
        # Overall totals
        total_income = df[df["type"] == "Income"]["amount"].sum()
        total_expense = df[df["type"] == "Expense"]["amount"].sum()
        
        # Per person breakdown
        summary_data = []
        for name in df["name"].unique():
            person_df = df[df["name"] == name]
            income = person_df[person_df["type"] == "Income"]["amount"].sum()
            expense = person_df[person_df["type"] == "Expense"]["amount"].sum()
            
            summary_data.append({
                "Name": name,
                "Total Income": f"₹{income:,.2f}",
                "Total Expense": f"₹{expense:,.2f}",
                "Net Balance": f"₹{income - expense:,.2f}",
                "Income_Raw": income,
                "Expense_Raw": expense,
                "Balance_Raw": income - expense
            })
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "per_person": summary_data,
            "all_transactions": df
        }
    
    def clear_all(self):
        """Clear all transactions"""
        self._save_data([])
    
    def get_transaction_count(self, only_approved=True):
        """Get total number of transactions"""
        transactions = self._load_data()
        if only_approved:
            transactions = [t for t in transactions if t.get("approved", False)]
        return len(transactions)
