import my_dogs_name_scraper as mdns
import visualisations as vis
import request_data as rd
import adopt_pet as adopt
import clean_data as cd
import breed_info as bi
import os


def main_menu() -> int:
    '''
        Create a main menu to display to the user
    '''

    print("\n\n**********Welcome to Furever Home!**********")
    print("How can we help you today?")
    print("")
    print("1. Find details about a particular dog breed.")
    print("2. Search for details about a dog breed.")
    print("3. Some statistics about dogs.")
    print("4. Adopt a dog.")
    print("5. Exit.")
    print("")
    print("Enter your choice: ")
    while True:
        try:
            choice = int(input())
            if choice < 1 or choice > 5:
                raise ValueError
            break
        except:
            print("Invalid input. Please enter a valid choice.")
    
    print()
    return choice


def main():
    '''
    '''

    # scrape my dogs name data and save it in a csv file 
    # if not os.path.exists('my_dogs_name_data.csv'):
    print("Loading some initial data, please wait...")
    dog_dict = mdns.download_my_dogs_name_data()
    dogs_name_data = rd.load_data('my_dogs_name_data.csv')
    dogs_name_data_frame = cd.clean_dogs_name_data('my_dogs_name_data.csv')

    while True:
        # create a menu for a user
        choice = main_menu()

        if choice == 1:
            bi.browse_dog_breeds(dogs_name_data_frame)

        elif choice == 2:
            bi.main(dog_dict)

        elif choice == 3:
            vis.main(dogs_name_data_frame)

        elif choice == 4:   # choice 4 to find a pet
            adopt.main(dogs_name_data)

        elif choice == 5:
            break



main()
