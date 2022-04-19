import random
import re
import string
from datetime import datetime
from django_otp.oath import totp
from django.core.validators import RegexValidator

abstract_images = [
    "https://www.wonderopolis.org/wp-content/uploads//2014/03/dreamstime_xl_30482329-custom.jpg",
    "https://images.unsplash.com/photo-1505909182942-e2f09aee3e89",
    "https://images.unsplash.com/photo-1505356822725-08ad25f3ffe4",
    'https://images.unsplash.com/photo-1510906594845-bc082582c8cc',
    'https://images.unsplash.com/photo-1524169358666-79f22534bc6e',
    'https://images.unsplash.com/photo-1541356665065-22676f35dd40',
    'https://images.unsplash.com/photo-1470790376778-a9fbc86d70e2',
    'https://images.unsplash.com/photo-1531169509526-f8f1fdaa4a67',
    'https://images.unsplash.com/photo-1491895200222-0fc4a4c35e18',
    'https://images.unsplash.com/photo-1534293507278-19b2539423f2',
    'https://images.unsplash.com/photo-1533158326339-7f3cf2404354',
    'https://images.unsplash.com/photo-1534312527009-56c7016453e6',
    'https://images.unsplash.com/photo-1556139954-ec19cce61d61',
    'https://images.unsplash.com/photo-1549241520-425e3dfc01cb',
    'https://images.unsplash.com/photo-1523895665936-7bfe172b757d',
    'https://images.unsplash.com/photo-1519750783826-e2420f4d687f',
    'https://images.unsplash.com/photo-1572851899307-3c130a64e831',
    'https://images.unsplash.com/photo-1532456745301-b2c645d8b80d',
    'https://images.unsplash.com/photo-1483959651481-dc75b89291f1',
    'https://images.unsplash.com/photo-1496096265110-f83ad7f96608',
    'https://images.unsplash.com/photo-1511933801659-156d99ebea3e',
]


def random_img():
    return random.sample(abstract_images, 1)[0]

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomNumber(length=5):
    """Generate a random number of fixed length """
    range_start = 10**(length-1)
    range_end = (10**length)-1
    return random.randint(range_start, range_end)


def time_duration(start_time, end_time):
    """Get difference between tow datetime """
    time_format = '%m/%d/%Y, %H:%M:%S'
    start_time = datetime.strptime(start_time, time_format) 
    end_time = datetime.strptime(end_time, time_format) 
    duration = end_time - start_time
    minutes = int(duration.seconds/60)
    seconds = duration.seconds % 60
    return {"minutes": minutes, "seconds":seconds, "duration":duration }
    
    
def generate_otp(user_id, duration, code_digits):
    """Generate a random OTP for with fix digits and time"""
    key =   str(user_id).encode()
    duration = int(duration)
    code_digits = int(code_digits)
    verificationCode = str(totp( key = key, step = duration, digits = code_digits ))
    while len(verificationCode) < code_digits:
        verificationCode = '0' + verificationCode
    return verificationCode
    
def verifyAlphaNumeric(string):
    pattern = '^\w+$'
    if re.match(pattern, string):
        return True
    else:
        return False
        
        
alphaNumricValidator = RegexValidator(
    regex=r'^\w+$',
    message="Data should be alpha numric."
)

def delete_s3_file(bucket_name, file_path):
    status_code = None
    try:
        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        response = s3_client.delete_object(Bucket=bucket_name, Key=file_path) 
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    except:
        status_code = 500
    return status_code


def get_random_alphanumeric_string(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    rtn_string = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return rtn_string


def map_case_data(data):
    try:
        case_data = {
            "title": "Demo",
            "plain_text": "Test",
            "citation": data["citation"],
            "kenyalaw_id": data["kenyalaw_id"],
            "file_id": data["file_id"],
            "caseclass": "CIVIL",
            "caseaction": "JUDGMENT",
            "delivery_date": datetime.strptime(data["datedelivered"], '%d %b %Y').date(),
            "judges": data["judge"]
        }
        return case_data
    except Exception as e:
        print(e)
        return None