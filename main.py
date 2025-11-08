#!/usr/bin/env python3
"""
Enhanced LangGraph AI Case Analysis System with Transaction Comparison
Main execution file with comprehensive transaction history analysis
"""

import sys
import os
from pathlib import Path
import argparse
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.config import Config
from workflow import EnhancedLangGraphWorkflow


class EnhancedLangGraphCaseAnalysisSystem:
    """Enhanced main orchestrator using LangGraph workflow with transaction comparison"""
    
    def __init__(self):
        self.config = Config()
        self.workflow = EnhancedLangGraphWorkflow(self.config)
    
    def find_case_files(self, input_dir=None):
        """Find all case files in the input directory"""
        if input_dir is None:
            input_dir = self.config.INPUT_FILE_PATH
        
        if not os.path.exists(input_dir):
            print(f"❌ Input directory not found: {input_dir}")
            return []
        
        case_files = []
        for file in os.listdir(input_dir):
            if file.lower().endswith('.txt') and ('case' in file.lower() or 'input' in file.lower()):
                full_path = os.path.join(input_dir, file)
                case_files.append(full_path)
        
        return case_files
    
    def auto_detect_case_file(self):
        """Automatically detect the case file to process"""
        case_files = self.find_case_files()
        
        if not case_files:
            print("❌ No case files found in data/ directory")
            print("💡 Please add a case file (e.g., case_input.txt) to the data/ directory")
            return None
        elif len(case_files) == 1:
            print(f"✅ Auto-detected case file: {case_files[0]}")
            return case_files[0]
        else:
            print(f"📁 Found {len(case_files)} case files:")
            for i, file in enumerate(case_files, 1):
                print(f"  {i}. {os.path.basename(file)}")
            
            print(f"🎯 Auto-selecting: {os.path.basename(case_files[0])}")
            return case_files[0]
    
    def analyze_case(self, case_file_path: str) -> dict:
        """Run enhanced case analysis using LangGraph workflow with transaction comparison"""
        
        print(f"🔍 Starting Enhanced LangGraph Analysis for: {os.path.basename(case_file_path)}")
        print("🚀 Enhanced Features: Transaction Comparison + Anomaly Detection")
        
        # Run the enhanced workflow
        result = self.workflow.run_analysis(case_file_path)
        
        if result.get('success'):
            # Display enhanced summary
            state = result.get('state', {})
            case_data = state.get('case_data', {})
            suspicion_score = result.get('suspicion_score', 0)
            output_file = result.get('report_path')
            comparison_analysis = result.get('comparison_analysis', {})
            
            print("\n" + "="*70)
            print("ENHANCED LANGGRAPH ANALYSIS SUMMARY:")
            print("="*70)
            print(f"Case ID: {case_data.get('Case ID', 'N/A')}")
            print(f"Customer: {case_data.get('Name', 'N/A')} (ID: {case_data.get('CustID', 'N/A')})")
            print(f"Suspicion Score: {suspicion_score:.1f}/100")
            print(f"Risk Level: {self._get_risk_level(suspicion_score)}")
            print(f"Processing Time: {result.get('processing_time', 0):.2f} seconds")
            
            # Enhanced: Show transaction comparison results
            if comparison_analysis and comparison_analysis.get('comparison_possible'):
                comp_summary = comparison_analysis.get('summary', {})
                print(f"\n📊 TRANSACTION COMPARISON RESULTS:")
                print(f"   Transactions Compared: {comp_summary.get('total_transactions_compared', 0)}")
                print(f"   High Risk Transactions: {comp_summary.get('high_risk_transactions', 0)}")
                print(f"   Statistical Outliers: {comp_summary.get('outlier_transactions', 0)}")
                print(f"   Comparison Risk Score: {comp_summary.get('total_risk_score', 0)}/100")
                print(f"   Max Z-Score Deviation: {comp_summary.get('maximum_z_score', 0):.2f}")
            else:
                print(f"\n⚠️  Transaction Comparison: Not possible (insufficient data)")
            
            # Show anomaly detection results
            anomaly_analysis = state.get('anomaly_analysis', {})
            if anomaly_analysis:
                anomalies = anomaly_analysis.get('detected_anomalies', [])
                risk_indicators = anomaly_analysis.get('risk_indicators', [])
                print(f"\n🔍 ANOMALY DETECTION RESULTS:")
                print(f"   Anomalies Detected: {len(anomalies)}")
                print(f"   Risk Indicators: {len(risk_indicators)}")
            
            print(f"\n📂 Report Location: {output_file}")
            print(f"✅ Workflow Status: Completed Successfully")
            
            # Show any errors/warnings
            errors = result.get('errors', [])
            if errors:
                print(f"\n⚠️  Warnings/Errors:")
                for error in errors:
                    print(f"   • {error}")
            
            print("="*70)
            
            if output_file:
                print(f"\n📄 Open the enhanced report file to view detailed analysis:")
                print(f"   {output_file}")
        
        else:
            print(f"\n❌ Analysis Failed: {result.get('error', 'Unknown error')}")
            print(f"Processing Time: {result.get('processing_time', 0):.2f} seconds")
        
        return result
    
    def _get_risk_level(self, score):
        """Get risk level description with enhanced categories"""
        if score >= 80:
            return "🚨 HIGH RISK"
        elif score >= 60:
            return "🔴 MEDIUM-HIGH RISK"
        elif score >= 40:
            return "🟠 MEDIUM RISK"
        elif score >= 20:
            return "🟡 LOW-MEDIUM RISK"
        else:
            return "🟢 LOW RISK"
    
    def analyze_case_by_id(self, case_id: str) -> dict:
        """Analyze case by searching for case ID file"""
        case_file_path = f"{self.config.INPUT_FILE_PATH}case_input_{case_id}.txt"
        
        if not os.path.exists(case_file_path):
            # Try alternative naming patterns
            alt_patterns = [
                f"{self.config.INPUT_FILE_PATH}case_{case_id}.txt",
                f"{self.config.INPUT_FILE_PATH}{case_id}.txt",
                f"{self.config.INPUT_FILE_PATH}input_{case_id}.txt"
            ]
            
            for pattern in alt_patterns:
                if os.path.exists(pattern):
                    case_file_path = pattern
                    break
            else:
                raise FileNotFoundError(f"Case file not found for ID: {case_id}")
        
        return self.analyze_case(case_file_path)
    
    def create_sample_case_file(self):
        """Create a sample case input file for testing"""
        sample_content = """Case ID: CASE-2025-001
Name: John Smith
CustID: CUST9001
Accounts: ACC602,ACC372,ACC590
Transactions: TX001,TX002,TX003
Previous Cases: PREV-001,PREV-002
"""
        
        # Create data directory if it doesn't exist
        os.makedirs(self.config.INPUT_FILE_PATH, exist_ok=True)
        
        # Write sample file
        sample_file = os.path.join(self.config.INPUT_FILE_PATH, 'case_input.txt')
        with open(sample_file, 'w') as f:
            f.write(sample_content)
        
        print(f"✅ Sample case file created: {sample_file}")
        return sample_file


def print_system_header():
    """Print enhanced system header"""
    header = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ENHANCED LANGGRAPH AI CASE ANALYSIS SYSTEM               ║
║                         with Transaction Comparison Analysis                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  🤖 AI-Powered Fraud Detection     📊 Statistical Analysis                   ║
║  🔍 Transaction Comparison          📈 Pattern Recognition                   ║
║  🎯 Risk Assessment                 📝 Comprehensive Reports                 ║
║  🚨 Anomaly Detection              ⚡ LangGraph Workflow                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(header)


def main():
    """Main entry point - Enhanced LangGraph workflow mode"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Enhanced LangGraph AI Case Analysis System with Transaction Comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Auto-detect case files
  python main.py data/case_input.txt       # Analyze specific file
  python main.py --case-id CASE-001        # Analyze by case ID
  python main.py --create-sample           # Create sample case file
  python main.py --config-check            # Check configuration
        """
    )
    
    parser.add_argument(
        'case_file', 
        nargs='?',
        help='Path to case input file or case ID'
    )
    
    parser.add_argument(
        '--case-id',
        help='Analyze case by ID'
    )
    
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Create a sample case input file'
    )
    
    parser.add_argument(
        '--config-check',
        action='store_true',
        help='Check system configuration and exit'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Print system header
    print_system_header()
    
    try:
        # Initialize system
        print("🔧 Initializing Enhanced LangGraph System...")
        
        # Validate configuration
        config_errors = Config.validate_config()
        
        if config_errors:
            print("❌ Configuration errors found:")
            for error in config_errors:
                print(f"   • {error}")
            print("\n💡 Please check your .env file and database files.")
            return False
        
        print("✅ Configuration validation passed!")
        
        # Print configuration if requested
        if args.config_check or args.verbose:
            Config.print_config()
        
        if args.config_check:
            print("✅ Configuration check completed.")
            return True
        
        # Initialize system
        system = EnhancedLangGraphCaseAnalysisSystem()
        
        # Handle different modes
        if args.create_sample:
            system.create_sample_case_file()
            return True
        
        if args.case_id:
            # Analyze by case ID
            try:
                result = system.analyze_case_by_id(args.case_id)
                return result.get('success', False)
            except FileNotFoundError as e:
                print(f"❌ {e}")
                return False
        
        elif args.case_file:
            # Direct file path or case ID provided
            if args.case_file.endswith('.txt') or os.path.exists(args.case_file):
                # Direct file path
                if os.path.exists(args.case_file):
                    result = system.analyze_case(args.case_file)
                    return result.get('success', False)
                else:
                    print(f"❌ File not found: {args.case_file}")
                    return False
            else:
                # Treat as case ID
                try:
                    result = system.analyze_case_by_id(args.case_file)
                    return result.get('success', False)
                except FileNotFoundError as e:
                    print(f"❌ {e}")
                    return False
        
        else:
            # No arguments - auto-detect case file
            print("🔍 Auto-detecting case files...")
            case_file = system.auto_detect_case_file()
            
            if case_file:
                try:
                    result = system.analyze_case(case_file)
                    return result.get('success', False)
                except Exception as e:
                    print(f"❌ Analysis failed: {str(e)}")
                    return False
            else:
                # Create sample file if none found
                print("🆕 Creating sample case file for demonstration...")
                sample_file = system.create_sample_case_file()
                
                print("\n💡 Usage Examples:")
                print("  python main.py                           # Auto-detect case files")
                print("  python main.py data/case_input.txt       # Analyze specific file")
                print("  python main.py --case-id CASE-001        # Analyze by case ID")
                print("  python main.py --create-sample           # Create sample case file")
                print("  python main.py --config-check            # Check configuration")
                
                # Offer to analyze the sample file
                try:
                    user_input = input("\n🚀 Would you like to analyze the sample case? (y/n): ").lower()
                    if user_input == 'y':
                        result = system.analyze_case(sample_file)
                        return result.get('success', False)
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    return True
                
                return True
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
