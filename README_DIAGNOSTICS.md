# 🛠️ Frappe LMS Diagnostic Scripts

This collection of scripts helps you quickly diagnose, monitor, and fix issues in your Frappe LMS development environment.

## 📋 Available Scripts

### 1. 🏥 `health_check.py` - Comprehensive Health Check
**Purpose**: Complete system health assessment with detailed reporting

```bash
python3 health_check.py
```

**What it checks**:
- ✅ Service availability (MariaDB, Web Server, Socket.IO, Redis)
- 🌐 API endpoint functionality 
- 🔧 Build files and configuration
- 📊 Overall system health percentage

**Sample Output**:
```
🏥 FRAPPE LMS HEALTH CHECK
✓ Web Server is running on port 8000
⚠ LMS Settings API returned status 500
📊 System Health: 76.9% (10/13) - GOOD
```

---

### 2. ⚡ `quick_fix.py` - Automated Problem Solver
**Purpose**: Automatically fix common issues based on detected problems

```bash
# Fix all issues automatically
python3 quick_fix.py all

# Fix specific issues
python3 quick_fix.py db        # Database issues
python3 quick_fix.py cache     # Cache and build issues
python3 quick_fix.py perms     # Permission issues
python3 quick_fix.py restart   # Service restart
```

**What it fixes**:
- 🗄️ MariaDB connection and startup issues
- 🔄 Cache clearing and asset rebuilding
- 📝 File permissions and configuration
- 🚀 Service restarts and process management

---

### 3. 📊 `service_monitor.py` - Real-time Service Monitoring
**Purpose**: Monitor services in real-time or perform quick status checks

```bash
# Single check
python3 service_monitor.py

# Continuous monitoring (updates every 5 seconds)
python3 service_monitor.py monitor
```

**What it monitors**:
- 🟢 Real-time service status
- 🌐 API endpoint health
- 💻 Process monitoring
- 📈 Continuous updates with status changes

---

### 4. 🛠️ `dev_helper.py` - Development Environment Manager
**Purpose**: Quick commands for common development workflows

```bash
python3 dev_helper.py <command>
```

**Available commands**:
- `start` - Start complete development environment
- `stop` - Stop all services cleanly
- `restart` - Restart all services
- `logs` - Show recent system logs
- `reset` - Nuclear reset (clears everything)
- `test` - Run comprehensive tests
- `monitor` - Start continuous monitoring

**Examples**:
```bash
python3 dev_helper.py start     # Start everything
python3 dev_helper.py monitor   # Watch services in real-time
python3 dev_helper.py reset     # Full reset when things go wrong
```

---

## 🚀 Quick Start Workflow

### When you make changes and want to test:
```bash
# 1. Check if everything is working
python3 health_check.py

# 2. If issues found, auto-fix them
python3 quick_fix.py all

# 3. Start/restart services
python3 dev_helper.py restart

# 4. Monitor in real-time (optional)
python3 service_monitor.py monitor
```

### When services won't start:
```bash
# 1. Stop everything
python3 dev_helper.py stop

# 2. Fix common issues
python3 quick_fix.py all

# 3. Start fresh
python3 dev_helper.py start
```

### When you see errors:
```bash
# 1. Quick diagnosis
python3 health_check.py

# 2. Check logs
python3 dev_helper.py logs

# 3. If desperate, nuclear option
python3 dev_helper.py reset
```

---

## 🎯 Use Cases

| Scenario | Recommended Script | Command |
|----------|-------------------|---------|
| 🆕 First time setup | Dev Helper | `python3 dev_helper.py start` |
| 🔍 Check if all working | Health Check | `python3 health_check.py` |
| 🚨 Something is broken | Quick Fix | `python3 quick_fix.py all` |
| 👀 Watch services live | Service Monitor | `python3 service_monitor.py monitor` |
| 💥 Everything is broken | Dev Helper | `python3 dev_helper.py reset` |
| 📝 See what went wrong | Dev Helper | `python3 dev_helper.py logs` |

---

## 📁 Script Locations

All scripts are located in the root directory:
```
/workspaces/The-frappe-LMS-/
├── health_check.py      # Health diagnostics
├── quick_fix.py         # Auto-fix common issues
├── service_monitor.py   # Real-time monitoring
├── dev_helper.py        # Development workflow
└── README_DIAGNOSTICS.md # This file
```

---

## 🏷️ Health Check Results Guide

### Status Indicators:
- ✅ **Green checkmark** - Service/API working perfectly
- ⚠️ **Yellow warning** - Service working but with issues
- ❌ **Red X** - Service down or failing
- 📊 **Percentage** - Overall health score

### Health Score Interpretation:
- **90-100%** 🟢 Excellent - All systems operational
- **75-89%** 🟡 Good - Minor issues, system functional  
- **50-74%** 🟠 Warning - Several issues, may impact functionality
- **Below 50%** 🔴 Critical - Major issues, system likely unusable

---

## 💡 Pro Tips

1. **Always run health_check.py first** - It gives you the complete picture
2. **Use monitoring mode during development** - Catch issues as they happen
3. **Keep logs handy** - `dev_helper.py logs` shows recent activity
4. **Reset is your friend** - When all else fails, `dev_helper.py reset`
5. **Automate fixes** - `quick_fix.py all` solves most common issues

---

## 🚨 Emergency Troubleshooting

**If nothing works:**
```bash
# Nuclear option - resets everything
python3 dev_helper.py reset

# Then start fresh
python3 dev_helper.py start

# Verify it worked
python3 health_check.py
```

**If scripts don't run:**
```bash
# Make sure Python path is correct
which python3

# Install missing dependencies
pip install requests

# Check file permissions
ls -la *.py
```

---

## 🤝 Contributing

Feel free to enhance these scripts by:
- Adding more health checks
- Improving auto-fix capabilities  
- Adding new monitoring features
- Better error messages and logging

---

**Happy Coding! 🚀**
