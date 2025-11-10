#!/usr/bin/env python3

import sys
import argparse
from workflow_steps.refresh_qdrant_collection import refresh_qdrant_collection
from workflow_steps.search_against_qdrant import search_against_qdrant
from config import CollectionConfig
from utils import print_metrics
from clients import OpenAIClient
from datetime import datetime


# Example usage
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Search for items in Qdrant collection')
    parser.add_argument('search_term', type=str, help='The search term to look for')
    parser.add_argument('--metrics', action='store_true', help='Print performance metrics at the end')
    parser.add_argument('--store-id', type=int, default=1741819, help='Store ID (default: 1741819)')
    parser.add_argument('--compare', action='store_true', help='Compare search term with results using LLM')
    parser.add_argument('--compare-top-n', type=int, default=3, help='Number of top results to compare (default: 3)')
    
    args = parser.parse_args()
    
    # Get search term from command line argument
    search_term = args.search_term
    store_id = args.store_id
    
    collection_name = CollectionConfig.get_collection_name(store_id)
    print(f"Collection name: {collection_name}")

    # Search
    search_terms = [search_term]
    print(f"Starting search for store: {store_id}")
    print(f"Search term: {search_term}")
    search_results_list = search_against_qdrant(
        search_terms=search_terms, 
        store_id=store_id, 
        collection_name=collection_name
    )
    for i in range(0, len(search_results_list)):
        print(f"\nSearch results for: '{search_terms[i]}'")
        print(f"Found {len(search_results_list[i].points)} results:")
        print("-" * 80)
        
        for rank, point in enumerate(search_results_list[i].points, 1):
            payload = point.payload
            score = point.score if hasattr(point, 'score') else 'N/A'
            print(f"\n  Result #{rank} (score: {score})")
            print(f"  MSID: {payload.get('msid')}")
            print(f"  Item Name: {payload.get('item_name')}")
            print(f"  Photo URL: {payload.get('photo_url')}")
        print("-" * 80)
    
    # Compare products using LLM if requested
    if args.compare:
        print("\n" + "=" * 80)
        print("PRODUCT COMPARISON (LLM-based)")
        print("=" * 80)
        
        openai_client = OpenAIClient()
        
        for i, search_term_used in enumerate(search_terms):
            results = search_results_list[i]
            num_to_compare = min(args.compare_top_n, len(results.points))
            
            print(f"\nComparing search term with top {num_to_compare} results...")
            print(f"Search Term: \"{search_term_used}\"")
            print("-" * 80)
            
            for rank in range(num_to_compare):
                point = results.points[rank]
                item_name = point.payload.get('item_name', 'Unknown')
                msid = point.payload.get('msid', 'N/A')
                photo_url = point.payload.get('photo_url', None)
                similarity_score = point.score if hasattr(point, 'score') else 'N/A'
                
                print(f"\n🔍 Comparing with Result #{rank + 1}:")
                print(f"   Catalog Item: \"{item_name}\"")
                print(f"   MSID: {msid} | Similarity Score: {similarity_score}")
                if photo_url:
                    print(f"   Photo URL: {photo_url}")
                
                # Perform LLM comparison with photo URL
                comparison = openai_client.compare_products(
                    search_term_used, 
                    item_name,
                    photo_url_2=photo_url
                )
                
                is_same = comparison.get('is_same_product', False)
                confidence = comparison.get('confidence', 'unknown')
                reasoning = comparison.get('reasoning', 'No reasoning provided')
                
                # Display result with icon
                if is_same:
                    status_icon = "✅"
                    status_text = "MATCH"
                else:
                    status_icon = "❌"
                    status_text = "NO MATCH"
                
                print(f"   {status_icon} {status_text} (Confidence: {confidence.upper()})")
                print(f"   Reasoning: {reasoning}")
                
                # Show key factors
                key_factors = comparison.get('key_factors', {})
                if key_factors:
                    factors_str = []
                    for factor, status in key_factors.items():
                        icon = "✓" if status == "match" else "✗" if status == "different" else "?"
                        factors_str.append(f"{icon} {factor}")
                    print(f"   Factors: {', '.join(factors_str)}")
                
                # Show differences if not a match
                differences = comparison.get('differences', [])
                if differences and not is_same:
                    print(f"   Differences: {', '.join(differences)}")
                
                print("-" * 80)
        
        print("=" * 80)
    
    # Print performance metrics if requested
    if args.metrics:
        print_metrics()