#!/usr/bin/env python
import sys
import os
from crewai_mcp_demo.crew import CrewaiMcpDemo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run():
    """
    Run the crew for technology stack validation.
    """
    print("\n" + "="*60)
    print("🚀 TECH STACK VALIDATOR - CrewAI MCP Demo")
    print("="*60 + "\n")
    
    # Get technology to evaluate
    if len(sys.argv) > 1:
        technology = " ".join(sys.argv[1:])
    else:
        technology = input("Enter the technology to evaluate (e.g., 'Supabase', 'FastAPI'): ").strip()
    
    if not technology:
        print("❌ Error: No technology specified.")
        return
    
    print(f"\n🔍 Evaluating: {technology}")
    print("-" * 60 + "\n")
    
    inputs = {
        'technology': technology
    }
    
    try:
        # Initialize and run the crew
        crew_instance = CrewaiMcpDemo()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        print("\n" + "="*60)
        print("✅ EVALUATION COMPLETED")
        print("="*60)
        print(f"\n{result}\n")
        
        # ✅ OPCIONAL: Guardar el resultado localmente si estás en desarrollo
        if os.getenv("SAVE_LOCAL_REPORT", "false").lower() == "true":
            reports_dir = os.getenv("REPORTS_DIR", "./reports")
            os.makedirs(reports_dir, exist_ok=True)
            report_path = os.path.join(reports_dir, f"tech_recommendation_{technology.replace(' ', '_')}.md")
            
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(str(result))
            
            print(f"💾 Report saved locally: {report_path}\n")
        
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}\n")
        raise

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "technology": "FastAPI"
    }
    try:
        CrewaiMcpDemo().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiMcpDemo().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "technology": "FastAPI"
    }
    try:
        crew_instance = CrewaiMcpDemo()
        eval_llm = os.getenv("MODEL", "openai/gemini-2.5-flash")
        crew_instance.crew().test(n_iterations=int(sys.argv[1]), eval_llm=eval_llm, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()