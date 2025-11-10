#!/usr/bin/env python3
"""
Logger Utility
Provides a logger that outputs to both console and rotating log files.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


class ColoredFormatter(logging.Formatter):
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[0m',        # Default
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[91m',      # Red
        'CRITICAL': '\033[95m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        
        return super().format(record)


def setup_logger(
    name='selection-scraper',
    log_file='output.log',
    max_bytes=10*1024*1024,  # 10MB default
    backup_count=5,
    console_level=logging.INFO,
    file_level=logging.DEBUG
):
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)  # Capture all levels
    logger.propagate = False  # Prevent duplicate messages from parent loggers
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_format = ColoredFormatter(
        '%(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # Rotating file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(file_level)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name='selection-scraper'):
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
    
    Returns:
        logging.Logger: Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


# Create a singleton logger instance for the application
_app_logger = None


def get_app_logger():
    """Get the application-wide logger singleton"""
    global _app_logger
    if _app_logger is None:
        _app_logger = setup_logger()
    return _app_logger

