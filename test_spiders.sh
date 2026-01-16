#!/bin/bash
# Test script for local spider execution

echo "========================================="
echo "Biomedical Data Scraper - Test Script"
echo "========================================="
echo ""

# Create data directories
echo "Creating data directories..."
mkdir -p data/raw/{biolincc,openicpsr,bioportal,kidsfirst,nsrr}
echo "✓ Directories created"
echo ""

# Test 1: List platforms
echo "Test 1: Listing available platforms"
echo "-----------------------------------"
python run_local.py --list
echo ""

# Test 2: Test Kids First spider (no auth required)
echo "Test 2: Testing Kids First spider (5 seconds timeout)"
echo "-----------------------------------"
timeout 5 python run_local.py --platform kidsfirst --verbose || true
echo ""
echo "✓ Kids First test completed (check data/raw/kidsfirst/ for results)"
echo ""

# Check if any data was collected
echo "Checking collected data..."
echo "-----------------------------------"
if [ -n "$(ls -A data/raw/kidsfirst/ 2>/dev/null)" ]; then
    echo "✓ Data files found in data/raw/kidsfirst/:"
    ls -lh data/raw/kidsfirst/
else
    echo "ℹ No data files yet (spider may need more time or site may be unavailable)"
fi
echo ""

echo "========================================="
echo "Test completed!"
echo "========================================="
echo ""
echo "To run a full scraping session:"
echo "  python run_local.py --platform kidsfirst"
echo ""
echo "To run all enabled platforms:"
echo "  python run_local.py --platform all"
echo ""
