import yaml
from pathlib import Path
from datetime import datetime


def calculate_book_value(property: dict, zone_price:int, coefficients: dict) -> float:
    book_value = zone_price
    
    book_value *= calculate_face_factor(property, coefficients)
    book_value *= calculate_floor_factor(property, coefficients)
    book_value *= calculate_area_factor(property, coefficients)
    book_value *= calculate_age_factor(property, coefficients)
    
    return book_value


def calculate_face_factor(property: dict, coefficients: dict) -> float:
    face_factor_key = 'no_face'
    if property['road_facing']:
        face_factor_key = 'single_facing'
    elif property['corner_plot']:
        face_factor_key = 'multi_facing'
    return coefficients['face_factor'][face_factor_key]


def calculate_floor_factor(property: dict, coefficients: dict) -> float:
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


def calculate_area_factor(property: dict, coefficients: dict) -> float:
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


def calculate_age_factor(property: dict, coefficients: dict) -> float:
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
        'area': 96,
        'road_facing': True,
        'corner_plot': False,
        'floor': 1,
        'construction_year': 1975,
        'property_type': 'Διαμέρισμα',
        
        
    }
    
    book_ppm = calculate_book_value(property= sample_property, zone_price= 2100, coefficients= coefficients)
    
    print(sample_property['area']*book_ppm)
    

if __name__ == "__main__":
    main()
