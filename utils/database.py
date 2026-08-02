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
    
    def add_transaction(self, name, place, amount, trans_type, comments=""):
        """Add a new transaction"""
        transactions = self._load_data()
        
        # Generate new ID
        new_id = 1
        if transactions:
            new_id = max(t.get("id", 0) for t in transactions) + 1
        
        transaction = {
            "id": new_id,
            "name": name.strip().title(),
            "place": place.strip().title(),
            "amount": float(amount),
            "type": trans_type,
            "comments": comments.strip(),
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M")
        }
        
        transactions.append(transaction)
        self._save_data(transactions)
        return transaction
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID"""
        transactions = self._load_data()
        transactions = [t for t in transactions if t.get("id") != transaction_id]
        self._save_data(transactions)
    
    def get_all_transactions(self):
        """Get all transactions sorted by newest first"""
        transactions = self._load_data()
        return sorted(transactions, key=lambda x: x.get("id", 0), reverse=True)
    
    def get_summary(self):
        """Get summary statistics"""
        transactions = self._load_data()
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
    
    def get_transaction_count(self):
        """Get total number of transactions"""
        return len(self._load_data())
