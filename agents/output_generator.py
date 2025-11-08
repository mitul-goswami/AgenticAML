from typing import Dict
import json
from datetime import datetime
import os
import time
from langchain_core.messages import HumanMessage
from agents.graph_state import CaseAnalysisState


class OutputGeneratorNode:
    """User-Friendly Output Generator Node with Enhanced Case Description and Narrative"""
    
    def __init__(self, config):
        self.config = config
    
    def __call__(self, state: CaseAnalysisState) -> CaseAnalysisState:
        """Generate user-friendly business report with detailed descriptions and narratives"""
        try:
            print("📝 Step 4: Generating detailed user-friendly business report...")
            
            case_data = state['case_data']
            description = state['description']
            suspicion_score = state['suspicion_score']
            narrative = state['narrative']
            db_results = state['db_results']
            
            # Get additional data for detailed analysis
            transaction_data = state.get('transaction_data', {})
            comparison_analysis = state.get('comparison_analysis', {})
            anomaly_analysis = state.get('anomaly_analysis', {})
            transaction_metrics = state.get('transaction_metrics', {})
            
            if not all([case_data, description is not None, suspicion_score is not None, narrative, db_results]):
                raise Exception("Missing required data for report generation")
            
            # Generate detailed business report
            report = self._generate_detailed_user_friendly_report(
                case_data, description, suspicion_score, narrative, db_results,
                transaction_data, comparison_analysis, anomaly_analysis, transaction_metrics
            )
            
            # Save report to file
            case_id = case_data.get('Case ID', 'UNKNOWN').replace(' ', '_')
            output_file = self._save_report_to_file(report, case_id)
            
            # Update state
            state['report'] = report
            state['output_file_path'] = output_file
            state['current_step'] = 'report_generated'
            state['completed_steps'].append('report_generation')
            
            state['messages'].append(
                HumanMessage(content=f"✅ Detailed user-friendly report generated: {output_file}")
            )
            
            print(f"✅ Detailed user-friendly report saved to: {output_file}")
            
        except Exception as e:
            error_msg = f"Error generating detailed report: {str(e)}"
            state['errors'].append(error_msg)
            state['messages'].append(HumanMessage(content=f"❌ {error_msg}"))
            print(f"❌ {error_msg}")
        
        return state
    
    def _generate_detailed_user_friendly_report(self, case_data, description, suspicion_score, narrative, db_results,
                                              transaction_data, comparison_analysis, anomaly_analysis, transaction_metrics):
        """Generate a detailed, business-friendly report with comprehensive case description and narrative"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        risk_level = self._get_risk_level(suspicion_score)
        risk_icon = self._get_risk_icon(suspicion_score)
        
        # Create detailed user-friendly report sections
        report_sections = []
        
        # Enhanced Header
        report_sections.append("=" * 70)
        report_sections.append("COMPREHENSIVE CASE ANALYSIS REPORT")
        report_sections.append("=" * 70)
        report_sections.append(f"Report Generated: {timestamp}")
        report_sections.append(f"Case ID: {case_data.get('Case ID', 'N/A')}")
        report_sections.append(f"Customer: {case_data.get('Name', 'N/A')}")
        report_sections.append(f"Analyst: AI-Powered Case Analysis System")
        report_sections.append("")
        
        # 1. DATA ANALYZED SECTION (Enhanced)
        report_sections.append("1. DATA ANALYZED")
        report_sections.append("=" * 35)
        
        stats = db_results['summary_stats']
        
        # Basic customer info
        report_sections.append(f"Customer Information:")
        report_sections.append(f"  • Full Name: {case_data.get('Name', 'N/A')}")
        report_sections.append(f"  • Customer ID: {case_data.get('CustID', 'N/A')}")
        
        # Detailed account information
        accounts = case_data.get('Accounts', [])
        if isinstance(accounts, list):
            report_sections.append(f"  • Number of Accounts Reviewed: {len(accounts)}")
            report_sections.append(f"  • Account Numbers: {', '.join(accounts)}")
        else:
            report_sections.append(f"  • Account Numbers: {accounts}")
        
        # Current transaction analysis
        report_sections.append(f"\nCurrent Transaction Analysis:")
        report_sections.append(f"  • Customer Records Found: {stats.get('total_records', 0)}")
        report_sections.append(f"  • Current Transaction Value: ${stats.get('total_transaction_amount', 0):,.2f}")
        report_sections.append(f"  • Average Current Transaction: ${stats.get('avg_transaction_amount', 0):,.2f}")
        report_sections.append(f"  • Unique Locations: {stats.get('unique_locations', 0)}")
        report_sections.append(f"  • Unique Employers: {stats.get('unique_employers', 0)}")
        
        # Historical data analysis
        if transaction_data:
            trans_stats = transaction_data.get('summary_stats', {})
            report_sections.append(f"\nHistorical Transaction Analysis:")
            report_sections.append(f"  • Historical Transactions Available: {trans_stats.get('total_transactions', 0)}")
            report_sections.append(f"  • Total Historical Value: ${trans_stats.get('total_amount', 0):,.2f}")
            report_sections.append(f"  • Average Historical Transaction: ${trans_stats.get('avg_amount', 0):,.2f}")
            report_sections.append(f"  • Historical Data Period: {trans_stats.get('months_covered', 0)} months")
            report_sections.append(f"  • Historical Account Coverage: {trans_stats.get('unique_accounts', 0)} accounts")
        
        # Risk factors
        if stats.get('previous_case_count', 0) > 0:
            report_sections.append(f"\nRisk Factors Identified:")
            report_sections.append(f"  • Previous Cases on Record: {stats.get('previous_case_count', 0)}")
            if stats.get('previous_cases_list'):
                report_sections.append(f"  • Previous Case IDs: {', '.join(stats.get('previous_cases_list', []))}")
        
        report_sections.append("")
        
        # 2. ENHANCED CASE DESCRIPTION SECTION
        report_sections.append("2. CASE DESCRIPTION")
        report_sections.append("=" * 35)
        
        # Create comprehensive case background
        detailed_background = self._create_comprehensive_case_background(
            case_data, db_results, transaction_data, comparison_analysis, anomaly_analysis
        )
        report_sections.append(detailed_background)
        report_sections.append("")
        
        # Add investigation context
        investigation_context = self._create_investigation_context(
            case_data, db_results, transaction_data, comparison_analysis
        )
        report_sections.append("Investigation Context:")
        report_sections.append(investigation_context)
        report_sections.append("")
        
        # Add AI analysis summary in business terms
        report_sections.append("Analysis Summary:")
        enhanced_description = self._enhance_description(description, comparison_analysis, anomaly_analysis)
        report_sections.append(enhanced_description)
        report_sections.append("")
        
        # 3. SUSPICION SCORE SECTION
        report_sections.append("3. SUSPICION SCORE")
        report_sections.append("=" * 30)
        report_sections.append(f"Overall Risk Assessment: {risk_icon} {suspicion_score:.0f} out of 100")
        report_sections.append(f"Risk Classification: {risk_level}")
        report_sections.append("")
        
        # Enhanced risk score breakdown
        report_sections.append("Risk Score Components:")
        risk_breakdown = self._create_risk_breakdown(
            suspicion_score, comparison_analysis, anomaly_analysis, db_results
        )
        for component in risk_breakdown:
            report_sections.append(f"  • {component}")
        report_sections.append("")
        
        report_sections.append("Risk Level Guide:")
        report_sections.append("• 0-20:   Low Risk - Continue routine monitoring")
        report_sections.append("• 21-40:  Low-Medium Risk - Regular review recommended")
        report_sections.append("• 41-60:  Medium Risk - Enhanced monitoring required")
        report_sections.append("• 61-80:  High Risk - Immediate attention and investigation needed")
        report_sections.append("• 81-100: Critical Risk - Urgent escalation and immediate action required")
        report_sections.append("")
        
        # Key findings section
        key_findings = self._extract_key_findings(comparison_analysis, anomaly_analysis, db_results)
        if key_findings:
            report_sections.append("Key Findings:")
            for finding in key_findings:
                report_sections.append(f"  • {finding}")
            report_sections.append("")
        
        # 4. ENHANCED DETAILED NARRATIVE SECTION
        report_sections.append("4. DETAILED NARRATIVE")
        report_sections.append("=" * 35)
        
        # Create comprehensive narrative
        comprehensive_narrative = self._create_comprehensive_narrative(
            narrative, case_data, db_results, transaction_data, comparison_analysis, anomaly_analysis, suspicion_score
        )
        report_sections.append(comprehensive_narrative)
        report_sections.append("")
        
        # Add behavioral analysis
        behavioral_analysis = self._create_behavioral_analysis(
            transaction_data, comparison_analysis, anomaly_analysis
        )
        if behavioral_analysis:
            report_sections.append("Behavioral Analysis:")
            report_sections.append(behavioral_analysis)
            report_sections.append("")
        
        # Enhanced recommendations
        report_sections.append("RECOMMENDATIONS AND NEXT STEPS:")
        recommendations = self._get_detailed_recommendations(
            suspicion_score, comparison_analysis, anomaly_analysis, db_results
        )
        for rec in recommendations:
            report_sections.append(f"• {rec}")
        report_sections.append("")
        
        # Conclusion
        conclusion = self._create_conclusion(suspicion_score, case_data, key_findings)
        report_sections.append("CONCLUSION:")
        report_sections.append(conclusion)
        report_sections.append("")
        
        # Enhanced footer
        report_sections.append("=" * 70)
        report_sections.append("END OF COMPREHENSIVE ANALYSIS REPORT")
        report_sections.append("=" * 70)
        report_sections.append("This comprehensive report was generated using advanced AI-powered analysis")
        report_sections.append("combining current transaction data with historical behavioral patterns.")
        report_sections.append("For questions or clarifications about this report, please contact your")
        report_sections.append("compliance team or case analysis department.")
        report_sections.append(f"Report ID: {case_data.get('Case ID', 'N/A')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return "\n".join(report_sections)
    
    def _create_comprehensive_case_background(self, case_data, db_results, transaction_data, comparison_analysis, anomaly_analysis):
        """Create a comprehensive, detailed case background"""
        name = case_data.get('Name', 'the customer')
        case_id = case_data.get('Case ID', 'this case')
        cust_id = case_data.get('CustID', 'N/A')
        
        stats = db_results['summary_stats']
        current_amount = stats.get('total_transaction_amount', 0)
        records_count = stats.get('total_records', 0)
        prev_cases = stats.get('previous_case_count', 0)
        
        background = f"This comprehensive analysis investigates the financial activities and transaction patterns of {name} "
        background += f"(Customer ID: {cust_id}) under case reference {case_id}. The investigation encompasses a thorough "
        background += f"review of both current and historical transaction data to identify potential risks, unusual patterns, "
        background += f"and behavioral inconsistencies.\n\n"
        
        if records_count > 0:
            background += f"Our analysis examined {records_count} current customer record(s) containing transaction activity "
            background += f"with a combined value of ${current_amount:,.2f}. These records include detailed information about "
            background += f"account usage, transaction locations, employment details, and associated financial activities.\n\n"
        
        if transaction_data:
            trans_stats = transaction_data.get('summary_stats', {})
            hist_count = trans_stats.get('total_transactions', 0)
            hist_months = trans_stats.get('months_covered', 0)
            hist_amount = trans_stats.get('total_amount', 0)
            
            if hist_count > 0:
                background += f"To establish a comprehensive behavioral baseline, we analyzed {hist_count} historical "
                background += f"transactions spanning {hist_months} months, representing ${hist_amount:,.2f} in total "
                background += f"historical activity. This extensive historical dataset allows us to identify the customer's "
                background += f"normal spending patterns, transaction frequency, typical amounts, and regular financial behaviors.\n\n"
        
        if prev_cases > 0:
            background += f"IMPORTANT NOTE: This customer has {prev_cases} previous case(s) on record, which significantly "
            background += f"impacts the risk assessment. Previous cases indicate potential recurring issues or patterns that "
            background += f"require enhanced scrutiny and monitoring.\n\n"
        
        # Add comparison methodology explanation
        if comparison_analysis and comparison_analysis.get('comparison_possible'):
            comp_summary = comparison_analysis.get('summary', {})
            compared_tx = comp_summary.get('total_transactions_compared', 0)
            
            background += f"Our investigation methodology included a detailed comparison of {compared_tx} current "
            background += f"transaction(s) against established historical patterns. This comparison analysis helps identify "
            background += f"transactions that deviate significantly from the customer's normal behavior, allowing us to "
            background += f"detect potential fraud, money laundering, or other suspicious activities."
        else:
            background += f"Historical comparison analysis could not be performed due to insufficient historical data. "
            background += f"This limitation means our assessment relies primarily on current transaction patterns and "
            background += f"available customer information, which may impact the comprehensiveness of our risk evaluation."
        
        return background
    
    def _create_investigation_context(self, case_data, db_results, transaction_data, comparison_analysis):
        """Create detailed investigation context"""
        context = "This investigation was initiated to evaluate potential financial crimes, suspicious activities, "
        context += "or compliance violations. The analysis methodology combines artificial intelligence with established "
        context += "financial crime detection techniques to provide a comprehensive risk assessment.\n\n"
        
        # Add scope details
        accounts = case_data.get('Accounts', [])
        if isinstance(accounts, list) and len(accounts) > 1:
            context += f"The investigation scope covers {len(accounts)} accounts, allowing for cross-account "
            context += f"pattern analysis and detection of potentially coordinated suspicious activities across "
            context += f"multiple financial products.\n\n"
        
        # Add data sources
        context += "Data Sources Utilized:\n"
        context += "• Current customer transaction records and account information\n"
        if transaction_data:
            context += "• Comprehensive historical transaction database for behavioral analysis\n"
        context += "• Previous case history and compliance records\n"
        context += "• AI-powered pattern recognition and anomaly detection systems\n"
        context += "• Cross-reference databases for enhanced due diligence"
        
        return context
    
    def _enhance_description(self, description, comparison_analysis, anomaly_analysis):
        """Enhance the AI description with more business context"""
        if not description:
            return "Detailed analysis could not be completed due to insufficient data."
        
        # Start with simplified description
        enhanced = self._simplify_description(description)
        
        # Add comparison insights
        if comparison_analysis and comparison_analysis.get('comparison_possible'):
            comp_summary = comparison_analysis.get('summary', {})
            high_risk_tx = comp_summary.get('high_risk_transactions', 0)
            outliers = comp_summary.get('outlier_transactions', 0)
            
            if high_risk_tx > 0 or outliers > 0:
                enhanced += f"\n\nTransaction Pattern Analysis: Our comparison of current transactions against "
                enhanced += f"historical behavior revealed significant concerns. "
                
                if high_risk_tx > 0:
                    enhanced += f"{high_risk_tx} transaction(s) show patterns significantly different from the "
                    enhanced += f"customer's established behavioral norms. "
                
                if outliers > 0:
                    enhanced += f"{outliers} transaction(s) fall outside the customer's typical spending range, "
                    enhanced += f"suggesting potential unusual or suspicious activity."
        
        # Add anomaly insights
        if anomaly_analysis:
            anomalies = anomaly_analysis.get('detected_anomalies', [])
            if len(anomalies) > 0:
                enhanced += f"\n\nBehavioral Anomaly Detection: Our analysis identified {len(anomalies)} unusual "
                enhanced += f"pattern(s) in the customer's transaction behavior that deviate from normal financial "
                enhanced += f"activity patterns. These anomalies require further investigation to determine if they "
                enhanced += f"represent legitimate changes in customer behavior or potential suspicious activity."
        
        return enhanced
    
    def _create_comprehensive_narrative(self, narrative, case_data, db_results, transaction_data, comparison_analysis, anomaly_analysis, suspicion_score):
        """Create a comprehensive, detailed narrative"""
        if not narrative:
            base_narrative = "A comprehensive analysis was conducted but detailed narrative generation was not possible."
        else:
            base_narrative = self._simplify_narrative(narrative)
        
        # Enhance narrative with detailed context
        enhanced_narrative = f"INVESTIGATION OVERVIEW:\n"
        enhanced_narrative += f"Our comprehensive investigation of {case_data.get('Name', 'the customer')} revealed important "
        enhanced_narrative += f"findings that contribute to the overall risk assessment. The analysis methodology combined "
        enhanced_narrative += f"multiple data sources and analytical techniques to provide a thorough evaluation.\n\n"
        
        enhanced_narrative += f"DETAILED ANALYSIS RESULTS:\n"
        enhanced_narrative += base_narrative + "\n\n"
        
        # Add transaction analysis details
        if transaction_data and comparison_analysis and comparison_analysis.get('comparison_possible'):
            trans_stats = transaction_data.get('summary_stats', {})
            comp_summary = comparison_analysis.get('summary', {})
            
            enhanced_narrative += f"TRANSACTION PATTERN ANALYSIS:\n"
            enhanced_narrative += f"We established a behavioral baseline using {trans_stats.get('total_transactions', 0)} "
            enhanced_narrative += f"historical transactions. When comparing current activity against this baseline, we found "
            enhanced_narrative += f"that {comp_summary.get('total_transactions_compared', 0)} current transaction(s) were analyzed "
            enhanced_narrative += f"for consistency with established patterns.\n\n"
            
            high_risk_tx = comp_summary.get('high_risk_transactions', 0)
            medium_risk_tx = comp_summary.get('medium_risk_transactions', 0)
            
            if high_risk_tx > 0:
                enhanced_narrative += f"CRITICAL FINDING: {high_risk_tx} transaction(s) demonstrated significant deviations "
                enhanced_narrative += f"from the customer's normal behavior patterns. These transactions warrant immediate "
                enhanced_narrative += f"investigation as they may indicate fraudulent activity, money laundering, or other "
                enhanced_narrative += f"financial crimes.\n\n"
            
            if medium_risk_tx > 0:
                enhanced_narrative += f"MODERATE CONCERN: {medium_risk_tx} transaction(s) showed patterns that differ from "
                enhanced_narrative += f"normal behavior but may have legitimate explanations. These require enhanced monitoring "
                enhanced_narrative += f"and possible customer contact for verification.\n\n"
        
        # Add risk assessment reasoning
        enhanced_narrative += f"RISK ASSESSMENT RATIONALE:\n"
        if suspicion_score >= 80:
            enhanced_narrative += f"The critical risk score of {suspicion_score:.0f}/100 indicates multiple severe risk factors "
            enhanced_narrative += f"that combine to create an urgent situation requiring immediate intervention. The combination "
            enhanced_narrative += f"of unusual transaction patterns, historical risk factors, and behavioral anomalies suggests "
            enhanced_narrative += f"a high probability of financial crimes or compliance violations.\n\n"
        elif suspicion_score >= 60:
            enhanced_narrative += f"The high risk score of {suspicion_score:.0f}/100 reflects significant concerns about the "
            enhanced_narrative += f"customer's current activity. While not at critical levels, the identified risk factors "
            enhanced_narrative += f"require prompt attention and enhanced monitoring to prevent potential losses or compliance "
            enhanced_narrative += f"violations.\n\n"
        elif suspicion_score >= 40:
            enhanced_narrative += f"The medium risk score of {suspicion_score:.0f}/100 indicates some areas of concern that "
            enhanced_narrative += f"warrant attention. While not immediately critical, these factors should be monitored closely "
            enhanced_narrative += f"to ensure they do not escalate into more serious issues.\n\n"
        else:
            enhanced_narrative += f"The low risk score of {suspicion_score:.0f}/100 suggests that current activity appears "
            enhanced_narrative += f"largely consistent with normal patterns. However, continued routine monitoring remains "
            enhanced_narrative += f"important to detect any changes in behavior or new risk factors.\n\n"
        
        # Add previous case context if applicable
        stats = db_results['summary_stats']
        if stats.get('previous_case_count', 0) > 0:
            enhanced_narrative += f"HISTORICAL CONTEXT:\n"
            enhanced_narrative += f"This customer's {stats.get('previous_case_count', 0)} previous case(s) significantly impact "
            enhanced_narrative += f"the current risk assessment. Customers with previous cases have statistically higher "
            enhanced_narrative += f"probabilities of future suspicious activities and require enhanced scrutiny. The combination "
            enhanced_narrative += f"of current findings with historical risk factors elevates the overall concern level."
        
        return enhanced_narrative
    
    # Include all other helper methods (simplified for brevity - same as previous version)
    def _create_risk_breakdown(self, suspicion_score, comparison_analysis, anomaly_analysis, db_results):
        """Create detailed risk score breakdown"""
        breakdown = []
        
        stats = db_results['summary_stats']
        prev_cases = stats.get('previous_case_count', 0)
        if prev_cases > 0:
            breakdown.append(f"Previous Case History: {prev_cases} previous case(s) contribute to elevated risk")
        
        if comparison_analysis and comparison_analysis.get('comparison_possible'):
            comp_summary = comparison_analysis.get('summary', {})
            comp_risk = comp_summary.get('total_risk_score', 0)
            if comp_risk > 0:
                breakdown.append(f"Transaction Pattern Deviation: Comparison analysis indicates {comp_risk}% risk level")
        
        if anomaly_analysis:
            anomalies = anomaly_analysis.get('detected_anomalies', [])
            if len(anomalies) > 0:
                breakdown.append(f"Behavioral Anomalies: {len(anomalies)} unusual pattern(s) detected")
        
        if suspicion_score >= 60:
            breakdown.append("Overall Assessment: Multiple risk factors combine to create significant concern")
        elif suspicion_score >= 40:
            breakdown.append("Overall Assessment: Moderate risk factors require enhanced monitoring")
        else:
            breakdown.append("Overall Assessment: Limited risk factors identified")
        
        return breakdown if breakdown else ["No specific risk factors identified"]
    
    def _extract_key_findings(self, comparison_analysis, anomaly_analysis, db_results):
        """Extract and format key findings"""
        findings = []
        
        stats = db_results['summary_stats']
        prev_cases = stats.get('previous_case_count', 0)
        if prev_cases > 0:
            findings.append(f"Customer has {prev_cases} previous case(s) on record, indicating recurring risk factors")
        
        if comparison_analysis and comparison_analysis.get('comparison_possible'):
            comp_summary = comparison_analysis.get('summary', {})
            high_risk_tx = comp_summary.get('high_risk_transactions', 0)
            extreme_outliers = comp_summary.get('extreme_outlier_transactions', 0)
            
            if high_risk_tx > 0:
                findings.append(f"Found {high_risk_tx} transaction(s) with significantly unusual amounts compared to customer history")
            
            if extreme_outliers > 0:
                findings.append(f"Identified {extreme_outliers} transaction(s) with extreme deviations from normal patterns")
        
        if anomaly_analysis:
            anomalies = anomaly_analysis.get('detected_anomalies', [])
            high_severity = len([a for a in anomalies if a.get('severity') == 'high'])
            
            if high_severity > 0:
                findings.append(f"Detected {high_severity} high-severity anomaly pattern(s) requiring investigation")
        
        return findings
    
    def _create_behavioral_analysis(self, transaction_data, comparison_analysis, anomaly_analysis):
        """Create behavioral analysis section"""
        if not transaction_data:
            return None
        
        trans_stats = transaction_data.get('summary_stats', {})
        analysis = f"Based on {trans_stats.get('total_transactions', 0)} historical transactions over "
        analysis += f"{trans_stats.get('months_covered', 0)} months, we established the customer's normal behavioral patterns. "
        analysis += f"The historical average transaction amount was ${trans_stats.get('avg_amount', 0):,.2f}, providing "
        analysis += f"a benchmark for evaluating current activity.\n\n"
        
        if comparison_analysis and comparison_analysis.get('comparison_possible'):
            comp_summary = comparison_analysis.get('summary', {})
            outliers = comp_summary.get('outlier_transactions', 0)
            
            if outliers > 0:
                analysis += f"Current behavior analysis reveals {outliers} transaction(s) that fall outside normal "
                analysis += f"behavioral ranges. This deviation from established patterns suggests potential changes "
                analysis += f"in the customer's financial circumstances or possible suspicious activities that require "
                analysis += f"further investigation."
        
        return analysis
    
    def _create_conclusion(self, suspicion_score, case_data, key_findings):
        """Create comprehensive conclusion"""
        conclusion = f"Based on our comprehensive analysis of {case_data.get('Name', 'the customer')}'s financial activity, "
        conclusion += f"we have assigned a risk score of {suspicion_score:.0f}/100. "
        
        if suspicion_score >= 80:
            conclusion += f"This critical risk level indicates immediate action is required. The combination of risk factors "
            conclusion += f"suggests a high probability of financial crimes or compliance violations that could result in "
            conclusion += f"significant financial losses or regulatory penalties if not addressed promptly."
        elif suspicion_score >= 60:
            conclusion += f"This high risk level requires enhanced monitoring and prompt investigation. While not at critical "
            conclusion += f"levels, the identified concerns could escalate without proper attention."
        elif suspicion_score >= 40:
            conclusion += f"This medium risk level suggests the need for increased attention and monitoring. Regular review "
            conclusion += f"and documentation of the customer's activities are recommended."
        else:
            conclusion += f"This low risk level indicates that current activities appear normal, but continued routine "
            conclusion += f"monitoring is important to detect any future changes."
        
        if key_findings:
            conclusion += f"\n\nThe most significant findings of this investigation include: "
            conclusion += "; ".join(key_findings[:3]) + ". "
            conclusion += f"These findings form the basis of our recommendations and should guide future monitoring activities."
        
        return conclusion
    
    def _get_detailed_recommendations(self, score, comparison_analysis, anomaly_analysis, db_results):
        """Get detailed, comprehensive recommendations"""
        recommendations = []
        
        if score >= 80:
            recommendations.extend([
                "IMMEDIATE ACTION REQUIRED: Escalate this case to senior management and compliance leadership within 24 hours",
                "URGENT: Contact fraud investigation team and consider freezing relevant accounts pending investigation",
                "REGULATORY COMPLIANCE: Prepare documentation for potential Suspicious Activity Report (SAR) filing"
            ])
        elif score >= 60:
            recommendations.extend([
                "HIGH PRIORITY: Schedule comprehensive case review with senior analyst within 48 hours",
                "ENHANCED MONITORING: Implement daily transaction monitoring with automated alerts",
                "CUSTOMER VERIFICATION: Consider contacting customer to verify recent transaction activity"
            ])
        elif score >= 40:
            recommendations.extend([
                "MODERATE PRIORITY: Schedule detailed case review within 7-14 days",
                "MONITORING ENHANCEMENT: Implement weekly monitoring protocols with pattern analysis"
            ])
        else:
            recommendations.extend([
                "STANDARD MONITORING: Continue routine monitoring protocols as per normal procedures"
            ])
        
        return recommendations
    
    # Include remaining helper methods from previous version
    def _simplify_description(self, description):
        """Convert technical AI description to simple business language"""
        if not description:
            return "No detailed analysis available."
        
        simple_desc = description.replace("statistical", "data")
        simple_desc = simple_desc.replace("anomaly", "unusual pattern")
        simple_desc = simple_desc.replace("z-score", "deviation from normal")
        simple_desc = simple_desc.replace("standard deviation", "typical range")
        simple_desc = simple_desc.replace("outlier", "unusual transaction")
        simple_desc = simple_desc.replace("variance", "variation")
        simple_desc = simple_desc.replace("algorithm", "analysis method")
        
        return simple_desc
    
    def _simplify_narrative(self, narrative):
        """Convert technical narrative to simple business language"""
        if not narrative:
            return "No detailed narrative available."
        
        simple_narr = narrative.replace("statistical analysis", "data review")
        simple_narr = simple_narr.replace("z-score", "comparison to normal behavior")
        simple_narr = simple_narr.replace("standard deviation", "typical range")
        simple_narr = simple_narr.replace("anomaly detection", "unusual pattern identification")
        simple_narr = simple_narr.replace("outlier", "unusual activity")
        simple_narr = simple_narr.replace("variance", "difference")
        simple_narr = simple_narr.replace("algorithm", "analysis")
        simple_narr = simple_narr.replace("threshold", "limit")
        
        sentences = simple_narr.split('. ')
        formatted_narrative = ""
        
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                formatted_narrative += sentence.strip()
                if not sentence.endswith('.'):
                    formatted_narrative += '.'
                if i < len(sentences) - 1:
                    formatted_narrative += ' '
                    
                if (i + 1) % 2 == 0 and i < len(sentences) - 1:
                    formatted_narrative += "\n\n"
        
        return formatted_narrative
    
    def _save_report_to_file(self, report, case_id):
        """Save report to a file with descriptive naming"""
        os.makedirs(self.config.OUTPUT_PATH, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Comprehensive_Case_Analysis_{case_id}_{timestamp}.txt"
        filepath = os.path.join(self.config.OUTPUT_PATH, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            return filepath
        except Exception as e:
            print(f"❌ Error saving report: {str(e)}")
            try:
                fallback_filename = f"Case_Report_{int(time.time())}.txt"
                with open(fallback_filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                return fallback_filename
            except Exception:
                return "report_save_failed.txt"
    
    def _get_risk_level(self, score):
        """Get risk level description"""
        if score >= 80:
            return "CRITICAL RISK"
        elif score >= 60:
            return "HIGH RISK"
        elif score >= 40:
            return "MEDIUM RISK"
        elif score >= 20:
            return "LOW-MEDIUM RISK"
        else:
            return "LOW RISK"
    
    def _get_risk_icon(self, score):
        """Get risk level icon"""
        if score >= 80:
            return "🚨"
        elif score >= 60:
            return "🔴"
        elif score >= 40:
            return "🟠"
        elif score >= 20:
            return "🟡"
        else:
            return "🟢"
