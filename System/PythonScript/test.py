import requests     
import socket
import json
# url =f'http://192.168.164.242:5000/runmodel/{50}'
# response = requests.get(url)
# if response.status_code == 200:
#     print("JSON Response ", response.json()['status'])
#     if response.json()['status'] != 'success':
#         print("An error has occured")
#     else:
#         print("case created successfully")

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# url = f"https://classroommonitoring.herokuapp.com/api/user/add_students_locations"
# headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
# data = {
# "student_number": 1,
# "exam_instance_id": 'test1',
# "x": 1,
# "y": 2,
# "w": 3,
# "h": 4
# }



#response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print("JSON Response ", response.json()['status'])
    if response.json()['status'] != 'success':
        print("An error has occured")
    else:
        print("student added successfully")