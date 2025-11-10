#!/usr/bin/env python3
"""
Item Catalog MCP Server
=======================

A Model Context Protocol server that provides access to item catalog information
through standardized tools that AI assistants can use.

Tools provided:
- check_item_menu_history: Check item menu history for a given MSID
- check_item_level_details: Get detailed item level information for a given MSID
- selection_insights: Analyze selection gaps for a store based on submarket performance
- price_insights: Compare item prices at a store against submarket average prices
- execute_sql_query: Execute a user-provided SQL query on Snowflake or Trino
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence
import os
import sys
from clients import SnowflakeClient, TrinoClient

# Add the parent directory to Python path to import clients and utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging first - write to local file
import tempfile
import os

# Try to write to current directory, fallback to temp directory if not writable
# Allow environment variable override
log_file_path = os.environ.get('MCP_LOG_FILE', 'mcp_server.log')

try:
    # Test if specified path is writable
    with open(log_file_path, 'a') as f:
        pass
except (OSError, PermissionError):
    # Fallback to temp directory
    temp_dir = tempfile.gettempdir()
    log_file_path = os.path.join(temp_dir, 'mcp_server.log')

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()  # Also log to console
    ]
)

# Create logger after configuration
logger = logging.getLogger(__name__)

# Log the log file location
logger.info(f"Logging to file: {log_file_path}")

# Try different import patterns for MCP
try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    import mcp.server.stdio
    import mcp.types as types
    MCP_IMPORT_STYLE = "new"
except ImportError:
    try:
        from mcp import server
        from mcp.server import Server, NotificationOptions
        from mcp.server.models import InitializationOptions
        import mcp.server.stdio
        import mcp.types as types
        MCP_IMPORT_STYLE = "alternative"
    except ImportError:
        # Fallback to basic MCP structure
        import mcp
        MCP_IMPORT_STYLE = "basic"
        types = None
        logger.error("Could not import MCP types - unsupported MCP version")


# Create the MCP server
if MCP_IMPORT_STYLE == "new":
    server = Server("item-catalog-mcp-server")
elif MCP_IMPORT_STYLE == "alternative":
    server = server.Server("item-catalog-mcp-server")
else:
    # Basic fallback - you might need to adjust this
    server = None
    logger.error("Could not create MCP server - unsupported MCP version")

data_sources = {
    ""
}

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools for checking item catalog information.
    """
    logger.info("Listing available tools")
    return [
        types.Tool(
            name="check_item_menu_history",
            description="Check item menu history for a given MSID (Merchant Supplied ID)",
            inputSchema={
                "type": "object",
                "properties": {
                    "msid": {
                        "type": "string",
                        "description": "Merchant Supplied ID (MSID) - required"
                    },
                    "store_id": {
                        "type": "string",
                        "description": "Store ID - optional filter"
                    },
                    "business_id": {
                        "type": "string",
                        "description": "Business ID - optional filter"
                    }
                },
                "required": ["msid"]
            }
        ),
        types.Tool(
            name="check_item_level_details",
            description="Get detailed item level information for a given MSID (Merchant Supplied ID)",
            inputSchema={
                "type": "object",
                "properties": {
                    "msid": {
                        "type": "string",
                        "description": "Merchant Supplied ID (MSID) - required"
                    },
                    "store_id": {
                        "type": "string",
                        "description": "Store ID - optional filter"
                    },
                    "business_id": {
                        "type": "string",
                        "description": "Business ID - optional filter"
                    }
                },
                "required": ["msid"]
            }
        ),
        types.Tool(
            name="selection_insights",
            description="Analyze selection gaps for a store by comparing its catalog against high-performing items in the same submarket and business vertical",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_id": {
                        "type": "string",
                        "description": "Store ID to analyze - required"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of top dd_sic items to analyze - defaults to 1000"
                    }
                },
                "required": ["store_id"]
            }
        ),
        types.Tool(
            name="price_insights",
            description="Compare item prices at a store against submarket average prices for the same dd_sic categories",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_id": {
                        "type": "string",
                        "description": "Store ID to analyze - required"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start timestamp in ISO format (e.g., '2024-01-01 00:00:00') - required"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End timestamp in ISO format (e.g., '2024-12-31 23:59:59') - required"
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of records to skip for pagination - defaults to 0"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of items to return - defaults to 100"
                    }
                },
                "required": ["store_id", "start_time", "end_time"]
            }
        ),
        types.Tool(
            name="execute_sql_query",
            description="Execute a user-provided SQL query on Snowflake or Trino database",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "The SQL query to execute - required"
                    },
                    "database_type": {
                        "type": "string",
                        "description": "Database type to use: 'snowflake' or 'trino' - defaults to 'snowflake'",
                        "enum": ["snowflake", "trino"]
                    },
                    "timeout_seconds": {
                        "type": "integer",
                        "description": "Query timeout in seconds - defaults to 300 (5 minutes)"
                    },
                    "max_rows": {
                        "type": "integer",
                        "description": "Maximum number of rows to return - defaults to 100"
                    }
                },
                "required": ["sql_query"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any]
) -> List[types.TextContent]:
    """
    Handle tool calls for item catalog operations.
    """
    logger.info(f"Tool call received: {name} with arguments: {arguments}")
    try:
        if name == "check_item_menu_history":
            return await check_item_menu_history_tool(arguments)
        elif name == "check_item_level_details":
            return await check_item_level_details_tool(arguments)
        elif name == "selection_insights":
            return await selection_insights_tool(arguments)
        elif name == "price_insights":
            return await price_insights_tool(arguments)
        elif name == "execute_sql_query":
            return await execute_sql_query_tool(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def check_item_menu_history_tool(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Check item menu history for a given MSID."""
    msid = arguments.get("msid")
    store_id = arguments.get("store_id")
    business_id = arguments.get("business_id")
    
    if not msid:
        return [types.TextContent(type="text", text="Error: msid parameter is required")]
    
    try:
        # Load the SQL query template
        sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "queries", "snowflake", "item_menu_history.sql")
        
        if not os.path.exists(sql_file_path):
            return [types.TextContent(type="text", text=f"Error: SQL file not found at {sql_file_path}")]
        
        with open(sql_file_path, 'r') as f:
            sql_template = f.read()
        
        # Replace placeholders with actual values
        sql_query = sql_template.replace("{{search_item_msid}}", msid)
        
        # Add optional filters if provided
        if store_id:
            sql_query = sql_query.replace("-- PLACEHOLDER FOR BUSINESS_ID FILTER --", 
                                        f"and ds.store_id = '{store_id}'")
        
        if business_id:
            # Find the business_id filter line and uncomment/modify it
            if "BUSINESS_ID in ('11116009','979026','331358')" in sql_query:
                sql_query = sql_query.replace("BUSINESS_ID in ('11116009','979026','331358')", 
                                            f"BUSINESS_ID = '{business_id}'")
            else:
                # Add business_id filter if not present
                sql_query = sql_query.replace("-- case when m.business_vertical_id in (166,167)", 
                                            f"and ds.business_id = '{business_id}'")
        
        # Execute the query
        with SnowflakeClient() as client:
            results = client.execute_query(sql_query)
            
            # Format results for display
            if results:
                result_text = f"Item Menu History for MSID: {msid}\n"
                if store_id:
                    result_text += f"Store ID: {store_id}\n"
                if business_id:
                    result_text += f"Business ID: {business_id}\n"
                result_text += f"\nQuery returned {len(results)} rows:\n\n"
                
                # Show column headers
                if results:
                    columns = list(results[0].keys())
                    result_text += f"Columns: {', '.join(columns)}\n\n"
                    
                    # Show first 10 rows
                    for i, row in enumerate(results[:10], 1):
                        result_text += f"Row {i}:\n"
                        for key, value in row.items():
                            result_text += f"  {key}: {value}\n"
                        result_text += "\n"
                    
                    if len(results) > 10:
                        result_text += f"... and {len(results) - 10} more rows\n"
            else:
                result_text = f"No menu history found for MSID: {msid}"
            
            logger.info(f"Item menu history query completed for MSID: {msid}, returned {len(results) if results else 0} rows")
            
            return [types.TextContent(type="text", text=result_text)]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Failed to check item menu history: {str(e)}")]


async def check_item_level_details_tool(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Get detailed item level information for a given MSID."""
    msid = arguments.get("msid")
    store_id = arguments.get("store_id")
    business_id = arguments.get("business_id")
    
    if not msid:
        return [types.TextContent(type="text", text="Error: msid parameter is required")]
    
    try:
        # Load the SQL query template
        sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "queries", "snowflake", "item_level_details_of_catalog_attributes.sql")
        
        if not os.path.exists(sql_file_path):
            return [types.TextContent(type="text", text=f"Error: SQL file not found at {sql_file_path}")]
        
        with open(sql_file_path, 'r') as f:
            sql_template = f.read()
        
        # Replace placeholders with actual values
        sql_query = sql_template.replace("{{search_item_msid}}", msid)
        
        # Add optional filters if provided
        if store_id:
            # Add store_id filter to the query
            sql_query += f"\n   and STORE_ID = '{store_id}'"
        
        if business_id:
            # Add business_id filter to the query
            sql_query += f"\n   and DD_BUSINESS_ID = '{business_id}'"
        
        # Execute the query
        with SnowflakeClient() as client:
            results = client.execute_query(sql_query)
            
            # Format results for display
            if results:
                result_text = f"Item Level Details for MSID: {msid}\n"
                if store_id:
                    result_text += f"Store ID: {store_id}\n"
                if business_id:
                    result_text += f"Business ID: {business_id}\n"
                result_text += f"\nQuery returned {len(results)} rows:\n\n"
                
                # Show column headers
                if results:
                    columns = list(results[0].keys())
                    result_text += f"Columns: {', '.join(columns)}\n\n"
                    
                    # Show first 10 rows
                    for i, row in enumerate(results[:10], 1):
                        result_text += f"Row {i}:\n"
                        for key, value in row.items():
                            result_text += f"  {key}: {value}\n"
                        result_text += "\n"
                    
                    if len(results) > 10:
                        result_text += f"... and {len(results) - 10} more rows\n"
            else:
                result_text = f"No item details found for MSID: {msid}"
            
            logger.info(f"Item level details query completed for MSID: {msid}, returned {len(results) if results else 0} rows")
            
            return [types.TextContent(type="text", text=result_text)]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Failed to get item level details: {str(e)}")]


async def selection_insights_tool(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Analyze selection gaps for a store based on submarket performance."""
    store_id = arguments.get("store_id")
    limit = arguments.get("limit", 1000)
    
    if not store_id:
        return [types.TextContent(type="text", text="Error: store_id parameter is required")]
    
    try:
        # Load the SQL query template
        sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "queries", "snowflake", "selection_insights.sql")
        
        if not os.path.exists(sql_file_path):
            return [types.TextContent(type="text", text=f"Error: SQL file not found at {sql_file_path}")]
        
        with open(sql_file_path, 'r') as f:
            sql_template = f.read()
        
        # Replace placeholders with actual values
        sql_query = sql_template.replace("{{input_store_id}}", str(store_id))
        sql_query = sql_query.replace("{{input_limit}}", str(limit))
        
        # Execute the query
        with SnowflakeClient() as client:
            results = client.execute_query(sql_query)
            
            # Format results for display
            if results:
                result_text = f"Selection Insights for Store ID: {store_id}\n"
                result_text += f"Top {limit} dd_sic items analyzed\n"
                result_text += f"\nQuery returned {len(results)} missing catalog items:\n\n"
                
                # Show column headers
                if results:
                    columns = list(results[0].keys())
                    result_text += f"Columns: {', '.join(columns)}\n\n"
                    
                    # Show first 20 rows for selection insights
                    for i, row in enumerate(results[:20], 1):
                        result_text += f"Row {i}:\n"
                        for key, value in row.items():
                            result_text += f"  {key}: {value}\n"
                        result_text += "\n"
                    
                    if len(results) > 20:
                        result_text += f"... and {len(results) - 20} more rows\n"
            else:
                result_text = f"No selection gaps found for Store ID: {store_id}\n"
                result_text += "This store already covers all top-performing items in its submarket."
            
            logger.info(f"Selection insights query completed for Store ID: {store_id}, returned {len(results) if results else 0} rows")
            
            return [types.TextContent(type="text", text=result_text)]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Failed to get selection insights: {str(e)}")]


async def price_insights_tool(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Compare item prices at a store against submarket average prices."""
    store_id = arguments.get("store_id")
    start_time = arguments.get("start_time")
    end_time = arguments.get("end_time")
    offset = arguments.get("offset", 0)
    limit = arguments.get("limit", 100)
    
    if not store_id:
        return [types.TextContent(type="text", text="Error: store_id parameter is required")]
    if not start_time:
        return [types.TextContent(type="text", text="Error: start_time parameter is required")]
    if not end_time:
        return [types.TextContent(type="text", text="Error: end_time parameter is required")]
    
    try:
        # Load the SQL query template
        sql_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "queries", "snowflake", "price_insights.sql")
        
        if not os.path.exists(sql_file_path):
            return [types.TextContent(type="text", text=f"Error: SQL file not found at {sql_file_path}")]
        
        with open(sql_file_path, 'r') as f:
            sql_template = f.read()
        
        # Replace placeholders with actual values (using :parameter syntax)
        sql_query = sql_template.replace(":storeId", str(store_id))
        sql_query = sql_query.replace(":startTimeStr", f"'{start_time}'")
        sql_query = sql_query.replace(":endTimeStr", f"'{end_time}'")
        sql_query = sql_query.replace(":offset", str(offset))
        sql_query = sql_query.replace(":limit", str(limit))
        
        # Execute the query
        with SnowflakeClient() as client:
            results = client.execute_query(sql_query)
            
            # Format results for display
            if results:
                result_text = f"Price Insights for Store ID: {store_id}\n"
                result_text += f"Time period: {start_time} to {end_time}\n"
                result_text += f"Offset: {offset}, Limit: {limit}\n"
                result_text += f"\nQuery returned {len(results)} items:\n\n"
                
                # Show column headers
                if results:
                    columns = list(results[0].keys())
                    result_text += f"Columns: {', '.join(columns)}\n\n"
                    
                    # Show all returned rows (since limit is already applied in query)
                    for i, row in enumerate(results, 1):
                        result_text += f"Row {i}:\n"
                        for key, value in row.items():
                            result_text += f"  {key}: {value}\n"
                        result_text += "\n"
            else:
                result_text = f"No price comparison data found for Store ID: {store_id}\n"
                result_text += f"Time period: {start_time} to {end_time}"
            
            logger.info(f"Price insights query completed for Store ID: {store_id}, returned {len(results) if results else 0} rows")
            
            return [types.TextContent(type="text", text=result_text)]
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Failed to get price insights: {str(e)}")]


async def execute_sql_query_tool(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Execute a user-provided SQL query on Snowflake or Trino database."""
    sql_query = arguments.get("sql_query")
    database_type = arguments.get("database_type", "snowflake").lower()
    timeout_seconds = arguments.get("timeout_seconds", 300)
    max_rows = arguments.get("max_rows", 100)
    
    if not sql_query:
        return [types.TextContent(type="text", text="Error: sql_query parameter is required")]
    
    if database_type not in ["snowflake", "trino"]:
        return [types.TextContent(type="text", text="Error: database_type must be 'snowflake' or 'trino'")]
    
    try:
        # Execute the query based on database type
        logger.info(f"Executing SQL query on {database_type}: {sql_query[:100]}...")
        if database_type == "snowflake":
            with SnowflakeClient() as client:
                if timeout_seconds != 300:
                    results = client.execute_query_with_timeout(sql_query, timeout_seconds)
                else:
                    results = client.execute_query(sql_query)
        else:  # trino
            with TrinoClient() as client:
                if timeout_seconds != 300:
                    results = client.execute_query_with_timeout(sql_query, timeout_seconds)
                else:
                    results = client.execute_query(sql_query)
        
        # Format results for display
        if results:
            result_text = f"SQL Query executed successfully on {database_type.upper()}\n"
            result_text += f"Query: {sql_query}\n"
            result_text += f"Timeout: {timeout_seconds} seconds\n"
            result_text += f"Query returned {len(results)} rows:\n\n"
            
            logger.info(f"SQL query executed successfully on {database_type}, returned {len(results)} rows")
            
            # Show column headers
            if results:
                columns = list(results[0].keys())
                result_text += f"Columns: {', '.join(columns)}\n\n"
                
                # Show rows up to max_rows
                display_rows = min(len(results), max_rows)
                for i, row in enumerate(results[:display_rows], 1):
                    result_text += f"Row {i}:\n"
                    for key, value in row.items():
                        # Truncate long values for display
                        display_value = str(value)
                        if len(display_value) > 100:
                            display_value = display_value[:97] + "..."
                        result_text += f"  {key}: {display_value}\n"
                    result_text += "\n"
                
                if len(results) > max_rows:
                    result_text += f"... and {len(results) - max_rows} more rows (truncated at {max_rows})\n"
        else:
            result_text = f"Query executed successfully on {database_type.upper()}, but returned no results\n"
            result_text += f"Query: {sql_query}\n"
            
            logger.info(f"SQL query executed successfully on {database_type}, but returned no results")
        
        return [types.TextContent(type="text", text=result_text)]
    
    except Exception as e:
        error_msg = f"Failed to execute SQL query on {database_type.upper()}: {str(e)}\n"
        error_msg += f"Query: {sql_query}\n"
        
        logger.error(f"SQL query execution failed on {database_type}: {str(e)}")
        
        # Add troubleshooting tips based on database type
        if database_type == "snowflake":
            error_msg += "\nTroubleshooting tips for Snowflake:\n"
            error_msg += "1. Ensure you're connected to DoorDash VPN\n"
            error_msg += "2. Verify SSO authentication is working\n"
            error_msg += "3. Check if the required tables exist\n"
            error_msg += "4. Verify you have permissions to access the tables\n"
        else:  # trino
            error_msg += "\nTroubleshooting tips for Trino:\n"
            error_msg += "1. Ensure you're connected to DoorDash VPN\n"
            error_msg += "2. Verify OAuth2 authentication is working\n"
            error_msg += "3. Check if the required catalogs/schemas exist\n"
            error_msg += "4. Verify you have permissions to access the data\n"
        
        return [types.TextContent(type="text", text=error_msg)]


async def main():
    """Main function to run the MCP server."""
    logger.info("Starting MCP server...")
    # Run the server using stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("MCP server started successfully")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="item-catalog-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main()) 