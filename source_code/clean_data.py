import re
import ast
import pandas as pd
import request_data as rd


def enrich_adopt_a_pet_data(data: list, dogs_name_data: list) -> list:
    '''
        Enrich data fetched from Adopt-A-Pet data source with my-dogs-name data source

        Attributes:
            data:   adopt-a-pet data list
            dogs_name_data:     my-dogs-name data list
        
        Return:
            a list of enriched adopt-a-pet data
    '''

    for row in data:
        # For each dog, fetch the extra details of the dog and update the record
        details = rd.get_adopt_a_pet_details(row['details_url'])
        row.update(details)

        # if there is extra data in my-dogs-name dataset, update the record with it too
        for dog_data in dogs_name_data:
            if row['primary_breed'] in dog_data['Breed']:

                row['Weight (lbs)'] = dog_data['Weight']
                row['Lifespan (Yrs)'] = dog_data['Lifespan']
                row['Trainable'] = dog_data['Trainable']
                row['Exercise'] = dog_data['Exercise']
                row['Shedding'] = dog_data['Shedding']

                break
    return data


def clean_adopt_a_pet_data(data: list) -> pd.DataFrame:
    '''
        Create a data frame from the data and clean it

        Attributes:
            data:   enriched adopt-a-pet data list
        
        Return:
            a pandas DataFrame containing cleaned data
    '''

    # Create a dataframe from the list of dogs
    df = pd.DataFrame(data)
    df.set_index('order', inplace=True)

    # reindex the pet name to be the first column in the data frame
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('pet_name')))
    df = df.reindex(columns=cols)

    # rename columns in the data frame
    df = df.rename(columns={'pet_name': 'Name'})
    df = df.rename(columns={'sex': 'Gender'})
    df = df.rename(columns={'age': 'Age'})
    df = df.rename(columns={'size': 'Size'})
    df = df.rename(columns={'primary_breed': 'Primary Breed'})
    df = df.rename(columns={'secondary_breed': 'Secondary Breed'})
    df = df.rename(columns={'addr_city': 'City'})
    df = df.rename(columns={'addr_state_code': 'State'})
    df = df.rename(columns={'shelter_name': 'Shelter Name'})
    df = df.rename(columns={'color': 'Color'})
    df = df.rename(columns={'hair_length': 'Hair Length'})
    df = df.rename(columns={'purebred': 'Purebred'})
    df = df.rename(columns={'special_needs': 'Special Needs'})
    df = df.rename(columns={'housetrained': 'House Trained'})
    df = df.rename(columns={'email': 'Email'})
    df = df.rename(columns={'contact_person': 'Contact Person'})
    df = df.rename(columns={'status': 'Status'})
    df = df.rename(columns={'images': 'Images'})

    # drop unwanted columns from the data frame
    df = df.drop('pet_id', axis=1)
    df = df.drop('results_photo_url', axis=1)
    df = df.drop('results_photo_width', axis=1)
    df = df.drop('results_photo_height', axis=1)
    df = df.drop('large_results_photo_url', axis=1)
    df = df.drop('large_results_photo_width', axis=1)
    df = df.drop('large_results_photo_height', axis=1)

    return df


def filter_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    '''
        Filter the pandas DataFrame based on the filters provided by the user

        Attributes:
            df:     pandas DataFrame with Adopt-A-Pet data
            filters:    user filters
        Returns:
            a filtered pandas Dataframe
    '''

    # apply filters to the data frame
    if filters['breed']:
        df = df[df['Primary Breed'].str.contains(filters['breed'], case=False, na=False)]

    if filters['age']:
        df = df[df['Age'].str.contains(filters['age'], case=False, na=False)]

    if filters['size']:
        df = df[df['Size'].str.contains(filters['size'], case=False, na=False)]

    if filters['gender']:
        df = df[df['Gender'].str.contains(filters['gender'], case=False, na=False)]
    
    if filters['purebred']:
        df = df[df['Purebred'].str.contains(filters['purebred'], case=False, na=False)]

    if filters['color']:
        df = df[df['Color'].str.contains(filters['color'], case=False, na=False)]
    
    return df


def clean_dogs_name_data(filename: str) -> pd.DataFrame:
    '''
        Read my-dogs-name data from the file and clean it

        Attributes:
            filename:   filename from where to read the data
        Returns:
            a pandas DataFrame with cleaned my-dogs-name data
    '''
    
    # Load the dataset
    dog_data = pd.read_csv(filename)

    # Remove incorrect data
    dog_data = dog_data[dog_data['Breed'] != 'Belgian Sheepdog']

    # Helper functions to clean data
    def parse_weight(weight_str):
        numbers = re.findall(r'\d+', str(weight_str))
        if len(numbers) == 2:
            return (int(numbers[0]) + int(numbers[1])) / 2
        elif len(numbers) == 1:
            return int(numbers[0])
        return None

    # Helper functions to clean data
    def parse_lifespan(lifespan_str):
        return sum(ast.literal_eval(lifespan_str)) / 2 if isinstance(ast.literal_eval(lifespan_str), tuple) else float(lifespan_str)

    dog_data['Avg Lifespan (Yrs)'] = dog_data['Lifespan'].apply(parse_lifespan)
    dog_data['Avg Weight (lbs)'] = dog_data['Weight'].apply(parse_weight)
    
    return dog_data
