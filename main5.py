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
    45: {"resource": "Sheep", "roll": 9},
    46: {"resource": "Sheep", "roll": 9},
    51: {"resource": "Wheat", "roll": 7},
    52: {"resource": "Brick", "roll": 4},
    53: {"resource": "Brick", "roll": 8},
    54: {"resource": "Sheep", "roll": 9},
    55: {"resource": "Sheep", "roll": 9},   
    61: {"resource": "Sheep", "roll": 9},
    62: {"resource": "Sheep", "roll": 9},
    63: {"resource": "Sheep", "roll": 9},
    64: {"resource": "Sheep", "roll": 9},
    71: {"resource": "Sheep", "roll": 9},
    72: {"resource": "Sheep", "roll": 9},
    73: {"resource": "Sheep", "roll": 9},
}

resources = [
    "Wood", "Wood", "Wood", "Wood",
    "Sheep", "Sheep", "Sheep", "Sheep",
    "Wheat", "Wheat", "Wheat", "Wheat",
    "Brick", "Brick", "Brick",
    "Ore", "Ore", "Ore",
    "Desert"
]
standard_distribution = [4,5,2,6,10,8,4,3,11,12,9,8,9,12,3,6,5,7,8,10,2,9,3,11,5,4,7,11,10,6]
tile_ids_in_order = sorted(tiles.keys())  # [11, 12, 13, 21, 22, 23, 24, 31, ...]

for i, tile_id in enumerate(tile_ids_in_order):
    tiles[tile_id]["roll"] = standard_distribution[i]
# Next, define the intersections. Each intersection references the tile IDs that touch it.
# For simplicity, here’s a tiny example with just a few intersections:
intersections = {
    #first
    "s_11_21_22":[11,21,22],
    "s_11_12_22":[11,12,22],
    "s_12_22_23":[12,22,23],
    "s_12_13_23":[12,13,23],    
    "s_13_23_24":[13,23,24],
    #second
    "s_21_31_32":[21,31,32],
    "s_21_22_32":[21,22,32],
    "s_22_32_33":[22,32,33],
    "s_22_23_33":[22,23,33],
    "s_23_33_34":[23,33,34],
    "s_23_24_34":[23,24,34],
    "s_24_34_35":[24,34,35],
    #third
    "s_31_41_42":[31,41,42],
    "s_31_32_42":[31,32,42],
    "s_32_42_43":[43,42,43],
    "s_32_33_43":[32,33,43],
    "s_33_43_44":[33,43,44],
    "s_33_34_44":[33,34,44],
    "s_34_44_45":[34,44,45],
    "s_34_35_45":[34,35,45],    
    "s_35_45_46":[35,45,46],
    #fouth
    "s_51_41_42":[51,41,42],
    "s_51_52_42":[51,52,42],
    "s_52_42_43":[52,42,43],
    "s_52_53_43":[52,53,43],
    "s_53_43_44":[53,43,44],
    "s_53_54_44":[53,54,44],
    "s_54_44_45":[54,44,45],
    "s_54_55_45":[54,55,45],    
    "s_55_45_46":[55,45,46],
    #fifth
    "s_61_51_52":[61,51,52],
    "s_61_62_52":[61,62,52],
    "s_62_52_53":[62,52,53],
    "s_62_63_53":[62,63,53],
    "s_63_53_54":[63,53,54],
    "s_63_64_54":[63,64,54],
    "s_64_54_55":[64,54,55],
    #sixth
    "s_61_62_71":[61,62,71],
    "s_71_72_62":[71,72,62],
    "s_72_62_63":[72,62,63],
    "s_72_73_63":[72,73,63],    
    "s_73_63_64":[73,63,64],

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