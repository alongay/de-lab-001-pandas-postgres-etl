#!/usr/bin/env python3
"""
scripts/monitoring/slack_mock.py

A lightweight enterprise-grade alerting simulator.
Prints high-visibility alerts to the terminal/container logs.
"""

import sys
import argparse
from datetime import datetime

def send_alert(pipeline: str, task: str, message: str, severity: str = "ERROR"):
    """Prints a formatted alert block to the console."""
    icon = "🚨" if severity == "ERROR" else "⚠️"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    alert_box = f"""
################################################################################
{icon} PLATFORM ALERT | {severity} | {now}
################################################################################
PIPELINE: {pipeline}
TASK:     {task}
MESSAGE:  {message}
################################################################################
"""
    print(alert_box)

def main():
    parser = argparse.ArgumentParser(description="Simulate a production alert.")
    parser.add_argument("--pipeline", required=True, help="Name of the pipeline")
    parser.add_argument("--task", required=True, help="Name of the failing task")
    parser.add_argument("--message", required=True, help="Alert message")
    parser.add_argument("--severity", default="ERROR", help="Alert severity (ERROR/WARNING)")
    
    args = parser.parse_args()
    send_alert(args.pipeline, args.task, args.message, args.severity)

if __name__ == "__main__":
    main()
