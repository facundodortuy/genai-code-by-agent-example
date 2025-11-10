#!/bin/bash
# Verification script for the AI Research Agents system

echo "======================================================================"
echo "AI RESEARCH AGENTS - SYSTEM VERIFICATION"
echo "======================================================================"
echo ""

echo "1. Checking Python version..."
python --version
echo ""

echo "2. Checking dependencies..."
pip show fastmcp pydantic httpx python-dotenv | grep "Name:\|Version:" | head -8
echo ""

echo "3. Running unit tests..."
python -m pytest tests/ -v --tb=short
echo ""

echo "4. Running linter..."
ruff check src/ tests/ demo.py test_mcp_server.py
echo ""

echo "5. Verifying MCP server initialization..."
python test_mcp_server.py
echo ""

echo "======================================================================"
echo "SYSTEM VERIFICATION COMPLETE"
echo "======================================================================"
echo ""
echo "To run the system:"
echo "  - Demo: python demo.py"
echo "  - MCP Server: python -m src.server"
echo ""
echo "For more information, see README.md"
echo "======================================================================"
