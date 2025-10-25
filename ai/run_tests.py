#!/usr/bin/env python3
"""
Test runner script with helpful presets.

Usage:
    python run_tests.py               # Run all unit tests
    python run_tests.py --all         # Run all tests (unit + integration)
    python run_tests.py --integration # Run only integration tests
    python run_tests.py --health      # Run Ollama health check
    python run_tests.py --coverage    # Run with coverage report
"""
import sys
import os
import argparse
import subprocess
from pathlib import Path


def run_command(cmd: list[str]) -> int:
    """Run a command and return its exit code."""
    print(f"\n🚀 Running: {' '.join(cmd)}\n")
    
    # Set PYTHONPATH to include parent directory
    env = os.environ.copy()
    parent_dir = Path(__file__).parent.parent.absolute()
    env['PYTHONPATH'] = str(parent_dir)
    
    result = subprocess.run(cmd, env=env)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run AI service tests")
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Run all tests (unit + integration)"
    )
    parser.add_argument(
        "--unit", 
        action="store_true", 
        help="Run only unit tests (default)"
    )
    parser.add_argument(
        "--integration", 
        action="store_true", 
        help="Run only integration tests (requires Ollama)"
    )
    parser.add_argument(
        "--health", 
        action="store_true", 
        help="Run Ollama health check"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true", 
        help="Run tests with coverage report"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Base command
    cmd = ["pytest"]
    
    # Determine which tests to run
    if args.health:
        print("\n" + "="*70)
        print("Running Ollama Health Check")
        print("="*70)
        cmd.extend(["tests/test_ollama_health.py", "-v", "-s"])
    elif args.all:
        print("\n" + "="*70)
        print("Running All Tests (Unit + Integration)")
        print("="*70)
        print("⚠️  Note: Integration tests require Ollama to be running")
        print("="*70)
        cmd.extend(["tests/", "-v"])
    elif args.integration:
        print("\n" + "="*70)
        print("Running Integration Tests Only")
        print("="*70)
        print("⚠️  Note: These tests require Ollama to be running")
        print("="*70)
        cmd.extend(["tests/", "-v", "-m", "integration"])
    else:
        # Default: run unit tests
        print("\n" + "="*70)
        print("Running Unit Tests Only (Fast)")
        print("="*70)
        cmd.extend(["tests/", "-v", "-m", "unit"])
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=ai", "--cov-report=term-missing", "--cov-report=html"])
        print("📊 Coverage report will be generated in htmlcov/")
    
    # Add verbose if requested
    if args.verbose:
        cmd.append("-vv")
    
    # Add show output for integration tests
    if args.integration or args.all or args.health:
        cmd.append("-s")
    
    # Run the tests
    exit_code = run_command(cmd)
    
    # Print summary
    print("\n" + "="*70)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print("="*70 + "\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
