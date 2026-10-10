"""Start the coursework web application from its repository directory."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="壳壳：旅行规划课程应用")
    parser.add_argument("--test", action="store_true", help="Send a live greeting to the configured API")
    args = parser.parse_args()
    os.chdir(Path(__file__).resolve().parent)
    if args.test:
        from src.agent.orchestrator import TravelAgent
        agent = TravelAgent.create_default()
        print(agent.process("你好")["response"][:200])
    else:
        return subprocess.call([sys.executable, "-m", "streamlit", "run", "src/ui/app.py"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
