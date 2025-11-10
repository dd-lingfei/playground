#!/usr/bin/env python3

import argparse
from workflow_steps import compare_two_products
from utils import print_metrics
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare two product names using LLM')
    parser.add_argument('product1', type=str, help='First product name')
    parser.add_argument('product2', type=str, help='Second product name')
    parser.add_argument('--photo-url-1', type=str, default=None, help='Photo URL for first product')
    parser.add_argument('--photo-url-2', type=str, default=None, help='Photo URL for second product')
    parser.add_argument('--price-1', type=str, default=None, help='Price for first product')
    parser.add_argument('--price-2', type=str, default=None, help='Price for second product')
    parser.add_argument('--size-1', type=str, default=None, help='Size for first product')
    parser.add_argument('--size-2', type=str, default=None, help='Size for second product')
    parser.add_argument('--metrics', action='store_true', help='Print performance metrics')
    parser.add_argument('--json', action='store_true', help='Output raw JSON response')
    
    args = parser.parse_args()
    
    # Compare products using workflow_steps function
    print(f"Comparing products using LLM...")
    if args.photo_url_1 or args.photo_url_2:
        print(f"Using photo URLs for additional context...")
    
    result = compare_two_products(
        args.product1, 
        args.product2,
        photo_url_1=args.photo_url_1,
        photo_url_2=args.photo_url_2,
        price_1=args.price_1,
        price_2=args.price_2,
        size_1=args.size_1,
        size_2=args.size_2
    )
    
    # Display raw JSON if requested
    if args.json:
        print("\n" + "=" * 80)
        print("RAW JSON RESPONSE")
        print("=" * 80)
        print(json.dumps(result, indent=2))
        print("=" * 80 + "\n")
    
    # Print metrics if requested
    if args.metrics:
        print_metrics()

