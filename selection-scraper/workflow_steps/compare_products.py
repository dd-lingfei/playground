#!/usr/bin/env python3
"""
Product Comparison Workflow Step
Performs LLM-based product comparison between scraped items and Qdrant search results.
"""

from clients import OpenAIClient
from utils import get_app_logger


def _print_subsection(title, logger):
    logger.info("\n" + "-" * 100)
    logger.info(f"  {title}")
    logger.info("-" * 100)


def _format_comparison_result(search_term, result_item, comparison, rank, search_photo_url=None, search_price=None, logger=None):
    """Format a single comparison result nicely"""
    if logger is None:
        logger = get_app_logger()
    
    item_name = result_item.get('item_name', 'Unknown')
    msid = result_item.get('msid', 'N/A')
    similarity_score = result_item.get('similarity_score', 'N/A')
    catalog_photo_url = result_item.get('photo_url', None)
    catalog_size = result_item.get('size', None)
    item_price_usd = result_item.get('price_usd', None)
    
    is_same = comparison.get('is_same_product', False)
    confidence = comparison.get('confidence', 'unknown')
    reasoning = comparison.get('reasoning', 'No reasoning provided')
    
    # Status icon and text
    if is_same:
        status_icon = "✅"
        status_text = "MATCH"
        status_color = "\033[92m"  # Green
    else:
        status_icon = "❌"
        status_text = "NO MATCH"
        status_color = "\033[91m"  # Red
    reset_color = "\033[0m"
    
    logger.info(f"\n  🔍 Result #{rank}:")
    
    # Print catalog item info
    logger.info(f"     DoorDash Item Name: \"{item_name}\"")
    logger.info(f"     MSID: {msid} | Vector Similarity: {similarity_score}")
    
    # Print size and price if available
    if catalog_size:
        logger.info(f"     DoorDash Item Size: {catalog_size}")
    if item_price_usd is not None:
        logger.info(f"     DoorDash Item Price: {item_price_usd}")
    
    # Print catalog photo URL if available
    if catalog_photo_url:
        logger.info(f"     DoorDash Item Photo: {catalog_photo_url}")
    
    logger.info(f"     {status_color}{status_icon} {status_text}{reset_color} (Confidence: {confidence.upper()})")
    logger.info(f"     LLM Reasoning: {reasoning}")
    
    # Show key factors
    key_factors = comparison.get('key_factors', {})
    if key_factors:
        factors_str = []
        for factor, status in key_factors.items():
            if status == "match":
                icon = "✓"
            elif status == "different":
                icon = "✗"
            else:
                icon = "?"
            factors_str.append(f"{icon} {factor.replace('_', ' ')}")
        logger.info(f"     Factors: {', '.join(factors_str)}")
    
    # Show differences if not a match
    differences = comparison.get('differences', [])
    if differences and not is_same:
        logger.info(f"     Differences: {'; '.join(differences)}")
    
    return is_same


def compare_two_products(product1, product2, photo_url_1=None, photo_url_2=None, price_1=None, price_2=None, size_1=None, size_2=None, openai_client=None, logger=None):
    if openai_client is None:
        openai_client = OpenAIClient()
    
    if logger is None:
        logger = get_app_logger()
    
    # Perform comparison
    comparison = openai_client.compare_products(
        product1,
        product2,
        photo_url_1=photo_url_1,
        photo_url_2=photo_url_2,
        price_1=price_1,
        price_2=price_2,
        size_1=size_1,
        size_2=size_2
    )
    
    # Format output
    logger.info("\n" + "=" * 80)
    logger.info("PRODUCT COMPARISON")
    logger.info("=" * 80)
    logger.info(f"Product 1: {product1}")
    if photo_url_1:
        logger.info(f"  Photo URL: {photo_url_1}")
    if price_1:
        logger.info(f"  Price: {price_1}")
    if size_1:
        logger.info(f"  Size: {size_1}")
        
    logger.info(f"Product 2: {product2}")
    if photo_url_2:
        logger.info(f"  Photo URL: {photo_url_2}")
    if price_2:
        logger.info(f"  Price: {price_2}")
    if size_2:
        logger.info(f"  Size: {size_2}")
    logger.info("-" * 80)
    
    is_same = comparison.get('is_same_product', False)
    confidence = comparison.get('confidence', 'unknown')
    reasoning = comparison.get('reasoning', 'No reasoning provided')
    
    status = "✓ SAME PRODUCT" if is_same else "✗ DIFFERENT PRODUCTS"
    logger.info(f"\nResult: {status}")
    logger.info(f"Confidence: {confidence.upper()}")
    logger.info(f"\nReasoning: {reasoning}")
    
    # Print key factors
    key_factors = comparison.get('key_factors', {})
    if key_factors:
        logger.info(f"\nKey Factors:")
        for factor, status in key_factors.items():
            icon = "✓" if status == "match" else "✗" if status == "different" else "?"
            logger.info(f"  {icon} {factor.replace('_', ' ').title()}: {status}")
    
    # Print differences if products are different
    differences = comparison.get('differences', [])
    if differences and not is_same:
        logger.info(f"\nKey Differences:")
        for diff in differences:
            logger.info(f"  • {diff}")
    
    logger.info("=" * 80 + "\n")
    
    return comparison


def compare_products_with_llm(items_to_process, search_results_list, store_id, openai_client=None, logger=None):
    if openai_client is None:
        openai_client = OpenAIClient()
    
    if logger is None:
        logger = get_app_logger()
    
    overall_stats = {
        'total_comparisons': 0,
        'total_matches': 0,
        'high_confidence_matches': 0,
        'no_matches': 0
    }
    
    # Storage for CSV export
    csv_results = []
    
    search_terms = items_to_process['Name'].tolist()
    
    for i, search_term in enumerate(search_terms):
        scraped_product = items_to_process.iloc[i]
        scraped_item_name = search_term
        scraped_photo_url = scraped_product.get('Image_URL') if 'Image_URL' in scraped_product else None
        scraped_price = scraped_product.get('Price') if 'Price' in scraped_product else None
        results = search_results_list[i]
        
        _print_subsection(f"Item {i+1}: \"{scraped_item_name}\"\n\tScraped Photo: {scraped_photo_url}\n\tScraped Price: {scraped_price}\n", logger)
        
        if not results.points or len(results.points) == 0:
            logger.warning(f"  ⚠️  No search results found for this item")
            continue
        
        logger.info(f"\n  Found {len(results.points)} potential matches in DD selection")
        
        # Compare with top 3 results
        num_to_compare = min(3, len(results.points))
        best_match = None
        best_match_rank = None
        
        # Store comparison results for this item
        comparison_results = [False, False, False]  # Results for top 3 comparisons
        msids = [None, None, None]
        confidence_levels = [None, None, None]  # Confidence for each comparison
        
        for rank in range(num_to_compare):
            point = results.points[rank]
            result_item = {
                'item_name': point.payload.get('item_name', 'Unknown'),
                'msid': point.payload.get('msid', 'N/A'),
                'photo_url': point.payload.get('photo_url', None),
                'size': point.payload.get('size', None),
                'price_usd': point.payload.get('price_usd', None),
                'similarity_score': f"{point.score:.4f}" if hasattr(point, 'score') else 'N/A'
            }
            
            # Store MSID for CSV
            msids[rank] = result_item['msid']
            
            # Perform LLM comparison with photo URLs, size, and price
            overall_stats['total_comparisons'] += 1
            
            
            comparison = openai_client.compare_products(
                search_term, 
                result_item['item_name'],
                photo_url_1=scraped_photo_url,
                photo_url_2=result_item['photo_url'],
                price_1=scraped_price,
                price_2=result_item['price_usd'],
                size_2=result_item['size']
            )
            
            is_match = _format_comparison_result(
                search_term, 
                result_item, 
                comparison, 
                rank + 1, 
                search_photo_url=scraped_photo_url,
                search_price=scraped_price,
                logger=logger
            )
            
            # Store comparison result and confidence
            comparison_results[rank] = is_match
            confidence_levels[rank] = comparison.get('confidence', 'unknown')
            
            if is_match:
                overall_stats['total_matches'] += 1
                if comparison.get('confidence') == 'high':
                    overall_stats['high_confidence_matches'] += 1
                
                if best_match is None:
                    best_match = result_item
                    best_match_rank = rank + 1
            else:
                overall_stats['no_matches'] += 1
        
        # Determine if item was found in DD (at least one comparison is True)
        item_found_in_dd = any(comparison_results)
        
        # Add row to CSV results with grouped msid/result/confidence columns
        csv_row = {
            'store_id': store_id,
            'item_name': search_term,
            'item_found_in_dd': item_found_in_dd,
            'msid_1': msids[0] if len(msids) > 0 else None,
            'comparison_1_result': comparison_results[0] if len(comparison_results) > 0 else False,
            'confidence_1': confidence_levels[0] if len(confidence_levels) > 0 else None,
            'msid_2': msids[1] if len(msids) > 1 else None,
            'comparison_2_result': comparison_results[1] if len(comparison_results) > 1 else False,
            'confidence_2': confidence_levels[1] if len(confidence_levels) > 1 else None,
            'msid_3': msids[2] if len(msids) > 2 else None,
            'comparison_3_result': comparison_results[2] if len(comparison_results) > 2 else False,
            'confidence_3': confidence_levels[2] if len(confidence_levels) > 2 else None,
        }
        csv_results.append(csv_row)
        
        # Summary for this item
        if best_match:
            logger.info(f"\n  ✅ Best Match: Result #{best_match_rank}")
            logger.info(f"     MSID: {best_match['msid']} - {best_match['item_name'][:60]}...")
        else:
            logger.warning(f"\n  ⚠️  No confident matches found in top {num_to_compare} results")
    
    return csv_results, overall_stats

