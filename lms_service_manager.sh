#!/bin/bash

# Quick LMS Service Manager Script
# Use this to quickly start/stop/restart/check LMS services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local message=$1
    local status=$2
    
    case $status in
        "SUCCESS") echo -e "${GREEN}✓${NC} $message" ;;
        "ERROR") echo -e "${RED}✗${NC} $message" ;;
        "WARNING") echo -e "${YELLOW}⚠${NC} $message" ;;
        *) echo -e "${BLUE}ℹ${NC} $message" ;;
    esac
}

# Function to check if a service is running
check_service() {
    local service_name=$1
    local port=$2
    
    if netstat -tlnp | grep -q ":$port "; then
        print_status "$service_name is running on port $port" "SUCCESS"
        return 0
    else
        print_status "$service_name is NOT running on port $port" "ERROR"
        return 1
    fi
}

# Function to start services
start_services() {
    echo -e "\n${BLUE}🚀 Starting LMS Services...${NC}"
    
    # Check and start MariaDB
    if ! sudo service mariadb status | grep -q "active (running)"; then
        print_status "Starting MariaDB..." "INFO"
        sudo service mariadb start
    else
        print_status "MariaDB already running" "SUCCESS"
    fi
    
    # Change to bench directory
    cd /workspaces/The-frappe-LMS-/lms-bench
    
    # Start bench services
    print_status "Starting Frappe LMS services..." "INFO"
    bench start &
    
    # Wait a moment for services to start
    sleep 5
    
    # Check if services started successfully
    check_services
}

# Function to stop services
stop_services() {
    echo -e "\n${BLUE}🛑 Stopping LMS Services...${NC}"
    
    # Kill bench processes
    pkill -f "bench start" || true
    
    # Kill individual service processes
    local ports=(8000 9000 11000 13000)
    for port in "${ports[@]}"; do
        local pid=$(lsof -ti:$port 2>/dev/null || true)
        if [ ! -z "$pid" ]; then
            print_status "Killing process on port $port (PID: $pid)" "INFO"
            kill -9 $pid 2>/dev/null || true
        fi
    done
    
    print_status "Services stopped" "SUCCESS"
}

# Function to check all services
check_services() {
    echo -e "\n${BLUE}🔍 Checking LMS Services...${NC}"
    
    local all_running=true
    
    # Check MariaDB
    if sudo service mariadb status | grep -q "active (running)"; then
        print_status "MariaDB is running" "SUCCESS"
    else
        print_status "MariaDB is not running" "ERROR"
        all_running=false
    fi
    
    # Check service ports
    check_service "Web Server" 8000 || all_running=false
    check_service "Socket.IO" 9000 || all_running=false
    check_service "Redis Queue" 11000 || all_running=false
    check_service "Redis Cache" 13000 || all_running=false
    
    if [ "$all_running" = true ]; then
        print_status "All services are running!" "SUCCESS"
        return 0
    else
        print_status "Some services are not running" "WARNING"
        return 1
    fi
}

# Function to restart services
restart_services() {
    echo -e "\n${BLUE}🔄 Restarting LMS Services...${NC}"
    stop_services
    sleep 3
    start_services
}

# Function to quick fix common issues
quick_fix() {
    echo -e "\n${BLUE}🔧 Running Quick Fix...${NC}"
    
    cd /workspaces/The-frappe-LMS-/lms-bench
    
    # Clear cache
    print_status "Clearing cache..." "INFO"
    bench clear-cache || print_status "Cache clear failed" "WARNING"
    
    # Check for syntax errors
    print_status "Checking for syntax errors..." "INFO"
    python -m py_compile apps/lms/lms/hooks.py || {
        print_status "Syntax error in hooks.py!" "ERROR"
        return 1
    }
    
    # Restart services
    restart_services
    
    # Run health check
    print_status "Running health check..." "INFO"
    python3 /workspaces/The-frappe-LMS-/health_check.py
}

# Function to show logs
show_logs() {
    echo -e "\n${BLUE}📋 Recent LMS Logs...${NC}"
    cd /workspaces/The-frappe-LMS-/lms-bench
    
    if [ -f "logs/frappe.log" ]; then
        echo -e "\n${YELLOW}Latest Frappe Logs:${NC}"
        tail -20 logs/frappe.log
    fi
    
    if [ -f "logs/worker.log" ]; then
        echo -e "\n${YELLOW}Latest Worker Logs:${NC}"
        tail -20 logs/worker.log
    fi
    
    if [ -f "logs/worker.error.log" ]; then
        echo -e "\n${YELLOW}Latest Error Logs:${NC}"
        tail -20 logs/worker.error.log
    fi
}

# Function to show help
show_help() {
    echo -e "\n${BLUE}🆘 LMS Service Manager Help${NC}"
    echo "Usage: ./lms_service_manager.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start all LMS services"
    echo "  stop      Stop all LMS services"  
    echo "  restart   Restart all LMS services"
    echo "  status    Check status of all services"
    echo "  fix       Run quick fix for common issues"
    echo "  logs      Show recent logs"
    echo "  health    Run comprehensive health check"
    echo "  help      Show this help message"
    echo ""
}

# Main script logic
case "$1" in
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "status"|"check")
        check_services
        ;;
    "fix")
        quick_fix
        ;;
    "logs")
        show_logs
        ;;
    "health")
        python3 /workspaces/The-frappe-LMS-/health_check.py
        ;;
    "help"|"--help"|"-h"|"")
        show_help
        ;;
    *)
        print_status "Unknown command: $1" "ERROR"
        show_help
        exit 1
        ;;
esac
