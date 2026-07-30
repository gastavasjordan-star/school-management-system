#!/usr/bin/env python3
"""
School Manager - Feature Demo Script
Demonstrates the Super Admin feature control system
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(text):
    """Print a section header"""
    print(f"\n▶ {text}")
    print("-" * 50)


def demo_feature_registry():
    """Demonstrate the feature registry"""
    print_header("FEATURE REGISTRY")
    
    from school_manager.models.features import FeatureRegistry
    
    features = FeatureRegistry.get_all_features()
    
    print(f"\nTotal Features: {len(features)}")
    
    # Group by category
    categories = FeatureRegistry.get_features_by_category()
    
    for cat_id, cat_features in categories.items():
        cat_name = FeatureRegistry.get_category_display_name(cat_id)
        print(f"\n{cat_name}: {len(cat_features)} features")
        
        for feat in cat_features:
            tier = feat.get('default_tier', 'core')
            tier_str = "Always" if tier is None else tier.upper()
            print(f"  {feat['icon']} {feat['name']:30} [{tier_str:10}]")


def demo_subscription_tiers():
    """Demonstrate subscription tiers"""
    print_header("SUBSCRIPTION TIERS")
    
    from school_manager.utils.licensing import SubscriptionPlan
    
    tiers = SubscriptionPlan.get_all_tiers()
    
    for tier in tiers:
        plan = SubscriptionPlan.get_plan_features(tier)
        display = SubscriptionPlan.get_tier_display_name(tier)
        
        print(f"\n{display}")
        print(f"  Price: ${plan['price_monthly']}/month or ${plan['price_annual']}/year")
        print(f"  Students: {plan['max_students']}")
        print(f"  Staff: {plan['max_staff']}")
        print(f"  Classes: {plan['max_classes']}")
        print(f"  Features included:")
        
        included_features = [k for k, v in plan['features'].items() if v]
        for feat in included_features[:5]:
            print(f"    ✓ {feat.replace('_', ' ').title()}")
        if len(included_features) > 5:
            print(f"    ... and {len(included_features) - 5} more")


def demo_license_generation():
    """Demonstrate license generation"""
    print_header("LICENSE KEY GENERATION")
    
    from school_manager.utils.licensing import LicenseKeyGenerator, SubscriptionPlan
    
    generator = LicenseKeyGenerator()
    
    # Generate a Gold tier license
    print("\nGenerating Gold tier license...")
    
    key, data = generator.generate(
        client_name="Bright Future Academy",
        tier=SubscriptionPlan.TIER_GOLD,
        expiry_date=datetime.now() + timedelta(days=365),
        terms=3,
        max_students=2000,
        max_staff=150,
        max_classes=50
    )
    
    print(f"\n  Client: {data['client_name']}")
    print(f"  Tier: {data['tier'].upper()}")
    print(f"  Students: {data['max_students']}")
    print(f"  Staff: {data['max_staff']}")
    print(f"  Classes: {data['max_classes']}")
    print(f"  Expiry: {data['expiry']}")
    print(f"\n  License Key:")
    print(f"  {key[:64]}...")
    
    # Generate a Bronze license
    print("\n" + "-" * 50)
    print("\nGenerating Bronze tier license...")
    
    bronze_key, bronze_data = generator.generate(
        client_name="Small Town School",
        tier=SubscriptionPlan.TIER_BRONZE,
        expiry_date=datetime.now() + timedelta(days=30),
        terms=1,
        max_students=50,
        max_staff=10,
        max_classes=3
    )
    
    print(f"\n  Client: {bronze_data['client_name']}")
    print(f"  Tier: {bronze_data['tier'].upper()}")
    print(f"  Features included:")
    
    for feat, enabled in bronze_data['features'].items():
        if enabled:
            print(f"    ✓ {feat.replace('_', ' ').title()}")


def demo_feature_access():
    """Demonstrate feature access checking"""
    print_header("FEATURE ACCESS CONTROL")
    
    from school_manager.models.features import FeatureRegistry, FeatureManager
    from school_manager.utils.licensing import SubscriptionPlan
    from school_manager.models.database import init_database, get_session, School, License
    from school_manager.utils.hardware import HardwareFingerprint
    
    # Initialize database
    db_path = 'demo_features.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    engine = init_database(db_path)
    session = get_session(engine)
    
    # Create demo school
    school = School(name="Demo School")
    session.add(school)
    session.commit()
    school_id = school.id
    
    # Create demo license (Gold tier)
    machine_id = HardwareFingerprint.get_machine_id()
    license = License(
        license_key="DEMO-KEY",
        machine_id=machine_id,
        client_name="Demo School",
        tier='gold',
        max_students=2000,
        max_staff=150,
        max_classes=50,
        terms_included=3,
        is_active=True,
        expiry_date=datetime.now() + timedelta(days=365)
    )
    session.add(license)
    session.commit()
    
    # Create feature manager
    manager = FeatureManager(session, school_id)
    
    # Show tier defaults
    print("\nGold Tier Default Features:")
    gold_features = manager.get_tier_defaults('gold')
    print(f"  Total: {len(gold_features)} features enabled by default")
    
    # Show Bronze tier defaults for comparison
    print("\nBronze Tier Default Features:")
    bronze_features = manager.get_tier_defaults('bronze')
    print(f"  Total: {len(bronze_features)} features enabled by default")
    
    # Disable some features for this school
    print("\n" + "-" * 50)
    print("\nSuper Admin disables some features for Demo School:")
    
    features_to_disable = [
        'premium_hostel',
        'premium_transport',
        'premium_canteen',
        'analytics_predictions'
    ]
    
    for feat in features_to_disable:
        manager.disable_feature(school_id, feat)
        feat_data = FeatureRegistry.get_all_features().get(feat, {})
        print(f"  ✗ {feat_data.get('icon', '📦')} {feat_data.get('name', feat)}")
    
    # Check feature access
    print("\n" + "-" * 50)
    print("\nFeature Access Check:")
    
    test_features = [
        'portal_parent',
        'premium_hostel',
        'integration_id_cards',
        'analytics_predictions',
        'core_students'
    ]
    
    for feat in test_features:
        enabled = manager.is_feature_enabled(school_id, feat)
        feat_data = FeatureRegistry.get_all_features().get(feat, {})
        status = "✓ ENABLED" if enabled else "✗ DISABLED"
        print(f"  {status:15} {feat_data.get('icon', '📦'):3} {feat_data.get('name', feat)}")
    
    # Final feature count
    final_features = manager.get_school_features(school_id)
    print(f"\nFinal enabled features: {len(final_features)}")
    
    # Cleanup
    session.close()
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("\n✓ Demo database cleaned up")


def demo_middleware():
    """Demonstrate the middleware decorator"""
    print_header("FEATURE ACCESS MIDDLEWARE")
    
    from school_manager.utils.middleware import (
        require_feature, 
        get_required_feature, 
        FEATURE_MODULES
    )
    
    print("\nModule to Feature Mapping:")
    print("-" * 50)
    
    for module, feature in FEATURE_MODULES.items():
        print(f"  {module:25} → {feature}")
    
    print(f"\nTotal module-feature mappings: {len(FEATURE_MODULES)}")


def demo_super_admin_control():
    """Demonstrate Super Admin control scenarios"""
    print_header("SUPER ADMIN CONTROL SCENARIOS")
    
    scenarios = [
        {
            "title": "🏫 New School Onboarding",
            "description": "Start with Bronze, upgrade as they grow",
            "actions": [
                "Enable Bronze tier features only",
                "Lock premium features (hostel, transport)",
                "Enable student photos after payment",
                "Set 50 student limit"
            ]
        },
        {
            "title": "💰 Pay-Per-Feature Model",
            "description": "Charge extra for add-ons",
            "actions": [
                "Enable core features by default",
                "Charge $20/month for Parent Portal",
                "Charge $30/month for SMS",
                "Charge $50/month for Analytics"
            ]
        },
        {
            "title": "🎓 School Network",
            "description": "Multi-branch management",
            "actions": [
                "All branches share analytics",
                "Centralized ID card template",
                "Branch-specific fee structures",
                "Network-wide announcements"
            ]
        },
        {
            "title": "⚡ Feature Gating",
            "description": "A/B testing new features",
            "actions": [
                "Enable for 10% of schools",
                "Collect feedback",
                "Monitor usage",
                "Roll out to all"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['title']}")
        print(f"  {scenario['description']}")
        print("  Actions:")
        for action in scenario['actions']:
            print(f"    → {action}")


def demo_pricing_strategies():
    """Demonstrate pricing strategies"""
    print_header("MONETIZATION STRATEGIES")
    
    strategies = [
        {
            "name": "📊 Per-Student Pricing",
            "description": "Most common in EdTech",
            "example": "5,000 students × $2/month = $10,000/month",
            "pros": ["Predictable revenue", "Scales with school"],
            "cons": ["Complex billing", "Churn risk"]
        },
        {
            "name": "🏆 Tiered Plans",
            "description": "Bronze/Silver/Gold/Platinum",
            "example": "$49 → $149 → $299 → $499/month",
            "pros": ["Simple", "Upsell opportunity"],
            "cons": ["Feature ceiling", "May over/undersell"]
        },
        {
            "name": "🎯 Pay-Per-Feature",
            "description": "Each feature has price",
            "example": "Portal $20, SMS $30, Analytics $50",
            "pros": ["Max revenue", "Pay for what you use"],
            "cons": ["Complex", "Hard to manage"]
        },
        {
            "name": "📅 Annual Commitment",
            "description": "Discount for annual",
            "example": "2 months free = 14% discount",
            "pros": ["Cash flow", "Retention"],
            "cons": ["Price anchoring", "Refund complexity"]
        },
        {
            "name": "🤝 Institutional Deals",
            "description": "Custom contracts",
            "example": "County schools: $50,000/year",
            "pros": ["Large deals", "Stability"],
            "cons": ["Negotiation time", "Support overhead"]
        }
    ]
    
    for strategy in strategies:
        print(f"\n{strategy['name']}")
        print(f"  {strategy['description']}")
        print(f"  Example: {strategy['example']}")
        print(f"  ✓ Pros: {', '.join(strategy['pros'])}")
        print(f"  ✗ Cons: {', '.join(strategy['cons'])}")


def main():
    """Run all demos"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║       🏫 SCHOOL MANAGER - FEATURE CONTROL DEMO 🏫              ║
    ║                                                                  ║
    ║    Super Admin Feature Management & Subscription Licensing       ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    demo_feature_registry()
    demo_subscription_tiers()
    demo_license_generation()
    demo_feature_access()
    demo_middleware()
    demo_super_admin_control()
    demo_pricing_strategies()
    
    print("\n" + "=" * 70)
    print("  DEMO COMPLETE!")
    print("=" * 70)
    print("""
    To run the actual application:
    
    1. Install dependencies:
       pip install -r requirements.txt
    
    2. Run the application:
       python school_manager/app.py
    
    3. Login as Super Admin:
       Username: Jordan
       Password: admin123
    
    4. Go to Settings → Feature Control to manage features
    """)


if __name__ == '__main__':
    main()
