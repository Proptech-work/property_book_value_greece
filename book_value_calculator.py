import yaml
from pathlib import Path
from datetime import datetime



def calculate_book_value(property: dict, zone_price:int, coefficients: dict) -> float:
    if property['property_type'] == 'Διαμέρισμα':
        zone_price *= _calculate_apartment_coefficients(property, coefficients['apartment'])
    elif property['property_type'] == 'Μονοκατοικία':
        zone_price *= _calculate_house_coefficients(property, coefficients)
    
    return zone_price


def _calculate_house_coefficients(property: dict,  coefficients: dict) -> float:
    pass




def _calculate_apartment_special_factors(property: dict, coefficients: dict) -> float:
    special_factors = 1
    if 'conservation_status' in property and property["conservation_status"]:
        special_factors *= coefficients['special_factors']['conservation_status']
    if 'expropriate_status' in property and property['expropriate_status']:
        special_factors *= coefficients['special_factors']['expropriate_status']
    if 'outer_walls_width_above_50cm' in property and property['outer_walls_width_above_50cm']:
        special_factors *= coefficients['special_factors']['outer_walls_width_above_50cm']
    if 'tin_or_asbestos_roof' in property and property['tin_or_asbestos_roof']:
        special_factors *= coefficients['special_factors']['tin_or_asbestos_roof']
    if  property['heating']=='Χωρίς Θέρμανση':
        special_factors *= coefficients['special_factors']['no_central_heating']
    if property['elevator']==False and property['floor']>2:
        special_factors *= coefficients['special_factors']['no_elevator_above_second_floor']
    if 'multiple_ownership' in property and property['multiple_ownership']:
        special_factors *= coefficients['special_factors']['multiple_ownership']
        
            
    return special_factors
        


def _calculate_apartment_construction_meterial(property: dict, coefficients: dict) -> float:
    
    construction_coefficient = 1
    if 'construction_material' in property:
        if property['construction_material'] == 'brick_or_stone':
            construction_material_key = 'brick_or_stone'    
        elif property['construction_material'] == 'other_inferior':
            construction_material_key = 'other_inferior'
        else:
            construction_material_key = 'concrete'
        construction_coefficient *= coefficients['construction_material'][construction_material_key]

    return construction_coefficient

def _calculate_apartment_coefficients(property: dict,  coefficients: dict) -> float:
    coeffs = 1.0
    
    coeffs *= _calculate_apartment_face_factor(property, coefficients)
    coeffs *= _calculate_apartment_floor_factor(property, coefficients)
    coeffs *= _calculate_apartment_area_factor(property, coefficients)
    coeffs *= _calculate_apartment_age_factor(property, coefficients)
    coeffs *= _calculate_apartment_special_factors(property, coefficients)
    coeffs *= _calculate_apartment_construction_meterial(property, coefficients)
    
    return coeffs


def _calculate_apartment_face_factor(property: dict, coefficients: dict) -> float:
    face_factor_key = 'no_face'
    if property['road_facing']:
        face_factor_key = 'single_facing'
    elif property['corner_plot']:
        face_factor_key = 'multi_facing'
    return coefficients['face_factor'][face_factor_key]


def _calculate_apartment_floor_factor(property: dict, coefficients: dict) -> float:
    floor_factor_key = 'ground_floor'
    if property['floor'] == 1:
        floor_factor_key = 'first_floor'
    elif property['floor'] == 2:
        floor_factor_key = 'second_floor'
    elif property['floor'] == 3:
        floor_factor_key = 'third_floor'
    elif property['floor'] == 4:
        floor_factor_key = 'fourth_floor'
    elif property['floor'] == 5:
        floor_factor_key = 'fifth_floor'
    elif property['floor'] >= 6: 
        floor_factor_key = 'sixth_floor_and_above'
    elif property['floor'] < 0:    
        floor_factor_key = 'basement'
    return coefficients['floor_factor'][floor_factor_key]


def _calculate_apartment_area_factor(property: dict, coefficients: dict) -> float:
    area_factor_key = 'g_500'
    if property['area'] <= 25:
        area_factor_key = 'leq_25'
    elif property['area'] < 100:
        area_factor_key = 'g_25_leq_100'
    elif property['area'] < 200:
        area_factor_key = 'g_100_leq_200'
    elif property['area'] < 300:
        area_factor_key = 'g_200_leq_300'
    elif property['area'] < 500:
        area_factor_key = 'g_300_leq_500'
    return coefficients['area_factor'][area_factor_key]


def _calculate_apartment_age_factor(property: dict, coefficients: dict) -> float:
    year_now = datetime.now().year
    building_age = year_now - property['construction_year']
    
    age_factor_key = 'g_25'
    if building_age <= 1:
        age_factor_key = 'leq_1'
    elif building_age <= 5:
        age_factor_key = 'leq_5'
    elif building_age <= 10:
        age_factor_key = 'leq_10'
    elif building_age <= 15:
        age_factor_key = 'leq_15'
    elif building_age <= 20:
        age_factor_key = 'leq_20'
    elif building_age <= 25:
        age_factor_key = 'leq_25'
    return coefficients['age_factor'][age_factor_key]


def load_coefficients(file: Path)->dict:
    #load the yaml file
    return yaml.load(open(file), Loader=yaml.FullLoader)
    
    

def main():
    
    #load the coefficients yaml file
    coefficients=load_coefficients(Path('coefficients.yaml'))
    
    #TODO: align this with the pricing dictioary keys
    sample_property={
        'area': 46,
        'road_facing': False,
        'corner_plot': False,
        'floor': 5,
        'construction_year': 1975,
        'property_type': 'Διαμέρισμα',
        'elevator': True,
        'heating': 'Αυτόνομη Θέρμανση',
        'construction_material': 'concrete',
        
        
    }
    
    book_ppm = calculate_book_value(property= sample_property, zone_price= 1150, coefficients= coefficients)
    
    print(sample_property['area']*book_ppm)
    

if __name__ == "__main__":
    main()
