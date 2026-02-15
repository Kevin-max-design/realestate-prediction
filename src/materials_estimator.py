"""
Building Materials & Cost Estimator
====================================
Estimates construction materials and costs for building a house
in Bangalore based on BHK, square footage, and area type.

Uses standard construction rates for Bangalore (2024-2025).
"""

from typing import Dict, List


# Bangalore construction material rates (INR)
# Based on average market rates in Bangalore metro area
MATERIAL_RATES = {
    "cement": {
        "unit": "bags (50kg)",
        "rate": 400,           # ₹400 per bag
        "per_sqft": 0.4,       # bags per sqft
        "icon": "🧱",
    },
    "steel": {
        "unit": "kg",
        "rate": 75,            # ₹75 per kg
        "per_sqft": 4.5,       # kg per sqft
        "icon": "🔩",
    },
    "bricks": {
        "unit": "pieces",
        "rate": 10,            # ₹10 per brick
        "per_sqft": 8,         # bricks per sqft
        "icon": "🧱",
    },
    "sand": {
        "unit": "cubic ft",
        "rate": 55,            # ₹55 per cubic ft
        "per_sqft": 1.25,      # cubic ft per sqft
        "icon": "⏳",
    },
    "aggregate": {
        "unit": "cubic ft",
        "rate": 45,            # ₹45 per cubic ft
        "per_sqft": 0.65,      # cubic ft per sqft
        "icon": "🪨",
    },
    "flooring": {
        "unit": "sq.ft",
        "rate": 85,            # ₹85 per sqft (vitrified tiles avg)
        "per_sqft": 1.0,
        "icon": "🏗️",
    },
    "plumbing": {
        "unit": "lumpsum/sqft",
        "rate": 120,           # ₹120 per sqft
        "per_sqft": 1.0,
        "icon": "🚿",
    },
    "electrical": {
        "unit": "lumpsum/sqft",
        "rate": 100,           # ₹100 per sqft
        "per_sqft": 1.0,
        "icon": "⚡",
    },
    "painting": {
        "unit": "sq.ft",
        "rate": 25,            # ₹25 per sqft
        "per_sqft": 2.5,       # wall area ~2.5x floor area
        "icon": "🎨",
    },
    "windows_doors": {
        "unit": "lumpsum/sqft",
        "rate": 150,           # ₹150 per sqft
        "per_sqft": 1.0,
        "icon": "🪟",
    },
    "labour": {
        "unit": "lumpsum/sqft",
        "rate": 350,           # ₹350 per sqft
        "per_sqft": 1.0,
        "icon": "👷",
    },
}

# BHK multipliers (larger homes need slightly more per sqft for rooms/walls)
BHK_MULTIPLIER = {
    1: 0.90,
    2: 0.95,
    3: 1.00,
    4: 1.05,
    5: 1.10,
    6: 1.15,
}

# Area type adjustments
AREA_TYPE_MULTIPLIER = {
    "Super built-up Area": 1.10,   # Higher quality finishes
    "Built-up Area": 1.00,
    "Plot Area": 0.95,
    "Carpet Area": 0.90,
}


def estimate_materials(total_sqft: float, bhk: int, area_type: str = "Super built-up Area") -> Dict:
    """
    Estimate building materials and costs for a house in Bangalore.

    Args:
        total_sqft: Total area in square feet
        bhk: Number of bedrooms (1-6+)
        area_type: Type of area measurement

    Returns:
        Dictionary with materials breakdown and total cost
    """
    bhk_mult = BHK_MULTIPLIER.get(min(bhk, 6), 1.0)
    area_mult = AREA_TYPE_MULTIPLIER.get(area_type, 1.0)
    combined_mult = bhk_mult * area_mult

    materials = []
    total_cost = 0

    for name, info in MATERIAL_RATES.items():
        quantity = round(info["per_sqft"] * total_sqft * combined_mult, 1)
        cost = round(quantity * info["rate"])
        total_cost += cost

        materials.append({
            "name": name.replace("_", " ").title(),
            "icon": info["icon"],
            "quantity": quantity,
            "unit": info["unit"],
            "rate": info["rate"],
            "cost": cost,
            "cost_formatted": format_inr(cost),
        })

    # Sort by cost (highest first)
    materials.sort(key=lambda x: x["cost"], reverse=True)

    return {
        "total_sqft": total_sqft,
        "bhk": bhk,
        "area_type": area_type,
        "materials": materials,
        "total_cost": total_cost,
        "total_cost_formatted": format_inr(total_cost),
        "cost_per_sqft": round(total_cost / total_sqft, 2),
        "cost_per_sqft_formatted": format_inr(round(total_cost / total_sqft, 2)),
    }


def format_inr(amount: float) -> str:
    """Format amount in Indian Rupee notation."""
    if amount >= 10000000:  # 1 Crore
        return f"₹{amount / 10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"₹{amount / 100000:.2f} Lakhs"
    elif amount >= 1000:
        return f"₹{amount:,.0f}"
    else:
        return f"₹{amount:.0f}"


if __name__ == "__main__":
    # Test
    result = estimate_materials(1500, 3, "Super built-up Area")
    print(f"Materials for 1500 sqft, 3 BHK:")
    print(f"{'Material':<20} {'Qty':>10} {'Unit':<15} {'Cost':>12}")
    print("-" * 60)
    for m in result["materials"]:
        print(f"{m['icon']} {m['name']:<17} {m['quantity']:>10} {m['unit']:<15} {m['cost_formatted']:>12}")
    print("-" * 60)
    print(f"{'TOTAL':<33} {'':15} {result['total_cost_formatted']:>12}")
    print(f"Cost per sqft: {result['cost_per_sqft_formatted']}")
