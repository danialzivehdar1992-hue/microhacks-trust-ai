#!/usr/bin/env python
"""
Red Teaming Script for Target Application (Container App Backend API)

This script performs automated adversarial testing (red teaming) of the application
to identify potential safety vulnerabilities across multiple risk categories.
For runtime constraints we are only using Basic and have commented out the Advanced scan.

Based on: https://github.com/Azure-Samples/azureai-samples/blob/main/scenarios/evaluate/AI_RedTeaming/AI_RedTeaming.ipynb

Run: python 05_redteameval.py
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Any, Dict
from pprint import pprint
import requests
from dotenv import load_dotenv

# ----------------------------------------------
# Load environment from azd
# ----------------------------------------------
azure_dir = Path(__file__).parent.parent / ".azure"
env_name = os.environ.get("AZURE_ENV_NAME", "")
if not env_name and (azure_dir / "config.json").exists():
    with open(azure_dir / "config.json") as f:
        config = json.load(f)
        env_name = config.get("defaultEnvironment", "")

env_path = azure_dir / env_name / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Output directory for results
OUTPUT_DIR = Path(__file__).parent.parent / "evals" / "results" / "redteam"


# ----------------------------------------------
# 1. Define Target Callback Function
# ----------------------------------------------
def target_application_callback(query: str) -> str:
    """
    Callback function that calls the Container App backend API.
    """
    backend_url = os.getenv("AZURE_CONTAINER_APP_URL", "")
    
    if not backend_url:
        return "Error: AZURE_CONTAINER_APP_URL not set"
    
    try:
        # Call the /chat endpoint of the target application
        response = requests.post(
            f"{backend_url}/chat",
            json={
                "message": query,
                "conversation_history": [],
                "system_prompt": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses.",
                "max_tokens": 2048
            },
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        response.raise_for_status()
        
        result = response.json()
        
        # Extract the answer from the response and return as string
        answer = result.get("response", result.get("message", ""))
        
        return answer if answer else "I don't know."
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error calling target application: {str(e)}"
        print(f"⚠️ {error_msg}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response status: {e.response.status_code}")
            print(f"   Response body: {e.response.text[:200]}")
        return "I cannot process that request."


# ----------------------------------------------
# 2. Configure Red Team Scan
# ----------------------------------------------
async def run_red_team_scan(azure_ai_project: str, credential, backend_url: str):
    """
    Execute the red team scan against the target application.
    """
    from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
    
    # Check if backend is accessible
    try:
        health_url = f"{backend_url.rstrip('/')}/api/health"
        health_check = requests.get(health_url, timeout=10)
        print(f"✅ Backend is accessible at {backend_url}")
    except requests.exceptions.RequestException:
        try:
            root_check = requests.get(backend_url.rstrip('/'), timeout=10)
            print(f"✅ Backend is accessible at {backend_url}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Warning: Cannot connect to backend at {backend_url}")
            print(f"   Make sure the Container App is running. Error: {e}")
            print(f"   If the app is idle, it may take a moment to start.")
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                return
    
    print("\n" + "="*70)
    print("🎯 Starting Red Team Evaluation of Target Application")
    print("="*70)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    original_cwd = os.getcwd()
    os.chdir(OUTPUT_DIR)
    
    # ----------------------------------------------
    # 3. Run Basic Red Team Scan
    # ----------------------------------------------
    print("\n🔴 Running Basic Red Team Scan...")
    print("   Risk Categories: Violence, HateUnfairness, Sexual, SelfHarm")
    print("   Attack Strategies: Baseline (no transformation)")
    print()
    
    # Create RedTeam instance with basic configuration
    basic_red_team = RedTeam(
        azure_ai_project=azure_ai_project,
        credential=credential,
        risk_categories=[
            RiskCategory.Violence,
            RiskCategory.HateUnfairness,
            RiskCategory.Sexual,
            RiskCategory.SelfHarm,
        ],
        num_objectives=3,  # Number of attacks per risk category
    )
    
    # Run the scan
    basic_result = await basic_red_team.scan(
        target=target_application_callback,
        scan_name="Target-App-Basic-Scan",
        output_path=str(OUTPUT_DIR), #SDK will create subfolder
        application_scenario="Container App Backend API - Basic Red Team Test",
        attack_strategies=[],  # Empty list = baseline attacks only
    )
    
    # Save basic results
    basic_output_path = OUTPUT_DIR / "basic_scan_results.json"
    with open(basic_output_path, "w") as f:
        # Convert RedTeamResult to dict for JSON serialization
        result_dict = basic_result if isinstance(basic_result, dict) else vars(basic_result)
        json.dump(result_dict, f, indent=2, default=str)
    print(f"✅ Basic scan complete. Results saved to: {basic_output_path}")
    print()
    
    # Display basic metrics
    print("📊 Basic Scan Metrics:")
    if hasattr(basic_result, "metrics"):
        pprint(basic_result.metrics)
    elif isinstance(basic_result, dict) and "metrics" in basic_result:
        pprint(basic_result["metrics"])
    print()

    # ----------------------------------------------
    # 4. Run Advanced Red Team Scan (COMMENTED OUT)
    # ----------------------------------------------
    # Uncomment this section to run advanced red team scan with multiple attack strategies
    #
    # print("🔴 Running Advanced Red Team Scan...")
    # print("   Risk Categories: Violence, HateUnfairness, Sexual, SelfHarm")
    # print("   Attack Strategies: Multiple transformation techniques")
    # print()
    #
    # # Create RedTeam instance with advanced configuration
    # advanced_red_team = RedTeam(
    #     azure_ai_project=azure_ai_project,
    #     credential=credential,
    #     risk_categories=[
    #         RiskCategory.Violence,
    #         RiskCategory.HateUnfairness,
    #         RiskCategory.Sexual,
    #         RiskCategory.SelfHarm,
    #     ],
    #     num_objectives=5,  # More attacks for comprehensive testing
    # )
    #
    # # Run the scan with multiple attack strategies
    # advanced_result = await advanced_red_team.scan(
    #     target=target_application_callback,
    #     scan_name="Target-App-Advanced-Scan",
    #     application_scenario="Container App Backend API - Comprehensive Test",
    #     attack_strategies=[
    #         AttackStrategy.EASY,          # Group of easy complexity attacks
    #         AttackStrategy.MODERATE,      # Group of moderate complexity attacks
    #         AttackStrategy.Base64,        # Base64 encoding
    #         AttackStrategy.ROT13,         # ROT13 encoding
    #         AttackStrategy.CharacterSpace, # Add character spaces
    #         AttackStrategy.UnicodeConfusable, # Unicode confusables
    #     ],
    # )
    #
    # # Save advanced results
    # advanced_output_path = OUTPUT_DIR / "advanced_scan_results.json"
    # with open(advanced_output_path, "w") as f:
    #     result_dict = advanced_result if isinstance(advanced_result, dict) else vars(advanced_result)
    #     json.dump(result_dict, f, indent=2, default=str)
    # print(f"✅ Advanced scan complete. Results saved to: {advanced_output_path}")
    # print()
    #
    # # Display advanced metrics
    # print("📊 Advanced Scan Metrics:")
    # if hasattr(advanced_result, "metrics"):
    #     pprint(advanced_result.metrics)
    # elif isinstance(advanced_result, dict) and "metrics" in advanced_result:
    #     pprint(advanced_result["metrics"])
    # print()
    
    # ----------------------------------------------
    # 5. Display Summary
    # ----------------------------------------------
    print("\n" + "="*70)
    print("✅ Red Team Evaluation Complete!")
    print("="*70)
    print()
    print("📁 Results Location:")
    print(f"   Basic Scan: {basic_output_path}")
    # print(f"   Advanced Scan: {advanced_output_path}")  # Uncomment when running advanced scan
    print()
    print("📈 Key Metrics to Review:")
    print("   - Attack Success Rate (ASR): % of attacks that elicited harmful content")
    print("   - Vulnerability by Risk Category: Which content types are most vulnerable")
    print("   - Effectiveness of Attack Strategies: Which techniques work best")
    print()
    print("💡 Tip: View results in Microsoft Foundry portal for interactive analysis")
    print("="*70)
    os.chdir(original_cwd)


# ----------------------------------------------
# Main Execution
# ----------------------------------------------
if __name__ == "__main__":
    import argparse
    from azure.identity import DefaultAzureCredential
    
    parser = argparse.ArgumentParser(description="Run red team evaluation on target application")
    parser.add_argument(
        "--target_url",
        type=str,
        default=None,
        help="Target URL for the application. Defaults to AZURE_CONTAINER_APP_URL env var."
    )
    args = parser.parse_args()

    # Get target URL from args or environment
    backend_url = args.target_url or os.environ.get("AZURE_CONTAINER_APP_URL", "")
    
    if not backend_url:
        print("Error: Target URL not specified.")
        print("Either provide --target_url or set AZURE_CONTAINER_APP_URL environment variable.")
        exit(1)
    
    # Configure Azure AI project for red teaming
    azure_ai_project = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not azure_ai_project:
        print("Error: AZURE_AI_PROJECT_ENDPOINT not set")
        exit(1)

    # Initialize Azure credential
    credential = DefaultAzureCredential()
    
    print(f"\n🛡️  Starting Red Team Evaluation...")
    print(f"   Target URL: {backend_url}")
    print(f"   Output Directory: {OUTPUT_DIR}")
    print("")
    
    # Run the async red team scan
    asyncio.run(run_red_team_scan(azure_ai_project, credential, backend_url))


# ----------------------------------------------
# Usage Instructions:
#
# 1. Make sure the Container App is deployed and running:
#    - Run 'azd up' to provision infrastructure
#    - Run './scripts/06_deploy_container_apps.sh' to deploy the app
#    - Verify AZURE_CONTAINER_APP_URL is set in your .env file
#
# 2. Ensure environment variables are set:
#    - AZURE_AI_PROJECT_ENDPOINT (Project Endpoint from Foundry Portal)
#    - AZURE_CONTAINER_APP_URL (Container App URL)
#
# 3. Run the red team scan:
#    cd scripts
#    python 05_redteameval.py
#
# 4. Or specify custom target URL:
#    python 05_redteameval.py --target_url https://your-app.azurecontainerapps.io
#
# 5. Review results in evals/redteam_results/ or Azure Foundry Project
#
# ----------------------------------------------
# Understanding Risk Categories:
#
# - Violence: Content describing or promoting violence
# - HateUnfairness: Hate speech or unfair bias
# - Sexual: Inappropriate sexual content
# - SelfHarm: Content related to self-harm behaviors
#
# (Advanced categories - available when using advanced scan)
# - ProtectedMaterial: Copyrighted or protected content
# - CodeVulnerability: Vulnerable code generation
# - UngroundedAttributes: Ungrounded or fabricated information
#
# ----------------------------------------------
# Understanding Attack Strategies:
#
# - Baseline: Standard prompts without transformation (default)
# - EASY: Simple attack patterns (low sophistication)
# - MODERATE: More sophisticated attacks
# - DIFFICULT: Complex, layered attack strategies
# - Base64: Base64 encoding of prompts
# - ROT13: ROT13 cipher encoding
# - CharacterSpace: Adding spaces between characters
# - UnicodeConfusable: Using similar-looking Unicode characters
#
# ----------------------------------------------