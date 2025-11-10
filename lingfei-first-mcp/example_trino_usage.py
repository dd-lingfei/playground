#!/usr/bin/env python3
"""
Example usage of the Trino Client
=================================

This script demonstrates how to use the TrinoClient class for common database operations.
"""

from clients.trino_client import TrinoClient


def example_basic_connection():
    """Example of basic connection and simple query."""
    print("🔗 Example: Basic Connection and Query")
    print("-" * 40)
    
    try:
        with TrinoClient() as trino:
            # Simple query
            results = trino.execute_query("SELECT current_user, current_timestamp")
            
            if results:
                user = results[0].get('current_user', 'Unknown')
                timestamp = results[0].get('current_timestamp', 'Unknown')
                print(f"✅ Connected as: {user}")
                print(f"✅ Current time: {timestamp}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")


def example_explore_catalogs():
    """Example of exploring available catalogs and schemas."""
    print("\n📚 Example: Exploring Catalogs and Schemas")
    print("-" * 40)
    
    try:
        with TrinoClient() as trino:
            # Show available catalogs
            catalogs = trino.show_catalogs()
            print(f"📋 Available catalogs ({len(catalogs)}):")
            
            for i, catalog in enumerate(catalogs[:5], 1):  # Show first 5
                catalog_name = catalog.get('Catalog', 'Unknown')
                print(f"   {i}. {catalog_name}")
                
                # Try to show schemas for this catalog
                try:
                    schemas = trino.show_schemas(catalog_name)
                    schema_names = [sch.get('Schema', 'Unknown') for sch in schemas[:3]]
                    print(f"      Schemas: {', '.join(schema_names)}")
                except Exception as e:
                    print(f"      Cannot access schemas: {e}")
                    
    except Exception as e:
        print(f"❌ Catalog exploration failed: {e}")


def example_table_operations():
    """Example of table operations."""
    print("\n📊 Example: Table Operations")
    print("-" * 40)
    
    try:
        with TrinoClient() as trino:
            # Try to access a common catalog and schema
            try:
                # Show tables in iceberg.nv_item_selection if accessible
                tables = trino.show_tables("iceberg", "nv_item_selection")
                print(f"📋 Tables in iceberg.nv_item_selection ({len(tables)}):")
                
                for i, table in enumerate(tables[:5], 1):  # Show first 5
                    table_name = table.get('Table', 'Unknown')
                    print(f"   {i}. {table_name}")
                    
                    # Try to describe the table structure
                    try:
                        description = trino.describe_table(table_name, "iceberg", "nv_item_selection")
                        print(f"      Columns: {len(description)}")
                        for col in description[:3]:  # Show first 3 columns
                            col_name = col.get('Column', 'Unknown')
                            col_type = col.get('Type', 'Unknown')
                            print(f"        - {col_name}: {col_type}")
                    except Exception as e:
                        print(f"      Cannot describe table: {e}")
                        
            except Exception as e:
                print(f"⚠️  Cannot access iceberg.nv_item_selection: {e}")
                print("   This is expected if you don't have access to this schema")
                
    except Exception as e:
        print(f"❌ Table operations failed: {e}")


def example_custom_query():
    """Example of executing a custom query."""
    print("\n🔍 Example: Custom Query Execution")
    print("-" * 40)
    
    try:
        with TrinoClient() as trino:
            # Custom query - adjust based on available catalogs/schemas
            custom_query = """
            SELECT 
                current_user as user,
                current_timestamp as timestamp,
                node_id
            FROM system.runtime.nodes 
            LIMIT 1
            """
            
            results = trino.execute_query(custom_query)
            
            if results:
                print("✅ Custom query executed successfully:")
                for key, value in results[0].items():
                    print(f"   {key}: {value}")
            else:
                print("⚠️  Query returned no results")
                
    except Exception as e:
        print(f"❌ Custom query failed: {e}")


def example_diagnostics():
    """Example of running connection diagnostics."""
    print("\n🔧 Example: Connection Diagnostics")
    print("-" * 40)
    
    try:
        with TrinoClient() as trino:
            # Run comprehensive diagnostics
            trino.run_diagnostics()
            
    except Exception as e:
        print(f"❌ Diagnostics failed: {e}")


def main():
    """Main example function."""
    print("🚀 Trino Client Usage Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_connection()
    example_explore_catalogs()
    example_table_operations()
    example_custom_query()
    example_diagnostics()
    
    print("\n" + "=" * 50)
    print("✅ Examples completed!")
    print("\n💡 Tips:")
    print("- Ensure you're connected to DoorDash VPN")
    print("- The client uses OAuth2 authentication")
    print("- Some operations may fail due to permissions")
    print("- Check the output above for any errors")


if __name__ == "__main__":
    main() 