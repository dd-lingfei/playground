# Logging Implementation

## Overview

All print statements have been converted to use a centralized logging system that outputs to both console and rotating log files.

## Features

### 1. **Dual Output**
   - **Console**: Color-coded output for easy reading during development
   - **File**: Timestamped logs saved to `output.log` for audit and debugging

### 2. **Log Rotation**
   - **Max Size**: 10MB per log file (configurable)
   - **Backup Count**: Keeps 5 backup files (configurable)
   - **Auto-Archive**: When `output.log` reaches max size:
     - Renamed to `output.log.1`
     - Previous backups shifted: `output.log.1` → `output.log.2`, etc.
     - New empty `output.log` created

### 3. **Color-Coded Console Output**
   - DEBUG: Cyan
   - INFO: Default (white)
   - WARNING: Yellow
   - ERROR: Red
   - CRITICAL: Magenta

### 4. **Log Levels**
   - **Console**: INFO level by default (shows INFO, WARNING, ERROR, CRITICAL)
   - **File**: DEBUG level by default (captures everything)

## Files Modified

### New Files Created
1. **`utils/logger.py`**
   - Core logging utility
   - `setup_logger()`: Configure logger with console and file handlers
   - `get_app_logger()`: Get singleton logger instance
   - `ColoredFormatter`: Custom formatter for colored console output

### Files Updated
1. **`utils/__init__.py`**
   - Exported logger functions: `get_app_logger`, `get_logger`, `setup_logger`

2. **`end_to_end_pipeline.py`**
   - Replaced all `print()` with `logger.info()`, `logger.error()`, etc.
   - Passes logger to all workflow steps
   - ~40 print statements converted

3. **`workflow_steps/compare_products.py`**
   - Accepts optional `logger` parameter
   - All output uses logger (info, warning, error levels)
   - ~30 print statements converted

4. **`workflow_steps/search_against_qdrant.py`**
   - Accepts optional `logger` parameter
   - Uses logger for search status messages

## Usage

### Basic Usage

```python
from utils import get_app_logger

logger = get_app_logger()

logger.debug("Detailed debugging information")
logger.info("General informational message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical error message")
```

### Custom Configuration

```python
from utils import setup_logger

logger = setup_logger(
    name='my-logger',
    log_file='my_custom.log',
    max_bytes=5*1024*1024,  # 5MB
    backup_count=10,
    console_level=logging.DEBUG,
    file_level=logging.DEBUG
)
```

## Log File Format

### Console Output
```
Test info message
⚠️  Test warning message
❌ Test error message
```

### File Output
```
2025-11-01 22:24:58 - selection-scraper - INFO - Test info message
2025-11-01 22:24:58 - selection-scraper - WARNING - Test warning message
2025-11-01 22:24:58 - selection-scraper - ERROR - Test error message
```

## Log Rotation Example

When `output.log` reaches 10MB:

**Before:**
```
output.log (10MB - full)
output.log.1 (10MB)
output.log.2 (10MB)
output.log.3 (10MB)
output.log.4 (10MB)
```

**After:**
```
output.log (0KB - new)
output.log.1 (10MB - was output.log)
output.log.2 (10MB - was output.log.1)
output.log.3 (10MB - was output.log.2)
output.log.4 (10MB - was output.log.3)
output.log.5 (10MB - was output.log.4)
```

Oldest file (`output.log.5`) will be deleted on next rotation.

## Benefits

1. **Audit Trail**: All operations are logged with timestamps
2. **Debugging**: DEBUG level logs in file help troubleshoot issues
3. **Storage Management**: Automatic rotation prevents disk space issues
4. **Performance Tracking**: Can review logs to analyze pipeline performance
5. **Error Analysis**: Error logs help identify and fix issues
6. **Consistency**: Uniform logging format across all modules

## Testing

Test the logger:
```bash
python3 -c "
from utils import get_app_logger
logger = get_app_logger()
logger.info('Test message')
"

# Check log file
tail output.log
```

## Configuration

Default settings (in `utils/logger.py`):
- **Log file**: `output.log`
- **Max size**: 10MB
- **Backup count**: 5 files
- **Console level**: INFO
- **File level**: DEBUG

These can be customized by calling `setup_logger()` with different parameters.

