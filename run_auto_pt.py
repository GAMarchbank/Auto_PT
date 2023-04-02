from auto_classes import biomentric
import time
import os
import json
import random
import datetime
from copy import deepcopy


# this funciton allows datatime objects to be saved into json format by converting them into strings
def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# this function works as an overall check of the user inputs in the program.  
# inp = userinput, tp = type of check ['num'(default), 'both', 'other'], check_lst = for num [range low, range high], for both [[range low, range high], [string check list]], for other [string check list]
def input_check(inp, tp = 'num', check_lst = 0):
    # whole function is encased in a try loop, if at any point it fails it rejects the user input
    try:
        # this is the section if the type of check is for floats
        if tp == 'num':
            # if a checklst is present, the program checks that the user input is a float and that the number is the range of the check list
            if check_lst != 0:
                if float(inp) not in range(check_lst[0]+1, check_lst[1]+1):
                    print('Input error')
                    return False
                else:
                    return float(inp)
            # if a checklist is not present it simply checks that it is a float
            else:
                return float(inp)
        # this is the section that checks if the code is either a float or a string
        elif tp == 'both':
            # here the code creates a list and fills it with the availble correct options both numbers and letters
            open_lst = []
            for numbs in range(check_lst[0][0]+1, check_lst[0][1]+1):
                open_lst.append(str(numbs))
            for let in check_lst[1]:
                open_lst.append(let)
            kal = True
            # here the code checks if the input is inside this list making kal = True, if the input can be rendered as lowercase it will also check the lowercase option
            if inp not in open_lst:
                kal = False
                try:
                    if inp.lower() in open_lst:
                        kal = True
                except:
                    pass
            # here if the input was recognised it checks if the input was a number or a string. if it was a number it converts it into a float before returning. 
            if kal == True:
                if inp not in check_lst[1]:
                    return float(inp)
                else:
                    return inp.lower()
            # if the input was not recognised it simply returns False
            else:
                print('Input error')
                return False 
        # this section checks that the string that returns is one of the availble options. 
        else:
            # this part of the code checks if there is a checklist selected, if there is automatically checks that the input is yes y no or n. 
            if check_lst == 0:
                check_lst = ['y', 'n', 'no', 'yes']
            # here it checks if the input is in the checklist, returning false if not and the input in lowercase if it is
            if inp.lower() not in check_lst:
                print('Input error')
                return False
            else:
                return inp.lower() 
    # if any errors are detected it returns false and the input is rejected
    except Exception as e:
        print('Input error')
        return False
    
# takes in lst which is a list of the items to be iterated, if more info for each item is required the lst can be lst of dictionarys, title of list option is value of key named 'init', others dont matter but key and value will be printed.
def lst_interation(lst):
    # the lower range is the starting index value of the list to be displayed
    lower_range = 0
    # the upper range is the hight list index that will be printed on this display page
    # if the list is under 10 items long, the upper range will equal the length of the list, else it will be 10
    if len(lst) >=10:
        upper_range = 10
    else:
        upper_range = len((lst))+1
    # here the main code loop begins
    while True:
        # the code creates a check variable that will check if there are any items left in the list that havent been displayed
        check = 0
        # here the code one at a time extracts the items from this lists with index values between lower_range and upper_range
        for number in range(lower_range, upper_range):
            try:
                # if the value is a dicitonary it prints more data
                if type(lst[number]) == dict:
                    for keys in lst[number]:
                        if keys == 'init':
                            print(f"{number+1}:\t{lst[number][keys]}")
                        else:
                            print(f"\t{keys}:\t{lst[number][keys]}")
                # else it prints the basic amount
                else:    
                    print(f"{number+1}:\t{lst[number]}")
            # an error will be encountered if the list does not contain an item at that index number, if so there are not remaining items in the list and check will no longer be 0
            except Exception:
                check += 1
        # if lower_range is not 0 then there are index's to view below the current lower_range index number
        if lower_range != 0:
            print(f"p:\tPrevious Page")
        # if check still equals 0 then there are items left in teh list to display
        if check == 0:
            print(f"n:\tNext page")
        print(f"b:\tBack.")
        # here the user inputs into the program
        iam = input('Select an item or exit menu.\t')
        iam = input_check(iam, 'both', [[lower_range, upper_range], ['p', 'n', 'b']])
        # if the input is not a valid option the loop restarts
        if iam == False:
            print('Unrecognised input.')
            continue 
        # here the user exits the loop without selecting an option       
        if iam == 'b':
            return False
        # if the user choses to see the next items then lower_range and upper_range are both increased by 10
        elif check == 0 and iam == 'n':
            print('Next page')
            lower_range += 10
            upper_range += 10
            continue
        # similarly if the user choses to see the previous items then lower_range and upper_range decrease by 10
        elif lower_range != 0 and iam == 'p':
            print('Previous page')
            lower_range -= 10
            upper_range -= 10
            continue 
        # if the use selects an item then that item is returned. 
        return lst[int(iam)-1]                  
                    

# here the main program begins with a section that loads users or creates new ones
# this variable tells the program that a user has been correctly loaded
main_profile_loaded = True
# these next dictionaries contain basic data used in the program
exercise_dic = {1: 'strength(bulking)', 2: 'strength(cut)', 3: 'weight loss', 4: 'toning', 5: 'cardio traing', 6: 'general health'}
dietary_dic = {1: 'None', 2: 'Vegetarian', 3: 'Vegan', 4: 'Pescitarian', 5: 'Keto', 6: 'Gulten Free'}
exercise_volume_dic = {1: 'Little to no exercise', 2: 'Light exercise', 3: 'Moderate exercise', 4: 'Heavy exercise', 5: 'Extremely heavy exercise'}
print('\nWelcome to the Auto_PT\nCreated by ECO-Himbo\n')
time.sleep(2)
while main_profile_loaded == True:
    profile_loaded = True
    # this input allows the player to choose weather to load a profile or create a new one
    print('Please select an option.\n1:\tLoad saved user data.\n2:\tCreate new user profile.')
    opt = input_check(input('choose\t'), 'num', [0, 2])
    if opt == False:
        continue
    print("\n")
    # the load user path
    if int(opt) == 1:
        # starts by checking that there is a saved user file for the program to load from. 
        if os.path.exists('user_data.txt'):
            # if there is a saved file the program extracts the data from that file.
            with open('user_data.txt', 'r')as file:
                file = file.read()
            u = json.loads(file)
            times = []
            # if there are no items in the list the program treats it like the file doesnt exist.
            if len(u) == 0:
                pas = False
            # the program pases through the list and creates a new list of the datetime values which it then orders by most recent.
            else:
                for items in u:
                    times.append(items['datetime'])
                times = sorted(times, reverse= True)
                # it then takes the full items from the orginal list ordered by the datetime valus in the datetime list.
                users = []
                for tim in times:
                    for items in u:
                        if items['datetime'] == tim:
                            users.append(items)
        else:
            pas = False
        # if there is no saved data or the data is empty then the while loop restarts
        if pas == False:
            print('No user data found.\tYou should create a profile.')
            continue
        # this loop is where the user selects the profile to load
        while profile_loaded == True:
            # here the user data is reformated to be used by the function lst_iteration()
            lst = []
            for user in users:
                lst.append({'init': user['name'], 'Age': user['age'], 'Gender': user['gender'], 'User ID': user['user_id']})
            # the function is then called upon to select a user
            inp = lst_interation(lst)
            # if the function returns False then the loop is broken from 
            if inp == False:
                break
            # the reformatted lists user_id is then matched to the orginial lists user_id
            for use in users:
                if inp['User ID'] == use['user_id']:
                    user = use
            # this section checks that the user is happy with the user that has been selected
            while True:
                print(f"\nYou have selected:\t{user['name']}\n\t\t\tAge:\t{user['age']}\t\tGender:\t{user['gender']}\n")
                time.sleep(1)
                conf = input_check(input('Are you happy with this selelction.\t'), 'other')
                if conf == False:
                    continue
                break
            if conf in ['n', 'no']:
                print('Please select again.')
                continue
            else:
                # the datetime value on the user is then updated for the current date
                users[users.index(user)]['datetime'] = datetime.datetime.now()
                # the user profile with this updated date is then saved resaved back to the user_data file in json format
                u = json.dumps(users, default=converter)
                with open('user_data.txt', 'w')as file:
                    file.write(u)
                # the datetime data is also changed on the user file in the program
                user['datetime'] = datetime.datetime.now()
                while True:
                    print(f"\nWhat action would you like to take.\n1:\tLoad profile\n2:\tDelete profile")
                    choice = input_check(input('Please choose an option'), 'num', [0, 2])
                    if choice == False:
                        continue
                    break
                # this path changes the variables that indicate a profile has been loaded and then create a class instance for the profile
                if int(choice) == 1:
                    profile_loaded = False
                    main_profile_loaded = False
                    current_user = biomentric(user['user_id'], user['name'], user['gender'], user['age'], user['height'], user['weight'], user['ff_weight'], user['goals'], user['v_ve_me'], user['exercise_volume'])
                    break
                # the path deletes the profile and erases its info fro the user_data file
                elif int(choice) == 2:
                    while True:
                        print(f"\nConfirm you would like to delete the profile for:\n{user['name']}\n\t\t\tage:\t{user['age']}\t\tgender:\t{user['gender']}")
                        choice = input_check(input('Enter y to confirm deletion'), 'other')
                        if choice == False:
                            continue
                        break
                    if choice in  ['y', 'yes']:
                        # a instance of the calss is created to delete this data. 
                        deleted = users.pop(users.index(user))
                        current_user = biomentric(deleted['user_id'], deleted['name'], deleted['gender'], deleted['age'], deleted['height'], deleted['weight'], deleted['ff_weight'], deleted['goals'], deleted['v_ve_me'], deleted['exercise_volume'])
                        current_user.delete_saved_data()
                        current_user = 0
                        file = json.dumps(users, default=converter)
                        with open('user_data.txt', 'w')as fil:
                            fil.write(file)
                        profile_loaded = False
                        print(f"The file:\t{deleted['name']}\n\tUser ID:\t{deleted['user_id']}\n\nHas been deleted")
                        break
                    else:
                        break
    # this path here creates a new user profile
    elif int(opt) == 2:
        # if a user_data file exists then that info is loaded
        try:
            with open('user_data.txt', 'r')as file:
                file = file.read()
            users = json.loads(file)
        # if it doesn't exist then a save data file is created along with an empty list. 
        except Exception:
            users = []
            us = json.dumps(users, default=converter)
            with open('user_data.txt', 'w')as file:
                file.write(us)
        print(f"\nCreate new user profile.")
        # the user dictionary is the foundation for the user profile
        user = {}
        # this is then populated with the date
        user['datetime'] = datetime.datetime.now()
        # the user then input their name which is inserted into the dictionary
        user['name'] = input('Name:\t')
        # the user then inputs their hormonal gender, if it is not one of the options availible then the program makes you input it again
        while True:
            user['gender'] = input_check(input('Gender (please enter the sex your hormones most allign with):\t'), 'other', ['m', 'male', 'f', 'female'])
            if user['gender'] == False:
                continue
            break        
        # the user then inputs their age, if its not a number it is rejected
        while True:
            user['age'] = input_check(input('Age:\t'), 'num')
            if user['age'] == False:
                continue
            break
        # same with height
        while True:
            user['height'] = input_check(input('Height:\t'), 'num')
            if user['height'] == False:
                continue
            break
        # same with weight
        while True:
            user['weight'] = input_check(input('Weight:\t'), 'num')
            if user['weight'] == False:
                continue
            break
        # same with lean body mass except the program also rejects it if its bigger then the weight
        while True:
            user['ff_weight'] = input_check(input('Lean body mass:\t'), 'num')
            if user['ff_weight'] == False:
                continue
            if user['ff_weight'] > user['weight']:
                print('It is impossible to weight more without fat.\nPlease try again.')
                continue
            break
        # the user then selects an exercise goal
        while True:
            num =1
            print(f"Please select your exercise goals")
            for keys in exercise_dic:
                print(f"{keys}:\t{exercise_dic[keys]}")
                num +=1
            user['goals'] = input_check(input('Your selection:\t'), 'num', [0, num-1])
            if user['goals'] == False:
                continue
            break
        # same for dietary requirements
        while True:
            num = 1
            print('Please select your dietary requirements')
            for keys in dietary_dic:
                print(f"{keys}:\t{dietary_dic[keys]}")
                num +=1
            user['v_ve_me'] = input_check(input('Your selection:\t'), 'num', [0, num-1])
            if user['v_ve_me'] == False:
                continue
            break
        # same for exercise volume
        while True:
            num = 1
            print('Please select the option that best describes the amount of exercise you do.')
            for keys in exercise_volume_dic:
                print(f"{keys}:\t{exercise_volume_dic[keys]}")
                num += 1
            user['exercise_volume'] = input_check(input('Your selection:\t'), 'num', [0, num-1])
            if user['exercise_volume'] == False:
                continue
            break
        # the program then creates a 32 digit user id number, if this user id number is the same as another profiles then it recreates a user id number       
        nums = 1
        id_check = True
        while True:
            user_id = ''
            while nums < 32:
                number = random.randrange(1, 9)
                user_id = user_id + str(number)
                nums+=1
            if len(users) != 0:
                for obs in users:
                    if user_id == obs['user_id']:
                        id_check = False
            if id_check != False:
                break
        # this user id number is then input into the user profile
        user['user_id'] = user_id
        # this new user is then saved to the user_data file in json format
        users.append(user)
        us = json.dumps(users, default=converter)
        with open('user_data.txt', 'w')as file:
            file.write(us)
        # a class instance for this user is created
        current_user = biomentric(user['user_id'], user['name'], user['gender'], user['age'], user['height'], user['weight'], user['ff_weight'], user['goals'], user['v_ve_me'], user['exercise_volume'])
        # and the main profile loaded variable is set to true, indicating that a profile has been loaded. 
        main_profile_loaded = False
        break

# after a profile has been loaded that main program begins
print(f'\n\nWelcome {current_user.return_name()} to your personal Auto-PT space.\n')
# the temp_check variable is created which will be used to inidcate weather there is a meal plan templated loaded
temp_check = 0
time.sleep(2)
while True:
    # the main menu of the program
    print("\n============\nMain Menu\n==========\n")
    print(f"1:\tView/edit biometric data\n2:\tNutrition menu")
    m_m_nav = input_check(input('Please select an option.\t'), 'num', [0,2])
    if m_m_nav == False:
        continue
    # this path allows the user to view and edit their biometric data
    if m_m_nav == 1:
        data_check = False
        while True:
            # the biometric data is printed then the user is given the option to edit the data or return to main menu
            current_user.print_biometric_info()
            bio_choice = input_check(input(f"\n1:\tEdit biometric data\nb:\tBack"), 'both', [[0, 1],['b']])
            if bio_choice == False:
                continue
            if bio_choice == 'b':
                if data_check == True:
                    current_user.new_biometric_data_addition()
                break
            elif bio_choice == 1:
                # if the user chooses to edit their biometric data then the class function edit_biometric_data() is called
                timtim = current_user.edit_biometric_data()
                # if the this function does not return False it itdicates the biometric data has been changed
                if timtim != False:
                    # if the data has been changed then the fucntion re_work_stats is called which reevaluates the nutrional data that is required for the meal plans
                    current_user.re_work_stats()
                    data_check = True
                continue
    # this path is for mealplans and other nutrition options
    if m_m_nav == 2:
        while True:
            # if there is no mealplan template loaded then the user has teh option to select a menu option
            if temp_check == 0:
                while True:
                    print('Nutrition Menu')
                    nute_nav = input_check(input('\n1:\tView recomended nutrition.\n2:\tMeal plans\n3:\tMeals/Recipes/Ingredients\nb:\tBack.\t'), 'both', [[0,3],['b']])
                    if nute_nav == False:
                        print('Unrecognised input')
                        continue
                    break
            # else altomatically the program selects to load the meal plans section
            else:
                nute_nav = 2
            if nute_nav == 'b':
                break
            # the option prints the data for recomended nutrition 
            elif nute_nav == 1:
                current_user.print_necessary_nut()
                input('')
                continue
            # this option is for creating mealplans and templates
            elif nute_nav == 2:
                # if there is no template loaded the user is given the option to select a menu option
                if temp_check == 0:
                    while True:
                        print('Meal Plans')
                        # this function checks if there are any templates saved in the user saved data file
                        if current_user.check_meal_plans('template') == False:
                            # if there arent the the user is direction to menu option one where they will create a template
                            print('You have no meal plans. Start by building a template.')
                            meal_nav = 1
                        # else they are given a choice to choose what menu option they would like to access
                        else:
                            meal_nav = input_check(input(f"\n1:\tCreate/edit meal plan templates.\n2:\tView/edit meal plans\nb:\tBack.\t"), 'both', [[0, 2],['b']])   
                        if meal_nav == False:
                            continue
                        # before the user carries on to their choice the template variable is reset to 0 to prevent any errors in the next sections
                        template = 0
                        break
                # if there is a template loaded then the users is directed towards menu option 2
                else:
                    meal_nav = 2
                if meal_nav == 'b':
                    break
                # this menu option is for creating new meal plan templates. 
                if meal_nav == 1:
                    while True:
                        # this function checkks if there are templates in the user saved data, if there are then the user is allowed to choose from teh menu
                        if current_user.check_meal_plans('template') == True: 
                            meal_choice = input_check(input(f"\n1:\tCreate new template.\n2:\tEdit template.\nb:\tBack.\t"), 'both', [[0, 2],['b']])
                        # if not then the user is directed towards the menu option for creating new templates
                        else:
                            meal_choice = 1
                        if meal_choice == False:
                            continue
                        break
                    if meal_choice == 'b':
                        break
                    # the menu option calls teh class funciton that creates new meal plan templates and assigns them to the variable template
                    if meal_choice == 1:
                        template = current_user.meal_plan_template_genorator()
                    # this menu option allows users to edit meal plan templates
                    if meal_choice == 2:
                        # it begins by loading a template from the saved data with the load_meal_plans class function
                        template = current_user.load_meal_plans('template')
                        if template == False:
                            continue
                        # the are then given the options to edit or delete this template
                        while True:
                            lm = input_check(input("\nWhat would you like to do.\n1:\tEdit template.\n2:\tDelete Template.\nb:\tBack.\t"), 'both', [[0,2],['b']])
                            if lm == False:
                                continue
                            break
                        if lm == 'b':
                            continue
                        # option one edits the meal plan templates
                        if lm == 1:
                            # the meal_plan_template_genorator() is called with the template entered as an argurment
                            template = current_user.meal_plan_template_genorator(template)
                        # this option is for deleting templates
                        else:
                            print('\nPlease check the template before you delete it.')
                            # this function prints the template
                            current_user.meal_plan_print(template)
                            # the user is then asked to confirm if they want to delete the template
                            while True:
                                check_choice = input_check(input('\nAre you sure you want to delete this template.\t'), 'other')
                                if check_choice == False:
                                    continue
                                break
                            # if they confirm yes then the delete_meal_plan function is called with the template and the string 'template' as arguemnts
                            if check_choice in ['y', 'yes']:
                                current_user.delete_meal_plan(template, 'template')
                            break
                    # here after the templates have been created the user is given the choice to immediately create a mael plan from this template or to return to the main menu
                    while True:
                        i = input_check(input('\nHow would you like to proceed.\n1:\tEdit this plan.\nb:\tReturn to menu'), 'both', [[0, 1],['b']])
                        if i == False:
                            continue
                        break
                    # if they select they want to turn it into a meal plan then the variable temp_check is equal to 1, if not then the template variable is equal to 0
                    if i == 1:
                        temp_check = 1
                    else:
                        template = 0
                    continue
                
                
                if meal_nav == 2:
                    while True:
                        exit_note =0
                        temp_check = 0
                        if template == 0:
                            if current_user.check_meal_plans('template') == False:
                                print('\nYou must create a meal plan template first.')
                                break
                            else:
                                while True:
                                    if current_user.check_meal_plans() == False:
                                        temp_choice = 1
                                    else:
                                        temp_choice = input_check(input("\n1:\tCreate meal plan from template.\n2:\tLoad saved meal plan.\nb:\tBack."), 'both', [[0, 2],['b']])
                                    if temp_choice == False:
                                        continue
                                    break
                                if temp_choice == 'b':
                                    break
                                if temp_choice == 1:
                                    print('\nPlease select a template to load.')
                                    templat = current_user.load_meal_plans('template')
                                    if templat == False:
                                        continue
                                    exit_note = 1
                                    break

                                elif temp_choice == 2:
                                    while True:
                                        if current_user.check_meal_plans() == False:
                                            print('You have no meal plans to load')
                                            break
                                        print('\nPlease select a meal plan to load.')
                                        temp = current_user.load_meal_plans()
                                        if temp == False:
                                            break
                                        current_user.meal_plan_print(temp)
                                        while True:
                                            mp_check = input_check(input('Are you happy with this meal plan?\t'), 'other')
                                            if mp_check == False:
                                                continue
                                            break
                                        if mp_check.lower() in ['n', 'no']:
                                            continue
                                        
                                        while True:
                                            print('What would you like to do with this meal plan?')
                                            while True:
                                                meal_plan_opt = input_check(input('1:\tEdit meal plan.\n2:\tUpdate with current Biometrics.\n3:\tCalculate cost.\n4\tDelete meal plan.\nb:\tBack.\t'), 'both', [[0,4], ['b']])
                                                if meal_plan_opt == False:
                                                    continue
                                                break
                                            if meal_plan_opt == 'b':
                                                break
                                            if meal_plan_opt == 1:
                                                exit_note = 1
                                                break
                                            elif meal_plan_opt == 2:
                                                while True:
                                                    choice_bio = input_check(input('Are you sure you want to update this meal plan?'), 'other')
                                                    if choice_bio == False:
                                                        continue
                                                    break
                                                if choice_bio.lower() in ['n', 'no']:
                                                    continue
                                                temp = current_user.update_meal_plan_biometrics(temp)
                                                for days in temp:
                                                    if days not in ['name', 'date']:
                                                        temp[days] = current_user.meal_meal_recalc(temp[days], 'on')
                                                current_user.meal_plan_print(temp)
                                            elif meal_plan_opt == 3:
                                                current_user.meal_plan_price_calculator(temp)
                                            elif meal_plan_opt == 4:
                                                while True:
                                                    mp_del_check = input_check(input('Are you sure you want to delete this meal plan?\t'), 'other')
                                                    if mp_del_check == False:
                                                        continue
                                                    break
                                                if mp_del_check.lower() in ['y', 'yes']:
                                                    current_user.delete_meal_plan(temp, 'complete')
                                                    temp = None
                                        if exit_note == 1:
                                            break      
                                    templat = 0
                                    if temp == 'False':
                                        continue
                                    if exit_note == 1:
                                        break       
                        else:
                            t_name = template['name']
                            templat = current_user.load_specific_template(t_name)
                            exit_note = 1
                            break

                    if exit_note == 0:
                        continue
                    if templat != 0:
                        temp = deepcopy(templat)
                        print(f"This template is called:\n{templat['name']}")
                        if current_user.check_meal_plan_name_validity(templat['name'], 'complete') == False:
                            print('Please choose another name for the meal plan.')
                            force_num = 'n'
                        else:
                            while True:
                                force_num = input_check(input('Would you like to keep this name:\t'), 'other')
                                if force_num == False:
                                    continue
                                break
                        if force_num in ['n', 'no']:
                            while True:
                                name = input('This meal plan shall be called:\t')
                                if current_user.check_meal_plan_name_validity(name, 'complete') == False:
                                    continue
                                temp['name'] = name
                                break
                    while True:
                        current_user.save_meal_template(temp, 'complete')
                        print('\nMeal plan editing menu.\n')
                        time.sleep(2)
                        current_user.meal_plan_print(temp)
                        while True:
                            me_ch = input_check(input('\nHow would you like to edit this meal plan.\n1:\tEdit name\n2:\tSelect day to edit.\nb:\tFinish editing meal plan.\t'), 'both', [[0,3], ['b']])
                            if me_ch == False:
                                continue
                            break
                        if me_ch == 'b':
                            break
                        elif me_ch == 1:
                            while True:
                                name = input('\nWhat would you like to change the name to?\t')
                                if current_user.check_meal_plan_name_validity(name, 'complete') == False:
                                    continue
                                old_name = {'name': temp['name']}
                                temp['name'] = name
                                current_user.delete_meal_plan(old_name, 'complete')
                                current_user.save_meal_template(temp, 'complete')
                                
                                
                                break
                        elif me_ch == 2: 
                            while True:
                                day_lst = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                                print('What day would you like to edit?')
                                for days in day_lst:
                                    print(f"{day_lst.index(days)+1}:\t{days}")
                                print("b:\tBack")
                                while True:
                                    day_choice = input_check(input('Your choice.\t'), 'both', [[0,7], ['b']])
                                    if day_choice == False:
                                        continue
                                    break
                                if day_choice == 'b':
                                    break
                                else:
                                    day_choice = int(day_choice)
                                while True: 
                                    temp[day_lst[day_choice-1]] = current_user.meal_meal_recalc(temp[day_lst[day_choice-1]])
                                    current_user.save_meal_template(temp, 'complete')
                                    print(f"\nEditing {day_lst[day_choice-1]}")
                                    current_user.meal_plan_print(temp, [day_lst[day_choice-1]])
                                    num = 0
                                    for meals in temp[day_lst[day_choice-1]]:
                                        if meals in ['on_off', 'meal nutes', 'rec meal nutes']:
                                            pass
                                        else:
                                            print(f"{meals}:\t{temp[day_lst[day_choice-1]][meals]['name']}")
                                            num += 1
                                    print("b:\tBack")
                                    while True:
                                        meal_select = input_check(input('What meal would you like to edit?\t'), 'both', [[0, num], ['b']])
                                        if meal_select == False:
                                            continue
                                        if meal_select != 'b':
                                            meal_select = str(int(meal_select))
                                        break
                                    if meal_select == 'b':
                                        break
                                    try:
                                        print(f"\nYou are editing:\n{day_lst[day_choice-1]}'s meal {meal_select}:\t{temp[day_lst[day_choice-1]][meal_select]['name']}")
                                    except KeyError:
                                        meal_select = int(meal_select)
                                        print(f"\nYou are editing:\n{day_lst[day_choice-1]}'s meal {meal_select}:\t{temp[day_lst[day_choice-1]][meal_select]['name']}")
                                    current_user.meal_plan_print(temp, [day_lst[day_choice-1]], [meal_select])
                                    if temp[day_lst[day_choice-1]][meal_select]['meal']['name'] != '0_none_0':
                                        while True:
                                            tempt = input_check(input('\nThis meal already contains a meal.\nWould you like to\n1:\tOverwrite meal data.\n2:\tEdit meal data.\n'), 'num', [0,2])
                                            if tempt == False:
                                                continue
                                            break
                                    else:
                                        tempt = 1
                                        
                                    if tempt == 2:
                                        llp = current_user.meal_dic_creator('meal', temp[day_lst[day_choice-1]][meal_select]['meal'], temp[day_lst[day_choice-1]][meal_select]['meal'])
                                        if llp == False:
                                            continue
                                        while True:
                                            save_choice = input_check(input('Would you like to save these changes to this meal?\t'), 'other')
                                            if save_choice == False:
                                                continue
                                            break
                                        if save_choice.lower() in ['y', 'yes']:
                                            current_user.delete_meals_rec_ingre(llp, 'meals')
                                            current_user.save_recipe_meal_ingredient(llp, 'meal')
                                        temp[day_lst[day_choice-1]][meal_select]['meal'] = llp
                                        
                                        
                                    elif tempt == 1:    
                                        if current_user.check_meal_fillers('meals') == False:
                                            print('\n1:\tCreate new meals\n2:\tLoad saved meals\nb:\tBack')
                                            while True:
                                                meal_choice = input_check(input('Please make your selection?\t'), 'both', [[0,2],['b']])
                                                if meal_choice == False:
                                                    continue
                                                break
                                            if meal_choice == 'b':
                                                break
                                        else:
                                            meal_choice = 1
                                        if meal_choice == 2:
                                            llp = current_user.return_meal_option_input('meal', 1)
                                            if llp == False:
                                                continue
                                            temp[day_lst[day_choice-1]][meal_select]['meal'] = llp           
                                        if meal_choice == 1:
                                            llp = current_user.meal_dic_creator('meal', day_nute_dic= temp[day_lst[day_choice-1]][meal_select]['rec meal nutes'])
                                            if llp == False:
                                                continue                                       
                                            temp[day_lst[day_choice-1]][meal_select]['meal'] = llp                                            
                                            current_user.save_recipe_meal_ingredient(llp,'meal')
                                    temp[day_lst[day_choice-1]][meal_select]['meal nutes'] = temp[day_lst[day_choice-1]][meal_select]['meal']['nutes'] 
            elif nute_nav == 3:
                while True:
                    print('Meals/Recipes/Ingredients Menu')
                    while True:
                        m_r_i_nav = input_check(input('1:\tMeals\n2:\tRecipes\n3:\tIngredients\nb:\tBack\t'), 'both', [[0,3],['b']])
                        if m_r_i_nav == False:
                            print('Unrecognised input')
                            continue
                        break
                    if m_r_i_nav == 'b':
                        break
                    elif m_r_i_nav == 1:
                        while True:
                            print('Meals')
                            if current_user.check_meal_fillers('meals') == False:
                                while True:
                                    meals_nav = input_check(input('1:\tCreate new meal.\n2:\tView previous meals.\nb:\tBack.'), 'both', [[0, 2],['b']])
                                    if meals_nav == False:
                                        print('Unrecognised input.')
                                        continue
                                    break
                            else:
                                while True:
                                    meals_nav = input_check(input('1:\tCreate new meal.\nb:\tBack.'), 'both', [[0,1],['b']])
                                    if meals_nav == False:
                                        print('Unrecognised input.')
                                        continue
                                    break
                            if meals_nav == 'b':
                                break
                            elif meals_nav == 1:
                                meall = current_user.meal_dic_creator('meal')
                                current_user.save_recipe_meal_ingredient(meall, 'meal')
                            elif meals_nav == 2:
                                while True:
                                    print('Meals database.')
                                    meall = current_user.return_meal_option_input('meal', 'in')
                                    if meall == False:
                                        break
                                    current_user.print_meal_individual(meall)
                                    while True:
                                        print('What would you like to do with this meal?')
                                        single_m_check = input_check(input('1:\tEdit meal.\n2:\tDelete meal.\nb:\tBack.'), 'both', [[0,2],['b']])
                                        if single_m_check == False:
                                            print('Unrecognised input')
                                            continue
                                        break
                                    if single_m_check == 'b':
                                        continue
                                    elif single_m_check == 1:
                                        mel = deepcopy(meall)
                                        meall = current_user.meal_dic_creator('meal', meall)
                                        current_user.delete_meals_rec_ingre(mel, 'meals')
                                        current_user.save_recipe_meal_ingredient(meall, 'meal')
                                    elif single_m_check == 2:
                                        print(f'You are considering deleting the meal {meall["name"]}.')
                                        while True:
                                            del_check = input_check(input('Are you sure you want to delete this meal?\t'), 'other')
                                            if del_check == False:
                                                print('Unrecognised input.')
                                                continue
                                            break
                                        if del_check.lower() in ['n', 'no']:
                                            continue
                                        else:
                                            current_user.delete_meals_rec_ingre(meall, 'meals')
                    elif m_r_i_nav == 2:
                        while True: 
                            print('Recipes')
                            while True:
                                if current_user.check_meal_fillers('recipies') == False:
                                    rec_nav = input_check(input('1:\tCreate new recipe.\n2:\tView previous recipes.\nb:\tBack.'), 'both', [[0, 2], ['b']])
                                    if rec_nav == False:
                                        print('Unrecognised input.')
                                        continue
                                    break
                                else:
                                    rec_nav = input_check(input('1:\tCreate new recipe.\nb:\tBack.'), 'both', [[0,1],['b']])
                                    if rec_nav == False:
                                        print('Unrecognised input.')
                                        continue
                                    break
                            if rec_nav == 'b':
                                break
                            elif rec_nav == 1:
                                recc = current_user.meal_dic_creator('recipe')
                                current_user.save_recipe_meal_ingredient(recc, 'recipe')
                            elif rec_nav == 2:
                                while True:
                                    print('Meals databse.')
                                    recc = current_user.return_meal_option_input('recipies', 'in')
                                    if recc == False:
                                        break
                                    current_user.print_recipe_individual(recc)
                                    while True:
                                        print('What would you like to do with this recipe?')
                                        single_r_check = input_check(input('1:\tEdit recipe.\n2:\tDelete recipe.\nb:\tBack.'), 'both', [[0,2], ['b']])
                                        if single_r_check == False:
                                            print('Unrecognised input')
                                            continue
                                        break
                                    if single_r_check == 'b':
                                        continue
                                    elif single_r_check == 1:
                                        re = deepcopy(recc)
                                        recc = current_user.meal_dic_creator('recipe', recc)
                                        current_user.delete_meals_rec_ingre(re, 'recipies')
                                        current_user.save_recipe_meal_ingredient(recc, 'recipe')
                                    elif single_r_check == 2:
                                        print(f"You are considering deleting the recipe {recc['name']}.")
                                        while True:
                                            re_check = input_check(input('Are you sure you want to delete this recipe?\t'), 'other')
                                            if re_check == False:
                                                print('Unrecognised input.')
                                                continue
                                            break
                                        if re_check.lower() in ['n', 'no']:
                                            continue
                                        else:
                                            current_user.delete_meals_rec_ingre(recc, 'recipies')
                                            
                    elif m_r_i_nav == 3:
                        while True:
                            print('Ingredients')
                            while True: 
                                if current_user.check_meal_fillers('ingredients') == False:
                                    ingre_nav = input_check(input('1:\tCreate new ingredient.\n2:\tView previous ingredients.\n3:\tUpdate saved ingredient nutrition.\nb:\tBack.\t'), 'both', [[0,3],['b']])
                                    if ingre_nav == False:
                                        print('Unrecognised input.')
                                        continue
                                    break
                                else:
                                    ingre_nav = input_check(input('1:\tCreate new recipe.\nb:\tBack.'), 'both', [[0,1],['b']])
                                    if ingre_nav == False:
                                        print('Unrecognised input.')
                                        continue
                                    break
                            if ingre_nav == 'b':
                                break
                            elif ingre_nav == 1:
                                ingred = current_user.meal_dic_creator('ingredient', 10)
                                if ingred == False:
                                    continue
                                if ingred[2] == False and ingred[3] == False:
                                    current_user.save_recipe_meal_ingredient(ingred[1], 'ingredient')
                                else:
                                    current_user.save_recipe_meal_ingredient(ingred[1], 'ingredient', ingred[2], ingred[3])
                            elif ingre_nav == 2:
                                while True:
                                    print('Ingredients database.')
                                    ingred = current_user.return_meal_option_input('ingredients', 'in', 'in')
                                    if ingred == False:
                                        break
                                    current_user.print_ingre_indiv(ingred[0])
                                    while True:
                                        print('What would you like to do with this recipe?')
                                        single_i_check = input_check(input('1:\tDelete ingredient.\nb:\tBack.\t'), 'both', [[0,1],['b']])
                                        if single_i_check == False:
                                            print('Unrecognised input')
                                            continue
                                        break
                                    if single_i_check == 'b':
                                        continue
                                    elif single_i_check == 1:
                                        print(f"You are considering deleting the recipe {ingred[0]['name']}.")
                                        while True:
                                            ing_check = input_check(input('Are you sure you want to delete this ingredient?\t'), 'other')
                                            if ing_check == False:
                                                print('Unrecognised input.')
                                                continue
                                            break
                                        if ing_check.lower() in ['n', 'no']:
                                            continue
                                        else:
                                            if ingred[1] in ['False', False] and ingred[2] in ['False', False]:
                                                current_user.delete_meals_rec_ingre(ingred[0], 'ingredients')
                                            else:
                                                current_user.delete_meals_rec_ingre(ingred[0], 'ingredients', [ingred[1], ingred[2]])
                            elif ingre_nav == 3:     
                                print("Confirm that you would like to update all supermarket ingredients with most recent supermarket data.\nThis may take some time.")
                                while True:
                                    update_check = input_check(input('Are you sure you want to update now?\t'), 'other')
                                    if update_check == False:
                                        print('Unrecognised input.')
                                        continue
                                    break
                                if update_check.lower() in ['n', 'no']:
                                    continue
                                update_check = current_user.full_update_saved_ingredents()
                                if update_check != False:
                                    print('Update completed.')

                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                
            

            
                            
                                
                                    
                                
                                                




# rejig calc crash
# time to move onto exercise genorator. 
# while going over make extensive notes to point people to what each part of the code does

# create scrape functions to pull other ingredients from other sites.