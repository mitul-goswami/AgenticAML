"""
Enhanced LangGraph Agents Package
Multi-Agent Workflow System for Case Analysis with Transaction Comparison
"""

from .input_parser import InputParserNode
from .database_agent import EnhancedDatabaseAgentNode
from .analysis_agent import EnhancedAnalysisAgentNode
from .output_generator import OutputGeneratorNode
from .graph_state import CaseAnalysisState

__all__ = [
    'InputParserNode',
    'EnhancedDatabaseAgentNode', 
    'EnhancedAnalysisAgentNode',
    'OutputGeneratorNode',
    'CaseAnalysisState'
]

# Enhanced LangGraph Agent metadata
ENHANCED_LANGGRAPH_AGENT_INFO = {
    'InputParserNode': {
        'description': 'Parses case input files and extracts structured data',
        'input_format': 'CaseAnalysisState with case_file_path',
        'output_format': 'CaseAnalysisState with parsed case_data',
        'features': ['Key-value extraction', 'Data normalization', 'Flexible field handling']
    },
    'EnhancedDatabaseAgentNode': {
        'description': 'Enhanced database agent with dual database queries and transaction comparison',
        'input_format': 'CaseAnalysisState with case_data',
        'output_format': 'CaseAnalysisState with db_results, transaction_data, comparison_analysis, anomaly_analysis',
        'features': [
            'Customer database queries',
            'Transaction history database queries', 
            'Statistical transaction comparison',
            'Z-score analysis and outlier detection',
            'Anomaly detection algorithms',
            'Risk scoring and pattern analysis'
        ],
        'databases': ['Customer DB (current transactions)', 'Transaction DB (historical data)']
    },
    'EnhancedAnalysisAgentNode': {
        'description': 'Enhanced OpenAI-powered agent with transaction comparison analysis',
        'input_format': 'CaseAnalysisState with case_data, db_results, transaction_data, comparison_analysis',
        'output_format': 'CaseAnalysisState with enhanced analysis results',
        'features': [
            'OpenAI GPT integration',
            'Transaction comparison analysis',
            'Statistical deviation assessment', 
            'Historical behavior pattern analysis',
            'Enhanced risk scoring',
            'Multi-factor fraud detection'
        ],
        'ai_model': 'OpenAI GPT with specialized fraud detection prompts'
    },
    'OutputGeneratorNode': {
        'description': 'Enhanced report generator with transaction comparison and anomaly results',
        'input_format': 'CaseAnalysisState with all analysis results',
        'output_format': 'CaseAnalysisState with comprehensive report and output_file_path',
        'features': [
            'Comprehensive report generation',
            'Transaction comparison details',
            'Individual transaction analysis',
            'Anomaly detection results',
            'Enhanced risk assessment breakdown',
            'Visual indicators and recommendations'
        ]
    },
    'CaseAnalysisState': {
        'description': 'Enhanced centralized state management for workflow',
        'state_fields': [
            'case_file_path', 'case_data', 'db_results', 'transaction_data',
            'comparison_analysis', 'anomaly_analysis', 'transaction_metrics',
            'description', 'suspicion_score', 'narrative', 'report',
            'output_file_path', 'messages', 'errors', 'processing_times'
        ],
        'features': ['Type safety', 'State persistence', 'Error tracking', 'Message logging']
    }
}

def get_enhanced_workflow_info():
    """Get information about the Enhanced LangGraph workflow"""
    return {
        'architecture': 'Enhanced Multi-Agent Sequential Pipeline with Transaction Comparison',
        'workflow_steps': [
            '1. Input Parser: Extract case data from input files',
            '2. Enhanced Database Agent: Query dual databases + transaction comparison',
            '3. Enhanced Analysis Agent: AI analysis with comparison data',
            '4. Output Generator: Comprehensive reporting'
        ],
        'enhanced_features': {
            'transaction_comparison': 'Current vs historical transaction statistical analysis',
            'anomaly_detection': 'Pattern recognition and outlier identification',
            'dual_database_support': 'Customer DB + Transaction history DB integration',
            'statistical_analysis': 'Z-score analysis, standard deviation, percentile ranking',
            'risk_assessment': 'Multi-factor risk scoring with comparison metrics',
            'comprehensive_reporting': 'Detailed transaction-by-transaction analysis'
        },
        'state_management': 'Enhanced centralized state with transaction comparison data',
        'error_handling': 'Built-in error tracking and recovery with fallback mechanisms',
        'ai_integration': 'OpenAI GPT with specialized transaction comparison prompts',
        'databases': {
            'customer_database': 'Current customer records and transactions',
            'transaction_database': 'Historical transaction patterns and behavior'
        },
        'analysis_types': [
            'Statistical outlier detection',
            'Z-score deviation analysis', 
            'Historical pattern comparison',
            'Anomaly detection algorithms',
            'Risk indicator identification',
            'Behavioral consistency assessment'
        ],
        'scalability': 'Enhanced parallel execution with transaction comparison support'
    }

def get_system_capabilities():
    """Get comprehensive system capabilities"""
    return {
        'core_analysis': {
            'customer_profiling': 'Comprehensive customer data analysis',
            'transaction_analysis': 'Current and historical transaction processing',
            'risk_assessment': 'Multi-factor fraud risk scoring',
            'pattern_recognition': 'Behavioral pattern analysis and anomaly detection'
        },
        'enhanced_features': {
            'transaction_comparison': {
                'description': 'Compare current transactions against historical patterns',
                'methods': ['Z-score analysis', 'Standard deviation', 'Percentile analysis'],
                'outputs': ['Risk scores', 'Outlier identification', 'Deviation metrics']
            },
            'anomaly_detection': {
                'description': 'Identify unusual patterns in transaction behavior',
                'algorithms': ['Statistical outliers', 'Variance analysis', 'Pattern breaks'],
                'indicators': ['Amount anomalies', 'Frequency anomalies', 'Timing anomalies']
            },
            'dual_database_integration': {
                'customer_db': 'Current customer records and active transactions',
                'transaction_db': 'Historical transaction patterns and behavior data',
                'comparison_engine': 'Statistical comparison and analysis framework'
            }
        },
        'ai_powered_analysis': {
            'model': 'OpenAI GPT with specialized fraud detection',
            'capabilities': [
                'Natural language analysis of customer profiles',
                'Risk narrative generation',
                'Transaction comparison interpretation',
                'Anomaly explanation and context',
                'Comprehensive fraud assessment'
            ]
        },
        'reporting': {
            'formats': ['Comprehensive text reports', 'Statistical summaries'],
            'content': [
                'Executive summary with risk indicators',
                'Detailed transaction comparison analysis',
                'Individual transaction risk assessment', 
                'Anomaly detection results',
                'AI-generated narrative and recommendations'
            ]
        },
        'workflow_management': {
            'state_tracking': 'Complete workflow state management',
            'error_handling': 'Comprehensive error tracking and recovery',
            'progress_monitoring': 'Real-time workflow progress updates',
            'performance_metrics': 'Processing time and efficiency tracking'
        }
    }

# System version and metadata
__version__ = '2.0.0'
__description__ = 'Enhanced LangGraph AI Case Analysis with Transaction Comparison and Anomaly Detection'
__author__ = 'Enhanced LangGraph Development Team'
__enhanced_features__ = [
    'Transaction Comparison Analysis',
    'Dual Database Integration', 
    'Statistical Anomaly Detection',
    'Enhanced Risk Assessment',
    'Comprehensive Reporting'
]

# Compatibility info
REQUIRED_DEPENDENCIES = [
    'langchain>=0.2.16',
    'langchain-core>=0.2.41', 
    'langchain-openai>=0.1.25',
    'langgraph>=0.2.16',
    'pandas>=2.2.2',
    'numpy>=1.26.4',
    'openpyxl>=3.1.5',
    'python-dotenv>=1.0.1'
]

def check_system_compatibility():
    """Check if system has required dependencies"""
    try:
        import langchain
        import langgraph
        import pandas
        import numpy
        import openpyxl
        return {
            'compatible': True,
            'message': 'All required dependencies found',
            'version': __version__
        }
    except ImportError as e:
        return {
            'compatible': False,
            'message': f'Missing dependency: {e}',
            'required': REQUIRED_DEPENDENCIES
        }

def print_system_info():
    """Print comprehensive system information"""
    print("=" * 80)
    print("ENHANCED LANGGRAPH AI CASE ANALYSIS SYSTEM")
    print("=" * 80)
    print(f"Version: {__version__}")
    print(f"Description: {__description__}")
    print()
    
    workflow_info = get_enhanced_workflow_info()
    print("ENHANCED WORKFLOW ARCHITECTURE:")
    for step in workflow_info['workflow_steps']:
        print(f"  {step}")
    print()
    
    print("ENHANCED FEATURES:")
    for feature, description in workflow_info['enhanced_features'].items():
        print(f"  • {feature.replace('_', ' ').title()}: {description}")
    print()
    
    capabilities = get_system_capabilities()
    print("SYSTEM CAPABILITIES:")
    for category, details in capabilities.items():
        print(f"  {category.replace('_', ' ').title()}:")
        if isinstance(details, dict):
            for key, value in details.items():
                if isinstance(value, str):
                    print(f"    - {key}: {value}")
                elif isinstance(value, list):
                    print(f"    - {key}: {', '.join(value)}")
        print()
    
    compatibility = check_system_compatibility()
    print("SYSTEM COMPATIBILITY:")
    print(f"  Status: {'✅ Compatible' if compatibility['compatible'] else '❌ Not Compatible'}")
    print(f"  Message: {compatibility['message']}")
    print("=" * 80)

# Make system info easily accessible
if __name__ == "__main__":
    print_system_info()
