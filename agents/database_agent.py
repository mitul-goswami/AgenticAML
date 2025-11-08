import pandas as pd
from typing import Dict, List, Optional, Any
import numpy as np
from langchain_core.messages import HumanMessage
from agents.graph_state import CaseAnalysisState
from datetime import datetime
import statistics

class EnhancedDatabaseAgentNode:
    """Enhanced Database Agent Node with exact column fetching and comprehensive transaction comparison"""
    
    def __init__(self, config):
        self.config = config
        self.customer_df = None
        self.transaction_df = None
        
        # Define EXACT columns to fetch from customer database
        self.REQUIRED_CUSTOMER_COLUMNS = [
            'CustID',
            'Name', 
            'Account',
            'TransactionID',
            'TransactionAmount',
            'Employer',
            'Location',
            'Occupation',
            'Age'
        ]
        
        self.load_databases()
    
    def __call__(self, state: CaseAnalysisState) -> CaseAnalysisState:
        """Enhanced database query with exact column fetching and comprehensive analysis"""
        try:
            print("🔍 Step 2: Querying databases with exact column specifications...")
            
            case_data = state['case_data']
            if not case_data:
                raise Exception("No case data available for database query")
            
            # Query customer database with EXACT columns only
            customer_results = self._query_customer_data_exact(case_data)
            
            # Query transaction database for historical data
            transaction_results = self._query_transaction_data_comprehensive(case_data)
            
            # Perform comprehensive transaction comparison analysis
            comparison_analysis = self._perform_comprehensive_transaction_comparison(
                customer_results, transaction_results, case_data
            )
            
            # Perform advanced anomaly detection
            anomaly_analysis = self._perform_advanced_anomaly_detection(
                transaction_results, customer_results, case_data
            )
            
            # Calculate comprehensive transaction metrics
            transaction_metrics = self._calculate_comprehensive_metrics(
                transaction_results, comparison_analysis, anomaly_analysis
            )
            
            # Update state with comprehensive results
            state['db_results'] = customer_results
            state['transaction_data'] = transaction_results
            state['comparison_analysis'] = comparison_analysis
            state['anomaly_analysis'] = anomaly_analysis
            state['transaction_metrics'] = transaction_metrics
            state['current_step'] = 'comprehensive_analysis_completed'
            state['completed_steps'].append('comprehensive_database_analysis')
            
            # Enhanced summary message
            total_historical = transaction_results['summary_stats'].get('total_transactions', 0)
            comparisons_made = comparison_analysis.get('summary', {}).get('total_transactions_compared', 0)
            anomalies_found = len(anomaly_analysis.get('detected_anomalies', []))
            
            state['messages'].append(
                HumanMessage(content=f"✅ Comprehensive analysis: {total_historical} historical records, {comparisons_made} comparisons, {anomalies_found} anomalies")
            )
            
            print(f"✅ Comprehensive analysis complete: {comparisons_made} comparisons, {anomalies_found} anomalies")
            
        except Exception as e:
            error_msg = f"Error in comprehensive database analysis: {str(e)}"
            state['errors'].append(error_msg)
            state['messages'].append(HumanMessage(content=f"❌ {error_msg}"))
            print(f"❌ {error_msg}")
        
        return state
    
    def load_databases(self):
        """Load both customer and transaction databases with validation"""
        try:
            # Load customer database
            self.customer_df = pd.read_excel(self.config.CUSTOMER_DATABASE_FILE)
            print(f"📊 Customer database loaded: {len(self.customer_df)} records")
            
            # Validate customer database columns
            missing_columns = [col for col in self.REQUIRED_CUSTOMER_COLUMNS if col not in self.customer_df.columns]
            if missing_columns:
                print(f"⚠️ Missing columns in customer database: {missing_columns}")
            
            available_columns = [col for col in self.REQUIRED_CUSTOMER_COLUMNS if col in self.customer_df.columns]
            print(f"✅ Available customer columns: {available_columns}")
            
            # Load transaction database
            self.transaction_df = pd.read_excel(self.config.TRANSACTION_DATABASE_FILE)
            print(f"📊 Transaction database loaded: {len(self.transaction_df)} records")
            
        except Exception as e:
            raise Exception(f"Error loading databases: {str(e)}")
    
    def _query_customer_data_exact(self, case_data: Dict) -> Dict:
        """Query customer database with EXACT columns only - nothing more, nothing less"""
        cust_id = case_data.get('CustID')
        name = case_data.get('Name')
        
        results = {
            'customer_records': [],
            'summary_stats': {},
            'columns_fetched': []
        }
        
        try:
            # Filter available columns to only those that exist and are required
            available_required_columns = [col for col in self.REQUIRED_CUSTOMER_COLUMNS if col in self.customer_df.columns]
            results['columns_fetched'] = available_required_columns
            
            print(f"🎯 Fetching EXACT columns: {available_required_columns}")
            
            # Query by Customer ID first (primary method)
            customer_records = pd.DataFrame()
            
            if cust_id and cust_id != "N/A":
                print(f"🔍 Searching by CustID: {cust_id}")
                customer_records = self.customer_df[self.customer_df['CustID'] == cust_id].copy()
                
                if len(customer_records) > 0:
                    print(f"✅ Found {len(customer_records)} records by CustID")
                else:
                    print(f"⚠️ No records found by CustID: {cust_id}")
            
            # Fallback to name search if no CustID results
            if len(customer_records) == 0 and name and name != "N/A":
                print(f"🔍 Fallback search by Name: {name}")
                name_mask = self.customer_df['Name'].str.contains(name, case=False, na=False)
                customer_records = self.customer_df[name_mask].copy()
                
                if len(customer_records) > 0:
                    print(f"✅ Found {len(customer_records)} records by Name")
                else:
                    print(f"⚠️ No records found by Name: {name}")
            
            # Select ONLY the required columns (nothing more, nothing less)
            if len(customer_records) > 0:
                customer_records_exact = customer_records[available_required_columns].copy()
                results['customer_records'] = customer_records_exact.to_dict('records')
                
                print(f"🎯 EXACT COLUMNS SELECTED: {list(customer_records_exact.columns)}")
                print(f"📊 Final customer records: {len(results['customer_records'])}")
            else:
                print("❌ No customer records found matching criteria")
                
        except Exception as e:
            print(f"❌ Error in customer data query: {str(e)}")
            results['error'] = str(e)
        
        # Calculate summary statistics
        results['summary_stats'] = self._calculate_exact_customer_stats(results['customer_records'])
        
        return results
    
    def _query_transaction_data_comprehensive(self, case_data: Dict) -> Dict:
        """Query transaction database for comprehensive historical analysis"""
        cust_id = case_data.get('CustID')
        
        if not cust_id or cust_id == "N/A":
            return {
                'transactions': [], 
                'summary_stats': {}, 
                'accounts_found': [],
                'date_range': {}
            }
        
        print(f"🔍 Querying historical transactions for CustID: {cust_id}")
        
        try:
            # Query all transactions for this customer (no account filtering)
            customer_transactions = self.transaction_df[self.transaction_df['CUSTID'] == cust_id].copy()
            print(f"📊 Found {len(customer_transactions)} total historical transactions for {cust_id}")
            
            # Convert to records and calculate comprehensive stats
            transaction_records = customer_transactions.to_dict('records')
            transaction_stats = self._calculate_comprehensive_transaction_stats(transaction_records)
            
            # Get account coverage and date range
            accounts_found = customer_transactions['ACCOUNT'].unique().tolist() if not customer_transactions.empty else []
            
            date_range = {}
            if not customer_transactions.empty and 'DATE' in customer_transactions.columns:
                date_range = {
                    'start': str(customer_transactions['DATE'].min()),
                    'end': str(customer_transactions['DATE'].max())
                }
            
            print(f"✅ Historical analysis complete: {len(transaction_records)} transactions across {len(accounts_found)} accounts")
            
            return {
                'transactions': transaction_records,
                'summary_stats': transaction_stats,
                'accounts_found': accounts_found,
                'date_range': date_range
            }
            
        except Exception as e:
            print(f"❌ Error querying transaction data: {str(e)}")
            return {
                'transactions': [], 
                'summary_stats': {}, 
                'accounts_found': [],
                'date_range': {},
                'error': str(e)
            }
    
    def _perform_comprehensive_transaction_comparison(self, customer_results: Dict, transaction_results: Dict, case_data: Dict) -> Dict:
        """Perform comprehensive transaction comparison analysis - current vs historical"""
        
        print("🔬 Performing comprehensive transaction comparison analysis...")
        
        # Get current transaction amounts from customer database (EXACT columns only)
        customer_records = customer_results.get('customer_records', [])
        current_transactions = []
        
        for record in customer_records:
            if record.get('TransactionAmount'):
                try:
                    amount = float(record.get('TransactionAmount', 0))
                    current_transactions.append({
                        'amount': amount,
                        'account': record.get('Account'),
                        'transaction_id': record.get('TransactionID', f"TX_{len(current_transactions)+1}"),
                        'customer_id': record.get('CustID'),
                        'customer_name': record.get('Name'),
                        'location': record.get('Location'),
                        'employer': record.get('Employer'),
                        'source': 'customer_database'
                    })
                except (ValueError, TypeError):
                    print(f"⚠️ Invalid transaction amount: {record.get('TransactionAmount')}")
                    continue
        
        # Get historical transaction data
        historical_transactions = transaction_results.get('transactions', [])
        
        print(f"📊 Current transactions to analyze: {len(current_transactions)}")
        print(f"📊 Historical transactions available: {len(historical_transactions)}")
        
        if not current_transactions or not historical_transactions:
            return {
                'comparison_possible': False,
                'reason': f'Insufficient data - Current: {len(current_transactions)}, Historical: {len(historical_transactions)}',
                'current_transactions_found': len(current_transactions),
                'historical_transactions_found': len(historical_transactions)
            }
        
        # Perform detailed comparison for each current transaction
        comparison_results = []
        min_transactions = getattr(self.config, 'MIN_TRANSACTIONS_FOR_ANALYSIS', 3)
        
        for current_tx in current_transactions:
            current_amount = current_tx['amount']
            current_account = current_tx['account']
            
            print(f"🔍 Analyzing transaction: {current_tx['transaction_id']} - Amount: ${current_amount:,.2f}")
            
            # Find historical data for the same account
            account_history = [
                tx for tx in historical_transactions 
                if tx.get('ACCOUNT') == current_account
            ]
            
            if len(account_history) >= min_transactions:
                # Extract historical amounts for this account
                historical_amounts = []
                for tx in account_history:
                    try:
                        amount = float(tx.get('AMOUNT', 0))
                        historical_amounts.append(amount)
                    except (ValueError, TypeError):
                        continue
                
                if len(historical_amounts) >= min_transactions:
                    # Perform comprehensive statistical analysis
                    comparison_result = self._perform_statistical_comparison(
                        current_tx, historical_amounts, account_history
                    )
                    comparison_results.append(comparison_result)
        
        # Calculate overall comparison summary
        if comparison_results:
            summary = self._calculate_comparison_summary(comparison_results)
            
            print(f"✅ Comparison analysis complete:")
            print(f"   📊 Transactions compared: {len(comparison_results)}")
            print(f"   🚨 High risk: {summary.get('high_risk_transactions', 0)}")
            print(f"   ⚠️ Medium risk: {summary.get('medium_risk_transactions', 0)}")
            print(f"   📈 Statistical outliers: {summary.get('outlier_transactions', 0)}")
            
            return {
                'comparison_possible': True,
                'transaction_comparisons': comparison_results,
                'summary': summary
            }
        else:
            return {
                'comparison_possible': False,
                'reason': 'No valid statistical comparisons could be performed',
                'current_transactions_found': len(current_transactions),
                'historical_transactions_found': len(historical_transactions)
            }
    
    def _perform_statistical_comparison(self, current_tx: Dict, historical_amounts: List[float], account_history: List[Dict]) -> Dict:
        """Perform detailed statistical comparison for a single transaction"""
        
        current_amount = current_tx['amount']
        
        # Calculate comprehensive historical statistics
        hist_mean = statistics.mean(historical_amounts)
        hist_std = statistics.stdev(historical_amounts) if len(historical_amounts) > 1 else 0
        hist_median = statistics.median(historical_amounts)
        hist_min = min(historical_amounts)
        hist_max = max(historical_amounts)
        hist_q1 = np.percentile(historical_amounts, 25)
        hist_q3 = np.percentile(historical_amounts, 75)
        
        # Calculate comparison metrics
        deviation_from_mean = abs(current_amount - hist_mean)
        z_score = (current_amount - hist_mean) / hist_std if hist_std > 0 else 0
        percentage_deviation = (deviation_from_mean / hist_mean * 100) if hist_mean > 0 else 0
        
        # Percentile ranking
        percentile_rank = (sum(1 for x in historical_amounts if x <= current_amount) / len(historical_amounts)) * 100
        
        # Determine risk level and score with default thresholds
        high_risk_threshold = getattr(self.config, 'COMPARISON_Z_SCORE_HIGH_RISK', 3.0)
        medium_risk_threshold = getattr(self.config, 'COMPARISON_Z_SCORE_MEDIUM_RISK', 2.0)
        deviation_threshold = getattr(self.config, 'COMPARISON_DEVIATION_THRESHOLD', 50.0)
        
        risk_level = 'low'
        risk_score = 0
        risk_reasons = []
        
        # Enhanced risk assessment logic
        if abs(z_score) > high_risk_threshold:
            risk_level = 'high'
            risk_score = 40
            risk_reasons.append(f"Extreme deviation from normal behavior")
        elif abs(z_score) > medium_risk_threshold:
            risk_level = 'medium'
            risk_score = 25
            risk_reasons.append(f"Significant deviation from normal behavior")
        elif percentage_deviation > deviation_threshold:
            risk_level = 'medium'
            risk_score = 20
            risk_reasons.append(f"High percentage deviation: {percentage_deviation:.1f}%")
        
        # Additional risk factors
        if current_amount > (hist_mean + 2 * hist_std):
            risk_reasons.append("Amount significantly higher than historical pattern")
            risk_score += 15
        elif current_amount < (hist_mean - 2 * hist_std):
            risk_reasons.append("Amount significantly lower than historical pattern")
            risk_score += 10
        
        # Percentile-based risk assessment
        if percentile_rank > 95 or percentile_rank < 5:
            risk_reasons.append(f"Extreme percentile ranking: {percentile_rank:.1f}%")
            risk_score += 10
        
        return {
            'transaction_id': current_tx['transaction_id'],
            'account': current_tx['account'],
            'current_amount': current_amount,
            'customer_details': {
                'customer_id': current_tx.get('customer_id'),
                'customer_name': current_tx.get('customer_name'),
                'location': current_tx.get('location'),
                'employer': current_tx.get('employer')
            },
            'historical_stats': {
                'mean': hist_mean,
                'median': hist_median,
                'std_dev': hist_std,
                'min': hist_min,
                'max': hist_max,
                'q1': hist_q1,
                'q3': hist_q3,
                'count': len(historical_amounts)
            },
            'comparison_metrics': {
                'deviation_from_mean': deviation_from_mean,
                'z_score': z_score,
                'percentage_deviation': percentage_deviation,
                'percentile_rank': percentile_rank,
                'risk_level': risk_level,
                'risk_score': min(risk_score, 100),
                'risk_reasons': risk_reasons
            },
            'analysis_flags': {
                'is_outlier': abs(z_score) > 2,
                'extreme_outlier': abs(z_score) > 3,
                'significantly_higher': current_amount > (hist_mean + 2 * hist_std),
                'significantly_lower': current_amount < (hist_mean - 2 * hist_std),
                'within_normal_range': abs(z_score) <= 1,
                'above_95th_percentile': percentile_rank > 95,
                'below_5th_percentile': percentile_rank < 5
            }
        }
    
    def _calculate_comparison_summary(self, comparison_results: List[Dict]) -> Dict:
        """Calculate comprehensive summary of comparison results"""
        
        if not comparison_results:
            return {}
        
        total_risk_score = sum([result['comparison_metrics']['risk_score'] for result in comparison_results])
        z_scores = [abs(result['comparison_metrics']['z_score']) for result in comparison_results]
        avg_z_score = statistics.mean(z_scores)
        max_z_score = max(z_scores)
        
        return {
            'total_transactions_compared': len(comparison_results),
            'total_risk_score': min(total_risk_score, 100),
            'average_z_score': avg_z_score,
            'maximum_z_score': max_z_score,
            'high_risk_transactions': len([r for r in comparison_results if r['comparison_metrics']['risk_level'] == 'high']),
            'medium_risk_transactions': len([r for r in comparison_results if r['comparison_metrics']['risk_level'] == 'medium']),
            'low_risk_transactions': len([r for r in comparison_results if r['comparison_metrics']['risk_level'] == 'low']),
            'outlier_transactions': len([r for r in comparison_results if r['analysis_flags']['is_outlier']]),
            'extreme_outlier_transactions': len([r for r in comparison_results if r['analysis_flags']['extreme_outlier']]),
            'above_95th_percentile': len([r for r in comparison_results if r['analysis_flags']['above_95th_percentile']]),
            'below_5th_percentile': len([r for r in comparison_results if r['analysis_flags']['below_5th_percentile']])
        }
    
    def _perform_advanced_anomaly_detection(self, transaction_results: Dict, customer_results: Dict, case_data: Dict) -> Dict:
        """Perform advanced anomaly detection on transaction patterns"""
        
        print("🔬 Performing advanced anomaly detection...")
        
        transactions = transaction_results.get('transactions', [])
        
        if not transactions:
            return {
                'detected_anomalies': [],
                'risk_indicators': [],
                'total_anomalies': 0
            }
        
        anomalies = []
        risk_indicators = []
        min_transactions = getattr(self.config, 'MIN_TRANSACTIONS_FOR_ANALYSIS', 3)
        
        # Extract amounts and organize by patterns
        amounts = []
        monthly_data = {}
        account_data = {}
        frequency_data = {}
        
        for tx in transactions:
            try:
                amount = float(tx.get('AMOUNT', 0))
                amounts.append(amount)
                
                # Group by month for temporal analysis
                date_key = str(tx.get('DATE', ''))[:7]  # YYYY-MM format
                if date_key not in monthly_data:
                    monthly_data[date_key] = []
                monthly_data[date_key].append(amount)
                
                # Group by account for account-specific analysis
                account_key = tx.get('ACCOUNT', '')
                if account_key not in account_data:
                    account_data[account_key] = []
                account_data[account_key].append(amount)
                
                # Track frequency patterns
                if date_key not in frequency_data:
                    frequency_data[date_key] = 0
                frequency_data[date_key] += 1
                
            except (ValueError, TypeError):
                continue
        
        if len(amounts) >= min_transactions:
            # Advanced Statistical Anomaly Detection
            anomalies.extend(self._detect_statistical_anomalies(amounts, transactions))
            
            # Temporal Pattern Analysis
            risk_indicators.extend(self._detect_temporal_anomalies(monthly_data, frequency_data))
            
            # Account Behavior Analysis
            risk_indicators.extend(self._detect_account_anomalies(account_data))
            
            # Amount Pattern Analysis
            risk_indicators.extend(self._detect_amount_pattern_anomalies(amounts))
        
        total_anomalies = len(anomalies) + len(risk_indicators)
        
        print(f"✅ Anomaly detection complete:")
        print(f"   🚨 Anomalies detected: {len(anomalies)}")
        print(f"   ⚠️ Risk indicators: {len(risk_indicators)}")
        print(f"   📊 Total anomalies: {total_anomalies}")
        
        return {
            'detected_anomalies': anomalies,
            'risk_indicators': risk_indicators,
            'total_anomalies': total_anomalies
        }
    
    def _detect_statistical_anomalies(self, amounts: List[float], transactions: List[Dict]) -> List[Dict]:
        """Detect statistical anomalies using multiple methods"""
        anomalies = []
        
        if len(amounts) < 3:
            return anomalies
        
        mean_amount = statistics.mean(amounts)
        std_dev = statistics.stdev(amounts) if len(amounts) > 1 else 0
        threshold = getattr(self.config, 'ANOMALY_DETECTION_THRESHOLD', 3.0)
        
        if std_dev > 0:
            for i, tx in enumerate(transactions):
                try:
                    amount = float(tx.get('AMOUNT', 0))
                    z_score = abs((amount - mean_amount) / std_dev)
                    
                    if z_score > threshold:
                        anomalies.append({
                            'type': 'statistical_outlier',
                            'transaction': tx,
                            'z_score': z_score,
                            'severity': 'high' if z_score > threshold * 1.5 else 'medium',
                            'description': f"Transaction amount ${amount:,.2f} deviates significantly from average ${mean_amount:,.2f}",
                            'detection_method': 'z_score_analysis'
                        })
                except (ValueError, TypeError):
                    continue
        
        return anomalies
    
    def _detect_temporal_anomalies(self, monthly_data: Dict, frequency_data: Dict) -> List[Dict]:
        """Detect temporal pattern anomalies"""
        risk_indicators = []
        
        if len(monthly_data) < 2:
            return risk_indicators
        
        # Analyze monthly amount variations
        monthly_totals = [sum(amounts) for amounts in monthly_data.values()]
        if len(monthly_totals) > 1:
            monthly_mean = statistics.mean(monthly_totals)
            monthly_std = statistics.stdev(monthly_totals)
            
            for month, amounts in monthly_data.items():
                month_total = sum(amounts)
                if monthly_std > 0:
                    z_score = abs((month_total - monthly_mean) / monthly_std)
                    if z_score > 2:
                        risk_indicators.append({
                            'type': 'temporal_anomaly',
                            'month': month,
                            'amount': month_total,
                            'z_score': z_score,
                            'severity': 'high' if z_score > 3 else 'medium',
                            'description': f"Monthly total ${month_total:,.2f} in {month} deviates significantly from typical monthly pattern",
                            'detection_method': 'temporal_analysis'
                        })
        
        # Analyze frequency anomalies
        frequencies = list(frequency_data.values())
        if len(frequencies) > 1:
            freq_mean = statistics.mean(frequencies)
            freq_std = statistics.stdev(frequencies)
            
            for month, freq in frequency_data.items():
                if freq_std > 0:
                    z_score = abs((freq - freq_mean) / freq_std)
                    if z_score > 2:
                        risk_indicators.append({
                            'type': 'frequency_anomaly',
                            'month': month,
                            'frequency': freq,
                            'z_score': z_score,
                            'severity': 'medium',
                            'description': f"Transaction frequency of {freq} in {month} deviates from normal pattern",
                            'detection_method': 'frequency_analysis'
                        })
        
        return risk_indicators
    
    def _detect_account_anomalies(self, account_data: Dict) -> List[Dict]:
        """Detect account-specific behavioral anomalies"""
        risk_indicators = []
        
        for account, amounts in account_data.items():
            if len(amounts) >= 3:
                account_mean = statistics.mean(amounts)
                account_std = statistics.stdev(amounts)
                
                # High volatility detection
                if account_mean > 0:
                    volatility = account_std / account_mean
                    if volatility > 0.8:  # High volatility threshold
                        risk_indicators.append({
                            'type': 'account_volatility',
                            'account': account,
                            'volatility': volatility,
                            'mean_amount': account_mean,
                            'std_dev': account_std,
                            'severity': 'high' if volatility > 1.2 else 'medium',
                            'description': f"Account {account} shows high volatility with coefficient of variation {volatility:.2f}",
                            'detection_method': 'volatility_analysis'
                        })
        
        return risk_indicators
    
    def _detect_amount_pattern_anomalies(self, amounts: List[float]) -> List[Dict]:
        """Detect anomalies in amount patterns"""
        risk_indicators = []
        
        if len(amounts) < 5:
            return risk_indicators
        
        # Detect round number bias
        round_amounts = [amt for amt in amounts if amt % 100 == 0 or amt % 1000 == 0]
        round_ratio = len(round_amounts) / len(amounts)
        
        if round_ratio > 0.7:  # More than 70% round numbers
            risk_indicators.append({
                'type': 'round_number_bias',
                'round_ratio': round_ratio,
                'round_count': len(round_amounts),
                'total_count': len(amounts),
                'severity': 'medium',
                'description': f"{round_ratio:.1%} of transactions are round numbers, which may indicate structured transactions",
                'detection_method': 'pattern_analysis'
            })
        
        return risk_indicators
    
    def _calculate_comprehensive_metrics(self, transaction_results: Dict, comparison_analysis: Dict, anomaly_analysis: Dict) -> Dict:
        """Calculate comprehensive transaction metrics"""
        
        transactions = transaction_results.get('transactions', [])
        
        if not transactions:
            return {'analysis_completed': False}
        
        # Calculate risk scoring
        total_risk_score = 0
        
        # Comparison analysis contribution
        if comparison_analysis and comparison_analysis.get('comparison_possible'):
            comp_risk = comparison_analysis.get('summary', {}).get('total_risk_score', 0)
            total_risk_score += comp_risk * 0.6  # 60% weight
        
        # Anomaly analysis contribution
        if anomaly_analysis:
            anomalies = anomaly_analysis.get('detected_anomalies', [])
            risk_indicators = anomaly_analysis.get('risk_indicators', [])
            
            high_severity_count = len([a for a in anomalies + risk_indicators if a.get('severity') == 'high'])
            medium_severity_count = len([a for a in anomalies + risk_indicators if a.get('severity') == 'medium'])
            
            anomaly_risk = (high_severity_count * 15) + (medium_severity_count * 8)
            total_risk_score += anomaly_risk * 0.4  # 40% weight
        
        # Calculate transaction volatility
        amounts = []
        for tx in transactions:
            try:
                amount = float(tx.get('AMOUNT', 0))
                amounts.append(amount)
            except (ValueError, TypeError):
                continue
        
        transaction_volatility = 0
        if len(amounts) > 1 and statistics.mean(amounts) > 0:
            transaction_volatility = statistics.stdev(amounts) / statistics.mean(amounts)
        
        return {
            'analysis_completed': True,
            'total_anomalies': len(anomaly_analysis.get('detected_anomalies', [])) + len(anomaly_analysis.get('risk_indicators', [])),
            'risk_score': min(total_risk_score, 100),
            'transaction_volatility': transaction_volatility,
            'analysis_date': datetime.now().isoformat(),
            'methodology': 'comprehensive_statistical_analysis'
        }
    
    def _calculate_exact_customer_stats(self, customer_records: List[Dict]) -> Dict:
        """Calculate statistics from EXACT customer columns only"""
        if not customer_records:
            return {
                'total_records': 0,
                'unique_accounts': 0,
                'total_transaction_amount': 0.0,
                'avg_transaction_amount': 0.0,
                'unique_locations': 0,
                'unique_employers': 0,
                'unique_occupations': 0,
                'previous_case_count': 0,
                'previous_cases_list': [],
                'age_range': {'min': None, 'max': None, 'avg': None}
            }
        
        # Calculate transaction amounts
        transaction_amounts = []
        for record in customer_records:
            amount = record.get('TransactionAmount', 0)
            if amount is not None:
                try:
                    transaction_amounts.append(float(amount))
                except (ValueError, TypeError):
                    transaction_amounts.append(0.0)
        
        # Calculate unique values from exact columns
        unique_accounts = len(set([r.get('Account') for r in customer_records if r.get('Account')]))
        unique_locations = len(set([r.get('Location') for r in customer_records if r.get('Location')]))
        unique_employers = len(set([r.get('Employer') for r in customer_records if r.get('Employer')]))
        unique_occupations = len(set([r.get('Occupation') for r in customer_records if r.get('Occupation')]))
        
        # Calculate age statistics
        ages = []
        for record in customer_records:
            age = record.get('Age')
            if age is not None:
                try:
                    ages.append(int(age))
                except (ValueError, TypeError):
                    continue
        
        age_range = {'min': None, 'max': None, 'avg': None}
        if ages:
            age_range = {
                'min': min(ages),
                'max': max(ages),
                'avg': sum(ages) / len(ages)
            }
        
        return {
            'total_records': len(customer_records),
            'unique_accounts': unique_accounts,
            'total_transaction_amount': sum(transaction_amounts),
            'avg_transaction_amount': sum(transaction_amounts) / len(transaction_amounts) if transaction_amounts else 0.0,
            'unique_locations': unique_locations,
            'unique_employers': unique_employers,
            'unique_occupations': unique_occupations,
            'previous_case_count': 0,  # Will be populated from case data
            'previous_cases_list': [],  # Will be populated from case data
            'age_range': age_range
        }
    
    def _calculate_comprehensive_transaction_stats(self, transactions: List[Dict]) -> Dict:
        """Calculate comprehensive statistics for historical transactions"""
        if not transactions:
            return {
                'total_transactions': 0,
                'total_amount': 0.0,
                'avg_amount': 0.0,
                'median_amount': 0.0,
                'min_amount': 0.0,
                'max_amount': 0.0,
                'std_deviation': 0.0,
                'unique_accounts': 0,
                'months_covered': 0,
                'avg_monthly_amount': 0.0
            }
        
        # Extract amounts
        amounts = []
        for tx in transactions:
            amount = tx.get('AMOUNT', 0)
            try:
                amounts.append(float(amount))
            except (ValueError, TypeError):
                amounts.append(0.0)
        
        # Calculate comprehensive statistics
        total_amount = sum(amounts)
        avg_amount = total_amount / len(amounts) if amounts else 0.0
        median_amount = statistics.median(amounts) if amounts else 0.0
        min_amount = min(amounts) if amounts else 0.0
        max_amount = max(amounts) if amounts else 0.0
        std_deviation = statistics.stdev(amounts) if len(amounts) > 1 else 0.0
        
        # Account and temporal analysis
        unique_accounts = len(set([tx.get('ACCOUNT') for tx in transactions if tx.get('ACCOUNT')]))
        unique_dates = len(set([str(tx.get('DATE', ''))[:7] for tx in transactions if tx.get('DATE')]))  # Unique months
        avg_monthly_amount = total_amount / unique_dates if unique_dates > 0 else 0.0
        
        return {
            'total_transactions': len(transactions),
            'total_amount': total_amount,
            'avg_amount': avg_amount,
            'median_amount': median_amount,
            'min_amount': min_amount,
            'max_amount': max_amount,
            'std_deviation': std_deviation,
            'unique_accounts': unique_accounts,
            'months_covered': unique_dates,
            'avg_monthly_amount': avg_monthly_amount
        }
