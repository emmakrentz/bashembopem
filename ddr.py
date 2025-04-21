import hid
import time

for device in hid.enumerate():
    # find DDR mat 1
    if device['product_string'] == 'USB Gamepad ':
        vendor_id = device['vendor_id']
        product_id = device['product_id']


# open DDR mat 1
device = hid.device()
device.open(vendor_id, product_id)
device.set_nonblocking(False)

arrow_dict = {15:'null',31:'left', 47:'down', 63:'down-left', 79:'up', 95:'up-left', 111:'up-down', 
              143:'right', 159:'left-right', 175:'down-right', 207:'up-right'}
button_dict = {0:'null',1:'square',2:'triangle',4:'x',8:'o',16:'select',32:'start'}

while True:
    # read DDR mat data
    data = device.read(64)
    if data:
        if arrow_dict[data[5]]!='null':
            #print(data)
            print(arrow_dict[data[5]])
            #print(button_dict[data[6]])
    
    
        time.sleep(0.1)  # adjust time as needed