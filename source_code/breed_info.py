from Levenshtein import ratio 
import re
import pandas as pd
import urllib
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Levenshtein.distance : This method calculates the Levenshtein Distance of two strings this defines 
# how many operations where needed to turn one string into another by inserting a character, removing
#  a character or replacing a character. 
# 
# Ratio on the other hand provides a similarity ratio in between the two string values which ranges 
# from 0 to 1. The smaller the represented value is to the 1, the more similar the strings belong
# to each other.

def make_Dog_Dictionary(file_path) -> dict:
    ''' 
        Given a file_path, converts an excel document into a nested dictionary 
        where the index column are the keys, and values contained a column-value pair
        
        Args: file_path : the location of the data in the relative directory
        Returns: A nested dictionary if the file is found, or an error message based 
        on the problem
    '''
    try:
        # Read the Excel file
        df = pd.read_csv(file_path, index_col=0)# engine='openpyxl')  # Specify engine if necessary
        dog_dict = df.to_dict(orient='index')
        print(f'dog dict: {dog_dict}')
        return dog_dict
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def find_approximate_dog_breed(dog_dictionary) -> None:
    '''
        Given a dog dictionary, this function prompts a user input, and attempts to 
        provide dog breed information as per the input.
         
        Args: A dictionary of dog data with breed name as keys and breed attribues as
        values.
         
        Return: None
    '''
    dog_names = dog_dictionary.keys()
    while True:
        while True:
            user_input = input("Please enter the kind of dog breed you would like to know information about: ").title()
            if user_input in dog_names:
                print("\nGreat, here is the information we have on the provided breed: ")
                dog = dog_dictionary[user_input]
                print(f'\nA {user_input} typically weighs: {dog['Weight']} lbs. Their lifespan spans {dog['Lifespan']} years, and these are their core metrics:')
                print(f'When it comes to Trainability, {user_input} scores a {dog['Trainable']}/5.')
                print(f'When it comes to Exercise needed, {user_input} scores a {dog['Exercise']}/5')
                print(f'When it comes to Shedding, {user_input} scores a {dog['Shedding']}/5')
                print("\nWe also have additional metrics regarding Behavior, Care, and environment...")
               
                user_more_data_request = input("Would you like to know about these details as well? Please type yes or no:").title()
                if re.match(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', user_more_data_request) != None:
                    # Behavior 
                    print(f'\nGreat, when it comes to Behavior, this is how the {user_input} scores:')
                    print("\n".join(f"{key}: {value}" for key, value in dog['Behavior'].items()))
                    # Care
                    print(f'\nWhen it comes to dogs, they all need some loving! Here are the typical care requirements for {user_input}:')
                    print("\n".join(f"{key}: {value}" for key, value in dog['Care'].items()))
                    #Environment
                    print(f'\nLastly, a {user_input} thrives in the following type of environment:')
                    print("\n".join(f"{key}: {value}" for key, value in dog['Environment'].items()))  
                    print()              
                
                break
                
            else: 
                distances = []
                for dog_name in dog_names:
                    distances.append((dog_name, ratio(dog_name, user_input)))

                distances.sort(key=lambda x: x[1], reverse=True)
                print("Hmmmm. we don't seem to have that particular breed...")
                print("Maybe it was a spelling error? Did you mean any of these dog breeds?")
                print([name for name, _ in distances[:5]])
                print()
        
        # Prompting the user to ask more questions
        continue_prompt = input("Would you like to ask about another dog breed? (yes/no): ").strip().lower()
        if re.match(r'^[yY][eE]{1}[sS]{1}$|^[yY]$', continue_prompt) == None:
            print("Thank you for using the dog breed information service!\n")
            break


def main(dog_dict):
    # print("Welcome! We hope to help you find information about any dog breed!")
    find_approximate_dog_breed(dog_dict)


# Dog information browsing
def browse_dog_breeds(dog_data: pd.DataFrame) -> None:
    for i, breed in enumerate(dog_data['Breed'], start=1):
        print(f"{i}. {breed}")
    print()

    while True:
        print('Enter a number to see the breed info ')
        print('Enter 0 to exit')
        choice = int(input())
        
        if choice == 0:
            break
        elif 1 <= choice <= len(dog_data):
            selected_breed = dog_data.iloc[int(choice) - 1]
            print(f"\nBreed: {selected_breed['Breed']}")
            print(f"Average Weight: {selected_breed['Avg Weight (lbs)']} lbs")
            print(f"Average Lifespan: {selected_breed['Avg Lifespan (Yrs)']} years")
            print(f"Shedding Level: {selected_breed['Shedding']}")
            print(f"Trainability: {selected_breed['Trainable']}")

            # Display the image if available
            if 'Photo' in dog_data.columns:
                image_url = selected_breed['Photo']
                print(f"Displaying image for {selected_breed['Breed']}:")

                # Create a request with a user-agent header
                req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})

                # Open the URL and load the image with Pillow
                with urllib.request.urlopen(req) as url:
                    img = Image.open(url)
                                
                # Convert the image to a NumPy array
                img_array = np.array(img)

                # Display the image using matplotlib
                plt.imshow(img_array)
                plt.axis('off')  # Hide axes
                plt.show()

            else:
                pass
                # print("Image not available for this breed.")
            print("\n")
        else:
            print('Invalid choice, Enter again.')
