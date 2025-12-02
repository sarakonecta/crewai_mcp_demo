#!/usr/bin/env python
import sys
import os
from crewai_mcp_demo.crew import CrewaiMcpDemo
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path, override=True)

def run():
    """
    Run the crew for technology stack validation.
    """
    print("\n" + "="*60)
    print("🚀 TECH STACK VALIDATOR")
    print("="*60 + "\n")
    
    # Get technology to evaluate
    if len(sys.argv) > 1:
        technology = " ".join(sys.argv[1:])
    else:
        technology = input("Enter the technology to evaluate: ").strip()
    
    if not technology:
        print("❌ Error: No technology specified.")
        return
    
    print(f"🔍 Evaluating: {technology}\n")
    
    inputs = {'technology': technology}
    
    try:
        crew_instance = CrewaiMcpDemo()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        print("\n" + "="*60)
        print("✅ EVALUATION COMPLETED")
        print("="*60)
        print(f"\n{result}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        raise

if __name__ == "__main__":
    run()