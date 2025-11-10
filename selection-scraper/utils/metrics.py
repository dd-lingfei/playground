#!/usr/bin/env python3

import time
from functools import wraps
from typing import Dict, List
from collections import defaultdict


class MetricsTracker:
    """Track function call counts and response times"""
    
    def __init__(self):
        self.call_counts: Dict[str, int] = defaultdict(int)
        self.response_times: Dict[str, List[float]] = defaultdict(list)
    
    def track(self, func):
        """Decorator to track function calls and timing"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a unique key for this function
            class_name = args[0].__class__.__name__ if args else "Unknown"
            func_key = f"{class_name}.{func.__name__}"
            
            # Track the call
            self.call_counts[func_key] += 1
            
            # Time the execution
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed_time = time.time() - start_time
                self.response_times[func_key].append(elapsed_time)
        
        return wrapper
    
    def print_stats(self):
        """Print collected metrics"""
        if not self.call_counts:
            print("\nNo metrics collected.")
            return
        
        print("\n" + "="*80)
        print("PERFORMANCE METRICS")
        print("="*80)
        
        # Sort by class name for better organization
        sorted_keys = sorted(self.call_counts.keys())
        
        current_class = None
        for func_key in sorted_keys:
            class_name = func_key.split('.')[0]
            
            # Print class header when it changes
            if class_name != current_class:
                if current_class is not None:
                    print()  # Add spacing between classes
                print(f"\n{class_name}:")
                print("-" * 80)
                current_class = class_name
            
            count = self.call_counts[func_key]
            times = self.response_times[func_key]
            avg_time = sum(times) / len(times) if times else 0
            total_time = sum(times)
            min_time = min(times) if times else 0
            max_time = max(times) if times else 0
            
            func_name = func_key.split('.', 1)[1]
            print(f"  {func_name:40} | Calls: {count:6} | "
                  f"Avg: {avg_time:7.3f}s | Total: {total_time:7.2f}s | "
                  f"Min: {min_time:6.3f}s | Max: {max_time:6.3f}s")
        
        print("\n" + "="*80)
        print(f"Total function calls tracked: {sum(self.call_counts.values())}")
        print("="*80 + "\n")
    
    def reset(self):
        """Reset all metrics"""
        self.call_counts.clear()
        self.response_times.clear()


# Global metrics tracker instance
metrics_tracker = MetricsTracker()


def print_metrics():
    """Convenience function to print metrics"""
    metrics_tracker.print_stats()

