import jwt
import datetime
import pytz
import pyotp

from django.http import Http404

from accountapp.models import User 


current_time = datetime.datetime.now(pytz.timezone('Asia/Dhaka'))

def jwt_expired_time():
    ## set jwt expired time 1 hour
    return current_time + datetime.timedelta(seconds=3600)


def otp_expired_time():
    inrerval = 86400
    return inrerval


def get_current_user(request):
    token = request.COOKIES.get('jwt')
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.get(id=payload['id'])
    return user





def send_otp_via_email(email):
    secret = pyotp.random_base32()        
    totp = pyotp.TOTP(secret, interval=86400)
    OTP = totp.now()
    
    ## here send otp via email  but now only print
    print(OTP)
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Http404
    user_obj.otp = OTP
    user_obj.activation_key = secret
    user_obj.save() 
    return True