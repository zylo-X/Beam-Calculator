import json

class MaterialDatabase:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.materials = json.load(file)

    def search_by_property(self, property_name, min_value=0, max_value=float('inf')):
        """Search materials by property within min and max limits."""
        results = [
            material for material in self.materials
            if property_name in material and min_value <= material[property_name] <= max_value
        ]
        return results

    def list_all_materials(self):
        """List all material names."""
        return [material["Material"] for material in self.materials]

    def print_materials(self, materials_list):
        """Nicely print materials from a given list."""
        for material in materials_list:
            print(f"- {material['Material']}:")
            for key, value in material.items():
                if key != "Material":
                    print(f"   {key}: {value}")
            print()