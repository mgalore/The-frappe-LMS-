#!/bin/bash

# LMS Health Check Launcher
# Quick way to check system health, manage services, and test APIs

echo "🔧 LMS Development Health Check Tools"
echo "======================================"
echo ""

case "${1:-help}" in
    "health")
        echo "🏥 Running comprehensive health check..."
        python3 /workspaces/The-frappe-LMS-/health_check.py
        ;;
    "api")
        echo "🔌 Running API tests..."
        python3 /workspaces/The-frappe-LMS-/api_tester.py
        ;;
    "service")
        shift
        echo "⚙️  Managing LMS services..."
        /workspaces/The-frappe-LMS-/lms_service_manager.sh "$@"
        ;;
    "all")
        echo "🚀 Running all checks..."
        echo ""
        echo "1️⃣ Health Check:"
        python3 /workspaces/The-frappe-LMS-/health_check.py
        echo ""
        echo "2️⃣ Service Status:"
        /workspaces/The-frappe-LMS-/lms_service_manager.sh status
        echo ""
        echo "3️⃣ API Tests:"
        python3 /workspaces/The-frappe-LMS-/api_tester.py
        ;;
    "help"|*)
        echo "Available commands:"
        echo "  health   - Run comprehensive system health check"
        echo "  api      - Run API connectivity tests"
        echo "  service  - Manage LMS services (start/stop/restart/status/fix/logs)"
        echo "  all      - Run all checks and show service status"
        echo ""
        echo "Examples:"
        echo "  ./lms_check.sh health"
        echo "  ./lms_check.sh service start"
        echo "  ./lms_check.sh service status"
        echo "  ./lms_check.sh all"
        ;;
esac
