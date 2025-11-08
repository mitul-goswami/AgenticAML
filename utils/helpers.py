import pandas as pd
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime

class DataValidator:
    """Utilities for data validation and cleaning"""
    
    @staticmethod
    def validate_case_id(case_id: str) -> bool:
        """Validate case ID format (e.g., CA1234)"""
        pattern = r'^CA\d+$'
        return bool(re.match(pattern, case_id))
    
    @staticmethod
    def clean_transaction_amount(amount: Any) -> float:
        """Clean and convert transaction amount to float"""
        if pd.isna(amount):
            return 0.0
        
        if isinstance(amount, str):
            # Remove currency symbols and commas
            cleaned = re.sub(r'[,$]', '', amount)
            try:
                return float(cleaned)
            except ValueError:
                return 0.0
        
        return float(amount) if amount else 0.0
    
    @staticmethod
    def parse_previous_cases(cases_str: str) -> List[str]:
        """Parse previous cases string into list"""
        if pd.isna(cases_str) or not cases_str:
            return []
        
        return [case.strip() for case in cases_str.split(',') if case.strip()]
    
    # Optional additions:
    @staticmethod
    def validate_customer_id(cust_id: str) -> bool:
        """Validate customer ID format (e.g., CUST1234)"""
        pattern = r'^CUST\d+$'
        return bool(re.match(pattern, cust_id))
    
    @staticmethod
    def validate_account_id(acc_id: str) -> bool:
        """Validate account ID format (e.g., ACC123)"""
        pattern = r'^ACC\d+$'
        return bool(re.match(pattern, acc_id))
    
    @staticmethod
    def validate_transaction_id(txn_id: str) -> bool:
        """Validate transaction ID format (e.g., TXN123)"""
        pattern = r'^TXN\d+$'
        return bool(re.match(pattern, txn_id))

class RiskCalculator:
    """Utilities for risk calculation"""
    
    @staticmethod
    def calculate_transaction_risk(amount: float, avg_amount: float) -> float:
        """Calculate risk based on transaction amount deviation"""
        if avg_amount == 0:
            return 0.0
        
        deviation_ratio = abs(amount - avg_amount) / avg_amount
        return min(deviation_ratio * 20, 40)  # Cap at 40 points
    
    @staticmethod
    def calculate_case_history_risk(previous_cases: List[str]) -> float:
        """Calculate risk based on previous case history"""
        case_count = len(previous_cases)
        
        if case_count == 0:
            return 0.0
        elif case_count == 1:
            return 15.0
        elif case_count <= 3:
            return 30.0
        else:
            return 50.0  # High risk for multiple cases
    
    # Optional additions:
    @staticmethod
    def calculate_age_occupation_risk(age: int, occupation: str, transaction_amount: float) -> float:
        """Calculate risk based on age-occupation-amount correlation"""
        risk_score = 0.0
        
        # High-value transactions by unemployed individuals
        if occupation.lower() == 'unemployed' and transaction_amount > 30000:
            risk_score += 25.0
        
        # Very young or very old with high transactions
        if (age < 25 or age > 65) and transaction_amount > 40000:
            risk_score += 15.0
        
        return min(risk_score, 30.0)  # Cap at 30 points
    
    @staticmethod
    def calculate_location_consistency_risk(locations: List[str]) -> float:
        """Calculate risk based on location consistency"""
        if len(set(locations)) > 3:  # More than 3 different locations
            return 10.0
        return 0.0
    
    @staticmethod
    def calculate_employer_consistency_risk(employers: List[str]) -> float:
        """Calculate risk based on employer consistency"""
        unique_employers = set(employers)
        if len(unique_employers) > 2:  # More than 2 different employers
            return 15.0
        return 0.0

# Optional: Additional utility functions
class DataAnalyzer:
    """Additional data analysis utilities"""
    
    @staticmethod
    def get_transaction_patterns(records: List[Dict]) -> Dict[str, Any]:
        """Analyze transaction patterns"""
        if not records:
            return {}
        
        amounts = [r.get('TransactionAmount', 0) for r in records]
        return {
            'min_amount': min(amounts) if amounts else 0,
            'max_amount': max(amounts) if amounts else 0,
            'median_amount': sorted(amounts)[len(amounts)//2] if amounts else 0,
            'amount_variance': sum((x - sum(amounts)/len(amounts))**2 for x in amounts) / len(amounts) if amounts else 0
        }
    
    @staticmethod
    def detect_anomalies(records: List[Dict]) -> List[str]:
        """Detect potential anomalies in the data"""
        anomalies = []
        
        for record in records:
            # Check for unusually high amounts for unemployed
            if (record.get('Occupation', '').lower() == 'unemployed' and 
                record.get('TransactionAmount', 0) > 35000):
                anomalies.append(f"High transaction amount ({record.get('TransactionAmount')}) for unemployed individual")
            
            # Check age-amount correlation
            age = record.get('Age', 0)
            amount = record.get('TransactionAmount', 0)
            if age < 25 and amount > 40000:
                anomalies.append(f"Very high transaction ({amount}) for young age ({age})")
            
        return anomalies
