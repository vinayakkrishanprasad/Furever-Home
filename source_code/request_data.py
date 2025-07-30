import requests
import copy
import csv
import os


def get_agopt_a_pet_data(zip_code: int, start_number: int, end_number: int) -> list:
  '''
  '''

  adoptAPet_url = f'https://api-staging.adoptapet.com/search/pet_search?key=hg4nsv85lppeoqqixy3tnlt3k8lj6o0c&v=3&output=json&species=dog&city_or_zip={zip_code}&geo_range=1000&start_number={start_number}&end_number={end_number}'
  adoptAPet_response = requests.get(adoptAPet_url)
  data = adoptAPet_response.json()
  # print(data)
  if data['status'] == 'ok':
    return data['pets']
  else:
    raise "Invalid Zip Code Error"


def get_dog_breed_api_data() -> list:
  '''
  '''
  dog_api_url = 'https://dog.ceo/api/breeds/list/all'
  dog_api_response = requests.get(dog_api_url)
  data = dog_api_response.json()
  # print(data)
  if data:
    return data
  else:
    raise "Invalid data"


def get_dog_breed_images(breed) -> list:
  '''
  '''
  dog_api_url = f'https://dog.ceo/api/breed/{breed}/images/random'
  dog_api_response = requests.get(dog_api_url)
  data = dog_api_response.json()
  # print(data)
  if data:
    return data
  else:
    raise "Invalid data"


def get_adopt_a_pet_details(details_url: str) -> dict:
  '''
  '''

  details_response = requests.get(details_url)
  data = details_response.json()
  return {
    'shelter_name': data['pet']['shelter_name'],
    'color': data['pet']['color'],
    'hair_length': data['pet']['hair_length'],
    'purebred': bool(data['pet']['purebred']),
    'special_needs': bool(data['pet']['special_needs']),
    'housetrained': bool(data['pet']['housetrained']),
    'email': data['pet']['email'],
    'contact_person': data['pet']['contact_person'],
    'status': data['pet']['status'],
    'images': data['pet']['images']
  }


def write_data(filename: str, data: list):
  '''
  '''

  try:
    data_copy = copy.deepcopy(data)
    with open(filename, 'a') as f:
      for item in data_copy:
        f.write(str(item) + '\n')
  except Exception as e:
    print('Error savign data copy', e)


def save_data_frame(filename: str, data_frame):
  '''
  '''

  data_frame.to_csv(filename)


def load_data(filename: str) -> list:
  '''
  '''
  
  try:
    data = []
    if os.path.exists(filename):
      with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
          data.append(line)
    return data
  except Exception as e:
    print('Error reading data from file: ', e)
    return data
