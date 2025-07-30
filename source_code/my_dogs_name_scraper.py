from pathlib import Path
import pandas as pd
import requests 
from bs4 import BeautifulSoup


BASE_FILEPATH = Path(__file__).resolve().parent.parent.parent


def extract_numbers(s) -> tuple:
    ''' Extracts the numbers contained in string x and returns a tuple of the numbers '''
    # Split the string by ' - ' and strip any extra spaces
    parts = s.split(' - ')
    # Extract the numbers and convert them to integers
    numbers = tuple(int(part.split()[0]) for part in parts)
    return numbers


def extract_data(soup, section_title) -> dict:
    ''' This function iterates through the given soup containing webpage data
    and extracts the data stored within the HTML element 'section_title
    
    Args: soup : A BeautifulSoup object in the html.parser format
          section_title : The specific 'h2' heading from which the data
          is to be extracted
          
    Returns: A dictionary with the heading as the key and extracted data
            as the values
    '''
    section_data = {}
    headers = soup.find_all('h2')
    
    for header in headers:
        if header.get_text() == section_title:
            # Get the following content after the header
            next_div = header.find_next()
            while next_div and next_div.name != 'h2':
                if next_div.name == 'div':
                    # Find the rating items
                    items = next_div.find_all('li')
                    for item in items:
                        name = item.find('strong').get_text()
                        rating = item.find('span', class_='breed-rating').get_text()
                        section_data[name] = rating
                next_div = next_div.find_next()

    return section_data


# def download_my_dogs_name_data(output_directory: Path = None) -> None:    
#     """Downloads dog breed infomation to a local directory

#     Args:
#         output_directory: desired output location. Defaults to 'Project/Data/Raw/myDogsName'
#     Modifies:
#         Saves raw files from dos.pa.gov to output_directory with a separate directory
#         for each year's files.
#     """
#     # source to store the data:
#     if output_directory is None:
#         output_directory = BASE_FILEPATH / "Project" / "Data" / "Raw" / "myDogsName"
#     else:
#         output_directory = Path(output_directory).resolve()

#     # URL of the page to scrape
#     url = "https://www.mydogsname.com/dog-breeds/"

#     # Send an HTTP request to the URL
#     response = requests.get(url)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Find all <div> elements with class 'breed-card'
#         breed_cards = soup.find_all('div', class_='breed-card')
        
#         animal_dict = {}
#         # Extract the text inside <h2> tags within each breed card
#         for card in breed_cards:
#             if card.find('h2'):
#                 dog_breed = card.find('h2').text.strip()
#                 dog_photo = [img.get('src') for img in card.find_all('img') if img.get('src') and 'data' not in img.get('src')][0]
#                 dog_weight, dog_lifespan = [info.get_text(separator=' ', strip=True) for info in card.find_all('div', class_='col-xs-6')]
#                 dog_weight = extract_numbers(dog_weight)
#                 dog_lifespan = extract_numbers(dog_lifespan)
#                 dog_train_val, dog_exercise_val, dog_shedding_val = [info.find('svg').find('text').get_text(strip=True) for info in card.find_all('div',class_='col-xs-4')]

#             animal_dict[dog_breed] = (dog_weight, dog_lifespan,dog_train_val, dog_exercise_val, dog_shedding_val, dog_photo)
        
#         animal_df = pd.DataFrame.from_dict(animal_dict, orient='index', columns=['Weight (lbs)','Lifespan (Yrs)','Trainable','Exercise','Shedding','Photo'])
#         animal_df.index.name = 'Breed'
#         animal_df.to_csv("my_dogs_name_data.csv")
#     else:
#         print(f"Failed to retrieve the webpage. Status code: {response.status_code}")



def download_my_dogs_name_data(output_directory: Path = None) -> None:    
    """Downloads dog breed infomation to a local directory

    Args:
        output_directory: desired output location. Defaults to 'Project/Data/Raw/myDogsName'
    Modifies:
        Saves raw files from dos.pa.gov to output_directory with a separate directory
        for each year's files.
    """
    # source to store the data:
    if output_directory is None:
        output_directory = BASE_FILEPATH / "Project" / "Data" / "Raw"
    else:
        output_directory = Path(output_directory).resolve()

    # URL of the page to scrape
    url = "https://www.mydogsname.com/dog-breeds/"

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <div> elements with class 'breed-card'
        breed_cards = soup.find_all('div', class_='breed-card')
        
        animal_dict = {}
        # Extract the text inside <h2> tags within each breed card
        for card in breed_cards:
            if card.find('h2'):
                dog_breed = card.find('h2').text.strip()
                dog_photo = [img.get('src') for img in card.find_all('img') if img.get('src') and 'data' not in img.get('src')][0]
                dog_weight, dog_lifespan = [info.get_text(separator=' ', strip=True) for info in card.find_all('div', class_='col-xs-6')]
                dog_weight = extract_numbers(dog_weight)
                dog_lifespan = extract_numbers(dog_lifespan)
                dog_train_val, dog_exercise_val, dog_shedding_val = [info.find('svg').find('text').get_text(strip=True) for info in card.find_all('div',class_='col-xs-4')]
                
                # extract other key metrics by switching to the more detailed web. 
                # the website is in the format: https://www.mydogsname.com/dog-breeds/breed-name/, where 'breed-name' is the dog breed
                new_url = f'{url}{dog_breed.replace(' ','-')}/'
                response = requests.get(new_url)
                dog_soup = BeautifulSoup(response.text, 'html.parser')
                behavior_data = extract_data(dog_soup, 'Behavior')
                care_data = extract_data(dog_soup,'Care')
                environment_data = extract_data(dog_soup,'Environment')

            animal_dict[dog_breed] = {'Weight': dog_weight, 
                                      'Lifespan': dog_lifespan,
                                      'Trainable': dog_train_val,
                                       'Exercise': dog_exercise_val, 
                                       'Shedding': dog_shedding_val, 
                                       'Photo': dog_photo, 
                                       'Behavior' : behavior_data, 
                                       'Care': care_data, 
                                       'Environment' : environment_data}
        
        animal_df = pd.DataFrame.from_dict(animal_dict, orient='index', 
                                           columns=['Weight','Lifespan','Trainable','Exercise','Shedding','Photo', 'Behavior','Care','Environment'])
        animal_df.index.name = 'Breed'
        animal_df.to_csv("my_dogs_name_data.csv")

        return(animal_dict)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Packages to be installed :
# requests ~=2.32.3     pip install requests
# beautifulsoup4 ~=4.12.3   pip install beautifulsoup4
# openpyxl ~=3.1.5  pip install openpyxl
# IPyhton ~=8.28.0 pip install IPython
# Pandas  pip install pandas
# Matplotlib pip install matplotlib
# Levenshtein pip install levenshtein