from enum import Enum
kind=Enum('kind',('constant','variable','procedure'))

class id(object):
    name='' 
    kind=kind
    level=''
    adr=0
