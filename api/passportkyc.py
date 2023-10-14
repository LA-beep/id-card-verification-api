from api.id_card_detector.id_card_detection_image import detect_card
from datetime import date
from passporteye import read_mrz

def extract_info(Id):
    image = Id.identity_card_image
   
    image_path = f'{image}'

    #Detect card and crop it and update passportimage
    detect_card(image_path)

    #extracting paasport mrz data
    mrz = read_mrz(image_path)

    mrz = mrz.to_dict()
    
    # extracting dob 
    mm = int(mrz['date_of_birth'][2:4])
    yyyy = int(mrz['date_of_birth'][:2])+2000
    if(yyyy > int(date.today().year)):
        yyyy-=100
    dd = int(mrz['date_of_birth'][4:6])
    dob = date(yyyy,mm,dd)
    
    return {
        'first_name_on_id' : mrz['names'],
        'last_name_on_id' : mrz['surname'],
        'dob_on_id' : dob,
        'gender_on_id' : mrz['sex'],
        'id_number' : mrz['number'],
        'country_on_id' : mrz['nationality'],
    }
