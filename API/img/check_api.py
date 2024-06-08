import requests

my_img = {'image': open(r'C:\projects\api_img\kartinki-labradory-6.jpg', 'rb')}

response = requests.post('http://127.0.0.1:3000/get_breed_by_img',files=my_img)
print(response.text)