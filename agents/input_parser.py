import re
from typing import Dict, List, Optional
from langchain_core.messages import HumanMessage
from agents.graph_state import CaseAnalysisState
import time

class InputParserNode:
    """Enhanced Input Parser Node for comprehensive case data extraction"""
    
    def __init__(self):
        # Define all expected fields for comprehensive parsing
        self.required_fields = [
            'Case ID', 'Name', 'CustID', 'Accounts', 'Transactions', 'Previous Cases'
        ]
        
        # Define parsing patterns for better extraction
        self.field_patterns = {
            'Case ID': [r'Case ID:', r'CaseID:', r'Case_ID:', r'ID:'],
            'Name': [r'Name:', r'Customer Name:', r'Customer:'],
            'CustID': [r'CustID:', r'Customer ID:', r'CustomerID:', r'Cust_ID:'],
            'Accounts': [r'Accounts:', r'Account:', r'Account Numbers:', r'Acc:'],
            'Transactions': [r'Transactions:', r'Transaction:', r'TXN:', r'Transaction ID:'],
            'Previous Cases': [r'Previous Cases:', r'Prev Cases:', r'Previous_Cases:', r'Prior Cases:']
        }
    
    def __call__(self, state: CaseAnalysisState) -> CaseAnalysisState:
        """Enhanced case input parsing with comprehensive field extraction"""
        try:
            print("📋 Step 1: Enhanced parsing of input file...")
            
            case_file_path = state['case_file_path']
            
            # Parse the case file with enhanced extraction
            case_data = self.parse_case_file_comprehensive(case_file_path)
            
            # Validate and enhance parsed data
            validated_data = self.validate_and_enhance_data(case_data)
            
            # Update state
            state['case_data'] = validated_data
            state['current_step'] = 'input_parsed_comprehensive'
            state['completed_steps'].append('enhanced_input_parsing')
            
            # Add detailed message for tracking
            parsed_fields = list(validated_data.keys())
            accounts_count = len(validated_data.get('Accounts', [])) if isinstance(validated_data.get('Accounts'), list) else 1
            transactions_count = len(validated_data.get('Transactions', [])) if isinstance(validated_data.get('Transactions'), list) else 1
            prev_cases_count = len(validated_data.get('Previous Cases', [])) if isinstance(validated_data.get('Previous Cases'), list) else 1
            
            state['messages'].append(
                HumanMessage(content=f"✅ Enhanced parsing complete: {len(parsed_fields)} fields, {accounts_count} accounts, {transactions_count} transactions, {prev_cases_count} previous cases")
            )
            
            print(f"✅ Enhanced parsing complete:")
            print(f"   📊 Fields parsed: {len(parsed_fields)}")
            print(f"   🏦 Accounts: {accounts_count}")  
            print(f"   💳 Transactions: {transactions_count}")
            print(f"   📋 Previous Cases: {prev_cases_count}")
            
        except Exception as e:
            error_msg = f"Error in enhanced parsing: {str(e)}"
            state['errors'].append(error_msg)
            state['messages'].append(HumanMessage(content=f"❌ {error_msg}"))
            print(f"❌ {error_msg}")
        
        return state
    
    def parse_case_file_comprehensive(self, file_path: str) -> Dict[str, str]:
        """Enhanced case file parsing with comprehensive field extraction"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"📄 Reading case file: {file_path}")
            print(f"📊 File size: {len(content)} characters")
            
            case_data = {}
            
            # Enhanced parsing using multiple methods
            case_data.update(self._parse_by_colon_delimiter(content))
            case_data.update(self._parse_by_pattern_matching(content))
            case_data.update(self._parse_by_line_analysis(content))
            
            print(f"✅ Raw parsing complete: {len(case_data)} fields extracted")
            
            # Validate required fields
            missing_fields = []
            for field in self.required_fields:
                if field not in case_data or not case_data[field] or case_data[field].strip() == '':
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"⚠️ Missing or empty fields: {missing_fields}")
                # Set defaults for missing fields
                for field in missing_fields:
                    case_data[field] = "N/A"
            
            return case_data
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Case file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error parsing case file: {str(e)}")
    
    def _parse_by_colon_delimiter(self, content: str) -> Dict[str, str]:
        """Parse using standard colon delimiter method"""
        case_data = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if ':' in line and len(line) > 3:
                try:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key and value and value.lower() not in ['', 'n/a', 'none', 'null']:
                        case_data[key] = value
                except ValueError:
                    continue
        
        return case_data
    
    def _parse_by_pattern_matching(self, content: str) -> Dict[str, str]:
        """Parse using regex pattern matching for better field extraction"""
        case_data = {}
        
        for field, patterns in self.field_patterns.items():
            for pattern in patterns:
                # Create regex pattern to find field and its value
                regex_pattern = rf'{re.escape(pattern)}\s*([^\n\r]+)'
                match = re.search(regex_pattern, content, re.IGNORECASE)
                
                if match:
                    value = match.group(1).strip()
                    if value and value.lower() not in ['', 'n/a', 'none', 'null']:
                        case_data[field] = value
                        break  # Use first successful match
        
        return case_data
    
    def _parse_by_line_analysis(self, content: str) -> Dict[str, str]:
        """Parse by analyzing each line for key-value patterns"""
        case_data = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to identify field based on common naming patterns
            line_lower = line.lower()
            
            # Case ID variations
            if any(term in line_lower for term in ['case id', 'caseid', 'case_id', 'id:']):
                value = self._extract_value_from_line(line)
                if value:
                    case_data['Case ID'] = value
            
            # Customer Name variations  
            elif any(term in line_lower for term in ['name:', 'customer name', 'customer:']):
                value = self._extract_value_from_line(line)
                if value:
                    case_data['Name'] = value
            
            # Customer ID variations
            elif any(term in line_lower for term in ['custid', 'customer id', 'customerid', 'cust_id']):
                value = self._extract_value_from_line(line)
                if value:
                    case_data['CustID'] = value
            
            # Accounts variations
            elif any(term in line_lower for term in ['account', 'acc']):
                value = self._extract_value_from_line(line)
                if value:
                    case_data['Accounts'] = value
            
            # Transactions variations
            elif any(term in line_lower for term in ['transaction', 'txn', 'tx']):
                value = self._extract_value_from_line(line)
                if value:
                    case_data['Transactions'] = value
            
            # Previous Cases variations
            elif any(term in line_lower for term in ['previous case', 'prev case', 'prior case']):
                value = self._extract_value_from_line(line)
                if value:
                    case_data['Previous Cases'] = value
        
        return case_data
    
    def _extract_value_from_line(self, line: str) -> str:
        """Extract value from a line using various methods"""
        # Try colon delimiter first
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                return parts[1].strip()
        
        # Try space delimiter for simple format
        parts = line.split()
        if len(parts) >= 2:
            # Return everything after the first word (assuming first word is the field name)
            return ' '.join(parts[1:])
        
        return ""
    
    def validate_and_enhance_data(self, case_data: Dict[str, str]) -> Dict[str, str]:
        """Validate and enhance parsed data with proper formatting"""
        enhanced_data = {}
        
        for key, value in case_data.items():
            # Clean and validate each field
            if key in ['Accounts', 'Transactions', 'Previous Cases']:
                # Handle multi-value fields (comma-separated)
                enhanced_data[key] = self._process_multi_value_field(value)
            else:
                # Handle single-value fields
                enhanced_data[key] = self._process_single_value_field(value)
        
        # Ensure all required fields are present
        for field in self.required_fields:
            if field not in enhanced_data:
                enhanced_data[field] = "N/A" if field not in ['Accounts', 'Transactions', 'Previous Cases'] else []
        
        # Add parsing metadata
        enhanced_data['_parsing_metadata'] = {
            'parsed_at': time.time(),
            'total_fields': len(enhanced_data),
            'parsing_method': 'comprehensive_enhanced'
        }
        
        print(f"✅ Data validation complete:")
        for field in self.required_fields:
            value = enhanced_data.get(field, 'Missing')
            if isinstance(value, list):
                print(f"   📋 {field}: {len(value)} items - {value}")
            else:
                print(f"   📋 {field}: {value}")
        
        return enhanced_data
    
    def _process_multi_value_field(self, value: str) -> List[str]:
        """Process fields that can contain multiple values (comma-separated)"""
        if not value or value.lower() in ['n/a', 'none', 'null', '']:
            return []
        
        # Split by common delimiters
        delimiters = [',', ';', '|', '\n']
        items = [value]
        
        for delimiter in delimiters:
            new_items = []
            for item in items:
                new_items.extend(item.split(delimiter))
            items = new_items
        
        # Clean and filter items
        cleaned_items = []
        for item in items:
            item = item.strip()
            if item and item.lower() not in ['', 'n/a', 'none', 'null']:
                cleaned_items.append(item)
        
        return cleaned_items if cleaned_items else []
    
    def _process_single_value_field(self, value: str) -> str:
        """Process single-value fields with cleaning and validation"""
        if not value:
            return "N/A"
        
        # Clean the value
        cleaned_value = value.strip()
        
        # Handle various null/empty representations
        if cleaned_value.lower() in ['', 'n/a', 'none', 'null', 'empty']:
            return "N/A"
        
        return cleaned_value
    
    def get_parsing_summary(self, case_data: Dict) -> Dict:
        """Get comprehensive parsing summary for debugging"""
        summary = {
            'total_fields_parsed': len(case_data),
            'required_fields_found': 0,
            'missing_fields': [],
            'multi_value_fields': {},
            'parsing_quality': 'good'
        }
        
        for field in self.required_fields:
            if field in case_data and case_data[field] != "N/A":
                summary['required_fields_found'] += 1
                
                # Count items in multi-value fields
                if isinstance(case_data[field], list):
                    summary['multi_value_fields'][field] = len(case_data[field])
            else:
                summary['missing_fields'].append(field)
        
        # Determine parsing quality
        completion_rate = summary['required_fields_found'] / len(self.required_fields)
        if completion_rate >= 0.9:
            summary['parsing_quality'] = 'excellent'
        elif completion_rate >= 0.7:
            summary['parsing_quality'] = 'good'
        elif completion_rate >= 0.5:
            summary['parsing_quality'] = 'fair'
        else:
            summary['parsing_quality'] = 'poor'
        
        return summary
