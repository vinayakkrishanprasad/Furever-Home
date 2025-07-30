import os
import re
import request_data as rd
import clean_data as cd
import pandas as pd
from IPython.display import display, HTML
import urllib
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import json

def user_filters() -> dict:
    '''
        Ask the user for different filters for dogs data

        Returns:
            a dictionary of all the filters a user wants to apply
    '''
    
    filters = {
       'breed': '',
        'age': '',
        'size': '',
        'gender': '',
        'purebred': '',
        'color': ''
    }

    while True:
        try:
            do_filter = input("Do you want to filter the data? Y/N ")
            if re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', do_filter) != None:
                do_filter = True
                break
            elif re.search(r'^[nN][oO]{1}$|^[nN]$', do_filter) != None:
                do_filter = False
                break
            else:
                raise ValueError
        except:
            print("Invalid input. Please enter a valid choice.")
    
    if do_filter:
        while True:
            try:
                filter = input("Filter by Breed? Y/N ")
                if re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', filter) != None:
                    filters['breed'] = input('Enter the breed name ')
                    break
                elif re.search(r'^[nN][oO]{1}$|^[nN]$', filter) != None:
                    break
                else:
                    raise ValueError
            except:
                print("Invalid input. Please enter a valid choice.")

        filter = ''
        while True:
            try:
                filter = input("Filter by Age? Y/N ")
                if re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', filter) != None:
                    print("Choose age: ")
                    print("1. Puppy")
                    print("2. Young")
                    print("3. Adult")
                    print("4. Senior")
                    filters['age'] = int(input())
                    if filters['age'] == 1:
                        filters['age'] = 'puppy'
                    elif filters['age'] == 2:
                        filters['age'] = 'young'
                    elif filters['age'] == 3:
                        filters['age'] = 'adult'
                    elif filters['age'] == 4:
                        filters['age'] = 'senior'
                    else:
                        raise ValueError
                    break
                elif re.search(r'^[nN][oO]{1}$|^[nN]$', filter) != None:
                    break
                else:
                    raise ValueError
            except:
                print("Invalid input. Please enter a valid choice.")

        filter = ''
        while True:
            try:
                filter = input("Filter by Size? Y/N ")
                if re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', filter) != None:
                    print("Choose size: ")
                    print("1. Small")
                    print("2. Medium")
                    print("3. Large")
                    filters['size'] = int(input())
                    if filters['size'] == 1:
                        filters['size'] = 'Small'
                    elif filters['size'] == 2:
                        filters['size'] = 'Med'
                    elif filters['size'] == 3:
                        filters['size'] = 'Large'
                    else:
                        raise ValueError
                    break
                elif re.search(r'^[nN][oO]{1}$|^[nN]$', filter) != None:
                    break
                else:
                    raise ValueError
            except:
                print("Invalid input. Please enter a valid choice.")

        filter = ''
        while True:
            try:
                filter = input("Filter by Gender? Y/N ")
                if re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', filter) != None:
                    filters['gender'] = input('Enter the Gender: M/F ')
                    if re.search(r'^[mM]$', filters['gender']) != None:
                        filters['gender'] = 'm'
                    elif re.search(r'^[fF]$', filters['gender']) != None:
                        filters['gender'] = 'f'
                    else:
                        raise ValueError
                    break
                elif re.search(r'^[nN][oO]{1}$|^[nN]$', filter) != None:
                    break
                else:
                    raise ValueError
            except:
                print("Invalid input. Please enter a valid choice.")

        filter = ''
        while True:
            try:
                filter = input("Filter by Purebred? Y/N ")
                if re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', filter) != None:
                    filters['purebred'] = True
                    break
                elif re.search(r'^[nN][oO]{1}$|^[nN]$', filter) != None:
                    filters['purebred'] = False
                    break
                else:
                    raise ValueError
            except:
                print("Invalid input. Please enter a valid choice.")

        filter = ''
        while True:
            try:
                filter = input("Filter by Color? Y/N ")
                if re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', filter) != None:
                    filters['color'] = input('Enter the Color: ')
                    break
                elif re.search(r'^[nN][oO]{1}$|^[nN]$', filter) != None:
                    break
                else:
                    raise ValueError
            except:
                print("Invalid input. Please enter a valid choice.")
    
    return filters


def print_data_frame(data_frame, start, end) -> None:
    '''
        A function to display the pet data using html tables instead of data frame

        Attributes:
            data_frame: the filtered data frame to be displayed
            start:      the starting index to display the data from
            end:        the ending index up to where to display the data
    '''

    df = data_frame.iloc[start:end]
    display(df[['Name', 'Gender', 'Age', 'Size', 'Color', 'Primary Breed', 'Shelter Name']])
    
    # # create table headers
    # html = "<table>"
    # html += "<tr>"
    # html += "<th>S.No.</th>"
    # html += "<th>Name</th>"
    # html += "<th>Gender</th>"
    # html += "<th>Age</th>"
    # html += "<th>Size</th>"
    # html += "<th>Color</th>"
    # html += "<th>Hair Length</th>"
    # html += "<th>Primary Breed</th>"
    # html += "<th>Secondary Breed</th>"
    # html += "<th>Purebred</th>"
    # html += "<th>Special Needs</th>"
    # html += "<th>House Trained</th>"
    # html += "<th>Shelter Name</th>"
    # html += "<th>City</th>"
    # html += "<th>State</th>"
    # html += "<th>Email</th>"
    # html += "<th>Contact</th>"
    # html += "<th>Status</th>"
    # html += "<th>Weight (lbs)</th>"
    # html += "<th>Lifespan (Yrs)</th>"
    # html += "<th>Trainable</th>"
    # html += "<th>Exercise</th>"
    # html += "<th>Shedding</th>"
    # html += "</tr>"
  
    # # for each record, create a table row
    # for i in range(start, end):
    #     record = data_frame.iloc[i].to_dict()
    #     html += "<tr>"
    #     html += "<td>" + str(i+1) + "</td>"
    #     html += "<td>" + str(record['Name']) + "</td>"
    #     html += "<td>" + str(record['Gender']) + "</td>"
    #     html += "<td>" + str(record['Age']) + "</td>"
    #     html += "<td>" + str(record['Size']) + "</td>"
    #     html += "<td>" + str(record.get('Color')) + "</td>"
    #     html += "<td>" + str(record.get('Hair Length')) + "</td>"
    #     html += "<td>" + str(record.get('Primary Breed')) + "</td>"
    #     html += "<td>" + str(record.get('Secondary Breed')) + "</td>"
    #     html += "<td>" + str(record.get('Purebred')) + "</td>"
    #     html += "<td>" + str(record.get('Special Needs')) + "</td>"
    #     html += "<td>" + str(record.get('House Trained')) + "</td>"
    #     html += "<td>" + str(record.get('Shelter Name')) + "</td>"
    #     html += "<td>" + str(record.get('City')) + "</td>"
    #     html += "<td>" + str(record.get('State')) + "</td>"
    #     html += "<td>" + str(record.get('Email')) + "</td>"
    #     html += "<td>" + str(record.get('Contact')) + "</td>"
    #     html += "<td>" + str(record.get('Status')) + "</td>"
    #     html += "<td>" + str(record.get('Weight (lbs)')) + "</td>"
    #     html += "<td>" + str(record.get('Lifespan (Yrs)')) + "</td>"
    #     html += "<td>" + str(record.get('Trainable')) + "</td>"
    #     html += "<td>" + str(record.get('Exercise')) + "</td>"
    #     html += "<td>" + str(record.get('Shedding')) + "</td>"
    #     html += "</tr>"
  
    # html += "</table>"
    # display(HTML(html))


def print_dog_details(dog_details: dict) -> None:
    print('Name:\t\t\t\t\t\t', dog_details['Name'])
    print('Gender:\t\t\t\t\t\t', dog_details['Gender'])
    print('Age:\t\t\t\t\t\t', dog_details['Age'])
    print('Size:\t\t\t\t\t\t', dog_details['Size'])
    print('Color:\t\t\t\t\t\t', dog_details['Color'])
    print('Hair Length:\t\t\t\t\t\t', dog_details['Hair Length'])
    print('Primary Breed:\t\t\t\t\t\t', dog_details['Primary Breed'])
    print('Secondary Breed:\t\t\t\t\t\t', dog_details['Secondary Breed'])
    print('Purebred:\t\t\t\t\t\t', dog_details['Purebred'])
    print('Special Needs?:\t\t\t\t\t\t', dog_details['Special Needs'])
    print('House Trained?:\t\t\t\t\t\t', dog_details['House Trained'])
    print('Weight (lbs):\t\t\t\t\t\t', dog_details['Weight (lbs)'])
    print('Lifespan (Yrs):\t\t\t\t\t\t', dog_details['Lifespan (Yrs)'])
    print('Trainable:\t\t\t\t\t\t', dog_details['Trainable'])
    print('Exercise:\t\t\t\t\t\t', dog_details['Exercise'])
    print('Shedding:\t\t\t\t\t\t', dog_details['Shedding'])
    print('Shelter Name:\t\t\t\t', dog_details['Shelter Name'])
    print('City:\t\t\t\t\t\t', dog_details['City'])
    print('State:\t\t\t\t\t\t', dog_details['State'])
    print('Contact Person:\t\t\t\t', dog_details['Contact Person'])
    print('Email:\t\t\t\t\t\t', dog_details['Email'])
    print('Ststus:\t\t\t\t\t\t', dog_details['Status'])

    
    # images_list = json.loads(dog_details['Images'])
    # print('Images list - ', images_list, type(images_list))
    # if images_list:
    #     for image in images_list:
    #         print('Image - ', image)
    #         image_url = image['thumbnail_url']
            
    #         print('imageurl - ', image_url)
    #         # Create a request with a user-agent header
    #         req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})

    #         print('req - ', req)
    #         # Open the URL and load the image with Pillow
    #         with urllib.request.urlopen(req) as url:
    #             img = Image.open(url)
                
    #         # Convert the image to a NumPy array
    #         img_array = np.array(img)

    #         # Display the image using matplotlib
    #         plt.imshow(img_array)
    #         plt.axis('off')  # Hide axes
    #         plt.show()
    


def main(dogs_name_data: list) -> None:
    '''
        Ask user inputs for pet adoption process

        Attributes:
            dogs_name_data:     my-dogs-name data read from a csv file as a list of dictionaries
    '''
    
    pets_data = []
    file_data = False
    
    print("Which city are you looking to adopt?")
    while True:           # While loop to get a correct zip code from user
        try:
            city_or_zip = int(input("Enter the zip code:  "))
            if len(str(city_or_zip)) != 5:            # validate zip code length
                raise ValueError
      
            # check if we already have cleaned data for that zip code
            if os.path.exists(f'{city_or_zip}.csv'):
                # If data already exists, load the data from the file
                pets_data = rd.load_data(f'{city_or_zip}.csv')

                # If there is no data that is loaded, then make an api call to fetch new data
                if len(pets_data) < 1:
                    print('We are fetching the data, it may take around a minute, please wait...')
                    pets_data = rd.get_agopt_a_pet_data(city_or_zip, 1, 500)
                else:
                    file_data = True
      
            else:
                # If data is not already available, then fetch the data from api
                print('We are fetching the data, it may take around a minute, please wait...')
                pets_data = rd.get_agopt_a_pet_data(city_or_zip, 1, 500)
      
            break
        except:
            print("Invalid input. Please enter a valid zip code.")
    
    # If data is not fetched from file, enrich the data and create a raw file for it
    if file_data == False:
        pets_data = cd.enrich_adopt_a_pet_data(pets_data, dogs_name_data)
        rd.write_data(f'{city_or_zip}_raw.json', pets_data)

    # ask user for the filters on the data
    filters = user_filters()

    # If data is not read form file, clean the and save the data frame
    if file_data == True:
        data_frame = pd.DataFrame(pets_data)
    else:
        data_frame = cd.clean_adopt_a_pet_data(pets_data)
        rd.save_data_frame(f'{city_or_zip}.csv', data_frame)
    
    # Filter data frame data based on the user filters
    filtered_data_frame = cd.filter_data(data_frame, filters)

    # If filtered data frame has more than 10 records, loop till the user stops
    if (len(filtered_data_frame) > 10):
        print_data_frame(filtered_data_frame, 0, 10)
        count = 1
        while True:
            print('Want to see more data? Y/N')
            print('Choose no if you want to see more details about a dog you like.')
            more_data = input()
            if (re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', more_data) != None):
                print_data_frame(filtered_data_frame, (10 * count), (10 * count) + 10)
                count += 1
            elif (re.search(r'^[nN][oO]{1}$|^[nN]$', more_data) != None):
                break
            else:
                print("Invalid input. Please enter a valid value.")
    elif len(filtered_data_frame) == 0:
        print("Sorry we don't have any dog based on your search results")
    else:
        print_data_frame(filtered_data_frame, 0, len(filtered_data_frame))

    while True:
        try:
            dog_choice = int(input('\n\nEnter the number for the dog you liked: '))
            if dog_choice < 0 or dog_choice >= len(filtered_data_frame):
                raise ValueError
            else:
                dog_details = filtered_data_frame.iloc[dog_choice].to_dict()
                # images_list = filtered_data_frame.iloc[dog_choice]['Images'].to_dict()
                print_dog_details(dog_details)

            
            more_data = input('\n\nWant to see data about another dog? Y/N ')
            if (re.search(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', more_data) != None):
                continue
            elif (re.search(r'^[nN][oO]{1}$|^[nN]$', more_data) != None):
                break
            else:
                print("Invalid input. Please enter a valid value.")
        except Exception as e:
            print("Invalid input. Please enter a valid value.", e)
