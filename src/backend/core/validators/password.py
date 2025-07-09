from django.core.exceptions import ValidationError
import re

messages = {
    'min_length': 'Password must be at least 8 characters long.',
    'min_digits': 'Password must have at least 3 digits.',
    'min_uppercase': 'Password must have at least 1 uppercase characters.',
    'min_non_alphanumeric': 'Password must have at least 1 non alphanumeric characters.'
}

def validate_min_length_8(value):
    if len(value)<8:
        raise ValidationError(messages['min_length'])
    

def validate_min_digits_3(value):
    if len(re.findall('\d', value)) < 3:
        raise ValidationError(messages['min_digits'])
    

def validate_min_uppercase_1(value):
    if len(re.findall('[A-Z]', value)) < 1:
        raise ValidationError(messages['min_uppercase'])
    

def validate_min_non_alphanumeric_1(value):
    if len(re.findall('\W', value)) < 1:
        raise ValidationError(messages['min_non_alphanumeric'])
