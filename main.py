import requests
import json
import mysql.connector


class DbHandler:

  @staticmethod
  def clean_database():
    instance_db = mysql.connector.connect(host='localhost',
                                          user='root',
                                          password='',
                                          database='socialcodia')
    cursor = instance_db.cursor()
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    query = 'TRUNCATE `attributes`'
    try:
      cursor.execute(query)
      cursor.close()
    except Exception as e:
      print(e)


token = ''
country = ''
state = ''
city = ''
refresh = ''


class ApiHandler:
  global token
  global refresh
  global country
  global state
  global city

  url = "http://127.0.0.1:8000/api/v1/"

  def call(self, payload, end_point, method='POST'):
    if token:
      headers = {
        'Authorization': f'Bearer {token}',
        'Refresh-Token': refresh,
        'Content-Type': 'application/json'
      }
    else:
      headers = {'Content-Type': 'application/json'}
    # print('REQUEST IS => ',str(payload))
    response = requests.request(method,
                                f'{self.url}{end_point}/',
                                headers=headers,
                                data=json.dumps(payload))
    if response.status_code < 500:
      print('RESPONSE IS => ', response.text)
    # print('RESPONSE IS => ',response.text)
    return response.json()


class Auth(ApiHandler):

  def do_register(self):
    try:
      payload = {
        "name": "Umair Farooqui",
        "email": "info.mufazmi@gmail.com",
        "password": "123456789"
      }
      res = self.call(payload, 'auth/register')
      print(str(res))
    except Exception as e:
      # print('e',e)
      pass

  def do_verify(self):
    try:
      payload = {
        "email": "info.mufazmi@gmail.com",
        "type": "email",
        "otp": "123456"
      }
      self.call(payload, 'auth/verify')
    except Exception as e:
      print(e)

  def do_login(self):
    global token
    global refresh
    try:
      payload = {"email": "info.mufazmi@gmail.com", "password": "123456789"}
      res = self.call(payload, 'auth/login')
      token = res.get('data').get('access')
      refresh = res.get('data').get('refresh')
    except Exception as e:
      print(e)

  def do_refresh(self):
    global token
    global refresh
    try:
      payload = {}
      res = self.call(payload, 'auth/refresh', 'GET')
      token = res.get('data').get('access')
      refresh = res.get('data').get('refresh')
    except Exception as e:
      print(e)


class Address(ApiHandler):

  def add_countries(self):
    global country
    countries = ['United State', 'Pakistan', 'India']
    countries_code = ['US', 'PAK', 'IN']
    for i, a in enumerate(countries):
      res = self.call({"name": a, "code": countries_code[i]}, 'countries')
      country = res.get('id')

  def add_states(self):
    global country
    global state
    states = ['Uttar Pardesh', 'Gujrat', 'Delhi', 'Maharashtra']
    for a in states:
      res = self.call({"name": a, "country": country}, 'states')
      state = res.get('id')

  def add_cities(self):
    global state
    global city
    cities = ['Kurla', 'Mumbai', 'Navi Mumbai', 'Mumbra']
    for a in cities:
      res = self.call({"name": a, "state": state}, 'cities')
      city = res.get('id')


class Data(ApiHandler):

  def add_medical(self):
    global token
    global country
    global state
    global city
    data = {
      "name": "Umair Medical",
      "license": "1234567",
      "mobile": "9867503256",
      "address": {
        "country": country,
        "state": state,
        "city": city,
        "pincode": "400612",
        "address": "Kausa, Mumbra, Thane, Maharashtra - 400612"
      }
    }
    self.call(data, 'medicals')

  def add_attributes(self):
    attributes = [
      '100GM', '200MG', '100GM', '200GM', '50ML', '100ML', '200ML', '500ML',
      '10 Tablets', '20 Tablets', '10 Capsules', '20 Capsules'
    ]
    for a in attributes:
      self.call({"name": a, "type": "size"}, 'attributes')

  def add_brands(self):
    brands = [
      'Cipla', 'Hamdard', 'Emcure', 'Dehlvi', 'Biocon', 'FHC', 'Mankind',
      'Shama', 'Lupin'
    ]
    for i, a in enumerate(brands):
      if i % 2:
        type = "pharmacy"
      else:
        type = "ayurvedic"
      self.call({"name": a, "type": type, "slug": "socialcodia"}, 'brands')

  def add_categories(self):
    categories = [
      'Capsule', 'Syrup', 'Tablet', 'Oinment', 'Sachet', 'Powder', 'Cream',
      'Majun', 'Habbe'
    ]
    for a in categories:
      self.call({"name": a}, 'categories')

  def add_items(self):
    items = [
      'Synofree Plus', 'Combiflam', 'Mimflam', 'Farooqui Massage Oil',
      'Lasani Chooran', 'Paracip', 'Paracetamol'
    ]
    items_d = [
      'Used for cought and cold.', 'Use for fever', 'Used for high fever',
      'Used for any kind of pain relief', 'Used for abdominal issues',
      'Used for fever', 'Used for fever'
    ]
    for i, a in enumerate(items):
      self.call({"name": a, "description": items_d[i]}, 'items')

  def add_locations(self):
    locations = [
      'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4',
      'DESK 1', 'DESK 2', 'DESK 3', 'DESK 4'
    ]
    for a in locations:
      self.call({"name": a, "type": "rack"}, 'locations')

  def add_distributors(self):
    distributors = [{
      "name": "Umair Farooqui",
      "mobile": "9867503256",
      "address": "Kausa, Mumbra Thane"
    }, {
      "name": "Sajid Farooqui",
      "mobile": "9867503256",
      "address": "Kausa, Mumbra Thane"
    }, {
      "name": "Akshay Matre",
      "mobile": "9867503256",
      "address": "Ahmdabad, Pune"
    }]
    for a in distributors:
      self.call(a, 'distributors')


auth = Auth()
address = Address()
data = Data()

auth.do_register()
auth.do_verify()
auth.do_login()

address.add_countries()
address.add_states()
address.add_cities()

data.add_medical()
auth.do_refresh()

data.add_attributes()
data.add_brands()
data.add_categories()
data.add_items()
data.add_locations()
data.add_distributors()

# DbHandler.clean_database()
