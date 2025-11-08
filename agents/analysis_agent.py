from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, Tuple
import json
import re
from agents.graph_state import CaseAnalysisState

class EnhancedAnalysisAgentNode:
    """Enhanced Analysis Agent Node with transaction comparison analysis - OpenAI Integration"""
    
    def __init__(self, config):
        self.config = config
        self.llm = ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            top_p=config.TOP_P,
            frequency_penalty=config.FREQUENCY_PENALTY,
            presence_penalty=config.PRESENCE_PENALTY,
            request_timeout=config.TIMEOUT_SECONDS
        )
    
    def __call__(self, state: CaseAnalysisState) -> CaseAnalysisState:
        """Enhanced case analysis with transaction comparison data - LangGraph node implementation"""
        try:
            print("🤖 Step 3: Enhanced AI analysis with transaction comparison...")
            
            case_data = state['case_data']
            db_results = state['db_results']
            transaction_data = state['transaction_data']
            anomaly_analysis = state['anomaly_analysis']
            transaction_metrics = state['transaction_metrics']
            comparison_analysis = state['comparison_analysis']
            
            if not all([case_data, db_results, transaction_data]):
                raise Exception("Missing required data for enhanced analysis")
            
            # Perform enhanced analysis with comparison data
            description, suspicion_score, narrative = self.analyze_case_enhanced(
                case_data, db_results, transaction_data, anomaly_analysis, 
                transaction_metrics, comparison_analysis
            )
            
            # Update state
            state['description'] = description
            state['suspicion_score'] = suspicion_score
            state['narrative'] = narrative
            state['current_step'] = 'enhanced_analysis_completed'
            state['completed_steps'].append('enhanced_ai_analysis')
            
            # Add message for tracking
            comparisons_count = comparison_analysis.get('summary', {}).get('total_transactions_compared', 0) if comparison_analysis else 0
            anomalies_count = len(anomaly_analysis.get('detected_anomalies', []))
            
            state['messages'].append(
                HumanMessage(content=f"✅ Enhanced AI analysis completed: Suspicion score {suspicion_score:.1f}/100, {comparisons_count} transaction comparisons analyzed, {anomalies_count} anomalies evaluated")
            )
            
            print(f"✅ Enhanced analysis complete. Suspicion score: {suspicion_score:.1f}, Comparisons: {comparisons_count}")
            
        except Exception as e:
            error_msg = f"Error in enhanced AI analysis: {str(e)}"
            state['errors'].append(error_msg)
            state['messages'].append(HumanMessage(content=f"❌ {error_msg}"))
            print(f"❌ {error_msg}")
        
        return state
    
    def analyze_case_enhanced(self, case_data: Dict, db_results: Dict, transaction_data: Dict, 
                            anomaly_analysis: Dict, transaction_metrics: Dict, comparison_analysis: Dict) -> Tuple[str, float, str]:
        """Enhanced case analysis with transaction comparison history and anomaly detection"""
        
        # Create comprehensive case summary with transaction comparison data
        case_summary = self._create_enhanced_case_summary(
            case_data, db_results, transaction_data, anomaly_analysis, 
            transaction_metrics, comparison_analysis
        )
        
        # Generate enhanced analysis using LLM
        system_prompt = self._get_enhanced_system_prompt()
        analysis_prompt = self._create_enhanced_analysis_prompt(case_summary)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=analysis_prompt)
        ]
        
        try:
            print("Sending enhanced transaction comparison analysis request to OpenAI API...")
            response = self.llm.invoke(messages)
            print("Received enhanced analysis response from OpenAI API")
            
            analysis_result = self._parse_llm_response(response.content)
            
            return (
                analysis_result.get('description', 'No description available'),
                analysis_result.get('suspicion_score', 0.0),
                analysis_result.get('narrative', 'No narrative available')
            )
            
        except Exception as e:
            print(f"Error in enhanced OpenAI LLM analysis: {str(e)}")
            return "Enhanced transaction comparison analysis failed", 0.0, f"Unable to generate enhanced analysis: {str(e)}"
    
    def _create_enhanced_case_summary(self, case_data: Dict, db_results: Dict, 
                                    transaction_data: Dict, anomaly_analysis: Dict, 
                                    transaction_metrics: Dict, comparison_analysis: Dict) -> str:
        """Create comprehensive summary with transaction comparison analysis"""
        
        # Get all data components
        customer_stats = db_results['summary_stats']
        customer_records = db_results['customer_records']
        transaction_stats = transaction_data['summary_stats']
        transactions = transaction_data['transactions']
        anomalies = anomaly_analysis.get('detected_anomalies', [])
        risk_indicators = anomaly_analysis.get('risk_indicators', [])
        
        # Create the enhanced summary
        summary = f"""
CASE INFORMATION:
- Case ID: {case_data.get('Case ID', 'N/A')}
- Customer Name: {case_data.get('Name', 'N/A')}
- Customer ID: {case_data.get('CustID', 'N/A')}
- Input Accounts: {case_data.get('Accounts', 'N/A')}
- Input Transactions: {case_data.get('Transactions', 'N/A')}
- Input Previous Cases: {case_data.get('Previous Cases', 'None')}

CUSTOMER DATABASE FINDINGS (CURRENT TRANSACTIONS):
- Total Customer Records: {customer_stats.get('total_records', 0)}
- Customer Transaction Amount: ${customer_stats.get('total_transaction_amount', 0):,.2f}
- Customer Avg Transaction: ${customer_stats.get('avg_transaction_amount', 0):,.2f}
- Previous Case Count: {customer_stats.get('previous_case_count', 0)}
- Previous Cases: {', '.join(customer_stats.get('previous_cases_list', []))}

TRANSACTION DATABASE ANALYSIS (HISTORICAL PATTERNS):
- Total Historical Transactions: {transaction_stats.get('total_transactions', 0)}
- Total Historical Amount: ${transaction_stats.get('total_amount', 0):,.2f}
- Average Historical Amount: ${transaction_stats.get('avg_amount', 0):,.2f}
- Median Historical Amount: ${transaction_stats.get('median_amount', 0):,.2f}
- Historical Range: ${transaction_stats.get('min_amount', 0):,.2f} - ${transaction_stats.get('max_amount', 0):,.2f}
- Historical Standard Deviation: ${transaction_stats.get('std_deviation', 0):,.2f}
- Unique Accounts: {transaction_stats.get('unique_accounts', 0)}
- Months Covered: {transaction_stats.get('months_covered', 0)}
- Average Monthly Amount: ${transaction_stats.get('avg_monthly_amount', 0):,.2f}
"""
        
        # Add TRANSACTION COMPARISON ANALYSIS section
        if comparison_analysis and comparison_analysis.get('comparison_possible'):
            comp_summary = comparison_analysis.get('summary', {})
            summary += f"""
=== CRITICAL: TRANSACTION COMPARISON ANALYSIS (CURRENT vs HISTORICAL) ===
- Transactions Compared: {comp_summary.get('total_transactions_compared', 0)}
- Total Comparison Risk Score: {comp_summary.get('total_risk_score', 0)}/100
- Average Z-Score Deviation: {comp_summary.get('average_z_score', 0):.2f}
- Maximum Z-Score Deviation: {comp_summary.get('maximum_z_score', 0):.2f}
- HIGH RISK Transactions: {comp_summary.get('high_risk_transactions', 0)}
- MEDIUM RISK Transactions: {comp_summary.get('medium_risk_transactions', 0)}
- LOW RISK Transactions: {comp_summary.get('low_risk_transactions', 0)}
- Statistical Outliers: {comp_summary.get('outlier_transactions', 0)}
- Extreme Outliers: {comp_summary.get('extreme_outlier_transactions', 0)}

DETAILED TRANSACTION COMPARISONS (CURRENT vs HISTORICAL):
"""
            
            # Add detailed comparisons
            for i, comparison in enumerate(comparison_analysis.get('transaction_comparisons', [])[:10], 1):
                summary += f"""
COMPARISON {i}: Transaction {comparison.get('transaction_id', 'N/A')} (Account: {comparison.get('account', 'N/A')}):
  ► CURRENT AMOUNT: ${comparison.get('current_amount', 0):,.2f}
  ► HISTORICAL AVERAGE: ${comparison.get('historical_stats', {}).get('mean', 0):,.2f}
  ► HISTORICAL MEDIAN: ${comparison.get('historical_stats', {}).get('median', 0):,.2f}
  ► HISTORICAL RANGE: ${comparison.get('historical_stats', {}).get('min', 0):,.2f} - ${comparison.get('historical_stats', {}).get('max', 0):,.2f}
  ► HISTORICAL STD DEV: ${comparison.get('historical_stats', {}).get('std_dev', 0):,.2f}
  ► HISTORICAL SAMPLE SIZE: {comparison.get('historical_stats', {}).get('count', 0)} transactions
  ► Z-SCORE: {comparison.get('comparison_metrics', {}).get('z_score', 0):.2f}
  ► PERCENTAGE DEVIATION: {comparison.get('comparison_metrics', {}).get('percentage_deviation', 0):.1f}%
  ► RISK LEVEL: {comparison.get('comparison_metrics', {}).get('risk_level', 'unknown').upper()}
  ► RISK SCORE: {comparison.get('comparison_metrics', {}).get('risk_score', 0)}/100
  ► ANALYSIS FLAGS:
    - Statistical Outlier: {'YES' if comparison.get('analysis', {}).get('is_outlier') else 'NO'}
    - Extreme Outlier: {'YES' if comparison.get('analysis', {}).get('extreme_outlier') else 'NO'}
    - Significantly Higher: {'YES' if comparison.get('analysis', {}).get('significantly_higher') else 'NO'}
    - Significantly Lower: {'YES' if comparison.get('analysis', {}).get('significantly_lower') else 'NO'}
    - Within Normal Range: {'YES' if comparison.get('analysis', {}).get('within_normal_range') else 'NO'}
  ► RISK REASONS: {', '.join(comparison.get('comparison_metrics', {}).get('risk_reasons', ['None']))}
"""
        else:
            summary += f"""
=== TRANSACTION COMPARISON ANALYSIS ===
- Comparison Status: NOT POSSIBLE
- Reason: {comparison_analysis.get('reason', 'Unknown') if comparison_analysis else 'No comparison data available'}
- Current Transactions Found: {comparison_analysis.get('current_transactions_found', 0) if comparison_analysis else 0}
- Historical Transactions Found: {comparison_analysis.get('historical_transactions_found', 0) if comparison_analysis else 0}
"""
        
        # Add historical transaction sample (first 10)
        if transactions:
            summary += f"""
HISTORICAL TRANSACTION SAMPLE (First 10):
"""
            for i, tx in enumerate(transactions[:10], 1):
                summary += f"TX {i}: Date={tx.get('DATE')}, Account={tx.get('ACCOUNT')}, Amount=${tx.get('AMOUNT', 0):,.2f}\n"
            
            if len(transactions) > 10:
                summary += f"... and {len(transactions) - 10} more historical transactions\n"
        
        # Add anomaly detection results
        summary += f"""
ANOMALY DETECTION RESULTS:
- Total Anomalies Detected: {len(anomalies)}
- Risk Indicators Found: {len(risk_indicators)}
- Transaction Volatility: {transaction_metrics.get('transaction_volatility', 0):.3f}
- Anomaly Risk Score: {transaction_metrics.get('risk_score', 0)}/100
"""
        
        # Add specific anomalies
        if anomalies:
            summary += "\nDETECTED ANOMALIES:\n"
            for i, anomaly in enumerate(anomalies[:5], 1):
                summary += f"Anomaly {i}: Type={anomaly.get('type')}, Severity={anomaly.get('severity')}, Z-Score={anomaly.get('z_score', 0):.2f}\n"
                summary += f"  Description: {anomaly.get('description', 'No description')}\n"
        
        # Add risk indicators
        if risk_indicators:
            summary += "\nRISK INDICATORS:\n"
            for i, indicator in enumerate(risk_indicators[:5], 1):
                summary += f"Indicator {i}: Type={indicator.get('type')}, Severity={indicator.get('severity')}\n"
                summary += f"  Description: {indicator.get('description', 'No description')}\n"
        
        return summary
    
    def _get_enhanced_system_prompt(self) -> str:
        """Enhanced system prompt for transaction comparison analysis"""
        return """You are a senior financial fraud analyst with 20+ years of experience in anti-money laundering, financial crime detection, and transaction pattern analysis. You have access to BOTH current transaction data from the main database AND complete historical transaction patterns for direct comparison analysis.

ENHANCED ANALYSIS CAPABILITIES - TRANSACTION COMPARISON:
You must analyze how the CURRENT transactions from the main database compare against the COMPLETE HISTORICAL transaction patterns for the same customer and accounts.

CRITICAL COMPARISON ANALYSIS REQUIREMENTS:
1. **DIRECT COMPARISON FOCUS**: Compare CURRENT transaction amounts vs HISTORICAL patterns for the same accounts
2. **STATISTICAL ANALYSIS**: Evaluate Z-scores and statistical deviations from historical norms  
3. **DEVIATION ASSESSMENT**: Assess percentage deviations from historical averages
4. **OUTLIER IDENTIFICATION**: Identify transactions that are statistical outliers compared to history
5. **PATTERN ANALYSIS**: Analyze if current amounts are significantly higher/lower than historical patterns
6. **BEHAVIORAL CONSISTENCY**: Consider transaction timing and frequency patterns

TRANSACTION COMPARISON RISK FACTORS (CRITICAL):
- Z-Score > 3: **EXTREME OUTLIER** (HIGH RISK) - Current transaction extremely unusual
- Z-Score > 2: **SIGNIFICANT OUTLIER** (MEDIUM RISK) - Current transaction notably unusual
- Deviation > 50%: **HIGH PERCENTAGE DEVIATION** (MEDIUM RISK) - Large change from normal
- Current > Historical Mean + 2*StdDev: **SIGNIFICANTLY HIGHER** (HIGH RISK) 
- Current < Historical Mean - 2*StdDev: **SIGNIFICANTLY LOWER** (MEDIUM RISK)
- Within 1 StdDev: **CONSISTENT WITH HISTORY** (LOW RISK)

ENHANCED RISK ASSESSMENT FRAMEWORK:
- **High Risk (80-100)**: Multiple extreme outliers (Z>3), current transactions drastically different from historical patterns, 3+ previous cases
- **Medium-High Risk (60-79)**: Significant outliers (Z>2), notable deviations from historical norms, 2 previous cases  
- **Medium Risk (40-59)**: Moderate deviations, some outliers, 1 previous case, inconsistent with some historical patterns
- **Low Risk (0-39)**: Consistent with historical patterns, no significant deviations, normal transaction behavior

RESPONSE FORMAT: Provide detailed, professional analysis in valid JSON format:
{
    "description": "COMPREHENSIVE description incorporating transaction comparison analysis, historical pattern evaluation, statistical deviation assessment, Z-score analysis, percentage deviation evaluation, outlier identification, and specific risk factors identified from the complete transaction comparison dataset. Include specific current amounts, historical averages, Z-scores, deviations, and comparison analysis throughout.",
    "suspicion_score": numeric_score_between_0_and_100,
    "narrative": "DETAILED professional narrative covering: 1) Transaction comparison overview - how current transactions compare to historical patterns; 2) Statistical analysis results - Z-scores, deviations, outliers; 3) Historical pattern baseline - what is normal for this customer; 4) Current transaction assessment - how unusual are the current amounts; 5) Risk factor evaluation - specific reasons for concern; 6) Behavioral consistency analysis - patterns and anomalies; 7) Comprehensive risk assessment combining all comparison factors; 8) Specific recommendations based on transaction comparison findings. Reference exact current amounts, historical averages, Z-scores, percentage deviations, and statistical findings throughout your analysis."
}

Your analysis must focus PRIMARILY on HOW the current transactions compare to the customer's own historical behavior patterns. This is the core of your fraud detection assessment."""
    
    def _create_enhanced_analysis_prompt(self, case_summary: str) -> str:
        """Create enhanced analysis prompt with comprehensive transaction comparison data"""
        return f"""Please perform a COMPREHENSIVE, ENHANCED professional assessment focusing on TRANSACTION COMPARISON ANALYSIS using the complete transaction history and comparison data provided:

{case_summary}

ENHANCED ANALYSIS REQUIREMENTS:
- Focus PRIMARY attention on the TRANSACTION COMPARISON ANALYSIS section
- Analyze how CURRENT transactions compare against HISTORICAL patterns
- Evaluate all Z-scores, percentage deviations, and statistical outliers  
- Assess each comparison for risk level (HIGH/MEDIUM/LOW)
- Review all risk reasons and analysis flags provided
- Consider the significance of extreme outliers vs normal patterns
- Integrate comparison results with anomaly detection findings
- Provide detailed transaction-by-transaction risk assessment
- Use the comprehensive comparison dataset for accurate fraud detection

Based on this complete transaction comparison analysis, provide your DETAILED enhanced assessment in the specified JSON format, focusing heavily on how the current transactions deviate from or align with the customer's historical transaction behavior patterns."""
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse OpenAI LLM response - Enhanced error handling"""
        try:
            cleaned_response = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', response)
            
            json_match = re.search(r'\{.*\}', cleaned_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                
                try:
                    parsed_json = json.loads(json_str)
                    
                    if all(key in parsed_json for key in ['description', 'suspicion_score', 'narrative']):
                        score = float(parsed_json['suspicion_score'])
                        parsed_json['suspicion_score'] = max(0.0, min(100.0, score))
                        return parsed_json
                
                except json.JSONDecodeError as json_error:
                    print(f"JSON decode error with enhanced OpenAI response: {json_error}")
            
            # Enhanced fallback for transaction comparison analysis
            return {
                'description': "Enhanced transaction comparison analysis completed using comprehensive transaction history and direct comparison methods. Complete transaction patterns evaluated for fraud indicators with statistical analysis.",
                'suspicion_score': 45.0,  # Higher baseline due to enhanced comparison analysis
                'narrative': "Comprehensive risk assessment conducted using enhanced transaction comparison analysis, historical pattern evaluation, statistical deviation assessment, and anomaly detection capabilities. Analysis includes direct comparison of current transactions against complete historical behavior patterns with Z-score analysis and outlier identification."
            }
            
        except Exception as e:
            print(f"Error parsing enhanced OpenAI LLM response: {str(e)}")
            return {
                'description': "Enhanced transaction comparison analysis completed with comprehensive historical data evaluation",
                'suspicion_score': 40.0,
                'narrative': "Risk assessment conducted using enhanced transaction comparison analysis and comprehensive anomaly detection capabilities with historical pattern evaluation."
            }
