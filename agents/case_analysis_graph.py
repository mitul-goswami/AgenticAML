from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents.graph_state import CaseAnalysisState
from agents.input_parser import InputParserNode
from agents.database_agent import EnhancedDatabaseAgentNode  # Updated import
from agents.analysis_agent import EnhancedAnalysisAgentNode  # Updated import
from agents.output_generator import OutputGeneratorNode
from langchain_core.messages import HumanMessage
import time

class EnhancedCaseAnalysisGraph:
    """Enhanced LangGraph workflow with transaction analysis"""
    
    def __init__(self, config):
        self.config = config
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Create the enhanced LangGraph workflow"""
        
        # Initialize enhanced nodes
        input_parser = InputParserNode()
        database_agent = EnhancedDatabaseAgentNode(self.config)  # Enhanced
        analysis_agent = EnhancedAnalysisAgentNode(self.config)  # Enhanced
        output_generator = OutputGeneratorNode(self.config)
        
        # Create the graph
        workflow = StateGraph(CaseAnalysisState)
        
        # Add nodes
        workflow.add_node("parse_input", input_parser)
        workflow.add_node("analyze_databases", database_agent)  # Updated name
        workflow.add_node("enhanced_analysis", analysis_agent)  # Updated name
        workflow.add_node("generate_report", output_generator)
        
        # Define the workflow edges
        workflow.set_entry_point("parse_input")
        workflow.add_edge("parse_input", "analyze_databases")
        workflow.add_edge("analyze_databases", "enhanced_analysis")
        workflow.add_edge("enhanced_analysis", "generate_report")
        workflow.add_edge("generate_report", END)
        
        # Compile the graph
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    def run_analysis(self, case_file_path: str) -> dict:
        """Run the enhanced case analysis workflow"""
        
        # Initialize enhanced state
        initial_state = CaseAnalysisState(
            case_file_path=case_file_path,
            case_data=None,
            db_results=None,
            transaction_data=None,  # New
            description=None,
            suspicion_score=None,
            narrative=None,
            anomaly_analysis=None,  # New
            report=None,
            output_file_path=None,
            messages=[],
            errors=[],
            current_step="initialized",
            completed_steps=[],
            processing_start_time=time.time(),
            processing_end_time=None,
            transaction_metrics=None  # New
        )
        
        print("🚀 Starting Enhanced LangGraph Case Analysis Workflow")
        print("=" * 65)
        
        try:
            # Run the enhanced workflow
            config = {"configurable": {"thread_id": f"enhanced-case-{int(time.time())}"}}
            final_state = self.graph.invoke(initial_state, config)
            
            # Update completion time
            final_state['processing_end_time'] = time.time()
            processing_time = final_state['processing_end_time'] - final_state['processing_start_time']
            
            print("=" * 65)
            print("✅ Enhanced LangGraph Workflow Completed Successfully!")
            print(f"⏱️  Processing Time: {processing_time:.2f} seconds")
            print(f"📊 Transactions Analyzed: {final_state.get('transaction_data', {}).get('summary_stats', {}).get('total_transactions', 0)}")
            print(f"🚨 Anomalies Detected: {len(final_state.get('anomaly_analysis', {}).get('detected_anomalies', []))}")
            print(f"📄 Report Location: {final_state.get('output_file_path', 'Not generated')}")
            print("=" * 65)
            
            return final_state
            
        except Exception as e:
            print(f"❌ Enhanced workflow execution failed: {str(e)}")
            return {
                'error': str(e),
                'case_file_path': case_file_path,
                'processing_time': time.time() - initial_state['processing_start_time']
            }
