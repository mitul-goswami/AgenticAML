from typing import TypedDict, List, Dict, Optional, Any
from langchain_core.messages import BaseMessage

class CaseAnalysisState(TypedDict):
    """Enhanced state definition for transaction comparison analysis workflow"""
    
    # Input data
    case_file_path: str
    case_data: Optional[Dict[str, Any]]
    
    # Database results (ENHANCED)
    db_results: Optional[Dict[str, Any]]
    transaction_data: Optional[Dict[str, Any]]
    
    # Analysis results (ENHANCED)
    description: Optional[str]
    suspicion_score: Optional[float]
    narrative: Optional[str]
    anomaly_analysis: Optional[Dict[str, Any]]
    comparison_analysis: Optional[Dict[str, Any]]  # NEW: Transaction comparison results
    
    # Output
    report: Optional[str]
    output_file_path: Optional[str]
    
    # Messages for LangGraph
    messages: List[BaseMessage]
    
    # Error handling
    errors: List[str]
    
    # Processing status
    current_step: str
    completed_steps: List[str]
    
    # Metadata
    processing_start_time: Optional[float]
    processing_end_time: Optional[float]
    
    # Transaction analysis metrics (ENHANCED)
    transaction_metrics: Optional[Dict[str, Any]]
