from djongo import models

#to store User details
class User(models.Model):
    contactNo = models.BigIntegerField(primary_key=True)
    firstName = models.CharField(max_length=50, blank=False)
    middleName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50, blank=False)
    dob = models.DateField()
    gender = models.CharField(max_length=6)
    houseNo = models.CharField(max_length=10)
    streetName = models.CharField(max_length=50)
    localityName = models.CharField(max_length=50)
    cityName = models.CharField(max_length=20)
    countryName = models.CharField(max_length=20)
    pinCode = models.IntegerField()
    userPhoto = models.ImageField(upload_to='UserPhoto', blank=True)


#to store idcard image and its type
class IdentityCards(models.Model):
    contactNo = models.ForeignKey(User, on_delete=models.CASCADE)
    identity_type = models.CharField(max_length=100)
    identity_card_image = models.ImageField(upload_to='Passport_img',blank =False)
    
    class Meta:
        unique_together = ('contactNo', 'identity_type')
    

#store passport details 
class PassportDetails(models.Model):
    contactNo = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name_on_id = models.CharField(max_length=50)
    last_name_on_id = models.CharField(max_length=50)
    gender_on_id = models.CharField(max_length=6)
    dob_on_id = models.DateField()
    country_on_id = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50)
    KYC_verified = models.BooleanField(default=False)