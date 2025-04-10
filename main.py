# Exact probabilities for each dice roll (excluding the robber effect)
dice_probabilities = {
    2: 1/36,
    3: 2/36,
    4: 3/36,
    5: 4/36,
    6: 5/36,
    7: 0,     # production is blocked by the robber
    8: 5/36,
    9: 4/36,
    10: 3/36,
    11: 2/36,
    12: 1/36
}

# OR if you just want pips (1 for 2/12, 2 for 3/11, ... 5 for 6/8)
"""
dice_pips = {
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 0,  # robber
    8: 5,
    9: 4,
    10: 3,
    11: 2,
    12: 1
}
"""


# Example: we define each tile with an ID, resource, and dice number.
resource_list = ["Wood","Brick","Sheep","Wheat","Ore"]
tiles = {
    11: {"resource": "Sheep", "roll": 10},
    12: {"resource": "Wheat", "roll": 6},
    13: {"resource": "Brick", "roll": 4},
    21: {"resource": "Sheep", "roll": 11},
    22: {"resource": "Wheat", "roll": 9},
    23: {"resource": "Brick", "roll": 5},
    24: {"resource": "Sheep", "roll": 12},
    31: {"resource": "Wheat", "roll": 10},
    32: {"resource": "Brick", "roll": 8},
    33: {"resource": "Sheep", "roll": 2},
    34: {"resource": "Wheat", "roll": 5},
    35: {"resource": "Brick", "roll": 3},
    41: {"resource": "Sheep", "roll": 11},
    42: {"resource": "Wheat", "roll": 3},
    43: {"resource": "Brick", "roll": 6},
    44: {"resource": "Sheep", "roll": 9},
    51: {"resource": "Wheat", "roll": 7},
    52: {"resource": "Brick", "roll": 4},
    53: {"resource": "Brick", "roll": 8}   
}

resources = [
    "Wood", "Wood", "Wood", "Wood",
    "Sheep", "Sheep", "Sheep", "Sheep",
    "Wheat", "Wheat", "Wheat", "Wheat",
    "Brick", "Brick", "Brick",
    "Ore", "Ore", "Ore",
    "Desert"
]
standard_distribution = [4,11,12,8,3,6,9,5,10,11,5,7,2,9,4,10,6,3,8]
tile_ids_in_order = sorted(tiles.keys())  # [11, 12, 13, 21, 22, 23, 24, 31, ...]

for i, tile_id in enumerate(tile_ids_in_order):
    tiles[tile_id]["roll"] = standard_distribution[i]
# Next, define the intersections. Each intersection references the tile IDs that touch it.
# For simplicity, here’s a tiny example with just a few intersections:
intersections = {
    "s_11_21_22":[11,21,22],
    "s_11_12_22":[11,12,22],
    "s_12_22_23":[12,22,23],
    "s_12_13_23":[12,13,23],    
    "s_13_23_24":[13,23,24],

    "s_21_31_32":[21,31,32],
    "s_21_22_32":[21,22,32],
    "s_22_32_33":[22,32,33],
    "s_22_23_33":[22,23,33],
    "s_23_33_34":[23,33,34],
    "s_23_24_34":[23,24,34],
    "s_24_34_35":[24,34,35],

    "s_41_31_32":[41,31,32],
    "s_41_42_32":[41,42,32],
    "s_42_32_33":[42,32,33],
    "s_42_43_33":[42,43,33],
    "s_43_33_34":[43,33,34],
    "s_43_44_34":[43,44,34],
    "s_44_34_35":[44,34,35],

    "s_41_42_51":[41,42,51],
    "s_51_52_42":[51,52,42],
    "s_52_42_43":[52,42,43],
    "s_52_53_43":[52,53,43],    
    "s_53_43_44":[43,43,44],

}

def calculate_intersection_value(
    intersections_dict, 
    tiles_dict, 
    dice_prob_dict
):
    """
    intersections_dict: dict of intersection_name -> list of tile_ids
    tiles_dict:         dict of tile_id -> { "resource": str, "roll": int }
    dice_prob_dict:     dict mapping dice roll (2..12) to probability
    Returns a dict: intersection_name -> total production value
    """
    intersection_values = {}

    for intersection_name, tile_ids in intersections_dict.items():
        total_value = 0.0
        for t_id in tile_ids:
            if t_id not in tiles_dict:
                continue
            dice_number = tiles_dict[t_id].get("roll")
            if dice_number not in dice_prob_dict:
                continue
            total_value += dice_prob_dict[dice_number]
        intersection_values[intersection_name] = total_value

    return intersection_values

def main():
    # 4. Calculate the production values for each intersection
    intersection_values = calculate_intersection_value(
        intersections, 
        tiles, 
        dice_probabilities
    )

    # 5. Sort the results in descending order by probability
    sorted_intersections = sorted(
        intersection_values.items(), 
        key=lambda x: x[1], 
        reverse=True
    )

    # 6. Print out the results
    print("=== Intersection Production Probabilities (Sorted) ===")
    for name, val in sorted_intersections:
        print(f"Intersection {name}: {val:.3f}")

if __name__ == "__main__":
    main()