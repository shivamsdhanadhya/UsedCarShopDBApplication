import os

class Config(object):
    SECRET_KY = os.evironment.get('SECRET_KY') or "sec_ky"
