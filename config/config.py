import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')
    MODEL_NAME = os.getenv('LLM_MODEL', 'gpt-4o-mini')
    OPENAI_API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1/chat/completions')
    
    # LLM Parameters
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2500))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.1))
    TOP_P = float(os.getenv('TOP_P', 0.9))
    FREQUENCY_PENALTY = float(os.getenv('FREQUENCY_PENALTY', 0.0))
    PRESENCE_PENALTY = float(os.getenv('PRESENCE_PENALTY', 0.0))
    
    # File Paths (ENHANCED for dual database system)
    CUSTOMER_DATABASE_FILE = os.getenv('CUSTOMER_DATABASE_FILE', 'data/large_case_database.xlsx')
    TRANSACTION_DATABASE_FILE = os.getenv('TRANSACTION_DATABASE_FILE', 'data/transaction_data_sample.xlsx')
    INPUT_FILE_PATH = os.getenv('INPUT_FILE_PATH', 'data/')
    OUTPUT_PATH = os.getenv('OUTPUT_PATH', 'output/')
    LOG_PATH = os.getenv('LOG_PATH', 'logs/')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', 45))
    
    # Risk Analysis Thresholds
    HIGH_RISK_THRESHOLD = int(os.getenv('HIGH_RISK_THRESHOLD', 80))
    MEDIUM_RISK_THRESHOLD = int(os.getenv('MEDIUM_RISK_THRESHOLD', 60))
    LOW_RISK_THRESHOLD = int(os.getenv('LOW_RISK_THRESHOLD', 40))
    
    # Database Settings
    MAX_RECORDS_TO_PROCESS = int(os.getenv('MAX_RECORDS_TO_PROCESS', 5000))
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'True').lower() == 'true'
    CACHE_EXPIRY_HOURS = int(os.getenv('CACHE_EXPIRY_HOURS', 24))
    
    # Transaction Analysis Settings (ENHANCED)
    ENABLE_TRANSACTION_ANALYSIS = os.getenv('ENABLE_TRANSACTION_ANALYSIS', 'True').lower() == 'true'
    ANOMALY_DETECTION_THRESHOLD = float(os.getenv('ANOMALY_DETECTION_THRESHOLD', 2.5))
    MIN_TRANSACTIONS_FOR_ANALYSIS = int(os.getenv('MIN_TRANSACTIONS_FOR_ANALYSIS', 3))
    TRANSACTION_VARIANCE_THRESHOLD = float(os.getenv('TRANSACTION_VARIANCE_THRESHOLD', 0.8))
    
    # Comparison Analysis Settings (NEW)
    ENABLE_TRANSACTION_COMPARISON = os.getenv('ENABLE_TRANSACTION_COMPARISON', 'True').lower() == 'true'
    COMPARISON_Z_SCORE_HIGH_RISK = float(os.getenv('COMPARISON_Z_SCORE_HIGH_RISK', 3.0))
    COMPARISON_Z_SCORE_MEDIUM_RISK = float(os.getenv('COMPARISON_Z_SCORE_MEDIUM_RISK', 2.0))
    COMPARISON_DEVIATION_THRESHOLD = float(os.getenv('COMPARISON_DEVIATION_THRESHOLD', 50.0))
    
    # Security Settings
    ENABLE_INPUT_VALIDATION = os.getenv('ENABLE_INPUT_VALIDATION', 'True').lower() == 'true'
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
    ALLOWED_FILE_EXTENSIONS = os.getenv('ALLOWED_FILE_EXTENSIONS', 'txt,xlsx,csv').split(',')
    
    # LangGraph Configuration
    LANGGRAPH_CHECKPOINTER_TYPE = os.getenv('LANGGRAPH_CHECKPOINTER_TYPE', 'memory')
    LANGGRAPH_MAX_ITERATIONS = int(os.getenv('LANGGRAPH_MAX_ITERATIONS', 100))
    LANGGRAPH_RECURSION_LIMIT = int(os.getenv('LANGGRAPH_RECURSION_LIMIT', 25))
    ENABLE_WORKFLOW_VISUALIZATION = os.getenv('ENABLE_WORKFLOW_VISUALIZATION', 'True').lower() == 'true'
    WORKFLOW_THREAD_ID_PREFIX = os.getenv('WORKFLOW_THREAD_ID_PREFIX', 'enhanced-case-analysis')
    
    # State Management
    ENABLE_STATE_PERSISTENCE = os.getenv('ENABLE_STATE_PERSISTENCE', 'True').lower() == 'true'
    STATE_STORAGE_PATH = os.getenv('STATE_STORAGE_PATH', 'state/')
    MAX_STATE_HISTORY = int(os.getenv('MAX_STATE_HISTORY', 15))
    
    # Workflow Monitoring
    ENABLE_WORKFLOW_MONITORING = os.getenv('ENABLE_WORKFLOW_MONITORING', 'True').lower() == 'true'
    WORKFLOW_LOG_LEVEL = os.getenv('WORKFLOW_LOG_LEVEL', 'INFO')
    TRACK_EXECUTION_METRICS = os.getenv('TRACK_EXECUTION_METRICS', 'True').lower() == 'true'
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings - Enhanced for dual database"""
        errors = []
        
        # Validate OpenAI API Key
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == 'your_openai_api_key_here':
            errors.append("OPENAI_API_KEY is not properly set")
        
        # Validate database files
        if not os.path.exists(cls.CUSTOMER_DATABASE_FILE):
            errors.append(f"Customer database file not found: {cls.CUSTOMER_DATABASE_FILE}")
        
        if not os.path.exists(cls.TRANSACTION_DATABASE_FILE):
            errors.append(f"Transaction database file not found: {cls.TRANSACTION_DATABASE_FILE}")
        
        # Create directories if they don't exist
        directories_to_create = [
            cls.INPUT_FILE_PATH,
            cls.OUTPUT_PATH,
            cls.LOG_PATH
        ]
        
        if cls.ENABLE_STATE_PERSISTENCE:
            directories_to_create.append(cls.STATE_STORAGE_PATH)
        
        for directory in directories_to_create:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                    print(f"✅ Created directory: {directory}")
                except Exception as e:
                    errors.append(f"Could not create directory {directory}: {str(e)}")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """Print current configuration - Enhanced for dual database"""
        print("=" * 60)
        print("ENHANCED TRANSACTION COMPARISON SYSTEM CONFIGURATION")
        print("=" * 60)
        print("🤖 AI CONFIGURATION:")
        print(f"   Model: {cls.MODEL_NAME}")
        print(f"   Max Tokens: {cls.MAX_TOKENS}")
        print(f"   Temperature: {cls.TEMPERATURE}")
        print(f"   API Key Set: {'Yes' if cls.OPENAI_API_KEY != 'your_openai_api_key_here' else 'No'}")
        print()
        print("📁 DATABASE FILES:")
        print(f"   Customer Database: {cls.CUSTOMER_DATABASE_FILE}")
        print(f"   Transaction Database: {cls.TRANSACTION_DATABASE_FILE}")
        print(f"   Input Path: {cls.INPUT_FILE_PATH}")
        print(f"   Output Path: {cls.OUTPUT_PATH}")
        print()
        print("📊 TRANSACTION COMPARISON ANALYSIS:")
        print(f"   Transaction Analysis: {'Enabled' if cls.ENABLE_TRANSACTION_ANALYSIS else 'Disabled'}")
        print(f"   Comparison Analysis: {'Enabled' if cls.ENABLE_TRANSACTION_COMPARISON else 'Disabled'}")
        print(f"   High Risk Z-Score: {cls.COMPARISON_Z_SCORE_HIGH_RISK}")
        print(f"   Medium Risk Z-Score: {cls.COMPARISON_Z_SCORE_MEDIUM_RISK}")
        print(f"   Deviation Threshold: {cls.COMPARISON_DEVIATION_THRESHOLD}%")
        print()
        print("🔧 LANGGRAPH SETTINGS:")
        print(f"   Workflow Monitoring: {'Enabled' if cls.ENABLE_WORKFLOW_MONITORING else 'Disabled'}")
        print(f"   State Persistence: {'Enabled' if cls.ENABLE_STATE_PERSISTENCE else 'Disabled'}")
        print("=" * 60)
