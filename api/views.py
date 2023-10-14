from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import UserRegistrationSerializer, IdentitycardSerializer, PassportDetailsSerializer
from rest_framework.status import HTTP_200_OK, HTTP_304_NOT_MODIFIED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from .models import User, IdentityCards
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .passportkyc import extract_info


# Create your views here.

#user registration

@csrf_exempt
@api_view(["POST"])
def usr_reg(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'user_registered': True}, status=HTTP_200_OK)
    return Response(serializer.errors)


#identity_verification.

@csrf_exempt
@api_view(["POST"])
def usr_id_verification(request, pk):
    user = User.objects.get(pk=pk)
    contact = user.contactNo
    id_type = request.data.get('identity_type')
    id_image = request.data.get('identity_card_image')
    
    serializer = IdentitycardSerializer(data={
        'contactNo' :contact, 
        'identity_type' : id_type,
        'identity_card_image' : id_image,
    })
    
    if serializer.is_valid():
        serializer.save()

        if (id_type == 'Passport'):    
            info = extract_info(IdentityCards.objects.get(contactNo = contact , identity_type=id_type))

            first_name_verified = user.firstName == info['first_name_on_id']
            last_Name_verified = user.lastName == info['last_name_on_id']
            dob_verified = user.dob == info['dob_on_id']
            gender_verified = user.gender == info['gender_on_id']
            country_verified = user.countryName == info['country_on_id']

            KYCverified = first_name_verified and last_Name_verified and dob_verified and gender_verified and country_verified

            verification_status = {
                'first_name_verified':first_name_verified,
                'last_Name_verified':last_Name_verified,
                'dob_verified':dob_verified,
                'gender_verified':gender_verified,
                'country_verified':country_verified
            }
            newserializer = PassportDetailsSerializer(data = {
                'contactNo' :contact,
                'first_name_on_id' : info['first_name_on_id'],
                'last_name_on_id'  : info['last_name_on_id'],
                'dob_on_id'        : info['dob_on_id'],
                'gender_on_id'     : info['gender_on_id'],
                'country_on_id'    : info['country_on_id'],
                'id_number'        : info['id_number'],
                'KYCverified'      : KYCverified
            })

            if not newserializer.is_valid():
                return Response(newserializer.errors, status=HTTP_400_BAD_REQUEST)  
            
            newserializer.save()
            return Response({ 'verification_status':verification_status,
                             'info_extrated':info}
                             ,status=HTTP_200_OK)
        
        else:
            return Response("identity type not available",status=HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)   