#!/usr/bin/env python3
"""
Connection Verification Utilities
"""

import sys


def verify_prod_connection():
    """Verify that the user has connected to the production environment"""
    print("\n" + "=" * 80)
    print("⚠️  PRODUCTION ENVIRONMENT CONNECTION REQUIRED")
    print("=" * 80)
    print("\nBefore proceeding, ensure you have connected to the production cluster.")
    print("\nRun the following command:")
    print("  dd-toolbox connect-to-cluster run main-00.prod-us-west-2")
    print("\n" + "-" * 80)
    
    while True:
        response = input("\nHave you connected to the production environment? (y/n): ").strip().lower()
        
        if response == 'y':
            print("\n✓ Proceeding with the operation...\n")
            return True
        elif response == 'n':
            print("\n❌ Please connect to the production environment first and try again.")
            print("   Run: dd-toolbox connect-to-cluster run main-00.prod-us-west-2\n")
            sys.exit(1)
        else:
            print("⚠️  Invalid input. Please type 'y' (yes) or 'n' (no).")

