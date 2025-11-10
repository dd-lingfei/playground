import json
from clients.openai_client import OpenAIClient
from clients.dd_selection_qdrant_client import DDSelectionQdrantClient

# Initialize clients
openai_client = OpenAIClient()
qdrant_client = DDSelectionQdrantClient()

# Example results
products_data = json.loads('''{
  "image_quality_assessment": {
    "viewing_angle": "front",
    "zoom_balance": "appropriate",
    "focus_relevance": "meat and tags predominant",
    "reflections": "minor, meats and tags legible"
  },
  "products": [
    {
      "product_name": "Blue Cheese Herb Butter",
      "type": "butter compound",
      "price": "0.99 $/each",
      "bounding_box": [0.00, 0.50, 0.35, 1.00],
      "anchor_point": [0.17, 0.75]
    },
    {
      "product_name": "Beef Oxtail",
      "type": "oxtail",
      "price": "12.99 $/lb",
      "bounding_box": [0.45, 0.16, 0.60, 0.42],
      "anchor_point": [0.52, 0.29]
    },
    {
      "product_name": "Sirloin Steak (Prime)",
      "type": "sirloin steak",
      "price": "14.99 $/lb",
      "bounding_box": [0.65, 0.16, 1.00, 0.38],
      "anchor_point": [0.82, 0.27]
    },
    {
      "product_name": "Prime Choice Beef Ribeye Steak",
      "type": "ribeye steak",
      "price": "15.99 $/lb",
      "bounding_box": [0.30, 0.45, 1.00, 1.00],
      "anchor_point": [0.65, 0.75]
    }
  ]
}''')

# Extract product names from example results
actual_spouts_market_names = [x['product_name'] for x in products_data['products']]
embeddings = [openai_client.generate_embeddings([name])[0] for name in actual_spouts_market_names]
qdrant_results_list = [qdrant_client.query_points(
    collection_name="collection_gap_scraper_908006_safeway",
    query=this_embeddings,
    using='sentence_embedding',
) for this_embeddings in embeddings]

# print qdrant_results_list
print("qdrant_results_list:")
print(qdrant_results_list)
