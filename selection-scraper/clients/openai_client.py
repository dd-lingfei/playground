from openai import OpenAI
from typing import List, Optional, Dict, Any
from utils import metrics_tracker
import json
import os

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_LLM_MODEL = "gpt-5"

class OpenAIClient:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern - only one instance of OpenAIClient will be created"""
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        portkey_api_key: str = None,
        portkey_virtual_key: str = None,
        gateway_url: str = None,
        max_retries: int = 10
    ):
        # Only initialize once
        if self._initialized:
            return
        
        # Read from environment variables
        portkey_api_key = portkey_api_key or os.getenv("PORTKEY_API_KEY")
        portkey_virtual_key = portkey_virtual_key or os.getenv("PORTKEY_VIRTUAL_KEY")
        gateway_url = gateway_url or os.getenv("GATEWAY_URL", "http://cybertron-service-gateway-offline-jobs.svc.ddnw.net:8080/v1")
        
        # Validate required parameters
        if not portkey_api_key:
            raise ValueError(
                "PORTKEY_API_KEY is required. Please set it as an environment variable or pass it to the constructor."
            )
        
        if not portkey_virtual_key:
            raise ValueError(
                "PORTKEY_VIRTUAL_KEY is required. Please set it as an environment variable or pass it to the constructor."
            )
            
        self.client = OpenAI(
            api_key="n/a",  # arbitrary, needs to not be blank
            base_url=gateway_url,
            default_headers={
                "x-portkey-api-key": portkey_api_key,
                "x-portkey-virtual-key": portkey_virtual_key
            },
            max_retries=max_retries
        )
        self._initialized = True
        print("✓ OpenAIClient singleton initialized")
    
    @metrics_tracker.track
    def generate_embeddings(
        self,
        texts: List[str],
        model: str = DEFAULT_EMBEDDING_MODEL,
        **kwargs
    ) -> List[List[float]]:
        MAX_BATCH_SIZE = 1000
        
        # Check if we need to batch
        if len(texts) > MAX_BATCH_SIZE:
            print(f"⚠️  WARNING: Input size ({len(texts)} texts) exceeds recommended batch size ({MAX_BATCH_SIZE}).")
            print(f"    Splitting into batches of {MAX_BATCH_SIZE}. This may reduce performance.")
            
            # Split into batches
            all_embeddings = []
            num_batches = (len(texts) + MAX_BATCH_SIZE - 1) // MAX_BATCH_SIZE
            
            for i in range(0, len(texts), MAX_BATCH_SIZE):
                batch_num = i // MAX_BATCH_SIZE + 1
                batch = texts[i:i + MAX_BATCH_SIZE]
                print(f"    Processing batch {batch_num}/{num_batches} ({len(batch)} texts)...")
                
                response = self.client.embeddings.create(
                    input=batch,
                    model=model,
                    **kwargs
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
            
            print(f"    ✓ Completed all {num_batches} batches ({len(all_embeddings)} embeddings)")
            return all_embeddings
        else:
            # Single batch - normal processing
            response = self.client.embeddings.create(
                input=texts,
                model=model,
                **kwargs
            )
            # Extract embeddings from response
            embeddings = [item.embedding for item in response.data]
            return embeddings

    @metrics_tracker.track
    def generate_embedding(
        self,
        text: str,
        model: str = DEFAULT_EMBEDDING_MODEL,
        **kwargs
    ) -> List[List[float]]:
        return self.generate_embeddings(texts=[text], model=model, **kwargs)[0]
    
    @metrics_tracker.track
    def _generate_llm_response(
        self,
        messages: List[Dict[str, str]],
        model: str = DEFAULT_LLM_MODEL,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        params = {
            "model": model,
            "messages": messages,
            **kwargs
        }
        
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        
        response = self.client.chat.completions.create(**params)
        
        # Extract the response text
        return response.choices[0].message.content
    
    @metrics_tracker.track
    def compare_products(
        self,
        item_name_1: str,
        item_name_2: str,
        photo_url_1: Optional[str] = None,
        photo_url_2: Optional[str] = None,
        price_1: Optional[float] = None,
        price_2: Optional[float] = None,
        size_1: Optional[str] = None,
        size_2: Optional[str] = None,
        model: str = DEFAULT_LLM_MODEL,
        compare_price: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        # Build product info with optional details
        product_1_info = f'"{item_name_1}"'
        if price_1 and compare_price:
            product_1_info += f"\nPrice: ${price_1}"
        if size_1:
            product_1_info += f"\nSize: {size_1}"
        if photo_url_1:
            product_1_info += f"\nPhoto URL: {photo_url_1}"
        
        product_2_info = f'"{item_name_2}"'
        if price_2 and compare_price:
            product_2_info += f"\nPrice: {price_2}"
        if size_2:
            product_2_info += f"\nSize: {size_2}"
        if photo_url_2:
            product_2_info += f"\nPhoto URL: {photo_url_2}"
        
        prompt = f"""You are a product matching expert. Compare these two product names and determine if they represent the same product.

Product 1: {product_1_info}
Product 2: {product_2_info}

Consider the following factors:
1. Product Type/Category (e.g., beverage, snack, cleaning product)
2. Brand Name
3. Size/Quantity (e.g., 12 oz, 6-pack, 500ml) - CRITICAL for matching
4. Variant/Flavor (e.g., original, cherry, sugar-free)
5. Organic vs Regular (IMPORTANT: organic and regular versions are DIFFERENT products)
6. Package Type (e.g., bottle, can, box)
7. Price (if provided, use as additional signal - similar prices suggest same product, very different prices may indicate different products)
8. Photo URLs (if provided, use as additional context for visual verification)
9. Any other distinguishing features

Note: If photo URLs are provided, you can reference them to gain additional context about the products, 
though you cannot actually view the images. Photo URLs can help confirm product identity.

Price Consideration (only if prices are provided):
- If prices are provided and similar (within ~20% variance), this supports products being the same
- If prices are very different (>50% variance), be more cautious - they may be different products or different sizes
- Price alone should not be the determining factor, but can support or weaken other evidence

Two products are considered the SAME if they differ only in:
- Minor wording differences (e.g., "oz" vs "ounce")
- Abbreviations vs full words (e.g., "ct" vs "count")
- Extra descriptive words that don't change the product
- Small price differences due to promotions or market conditions

Two products are considered DIFFERENT if they differ in:
- Brand
- Size/quantity (CRITICAL: "12 oz" ≠ "24 oz", "1 ct" ≠ "6 ct")
- Flavor/variant
- Product type
- Package type
- Organic vs Regular (e.g., "Organic Milk" vs "Milk", "Organic Bananas" vs "Bananas")

CRITICAL: Organic and non-organic versions of the same product are DIFFERENT products.
Examples:
- "Organic Strawberries" ≠ "Strawberries"
- "Organic Valley Whole Milk" ≠ "Valley Whole Milk"
- "Simple Truth Organic Eggs" ≠ "Simple Truth Eggs"

Respond in JSON format with the following structure:
{{
    "is_same_product": true/false,
    "confidence": "high/medium/low",
    "reasoning": "Brief explanation of your decision",
    "key_factors": {{
        "product_type": "match/different/uncertain",
        "brand": "match/different/uncertain",
        "size": "match/different/uncertain",
        "variant": "match/different/uncertain",
        "organic_status": "match/different/uncertain",
        "price": "similar/different/uncertain"
    }},
    "differences": ["list of key differences if products are different"]
}}

Respond ONLY with valid JSON, no additional text."""

        messages = [
            {"role": "system", "content": "You are a precise product matching assistant. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response_text = self._generate_llm_response(
            messages=messages,
            model=model,
            **kwargs
        )
        
        # Parse JSON response
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return a structured error
            return {
                "is_same_product": False,
                "confidence": "low",
                "reasoning": f"Failed to parse LLM response: {str(e)}",
                "key_factors": {},
                "differences": ["Unable to determine - parsing error"],
                "raw_response": response_text
            }