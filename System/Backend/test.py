import requests
import sys



url = "http://192.168.1.11:5000/api/user/add_students_locations"
headers = {'accept':'application/json','Content-Type': 'application/json'}
data = {
  "student_number": 2,
  "exam_instance_id": "test1",
  "x": 3,
  "y": 3,
  "w": 3,
  "h": 3
}
response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print("JSON Response ", response.json()['status'])
    if response.json()['status'] != 'success':
        print("An error has occured")
    else:
        print("student added successfully")