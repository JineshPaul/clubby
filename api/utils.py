from rest_framework.response import Response
from rest_framework import status
from random import randint

import string
import random
import time


def response(data, code=status.HTTP_200_OK, error="",headers=None):
    """
    Overrides rest_framework response

    :param data: data to be send in response
    :param code: response status code(default has been set to 200)
    :param error: error message(if any, not compulsory)

    """
    res = {"status_code": code, "error": error, "response": data}
    return Response(data=res, status=status.HTTP_200_OK,headers=headers)


def gen_hash(seed):
    """
    :param seed: seed for random generation
    :return: hash key
    """
    base = string.ascii_letters+string.digits  # Output hash base: all alphabets and digits
    random.seed(seed)  # Input string as the random seed
    hash_value = ""
    for i in range(15):
        # Generate a 15-character hash by randomly select characters from base
        hash_value += random.choice(base)
    return hash_value


def expires():
    """
    :return: a UNIX style timestamp representing 5 minutes from now
    """
    return int(random.randint(1, 9969)*(time.time()+300))


def create_error_message(error_dict):
    """
    Changes a dict of errors into a string
    :param error_dict:a dictionary of errors
    :return:a string made of errors
    """
    error_string = ''
    for error in error_dict:
        error_string += error_dict[error] + ". "
    return error_string


def generate_error_message(errors):
    """
    :param errors:
    :return: Returns a string used to send directly as error message.
    """
    error_message = ""
    for key, value in errors.items():
        error_message = key.replace("_", " ").title() + " : " + error_message + " " + str(" ".join(value)) + ", "
    return error_message[:-2]


def random_with_N_digits(n):
    """
    :param n: the length of random number length
    :return: random number of length n
    """
    range_start = 10**(n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


def code_generator(size, chars=string.ascii_uppercase + string.digits):
    """

    :param size:
    :param chars:
    :return: a random string with caps alphabet and numeric fields
    """
    return ''.join(random.choice(chars) for _ in range(size))

