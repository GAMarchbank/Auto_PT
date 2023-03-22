import json
import requests
from nutritionix import Nutritionix
import datetime
import os
import random
import time
from copy import deepcopy


nix = Nutritionix(app_id = 'c6568ef8', api_key = '058a5f2f45eb89a68db36703c6ec16f2')

# 1: inp = input, tp = type of check ['num'(default), 'both', 'other'], check_lst = for num [range low, range high] defult is no range, for mix [[range low, range high], [string check list]], for other [string check list]
def input_check(inp, tp = 'num', check_lst = 0):
    try:
        if tp == 'num':
            if check_lst != 0:
                if float(inp) not in range(check_lst[0]+1, check_lst[1]+1):
                    print('Input error')
                    return 'False'
                else:
                    return float(inp)
            else:
                return float(inp)
        elif tp == 'both':
            open_lst = []
            for numbs in range(check_lst[0][0]+1, check_lst[0][1]+1):
                open_lst.append(str(numbs))
            for let in check_lst[1]:
                open_lst.append(let)
            kal = True
            if inp not in open_lst:
                kal = False
                try:
                    if inp.lower() in open_lst:
                        kal = True
                    else:
                        pass
                except:
                    pass
            if kal == True:
                if inp not in check_lst[1]:
                    return float(inp)
                else:
                    return inp.lower()
            else:
                print('Input error')
                return 'False'   
        else:
            if check_lst == 0:
                check_lst = ['y', 'n', 'no', 'yes']
            if inp.lower() not in check_lst:
                print('Input error')
                return 'False'
            else:
                return inp.lower() 
    except Exception:
        print('Input error')
        return 'False'

# takes in lst which is a list of the items to be iterated, lst can be lst of dictionarys made of keys for item to print with fist key under value 'init'
def lst_interation(lst):
    lower_range = 0
    if len(lst) >=10:
        upper_range = 10
    else:
        upper_range = len((lst))+1
    while True:
        check = 0
        for number in range(lower_range, upper_range):
            try:
                if type(lst[number]) == dict:
                    for keys in lst[number]:
                        if keys == 'init':
                            print(f"{number+1}:\t{lst[number][keys]}")
                        else:
                            print(f"\t{keys}:\t{lst[number][keys]}")
                else:    
                    print(f"{number+1}:\t{lst[number]}")
            except Exception:
                check += 1
        if lower_range != 0:
            print(f"p:\tPrevious Page")
        if check == 0:
            print(f"n:\tNext page")
        print(f"b:\tBack.")
        iam = input('Select an item or exit menu.\t')
        iam = input_check(iam, 'both', [[lower_range, upper_range], ['p', 'n', 'b']])
        if iam == 'False':
            continue        
        if iam == 'b':
            return 'False'
        elif check == 0 and iam == 'n':
            print('Next page')
            lower_range += 10
            upper_range += 10
            continue
        elif lower_range != 0 and iam == 'p':
            print('Previous page')
            lower_range -= 10
            upper_range -= 10
            continue 
        return lst[int(iam)-1] 
  
def time_sort(check):
    times_lst = []
    for items in check:
        times_lst.append(str(items['date']))
    times_lst = sorted(times_lst, reverse=True)
    meals_dic = []
    for times in times_lst:
        for items in check:
            if times == items['date']:
                meals_dic.append(items['name'])
    return meals_dic

def volume_of_rec_calc(whole_rec):
    whole_vol = 0
    for ingre in whole_rec['ingredients']:
        whole_vol += ingre['volume']
    return whole_vol
  
#saves file, data = self.user_saved_data, path = self.used_foods_database_path
def save_data(data, path):
    file = json.dumps(data, default=converter)
    with open(path, 'w') as fil:
        fil.write(file)
    with open(path, 'r') as fil:
        file = fil.read()
    file = json.loads(file)
    return file

def gram_converter(eys, energy= 0):
    to_be_check = []
    less_than_check = 0
    rep_lst = []
    keys = str(eys)
    if energy == 0:
        k = [keys]
    else:
        try:
            k = keys.split('/')
        except Exception:
            try:
                k = keys.split('()')
            except Exception:
                k = [keys]           
    for key in k:
        take_2 = deepcopy(key)
        try:
            key_lst = key.split('per ')
        except Exception:
            pass
        try:
            key_lst = key.split('Per ')
        except Exception:
            pass
        try: 
            key_lst = key.split(' Per')
        except Exception:
            pass
        try:
            key_lst = key.split(' per')
        except Exception:
            pass
        try:
            key_lst = key.split('er. ')
        except Exception:
            pass
        try:
            key = key_lst[1]
        except Exception:
            pass
        try:
            key_lsts = key.split('(')
            key = key_lsts[0]
        except Exception:
            pass
        num = ''
        weight = ''
        for letters in key:
            if letters in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ',']:
                num = num + letters
            else:
                weight = weight + letters
        num = num.replace(',', '.')
        try:
            num = float(num)
        except Exception:
            try:
                take_lst = take_2.split(')')
                try:
                    take = take_lst[1].split('per ')
                except Exception:
                    pass
                try:
                    take = take_lst[1].split('Per ')
                except Exception:
                    pass
                num = ''
                weight = ''
                for letters in take[1]:
                    if letters in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',', '.']:
                        num = num + letters
                    else:
                        weight = weight + letters    
                num = num.replace(',', '.')
                num = float(num)
            except Exception:
                try:
                    take_lst = take_2.split(' of')
                    num = ''
                    weight = ''
                    for letters in take_lst[0]:
                        if letters in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',', '.']:
                            num = num + letters
                        else:
                            weight = weight + letters    
                    num = num.replace(',', '.')
                    num = float(num)
                except Exception:
                    pass
        if weight.lower() in ['kg', ' kg', 'kg ']:
            num = num * 1000
        elif weight.lower() in ['lb', ' lb', 'lb ']:
            num = num * 453.59237
        elif weight.lower() in ['st', ' st', 'st ']:
            num = num * 6350.29318
        if energy == 0:
            if weight.lower() in ['kcal', ' kcal', 'kcal ', ' kcal ']:
                return [num, 'Energy indicator']
            rep_lst.append(num)
        elif energy != 0:
            if weight.lower() in ['kcal', ' kcal', 'kcal ', ' kcal ']:
                rep_lst.append(num)
            else:
                if bool(weight)== False:
                    to_be_check.append(num)
                pass
    if len(to_be_check) == len(k):
        rep_lst.append(to_be_check[1])
    return rep_lst[0]

def nute_sorter_ingredients_to_recipes(vol, data):
    key = gram_converter(data['key'])
    try:
        cals = data['data']['Energy kcal']
    except Exception:
        try:
            cals = data['data']['Kcal']
        except Exception:
            try:
                cals = data['data']['kcal']
            except Exception:
                try:
                    cals = data['data']['- kcal Calories']
                except Exception:
                    cals = 0
    try:
        prot = data['data']['Protein']
    except Exception:
        try:
            prot = data['data']['Protein g']
        except Exception:
            prot = 0
    try:
        fat = data['data']['Fat']
    except Exception:
        try:
            fat = data['data']['Fat g']
        except Exception:
            try:
                fat = data['data']['Fat, total']
            except Exception:
                try:
                    fat = data['data']['Total Fat']
                except Exception:
                    fat = 0
    if type(prot)== str:
        prot = 0
    if type(fat)== str:
        fat = 0 
    key_num = vol/key
    return {'calories': cals*key_num, 'protein': prot*key_num, 'fat': fat*key_num}

def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
    
def nute_fill_check(text):
    while True:
        l = input(text)
        try:
            float(l)
            break
        except Exception:
            print('Entry error.')
            continue
    return l

def nute_data_search_func():
    while True:
        print(f'Please select an option.\n1:\t\tSearch for information.\n2:\t\tEnter information manually.')
        im = input('Enter your selection.')
        try:
            if int(im) == 1:
                while True:
                    print('Search database for food by name.')
                    search = input('Search...')
                    objec = nix.search(search)
                    result = objec.json()
                    if len(result['hits']) == 0:
                        print('No results found. Try again.')
                        continue
                    else:
                        num = 1
                        for obs in result['hits']:
                            print(f"{num}:\t\t{obs['fields']['item_name']}")
                            num += 1
                        print(f'{num}:\t\t Back.')
                        re = input('Choose item.')
                        try:
                            chosen = result['hits'][int(re)-1]
                            print(f"You have chosen {chosen['fields']['item_name']}.")
                            confirm = input('Do you wish to continue.')
                            if confirm.lower() in ['y', 'yes']:
                                break
                            else:
                                continue
                        except Exception:
                            continue
                in_dic = {}
                out_dic = {}
                choose = nix.item(id=chosen['_id']).json()
                if type(choose['nf_serving_weight_grams']) == float or type(choose['nf_serving_weight_grams']) == int:
                    in_dic['key'] = str(choose['nf_serving_weight_grams']) + 'g'
                elif type(choose['nf_serving_size_qty']) == float or type(choose['nf_serving_size_qty']) == int:
                    editio = choose['nf_serving_size_qty']
                    if choose['nf_serving_size_unit'] == 'grams' or choose['nf_serving_size_unit'] == 'g':
                        ad = 'g'
                    elif choose['nf_serving_size_unit'] == 'kilograms' or choose['nf_serving_size_unit'] == 'kg':
                        editio = editio * 1000
                    elif choose['nf_serving_size_unit'] == 'ounces' or choose['nf_serving_size_unit'] == 'oz':
                        editio = editio * 28.3495231
                    elif choose['nf_serving_size_unit'] == 'stone' or choose['nf_serving_size_unit'] == 'st':
                        editio = editio * 6350.29318
                    in_dic['key'] = str(choose['nf_serving_size_qty']) + 'g'
                else:
                    in_dic['key'] = '1 item'
                cal = choose['nf_calories']
                jules = cal * 4.2142857
                out_dic['Energy kcal'] = cal
                out_dic['Energy kJ'] = jules
                out_dic['Fat'] = choose['nf_total_fat']
                out_dic['of which saturates'] = choose['nf_saturated_fat']
                out_dic['Carbohydrate'] = choose['nf_total_carbohydrate']
                out_dic['of which sugars'] = choose['nf_sugars']
                out_dic['Fibre'] = choose['nf_dietary_fiber']
                out_dic['Protein'] = choose['nf_protein']
                out_dic['Salt'] = choose['nf_sodium']
                in_dic['data'] = out_dic
                return(in_dic)
            elif int(im) == 2:
                while True:
                    out_dic = {}
                    in_dic = {}
                    print('Please manually enter the nutritional information')
                    key = nute_fill_check('Nutrition information per:\t')
                    out_dic['key'] = key
                    cal = nute_fill_check('Energy in kcal:\t\t\t')
                    jules = float(cal)* 4.2142857
                    print(f'Energy in kJ:\t\t\t{jules}')
                    fat = nute_fill_check('Total fat:\t\t\t')
                    saturates = nute_fill_check('of which saturates:\t\t')
                    carbs = nute_fill_check('Carbohydrates:\t\t\t')
                    sugars = nute_fill_check('of which sugars:\t\t')
                    fiber = nute_fill_check('Fiber:\t\t\t\t')
                    prot = nute_fill_check('Protein:\t\t\t')
                    salt = nute_fill_check('Salt:\t\t\t\t')
                    in_dic['Energy kcal'] = cal
                    in_dic['Energy kJ'] = jules
                    in_dic['Fat'] = fat
                    in_dic['of which saturates'] = saturates
                    in_dic['Carbohydrate'] = carbs
                    in_dic['of which sugars'] = sugars
                    in_dic['Fibre'] = fiber
                    in_dic['Protein'] = prot
                    in_dic['Salt'] = salt
                    out_dic['data'] = in_dic
                    print(f"Nutrition per:\t\t{out_dic['key']}")
                    for keys in out_dic['data'].keys():
                        print(f"{keys}:\t\t{out_dic['data'][keys]}")
                    lim = input('Is this info correct?')
                    if lim.lower() in ['y', 'yes']:
                        return out_dic
                    else:
                        while True:
                            nums = 1
                            lst = [out_dic['key']]
                            print(f"{nums}:\t\tNutrition per:\t\t\t{out_dic['key']}")
                            nums += 1
                            for keys in out_dic['data'].keys():
                                lst.append(keys)
                                print(f"{nums}:\t\t{keys}:\t\t\t{out_dic['data'][keys]}")
                                nums += 1
                            print(f"\n{nums}:\tContinue with this information")
                            jim = input('Select element to change, or confirm data.')
                            try:
                                if int(jim) in range(1, nums +1):
                                    pass
                                else:
                                    print('Input error.')
                                    continue
                            except Exception:
                                print('Input error.')
                                continue
                            if int(jim) == nums:
                                return out_dic
                            else:
                                if int(jim) - 1 == 0:
                                    out_dic['key'] = input('Editing\nNutrition per:\t')
                                else:
                                    da = lst[int(jim)-1]
                                    print(da)
                                    for keys in out_dic['data'].keys():
                                        if keys == lst[int(jim)-1]:
                                            out_dic['data'][keys] = input(f'Editing\t{keys}:\t')
            else:
                print('Unrecognised entry.')
                continue
        except Exception as e:
            print('Unrecognised entry.')
            print(e)
            continue
        
# all meals = total number of daily meals, main_meals = number of main meals. p_shakes = number of protein shakes, snacks = number of snacks    
def meal_plan_meal_alocator(all_meals, main_meals, p_shakes, snacks):
    mm_dic = {}
    for numbers in range(1, all_meals+1):
        menu_dic = {'Main Meal': main_meals, 'Snack': snacks, 'Protein Shake': p_shakes}
        lst = []
        for keys in menu_dic:
            if menu_dic[keys] > 0:
                lst.append(keys)
        print(f"Meals left:\nMain Meals:\t{main_meals}\tSnacks:\t{snacks}\tProtein Shakes:\t{p_shakes}")
        print(f"Meal {numbers}:")
        for sp_meal in lst:
            print(f"{lst.index(sp_meal)+1}:\t\t{sp_meal}")
        while True:
            tp = input_check(input('What is this meal?\t'), 'num', [0, len(lst)])
            if tp == 'False':
                continue
            tp = int(tp)
            break
        if lst[tp-1] == 'Main Meal':
            if main_meals == 3:
                mm_dic[numbers] = 'Breakfast'
                main_meals -= 1
            elif main_meals == 2:
                mm_dic[numbers] = 'Lunch'
                main_meals -= 1
            elif main_meals == 1:
                mm_dic[numbers] = 'Dinner'
                main_meals -= 1
        elif lst[tp-1] == 'Snack':
            mm_dic[numbers] = 'Snack'
            snacks -=1
        elif lst[tp-1] == 'Protein Shake':
            mm_dic[numbers] = 'Protein Shake'
            p_shakes -= 1
    return mm_dic      

def food_search(supermarket_choice, food_search):
    return_prod = []
    if supermarket_choice == 'Asda':
        with open('asda_data_nut.txt', 'r')as file:
            asda = file.read()
        super_dic = json.loads(asda)
    for products in super_dic.keys():
        try:
            products_lst = []
            products_ls = products.split(' ')
            for produ in products_ls:
                products_lst.append(produ.lower())
        except Exception:
            products_lst = [products.lower()]
        check = 0
        for words in food_search.split(' '):
            if words not in products_lst:
                check +=1
            else:
                pass
        if check == 0:
            return_prod.append(products)
    if len(return_prod) == 0:
        return False
    while True:
        num = 1
        for product in return_prod:
            print(f'{num}:\t\t{product}')
            num += 1
        try:
            im = int(input('Select product. ')) -1
            returned = return_prod[im]
        except Exception: 
            print('Unrecognised entry.')
            continue
        print(f'You have selected:\t\t{returned}')
        l = input('Did you mean to select this product.')
        if l.lower() in ['y', 'yes']:
            print('Item selected')
            break
        else:
            continue
    return returned

def return_nute_info(food):       
    with open('asda_data_nut.txt', 'r')as file:
        asda = file.read()
    asda_dic = json.loads(asda)
    if asda_dic[food]['nute']['data'] == 'None':
        print('No nutritional data availble.')
        lm = nute_data_search_func()
        nd = asda_dic[food]
        nd['nute'] = lm
        return [1, {food: nd}]
    else:
        return [2, {food: asda_dic[food]}]

def supermarket_search_data_sort(sup, vol = 'fail'):
    return_dic = {'key': 0, 'data': {}}
    for keys in sup:
        if keys == 'key':
            if vol == 'fail':
                return_dic['key'] = gram_converter(sup['key'])
                if type(return_dic['key']) == str:
                    return 'Fail'
            else:
                return_dic['key'] = gram_converter(vol)
        elif keys == 'data':
            for kes in sup[keys]:
                try:
                    if kes in  ['Energy','Energy - kJ/ kcal', 'Energy:', 'Energy kj/kcal', 'Energy /', 'Energy (kJ/kcal)', 'Energy (kJ/kcal):', 'Energy, kJ/kcal']:
                        try:
                            trim = gram_converter(sup[keys][kes], 'Energy')
                        except Exception:
                            trim = gram_converter(sup[keys][kes])
                    else: 
                        trim = gram_converter(sup[keys][kes])
                    if trim == False:
                        pass   
                    elif type(trim) == list:
                        return_dic['data']['Energy kcal'] = trim[0]
                    elif kes in ['Energy', 'Energy - kJ/ kcal', 'Energy:', 'Energy kj/kcal', 'Energy /', 'Calories', 'Energy (kJ/kcal)', 'Energy (kJ/kcal):', 'Energy, kJ/kcal']: 
                        return_dic['data']['Energy kcal'] = trim
                    else:
                        try:
                            kes = kes.replace('(', '')
                            kes = kes.replace(')', '')
                        except Exception:
                            pass
                        try:
                            kes = kes.replace(':', '')
                        except Exception:
                            pass
                        try:
                            kes = kes.replace(' /', '')
                        except Exception:
                            pass
                        return_dic['data'][kes] = trim 
                except ValueError:
                    pass
    return return_dic
          
class biomentric():
    def __init__(self, user_id, name, gender, age, height, weight, ff_weight, goals, v_ve_me, exercise_volume):
        self.shop_lst = ['Asda']
        self.name = name
        if gender.lower() in ['m', 'male']:
            self.gender = 'male'
        else:
            self.gender = 'female'
        self.age = age
        self.height = height
        self.weight = weight
        self.ff_weight = ff_weight
        self.goals = goals
        self.v_ve_me = v_ve_me
        self.required_protein = float(ff_weight) * 1.8
        if gender.lower() == 'male' or 'm':
            m = 88.4 + 13.4 * float(ff_weight)
            n = 4.8 * float(height)
            o = 5.68 * float(age)
            bmr = n + n - o
        else:
            m = 447.6 + 9.25 * float(ff_weight)
            n = 3.10 * float(height)
            o = 4.33 * float(age)
            bmr = m + n - o 
        self.bmr = bmr
        self.exercise_volume = exercise_volume
        if exercise_volume == 1:
            ex_v = 1.2
        elif exercise_volume == 2:
            ex_v = 1.375
        elif exercise_volume == 3:
            ex_v = 1.55
        elif exercise_volume == 4:
            ex_v = 1.725
        elif exercise_volume == 5:
            ex_v = 1.9
        self.required_calories = bmr * ex_v
        self.required_calories_off_day = self.required_calories - 200
        m = self.required_calories * 0.25
        self.required_fat = m / 9
        n = self.required_calories_off_day * 0.25
        self.required_fat_day_off = n / 9
        self.required_protein_cals = self.required_protein * 4
        l = self.required_calories - m
        o = self.required_calories_off_day - n
        self.required_carbs_cals = l - self.required_protein_cals
        self.required_carbs = self.required_carbs_cals / 4
        self.required_carbs_cals_off_day = o - self.required_protein_cals
        self.required_carbs_off_day = self.required_carbs_cals_off_day / 4
        self.req_prot_percent = self.required_protein_cals * 100 / self.required_calories
        self.req_carb_percent = self.required_carbs_cals * 100 / self.required_calories
        self.req_prot_percent_off_day = self.required_protein_cals * 100 / self.required_calories_off_day
        self.req_carb_persent_off_day = self.required_carbs_cals_off_day * 100 / self.required_calories_off_day
        self.user_id = user_id 
        self.used_foods_database_path = f'{user_id}_database.txt'
        self.exercise_dic = {1: 'strength(bulking)', 2: 'strength(cut)', 3: 'weight loss', 4: 'toning', 5: 'cardio traing', 6: 'general health'}
        self.dietary_dic = {1: 'None', 2: 'Vegetarian', 3: 'Vegan', 4: 'Pescitarian', 5: 'Keto', 6: 'Gulten Free'}
        self.exercise_volume_dic = {1: 'Little to no exercise', 2: 'Light exercise', 3: 'Moderate exercise', 4: 'Heavy exercise', 5: 'Extremely heavy exercise'}
        # with open('exercise_scrape_bodybuilding.txt', 'r')as file:
        #     ex = file.read()
        # self.exercise = json.loads(ex)
        
        try:
            with open(self.used_foods_database_path, 'r')as file:
                file= file.read()
            temp = json.loads(file)
            time_lst = []
            for time in temp['user biometrics database']:
                time_lst.append(time['end_date'])
            time_lst = sorted(time_lst, reverse=True)
            for users in temp['user biometrics database']:
                if users['end_date'] == time_lst[0]:
                    temp['user biometrics database'].remove(users)
                    users['end_data'] = datetime.datetime.now()
                    temp['user biometrics database'].append(users)
            self.user_saved_data = temp
        except Exception:
            fil = {'meal plans': {'complete': [], 'template': []}, 'foods database': {'supermarket products': {'Asda': {'user nute': [], 'store nute': []}, 'Tesco': {'user nute': [], 'store nute': []}, 'Sainsburys': {'user nute': [], 'store nute': []}, 'Morisons': {'user nute': [], 'store nute': []}}, 'user products': []},'meals database': [], 'recipies database': [], 'user biometrics database': [{'start_date': datetime.datetime.now(), 'end_date': datetime.datetime.now(), 'data': {'name': self.name, 'age': self.age, 'gender': self.gender, 'height': self.height, 'weight': self.weight, 'lean body mass': self.ff_weight, 'bmr': self.bmr, 'goals': self.goals, 'v_ve_me': self.v_ve_me, 'exercise volume': self.exercise_volume}}]}
            filp = json.dumps(fil, default= converter)
            with open(self.used_foods_database_path, 'w')as file:
                file.write(filp)
            with open(self.used_foods_database_path, 'r')as file:
                file = file.read()
            self.user_saved_data = json.loads(file)
    
    def re_work_stats(self):
        if self.gender.lower() == 'male' or 'm':
            m = 88.4 + 13.4 * float(self.ff_weight)
            n = 4.8 * float(self.height)
            o = 5.68 * float(self.age)
        else:
            m = 447.6 + 9.25 * float(self.ff_weight)
            n = 3.10 * float(self.height)
            o = 4.33 * float(self.age)
        self.bmr = m + n -o
        if self.exercise_volume == 1:
            ex_v = 1.2
        elif self.exercise_volume == 2:
            ex_v = 1.375
        elif self.exercise_volume == 3:
            ex_v = 1.55
        elif self.exercise_volume == 4:
            ex_v = 1.725
        elif self.exercise_volume == 5:
            ex_v = 1.9
        self.required_protein = float(self.ff_weight) * 1.8
        self.required_calories = self.bmr * ex_v
        self.required_calories_off_day = self.required_calories - 200
        m = self.required_calories * 0.25
        self.required_fat = m / 9
        n = self.required_calories_off_day * 0.25
        self.required_fat_day_off = n / 9
        self.required_protein_cals = self.required_protein * 4
        l = self.required_calories - m
        o = self.required_calories_off_day - n
        self.required_carbs_cals = l - self.required_protein_cals
        self.required_carbs = self.required_carbs_cals / 4
        self.required_carbs_cals_off_day = o - self.required_protein_cals
        self.required_carbs_off_day = self.required_carbs_cals_off_day / 4
        self.req_prot_percent = self.required_protein_cals * 100 / self.required_calories
        self.req_carb_percent = self.required_carbs_cals * 100 / self.required_calories
        self.req_prot_percent_off_day = self.required_protein_cals * 100 / self.required_calories_off_day
        self.req_carb_persent_off_day = self.required_carbs_cals_off_day * 100 / self.required_calories_off_day

    def delete_saved_data(self):
        os.remove(self.used_foods_database_path)

    def new_biometric_data_addition(self):
        self.user_saved_data['user biometrics database'].append({'start_date': datetime.datetime.now(), 'end_date': datetime.datetime.now(), 'data': {'name': self.name, 'age': self.age, 'gender': self.gender, 'height': self.height, 'weight': self.weight, 'lean body mass': self.ff_weight, 'bmr': self.bmr, 'goals': self.goals, 'v_ve_me': self.v_ve_me, 'exercise volume': self.exercise_volume}})
        self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)
        with open('user_data.txt', 'r')as file:
            user_data = file.read()
        user_data = json.loads(user_data)
        for users in user_data:
            if users['user_id'] == self.user_id:
                user_data.remove(users)
                users['name'] = self.name
                users['gender'] = self.gender
                users['age'] = self.age
                users['height'] = self.height
                users['weight'] = self.weight
                users['ff_weight'] = self.ff_weight
                users['goals'] = self.goals
                users['v_ve_me'] = self.v_ve_me
                users['exercise_volume'] = self.exercise_volume
                user_data.append(users)
        user_data = json.dumps(user_data)
        with open('user_data.txt', 'w') as file:
            file.write(user_data)
        self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)
       
    def edit_biometric_data(self):
        print('Please select the biometric data you would like to edit')
        print(f"1:\tName:\t\t\t\t{self.name}\n2:\tAge:\t\t\t\t{self.age}\n3:\tGender:\t\t\t\t{self.gender}\n4:\tHeight:\t\t\t\t{self.height}cm\n5:\tWeight:\t\t\t\t{self.weight}kg\n6:\tLean Body Mass:\t\t\t{self.ff_weight}kg")
        for keys in self.exercise_dic:
            if self.goals == keys:
                print(f"7:\tExercise Goals:\t\t\t{self.exercise_dic[keys]}")
        for keys in self.dietary_dic:
            if self.v_ve_me == keys:
                print(f"8:\tDietary Requirements:\t\t{self.dietary_dic[keys]}")
        for keys in self.exercise_volume_dic:
            if self.exercise_volume == keys:
                print(f"9:\tWeekly Exercise Volume:\t\t{self.exercise_volume_dic[keys]}")
        print('b:\tBack.')
        while True:
            choice = input('Select data.\t')
            try:
                if int(choice) not in range(1, 10):
                    print('Input error')
                    continue
                else:
                    break
            except Exception:
                if choice.lower() !='b':
                    print('Input error')
                    continue
                break
        if choice.lower() == 'b':
            return False
        if int(choice) == 1:
            self.name = input("Name:\t")
        elif int(choice) == 2:
            while True:
                age = input_check(input("Age:\t"), 'num')
                if age == 'False':
                    print('Unrecognised entry.')
                    continue
                self.age = age
                break
        elif int(choice) == 3:
            while True:
                gender = input_check(input('Gender:\t'), 'other', ['m', 'male', 'f', 'female'])
                if gender == 'False':
                    print('Unrecognised input.')
                    continue
                if gender in ['m', 'male']:
                    self.gender = 'male'
                else:
                    self.gender = 'female'
                self.gender = gender
                break
        elif int(choice) == 4:
            while True:
                height = input_check(input("Height:\t"), 'num')
                if height == 'False':
                    print('Unrecognised input.')
                    continue
                self.height = height
                break
        elif int(choice) == 5:
            while True:
                weight = input_check(input("Weight:\t"), 'num')
                if weight == 'False':
                    print('Unrecognised input')
                    continue
                self.weight = weight
                break
        elif int(choice) == 6:
            while True:
                ff_weight = input_check(input("Lean Body Mass:\t"), 'num')
                if ff_weight == 'False':
                    print('Unrecognised input.')
                    continue
                if ff_weight > self.weight:
                    print('It is impossible to weight more without fat.\nPlease try again.')
                    continue
                self.ff_weight = ff_weight
                break
        elif int(choice) == 7:
            while True:
                print('Select exercise goals.')
                for keys in self.exercise_dic:
                    print(f"{keys}:\t{self.exercise_dic[keys]}")    
                chip = input('Your selection:\t')
                try:
                    tm = self.exercise_dic[int(chip)]
                    self.goals = int(chip)
                    break
                except Exception:
                    print('Input error')
                    continue
        elif int(choice) == 8:
            while True:
                for keys in self.dietary_dic:
                    print(f"{keys}:\t{self.dietary_dic[keys]}")
                chip = input('Your selection:\t')
                try: 
                    tm = self.dietary_dic[int(chip)]
                    self.v_ve_me = int(chip)
                    break
                except Exception:
                    print('Input error')
                    continue
        elif int(choice) == 9:
            while True:
                print("Select the volume of weekly exercise you perform:")
                for keys in self.exercise_volume_dic:
                    print(f"{keys}:\t{self.exercise_volume_dic[keys]}")
                chip = input('Your selection:\t')
                try:
                    tm = self.exercise_volume_dic[int(chip)]
                    self.exercise_volume =  int(chip)
                    break
                except Exception:
                    print('Input error')
                    continue 
        
    def return_name(self):
        return self.name
    
    def print_biometric_info(self):
        print(f'Name:\t\t\t\t{self.name}\nAge:\t\t\t\t{self.age}\nGender:\t\t\t\t{self.gender}')
        print(f'Height:\t\t\t\t{self.height}cm\nWeight:\t\t\t\t{self.weight}kg\nLean Body Mass:\t\t\t{self.ff_weight}kg')
        print(f'Basal Metabolic Rate:\t\t{round(self.bmr)}cal')
        for keys in self.exercise_dic:
            if self.goals == keys:
                print(f"Exercise Goals:\t\t\t{self.exercise_dic[keys]}")
        for keys in self.dietary_dic:
            if self.v_ve_me == keys:
                print(f"Dietary Requirements:\t\t{self.dietary_dic[keys]}")
        for keys in self.exercise_volume_dic:
            if self.exercise_volume == keys:
                print(f"Weekly Exercise Volume:\t\t{self.exercise_volume_dic[keys]}")
            
    def return_biometric_info(self):
        return {'user_id': self.user_id, 'name': self.name, 'age': self.age, 'gender': self.gender, 'height': self.height, 'weight': self.weight, 'lean body mass': self.ff_weight, 'goals': self.goals, 'v_ve_me': self.v_ve_me, 'exercise volume': self.exercise_volume}
    
    def print_necessary_nut(self):
        print(f'Name:\t\t{self.name}\n')
        print('Gym Day\n')
        print(f'Required Calories:\t\t{round(self.required_calories)}cal')
        print(f'{round(self.req_prot_percent)}% Protein:\t\t{round(self.required_protein)}g')
        print(f'{round(self.req_carb_percent)}% Carbohydrates:\t{round(self.required_carbs)}g\t{round(self.required_carbs_cals)}cal')
        print(f'25% Fat:\t\t{round(self.required_fat)}g\n')
        print('Off Day\n')
        print(f'Required Calories:\t\t{round(self.required_calories_off_day)}cal')
        print(f'{round(self.req_prot_percent_off_day)}% Protein:\t\t{round(self.required_protein)}g')
        print(f'{round(self.req_carb_persent_off_day)}% Carbohydrates:\t{round(self.required_carbs_off_day)}g\t{round(self.required_carbs_cals_off_day)}cal')
        print(f'25% Fat:\t\t{round(self.required_fat_day_off)}g')
        
    def check_meal_plans(self, specify = 0):
        if specify == 0:
            if len(self.user_saved_data['meal plans']['complete']) == 0:
                return 'False'
            else:
                return 'True'
        elif specify == 'template':
            if len(self.user_saved_data['meal plans']['template']) == 0:
                return 'False'
            else:
                return 'True'
    
    def check_meal_fillers(self, choice):
        if choice == 'ingredients':
            num = 0
            store_dic = ['Asda', 'Morisons', 'Sainsburys', 'Tesco']
            lp_dic = ['store nute', 'user nute']
            for stores in store_dic:
                for lp in lp_dic:
                    if len(self.user_saved_data['foods database']['supermarket products'][stores][lp]) != 0:
                        num += 1
            if len(self.user_saved_data['foods database']['user products']) != 0:
                num += 1
            if num != 0:
                return 'False'
            else:
                return 'True'            
        elif choice == 'recipies':
            if len(self.user_saved_data['recipies database']) != 0:
                return 'False'
            else:
                return 'True'
        else:
            if len(self.user_saved_data['meals database']) != 0:
                return 'False'
            else:
                return 'True'
                
            
    
    # call with meal plan first, then list of days you want to view (none if want to view all), then list of meals to view (none if you want to view all)
    def meal_plan_print(self, meal_plan, day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], meal = 0):
        print("\n\n")
        if len(day) == 7:
            print(f"{self.name}'s Meal Plan:\t{meal_plan['name']}")
        else:
            day_str = ''
            for days in day:
                day_str = day_str + '\t' + days
            print(f"{self.name}'s Meal Plan")
            print(f"Showing:" + day_str)
        for days in day:
            try:
                main_string = f"\nDaily Calories:\t{round(meal_plan[days]['meal nutes']['calories'])}/{round(meal_plan[days]['rec meal nutes']['calories'])}\t\tProtein:\t{round(meal_plan[days]['meal nutes']['protein'])}/{round(meal_plan[days]['rec meal nutes']['protein'])}\t\tFat:\t{round(meal_plan[days]['meal nutes']['fat'])}/{round(meal_plan[days]['rec meal nutes']['fat'])}\n"
            except Exception:
                main_string = f"\nDaily Calories:\t{round(meal_plan[days]['rec meal nutes']['calories'])}\t\tProtein:\t{round(meal_plan[days]['rec meal nutes']['protein'])}\t\tFat:\t{round(meal_plan[days]['rec meal nutes']['fat'])}\n"
            if meal_plan[days]['on_off'] == 'on':
                print(f"\n\t\t{days}\t\t\tWorkout-Day" + main_string)
            else:
                print(f"\n\t\t{days}\t\t\tRest-Day" + main_string)
            for keys in meal_plan[days]:
                if meal == 0 or keys in meal:
                    if keys in ['on_off', 'meal nutes', 'rec meal nutes']:
                        pass
                    else:
                        print(f"\n{keys}:\t{meal_plan[days][keys]['name']}")
                        if meal_plan[days][keys]['meal nutes']['calories'] >= meal_plan[days][keys]['rec meal nutes']['calories']:
                            cal_str = round(meal_plan[days][keys]['meal nutes']['calories'])
                        else: 
                            cal_str = f"{round(meal_plan[days][keys]['meal nutes']['calories'])}/{round(meal_plan[days][keys]['rec meal nutes']['calories'])}"
                        if meal_plan[days][keys]['meal nutes']['protein'] >= meal_plan[days][keys]['rec meal nutes']['protein']:
                            prot_str = round(meal_plan[days][keys]['meal nutes']['protein']) 
                        else:
                            prot_str = f"{round(meal_plan[days][keys]['meal nutes']['protein'])}/{round(meal_plan[days][keys]['rec meal nutes']['protein'])}"
                        if meal_plan[days][keys]['meal nutes']['fat'] >= meal_plan[days][keys]['rec meal nutes']['fat']:
                            fat_str = round(meal_plan[days][keys]['meal nutes']['fat'])
                        else:
                            fat_str = f"{round(meal_plan[days][keys]['meal nutes']['fat'])}/{round(meal_plan[days][keys]['rec meal nutes']['fat'])}"
                        print(f"\tCalories:\t{cal_str}\tProtein:\t{prot_str}\tFat:\t{fat_str}")
                        if meal_plan[days][keys]['meal']['name'] != '0_none_0':
                            print(f"\t- {meal_plan[days][keys]['meal']['name']}")
                            for recipies in meal_plan[days][keys]['meal']['recipies']:
                                print(f"\t\t- {recipies['name']}\t\t{recipies['serving size']}\n\t\tCals:\t{round(recipies['nutes']['calories'])}\tProt:\t{round(recipies['nutes']['protein'])}\tFat:\t{round(recipies['nutes']['fat'])}")
                                for ingredients in recipies['ingredients']:
                                    print(f"\t\t\t- {ingredients['name']}\t\t{ingredients['volume']}")
            print("\n\n")
    
    # this funciton takes in the number of various meals in the day of the meal plan and outputs the correct recomended nutrition, either to match the empty plan, or to fill the remaining nutrition
    def rejig_calc(self, snack_num, main_meal_num, scoop_num, p_shake_num, opt_dic = 0):
        # the opt dic is automatically the nutrtion for the biometric profile of the user, if the meal plan already has nutrition however it will use that nutrition
        if opt_dic == 0:
            opt_dic = {'required protein': self.required_protein, 'required calories': self.required_calories, 'required calories off day': self.required_calories_off_day, 'required fat': self.required_fat, 'required fat off day': self.required_fat_day_off}        
        base_powder_prot_per_scoop = 10.5     
        # here begins the while loop to select the correct amont of protein shake the user should be taking to complete the plan, if their normal amount means they will go over the recomended nutrition the plan automatically reduces teh number of scoops they will be drinking until they are under. if this can't be done the then program treats protein shakes like snacks
        while True:
            pp_prot = base_powder_prot_per_scoop * scoop_num
            j = opt_dic['required protein'] - (p_shake_num * pp_prot)
            if j <= 0:
                j = 0
            if opt_dic['required protein'] <= pp_prot * p_shake_num:
                scoop_num -= 1
                continue
            if pp_prot == 0:
                snack_num += 1
                l = opt_dic['required calories']
                pp_cal = 0
            else:
                pp_cal = pp_prot * 4
                l = opt_dic['required calories'] - (p_shake_num * pp_cal)
                if l <= 0:
                    l = 0
                if opt_dic['required calories'] <= pp_cal * p_shake_num: 
                    scoop_num -= 1
                    continue
            break
        # here the program calcutes the nutrtional divison between main meals and snacks, with double the nutritonal balence being given to main meals
        fix = snack_num + (main_meal_num * 2)
        p = opt_dic['required calories off day'] - (p_shake_num * pp_cal)
        # this section of the code prevents errors occuring if the meal plan is over the recomended nutrition
        if p <= 0:
            p = 0
        try:
            s_prot = j/fix
        except ZeroDivisionError:
            s_prot = 0
        try:
            s_cal = l/fix
        except ZeroDivisionError:
            s_cal = 0
        try:
            s_cal_off = p/fix
        except ZeroDivisionError:
            s_cal_off = 0
        try:
            s_fat = opt_dic['required fat']/fix
        except ZeroDivisionError:
            s_fat = 0
        try:
            s_fat_off = opt_dic['required fat off day']/fix
        except ZeroDivisionError:
            s_fat_off = 0
        # here if the code ascribes the values for snacks to protein shakes if if cant work out the correct number of scoops to give the shakes
        if pp_prot == 0:
            pp_prot = s_prot
        if pp_cal == 0:
            pp_cal = s_cal
        # here the plan ascribes the nutritional values to the main meals and the snacks
        mm_prot = s_prot * 2
        mm_cal = s_cal * 2
        mm_cal_off = s_cal_off * 2
        mm_fat = s_fat * 2
        mm_fat_off = s_fat_off * 2
        # this is the dicitonary that the function will return
        re = {'pp_prot': pp_prot, 'pp_cal': pp_cal, 's_prot': s_prot, 's_cal': s_cal, 's_cal_off': s_cal_off, 's_fat': s_fat, 's_fat_off': s_fat_off, 'mm_prot': mm_prot, 'mm_cal': mm_cal, 'mm_cal_off': mm_cal_off, 'mm_fat': mm_fat, 'mm_fat_off': mm_fat_off, 'scoop_num': scoop_num}
        # here the function checks that non of the values in the dicitonary are negative, and returns 0 if they are
        for keys in re:
            if re[keys] < 0:
                re[keys] = 0
        return re
    
     
    def load_specific_template(self, name):
        for items in self.user_saved_data['meal plans']['template']:
            if items['name'] == name:
                return items
    
    #none of this is working, the day function needs to change so that it calls unto a dictionary where it can be sub saved 
    def daily_temp_calc(self, un_dic, order_dic, on_off):
        day = {}
        day['on_off'] = on_off
        if day['on_off'] == 'on':
            day['rec meal nutes'] = {'calories': self.required_calories, 'protein': self.required_protein, 'fat': self.required_fat}
        else:
            day['rec meal nutes'] = {'calories': self.required_calories_off_day, 'protein': self.required_protein, 'fat': self.required_fat_day_off}
        for keys in order_dic:
            day[keys] = {'name': order_dic[keys], 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}}
            if order_dic[keys] in ['Breakfast', 'Lunch', 'Dinner']:
                if day['on_off'] == 'on':
                    day[keys]['rec meal nutes'] = {'calories': un_dic['mm_cal'], 'protein': un_dic['mm_prot'], 'fat': un_dic['mm_fat']}
                else: 
                    day[keys]['rec meal nutes'] = {'calories': un_dic['mm_cal_off'], 'protein': un_dic['mm_prot'], 'fat': un_dic['mm_fat_off']}
            elif order_dic[keys] == 'Snack':
                if day['on_off'] == 'on':
                    day[keys]['rec meal nutes'] = {'calories':un_dic['s_cal'], 'protein': un_dic['s_prot'], 'fat': un_dic['s_fat']}
                else: 
                    day[keys]['rec meal nutes'] = {'calories': un_dic['s_cal_off'], 'protein': un_dic['s_prot'], 'fat': un_dic['s_fat_off']}
            elif order_dic[keys] == 'Protein Shake':
                day[keys]['rec meal nutes'] = {'calories': un_dic['pp_cal'], 'protein': un_dic['pp_prot'], 'fat': 0, 'scoop_num': un_dic['scoop_num']}
        return day
                
    def save_meal_template(self, meal_plan, typ = 'template'):
        meal_plan['date'] = datetime.datetime.now()
        ed_lst = self.user_saved_data['meal plans'][typ]
        for items in ed_lst:
            if items['name'] == meal_plan['name']:
                del ed_lst[ed_lst.index(items)]
        self.user_saved_data['meal plans'][typ] = ed_lst
        self.user_saved_data['meal plans'][typ].append(meal_plan)
        self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)
    
    def check_meal_plan_name_validity(self, name, order = 'template'):
        check = []
        if order == 'template':
            for items in self.user_saved_data['meal plans']['template']:
                check.append(items['name'])
        elif order == 'complete':
            for items in self.user_saved_data['meal plans']['complete']:
                check.append(items['name'])
        for obs in check:
            lp = obs.lower().replace(' ', '')
            if lp == name:
                print('That name is already in use.')
                return 'False'
        return 'True'
    
    # previously generated templates are able to be loaded for editing by inserting them into the previous_temp variable    
    def meal_plan_template_genorator(self, previous_temp = 0):
        if previous_temp == 0:
            while True:
                print('Creating new meal plan template.\nPlease answer the following questions.')
                while True:
                    name = input('\nEnter a name for this new template:\t')
                    if self.check_meal_plan_name_validity(name, 'template') == 'True':
                        break
                    continue
                while True:
                    av_meals = input_check(input('\nIncluding protein shakes, how many meals do you eat a day?\n(If your meals are less regular this can be changed later):\t'), 'num', [0, 20])
                    if av_meals == 'False':
                        continue
                    av_meals = int(av_meals)
                    break
                while True:
                    p_shake_num = input_check(input('\nHow many of these meals are protein shakes?\nIf you do not consume protein shakes please enter 0:\t'), 'num', [-1, av_meals-1])
                    if p_shake_num == 'False':
                        continue
                    p_shake_num = int(p_shake_num)
                    break
                if p_shake_num != 0:
                    while True:
                        scoop_num = input_check(input('\nHow many 15g scoops of protein powder do you have in your shake?\t'), 'num')
                        if scoop_num == 'False':
                            continue
                        scoop_num = int(scoop_num)
                        break
                else:
                    scoop_num = 0
                day_dict = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '', 'Friday': '', 'Saturday': '', 'Sunday': ''}
                print('Now for each day of the week, please specify if you workout on that day.')
                for days in day_dict:
                    while True:
                        tmm = input_check(input(F"Do you workout on {days}:\t"), 'other')
                        if tmm == 'False':
                            continue
                        break
                    if tmm in ['y', 'yes']:
                        day_dict[days] = 'on'
                    else:
                        day_dict[days] = 'off'
                if av_meals - p_shake_num >= 3:
                    main_meal_num = 3
                    snack_num = av_meals - p_shake_num - 3
                else:
                    main_meal_num = av_meals - p_shake_num
                    snack_num = 0
                un_dic = self.rejig_calc(snack_num, main_meal_num, scoop_num, p_shake_num)
                print('Please specify in what order you eat your meals')
                order_dic = meal_plan_meal_alocator(av_meals, main_meal_num, p_shake_num, snack_num)
                meal_plan = {'name': name}
                for days in day_dict:
                    meal_plan[days] = self.daily_temp_calc(un_dic, order_dic, day_dict[days])
                print('Meal Plan Generated')
                time.sleep(2)
                self.meal_plan_print(meal_plan)
                while True:
                    checky = input_check(input('Are you happy with this template?\t'), 'other')
                    if checky == 'False':
                        continue
                    break
                if checky in ['y', 'yes']:
                    self.save_meal_template(meal_plan)
                    return meal_plan
                else:
                    while True:
                        chip = input_check(input('What would you like to do?\n1:\tEdit plan.\n2:\tStart over.\nYour choice\t'), 'num', [0,2])
                        if chip == 'False':
                            continue
                        break
                    if chip == 2:
                        continue
                    elif chip == 1:
                        previous_temp = meal_plan
                        break
        day_lst = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        while True:
            while True:
                l_choice = input_check(input("What would you like to edit?\n1:\tName.\n2:\tSpecific day.\nb:\tExit.\t"), 'both', [[0, 2],['b']])
                if l_choice == 'False':
                    continue
                break
            if l_choice == 1:
                while True:
                    previous_temp['name'] = input('Please enter the new name of the template.\t')
                    if self.check_meal_plan_name_validity(previous_temp['name'], 'template') == 'False':
                        continue
                    break
            elif l_choice == 2:
                print('What day would you like to edit?')
                while True:
                    for days in day_lst:
                        print(f"{day_lst.index(days)+1}:\t{days}")
                    choice = input_check(input('Your selection?\t'), 'num', [0, 7])
                    if choice == 'False':
                        continue
                    choice = int(choice)
                    break
                for days in previous_temp:
                    if days == day_lst[choice-1]:
                        mm_n = 0
                        s_n = 0
                        p_n = 0
                        av_n = 0
                        k = {}
                        or_dic = {}
                        for keys in previous_temp[days]:
                            if previous_temp[days][keys] in ['on', 'off']:
                                l = previous_temp[days][keys]
                            else:
                                k[keys] = previous_temp[days][keys]
                            if previous_temp[days][keys] in ['on', 'off'] or keys in ['rec meal nutes', 'meal nutes']:
                                pass
                            elif previous_temp[days][keys]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                                or_dic[keys] = previous_temp[days][keys]['name']
                                av_n +=1
                                mm_n += 1
                            elif previous_temp[days][keys]['name'] == 'Snack':
                                or_dic[keys] = previous_temp[days][keys]['name']
                                av_n += 1
                                s_n += 1
                            elif previous_temp[days][keys]['name'] == 'Protein Shake':
                                or_dic[keys] = previous_temp[days][keys]['name']
                                s_coo_num = previous_temp[days][keys]['rec meal nutes']['protein'] / 10.5
                                av_n += 1
                                p_n += 1
                        un_d = self.rejig_calc(s_n, mm_n, s_coo_num ,p_n)
                        self.meal_plan_print(previous_temp, [days])
                        while True:
                            while True:
                                imp = input_check(input('What would you like to edit?\n1:\tWorkout/Rest day\n2:\tNumber of meals\n3:\tMeal order\nb:\tBack\n'), 'both', [[0, 3],['b']])
                                if imp == 'False':
                                    continue
                                break
                            if imp == 1:
                                if l == 'on':
                                    print(f"{days} is current a Workout-Day.")
                                else:
                                    print(f"{days} is currently a Rest-Day.")
                                while True:
                                    it = input_check(input('Would you like to change this?\t'), 'other')
                                    if it == 'False':
                                        continue
                                    break
                                if it in ['yes', 'y']:
                                    if l == 'on':
                                        l = 'off'
                                    else:
                                        l = 'on'
                                    continue
                                else:
                                    continue
                            if imp == 2:
                                while True:
                                    av_n = input_check(input('Including protein shakes, how many meals do you eat a day?\n(If your meals are less regular this can be changed later):\t'), 'num', [0, 20])
                                    if av_n == 'False':
                                        continue
                                    av_n = int(av_n)
                                    break
                                while True:
                                    p_num = input_check(input('How many of these meals are protein shakes?\nIf you do not consume protein shakes please enter 0:\t'), 'num', [-1, av_meals-1])
                                    if p_num == 'False':
                                        continue
                                    p_num = int(p_num)
                                    break
                                if p_num != 0:
                                    while True:
                                        s_coo_num = input_check(input('How many 15g scoops of protein powder do you have in your shake?\t'), 'num')
                                        if s_coo_num == 'False':
                                            continue
                                        s_coo_num = int(s_coo_num)
                                        break
                                else:
                                    s_coo_num = 0
                                un_d = self.rejig_calc(s_n, mm_n, s_coo_num, p_n)
                                or_dic = meal_plan_meal_alocator(av_n, mm_n, p_n, s_n)
                                continue
                            if imp == 3:
                                or_dic = meal_plan_meal_alocator(av_n, mm_n, p_n, s_n)
                                continue
                            else:
                                previous_temp[days] = self.daily_temp_calc(un_d, or_dic, l)
                                break
            elif l_choice == 'b':
                self.save_meal_template(previous_temp)
                return previous_temp
    
    def delete_meal_plan(self, meal_plan, choice = 'template'):
        if choice == 'template':
            gm = self.user_saved_data['meal plans']['template']
        else:
            gm = self.user_saved_data['meal plans']['complete']
        for items in gm:
            if items['name'] == meal_plan['name']:
                del gm[gm.index(items)]
        if choice == 'template':
            self.user_saved_data['meal plans']['template'] = gm
        else:
            self.user_saved_data['meal plans']['complete'] = gm
        self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)

    def load_meal_plans(self, check = 0):
        if check == 'template':
            lst = self.user_saved_data['meal plans']['template']
        else:
            lst = self.user_saved_data['meal plans']['complete']
        tim_lst = []
        for items in lst:
            tim_lst.append(items['date'])
        tim_lst = sorted(tim_lst, reverse=True)
        meal_plans = []
        for times in tim_lst:
            for items in lst:
                if items['date'] == times:
                    meal_plans.append(items)
        iterable_lst = []
        for items in meal_plans:
            iterable_lst.append({'init': items['name'], 'Date': items['date']})
        it_choice = lst_interation(iterable_lst)
        if it_choice == 'False':
            return 'False'
        else:
            for items in meal_plans:
                if items['name'] == it_choice['init']:
                    return items
                
    # type options are [meal, recipies, ingreidents]   
    def return_meal_option_input(self, typ = 'meal', opt = 0, crysis = 0):
        tri = False
        if typ == 'meal':
            check = self.user_saved_data['meals database']
            choice = lst_interation(time_sort(check))
            if opt != 0:
                for obs in self.user_saved_data['meals database']:
                    if obs['name'] == choice:
                        tri = True
                        choice = obs
            # return choice
        elif typ == 'recipies':
            check = self.user_saved_data['recipies database']
            choice = lst_interation(time_sort(check))
            if opt != 0:
                for obs in self.user_saved_data['recipies database']:
                    if obs['name'] == choice:
                        tri = True
                        choice = obs
            # return choice
        elif typ == 'ingredients':
            while True:
                check_dic = {}
                lp_duc = {}
                num = 1
                if len(self.user_saved_data['foods database']['user products']) != 0:
                    check_dic['Custom user ingredients'] = self.user_saved_data['foods database']['user products']
                    lp_duc[num] = 'Custom user ingredients'
                    num +=1
                sp_dic = ['Asda', 'Morisons', 'Tesco', 'Sainsburys']
                tt_dic = ['store nute', 'user nute']
                sp_check_num = []
                for sp in sp_dic:
                    if len(self.user_saved_data['foods database']['supermarket products'][sp][tt_dic[0]]) != 0 or len(self.user_saved_data['foods database']['supermarket products'][sp][tt_dic[1]]) != 0:
                        sp_check_num.append(sp)
                if len(sp_check_num) != 0:
                    check_dic['Supermarket ingredients'] = self.user_saved_data['foods database']['supermarket products']
                    lp_duc[num] = 'Supermarket ingredients'
                    num +=1
                for keys in lp_duc:
                    print(f"{keys}:\t{lp_duc[keys]}")
                print("b:\tBack")
                if bool(lp_duc) == False:
                    print('This database is empty.\nPlease create an ingredient.')
                    tt = 'b'
                else:
                    while True:
                        tt = input_check(input('Please select an option?\t'), 'both', [[0, num-1],['b']])
                        if tt == 'False':
                            continue
                        if tt != 'b':
                            tt = int(tt)
                        break
                if tt == 'b':
                    return 'False'
                if lp_duc[tt] == 'Custom user ingredients':
                    while True:
                        choice = lst_interation(time_sort(check_dic[lp_duc[tt]]))
                        if choice == 'False':
                            break
                        if opt != 0:
                            for obs in self.user_saved_data['foods database']['user products']:
                                if obs['name'] == choice:
                                    tri = True
                                    choice = obs 
                                    sup_choi = False
                                    nute_choi = False
                                    break    
                        if tri == True:
                            break                  
                else:
                    while True:
                        super_dic = {}
                        nums = 1
                        for sp in sp_dic:
                            if len(check_dic['Supermarket ingredients'][sp][tt_dic[0]]) != 0 or len(check_dic['Supermarket ingredients'][sp][tt_dic[1]]) != 0:
                                super_dic[nums] = sp
                                nums+=1
                        for keys in super_dic:
                            print(f"{keys}:\t{super_dic[keys]}")
                        print('b:\tBack')
                        while True:
                            super_choi_choice = input_check(input('Please Select a supermarket.\t'), 'both', [[0, nums],['b']])
                            if super_choi_choice == 'False':
                                print('Unrecognised Entry')
                                continue
                            break
                        if super_choi_choice == 'b':
                            break
                        while True:
                            double_dic = {}
                            nums = 1
                            for slt in tt_dic:
                                if len(check_dic['Supermarket ingredients'][super_dic[super_choi_choice]][slt]) != 0:
                                    double_dic[nums] = slt
                                    nums += 1
                            for keys in double_dic:
                                if double_dic[keys] == 'store nute':
                                    print(f"{keys}:\tOfficial Nutrition")
                                    nums+=1
                                else:
                                    print(f"{keys}:\tCustom Nutrition")
                                    nums+=1
                            print("b:\tBack")
                            while True:
                                tt_choice = input_check(input('Please select an option?\t'), 'both', [[0, nums-1],['b']])
                                if tt_choice == 'False':
                                    continue
                                if tt_choice != 'b':
                                    tt_choice = int(tt_choice)
                                break
                            if tt_choice == 'b':
                                break
                            choice = lst_interation(time_sort(check_dic['Supermarket ingredients'][super_dic[super_choi_choice]][double_dic[tt_choice]]))
                            if choice == 'False':
                                continue
                            for items in check_dic['Supermarket ingredients'][super_dic[super_choi_choice]][double_dic[tt_choice]]:
                                if items['name'] == choice:
                                    tri = True
                                    choice = items
                                    sup_choi = super_dic[super_choi_choice]
                                    nute_choi = double_dic[tt_choice]
                                    break
                            if tri == True:
                                break
                        if tri == True:
                            break
                if tri ==True:
                    break
        try:
            choice['date'] = str(datetime.datetime.now())
            self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)
        except Exception:
            pass
        if crysis != 0:
            return [choice, sup_choi, nute_choi]
        return choice
    # put into here so when a meal is called upon it updates the time function on the meal so it is placed first upon the list of meals most recently called upon 

    def print_meal_individual(self, meal, day_nute_dic = 0):
        print(f"\n\nMeal:\t{meal['name']}")
        # if day_nute_dic != 0:
        #     print(f"\tCalories:\t{meal['nutes']['calories']}/{day_nute_dic['calories']}\tProtein:\t{meal['nutes']['protein']}/{day_nute_dic['protein']}\tFat:\t{meal['nutes']['fat']}/{day_nute_dic['fat']}")
        print(f"Calories:\t{round(meal['nutes']['calories'])}\tProtein:\t{round(meal['nutes']['protein'])}\tFat:\t{round(meal['nutes']['fat'])}")
        if len(meal['recipies']) != 0:
            for rec in meal['recipies']:
                print(f"\t\t{rec['name']}\t\t{rec['serving size']}\n\t\tCals:\t{round(rec['nutes']['calories'])}\tProt:\t{round(rec['nutes']['protein'])}\tFat:\t{round(rec['nutes']['fat'])}")
                for ingredients in rec['ingredients']:
                    print(f"\t\t\t{ingredients['name']}\n\t\t\tCals:\t{round(ingredients['nutes']['calories'])}\tProt:\t{round(ingredients['nutes']['protein'])}\tFat:\t{round(ingredients['nutes']['fat'])}")
        print("\n\n")
    
    def print_recipe_individual(self, recipe):
        print(f"\nRecipe:\t{recipe['name']}\t\t{recipe['serving size']}")
        if len(recipe['ingredients']) != 0:
            for ingredients in recipe['ingredients']:
                print(f"\t\t{ingredients['name']}\t\t{ingredients['volume']}")
                print(f"\t\t\tCals:\t{round(ingredients['nutes']['calories'])}\tProt:\t{round(ingredients['nutes']['protein'])}\tFat:\t{round(ingredients['nutes']['fat'])}")
        print('\n')
        
    def recipe_adjuster(self, recpie, tpe = 'new', volume = 0):
        if tpe == 'new':
            num = 0
            for ingredients in recpie['ingredients']:
                num = num + float(ingredients['volume'])
                for nute in ingredients['nutes']:
                    recpie['nutes'][nute] += ingredients['nutes'][nute]
                
            recpie['serving size'] = num
            return recpie
        else:
            key = volume / recpie['serving size']
            for nute in recpie['nutes']:
                recpie['nutes'][nute] = recpie['nutes'][nute] * key
            for ingredients in recpie['ingredients']:
                ingredients['volume'] = ingredients['volume'] * key
                for nute in ingredients['nutes']:
                    ingredients['nutes'][nute] = ingredients['nutes'][nute]*key
            recpie['serving size'] = volume
            return recpie
                                              
    # input recipe for recipies, meal for meals, ingredient for ingredients
    # only need shop or nute_loc if its an ingredient
    def save_recipe_meal_ingredient(self, inp ,typ = 'recipe', shop = 'other', nute_loc = 'user'):    
        inp['date'] = datetime.datetime.now()
        if typ == 'recipe':
            self.user_saved_data['recipies database'].append(inp)
            self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)
        if typ == 'meal':
            self.user_saved_data['meals database'].append(inp)
            self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)
        if typ == 'ingredient':
            if shop in ['Asda', 'Morisons', 'Tesco', 'Sainsburys']:
                if nute_loc == 'user':
                    for items in self.user_saved_data['foods database']['supermarket products'][shop]['user nute']:
                        if items['name'] == inp['name']:
                            self.user_saved_data['foods database']['supermarket products'][shop]['user nute'].remove(items)
                    self.user_saved_data['foods database']['supermarket products'][shop]['user nute'].append(inp)
                else:
                    for items in self.user_saved_data['foods database']['supermarket products'][shop]['store nute']:
                        if items['name'] == inp['name']:
                            self.user_saved_data['foods database']['supermarket products'][shop]['store nute'].remove(items)
                    self.user_saved_data['foods database']['supermarket products'][shop]['store nute'].append(inp)
            else:
                self.user_saved_data['foods database']['user products'].append(inp)
            self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)      
    
    
    # path = meal for meals, path = recipies for recipies, path = ['supermarket products/user products' ,'store name'] for ingredients
    def meal_ingre_rec_name_validity(self, item, path):
        if path == 'meal':
            for names in self.user_saved_data['meals database']:
                if item == names['name']:
                    return 'False'
            return 'True'
        if path == 'recipies':
            for names in self.user_saved_data['recipies database']:
                if item == names['name']:
                    return 'False'
            return 'True'
        if type(path) == list:
            if path[0]== 'user products':
                for items in self.user_saved_data['foods database']['user products']:
                    if items['name'] == item:
                        return 'False'
            else:
                for it in ['store nute', 'user nute']:
                    for obs in self.user_saved_data['foods database']['supermarket products'][path[1]][it]:
                        if obs['name'] == item:
                            return 'False'
            return 'True'
            
            
        
    def meal_readjuster_dic(self, meal):
        cals = 0
        prot = 0
        fat = 0
        for recipies in meal['recipies']:
            cals += recipies['nutes']['calories']
            prot += recipies['nutes']['protein']
            fat += recipies['nutes']['fat']
        meal['nutes']['calories'] = cals
        meal['nutes']['protein'] = prot
        meal['nutes']['fat'] = fat
        return meal
            
        
        
        
        
        
    # if using previouse meals enter into edit_meal, other wise enter 0, enter day_nute_dic if you are using this with a greater meal plan, dont enter if you are only creating a meal
    # for ingredient enter a value into edit_meal if you are not using this within a recipe
    # either = ['meal', 'recipe', 'ingredient'] 
    # if creating recipe you dont need to input anything into edit_meal or day_nute_dic
    def meal_dic_creator(self, typ = 'meal', edit_meal = 0, day_nute_dic = 0):
        if typ == 'ingredient':
            while True:
                while True:
                    ing_choice = input_check(input('Where did you buy this ingredient.\n1:\tSupermarket\n2:\tOther shop.\nb:\tBack.\t'), 'both', [[0,2],['b']])
                    if ing_choice == 'False':
                        continue
                    break
                if ing_choice == 'b':
                    break
                if ing_choice == 1:
                    supermarket_lst = ['Asda']
                    if len(supermarket_lst) > 1:
                        print('What supermarket did you purchase this ingreident from?')
                        super_choice = lst_interation(supermarket_lst)
                        if super_choice == 'False':
                            continue
                    else:
                        super_choice = supermarket_lst[0]
                    chiip = True
                    while True:
                        food = input(f"What is this {super_choice} product called?\t")
                        tts = food_search(super_choice, food)
                        if tts == False:
                            print('There is no products that match that name.')
                            while True:
                                chiip = input_check(input('Would you like to try again?\t'), 'other')
                                if chiip == 'False':
                                    continue
                                break
                            if chiip in ['y', 'yes']:
                                continue
                        break
                    if chiip in ['n', 'no']:
                        continue
                    if edit_meal == 0:
                        while True:
                            volume = input_check(input('How much of this ingredient are you using in the recipe?\t'), 'num')
                            if volume == 'False':
                                print('Unrecognised input?')
                                continue
                            break
                    lls = return_nute_info(tts)
                    if lls[0] == 2:
                        super_location = 'Nute data'
                    else:
                        super_location = 'user'
                    for keys in lls[1]:
                        price = lls[1][keys]['price']
                        key_nutes = supermarket_search_data_sort(lls[1][keys]['nute'])
                        package_volume = gram_converter(lls[1][keys]['volume'])
                        if key_nutes == 'Fail':
                            key_nutes = supermarket_search_data_sort(lls[1][keys]['nute'], lls[1][keys]['volume'])
                    if edit_meal != 0:
                        volume = gram_converter(key_nutes['key'])
                    nutes = nute_sorter_ingredients_to_recipes(volume, key_nutes)
                    ing_dic = {'name': tts, 'price': price, 'volume': volume, 'nutes': nutes, 'key_nutes': key_nutes, 'package volume': package_volume}
                    save_dic = {'name': tts, 'key_nutes': key_nutes, 'price': price, 'package volume': package_volume}
                    print(f"\n{tts}:\t\t{volume}\n\n")
                    for ttt in nutes:
                        try:
                            print(f"{ttt}:\t{round(nutes[ttt])}")
                        except Exception:
                            print(f"{ttt}:\t{nutes[ttt]}")
                    while True:
                        ingre = input_check(input('Are you happy with this ingredient?\t'), 'other')
                        if ingre == 'False':
                            print('Unrecognised input')
                            continue
                        break
                    if ingre in ['n', 'no']:
                        continue
                    return [ing_dic, save_dic, super_choice, super_location]
                if ing_choice == 2:
                    while True:
                        name = input('What is the ingredient called?\t')
                        if self.meal_ingre_rec_name_validity(name, ['user products']) == 'False':
                            print('That name is already in use.\nPlease rename the product.')
                            continue
                        break    
                    while True:
                        price = input_check(input('How much did the ingredient cost you?\t'), 'num')
                        if price == 'False':
                            continue
                        price = '£' + str(price)
                        break
                    while True:
                        package_vol = input_check(input('How many grams of this ingredient did you buy?\t'), 'num')
                        if package_vol == 'False':
                            continue
                        break
                    if edit_meal == 0:
                        while True:
                            volume = input_check(input('How many grams of the ingredient are you using?\t'), 'num')
                            if volume == 'False':
                                continue
                            break
                    key_nutes = nute_data_search_func()
                    if edit_meal != 0:
                        volume = gram_converter(key_nutes['key'])
                    nutes = nute_sorter_ingredients_to_recipes(volume, key_nutes)
                    ing_dic = {'name': name, 'price': price, 'volume': volume, 'nutes': nutes, 'key_nutes':key_nutes, 'package volume': package_vol}
                    save_dic = {'name': name, 'key_nutes': key_nutes, 'price': price, 'package volume': package_vol}
                    print(f"\n{name}:\t\t{volume}\n\n")
                    for itt in nutes:
                        try:
                            print(f"{itt}:\t{round(nutes[itt])}")
                        except Exception:
                            print(f"{itt}:\t{nutes[itt]}")
                    print("\n")
                    while True:
                        ingre = input_check(input('Are you happy with this ingredient?\t'), 'other')
                        if ingre == 'False':
                            continue
                        break
                    if ingre in ['n', 'no']:
                        continue
                    return [ing_dic, save_dic, False, False]
            return False
        elif typ == 'recipe':
            if edit_meal == 0:
                while True:
                    name = input('What would you like to name this recipie?\t')
                    if self.meal_ingre_rec_name_validity(name, 'recipies') == 'False':
                        print('That name is already in use?\nPlease try again.')
                        continue
                    break
                recipe_dic = {'name': name, 'nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'ingredients': [], 'serving size': 0}
            else:
                recipe_dic = edit_meal
            while True:
                if len(recipe_dic['ingredients']) == 0:
                    self.print_recipe_individual(recipe_dic)
                    print('Add ingredients to recipe.')
                    rec_check = 1
                else:
                    self.print_recipe_individual(recipe_dic)
                    while True:
                        rec_check = input_check(input('What would you like to do?\n1:\tAdd ingredient.\n2:\tRemove ingredient.\nb:\tFinished creating recipe.\t'), 'both', [[0,2],['b']])
                        if rec_check == 'False':
                            continue
                        break
                if rec_check == 'b':
                    return recipe_dic
                if rec_check == 2:
                    lst = []
                    for names in recipe_dic['ingredients']:
                        lst.append(names['name'])
                    lst_choice = lst_interation(lst)
                    if lst_choice == 'False':
                        continue
                    while True:
                        lmp =input_check(input('Are you sure you want to delete this ingredient?'), 'other')
                        if lmp == 'False':
                            continue
                        break
                    if lmp in ['no', 'n']:
                        continue
                    ing = recipe_dic['ingredients']
                    for names in ing:
                        if names['name'] == lst_choice:
                            del ing[ing.index(names)]
                    recipe_dic['ingredients'] = ing
                if rec_check == 1:
                    if self.check_meal_fillers('ingredients') == 'True':
                        check = 1
                    else:
                        while True:
                            check = input_check(input('Add ingredient.\n1:\tCreate new ingredient.\n2:\tLoad saved ingredient.\nb:\tBack.\n\t'), 'both', [[0,2],['b']])
                            if check == 'False':
                                continue
                            break
                        if check == 'b':
                            continue
                    if check == 1:
                        ing_lst = self.meal_dic_creator('ingredient')
                        if ing_lst == False:
                            continue
                        if ing_lst[2] == False and ing_lst[3] == False:
                            self.save_recipe_meal_ingredient(ing_lst[1], 'ingredient')                      
                            recipe_dic['ingredients'].append(ing_lst[0])
                        else:
                            self.save_recipe_meal_ingredient(ing_lst[1], 'ingredient', ing_lst[2], ing_lst[3])
                            recipe_dic['ingredients'].append(ing_lst[0])
                    elif check == 2:
                        chip = self.return_meal_option_input('ingredients', 'in')
                        if chip == 'False':
                            continue
                        while True:
                            volume = input_check(input('How much of this ingredient are you using?'), 'num')
                            if volume == 'False':
                                print('Unrecognised input')
                                continue
                            break
                        nutes = nute_sorter_ingredients_to_recipes(volume, chip['key_nutes'])
                        print(f"\n{chip['name']}:\t\t{volume}")
                        for itt in nutes:
                            print(f"{itt}:\t{nutes[itt]}")
                        print("\n")
                        while True:
                            ingre = input_check(input('Are you happy with this ingredient?\t'), 'other')
                            if ingre == 'False':
                                continue
                            break
                        if ingre in ['n', 'no']:
                            continue
                        chip['volume'] = volume
                        chip['nutes'] = nutes
                        recipe_dic['ingredients'].append(chip)        
        if typ == 'meal':
            if edit_meal == 0:
                print('Creating new meal.')
                while True:
                    name = input('What would you like to call this meal?\t')
                    if self.meal_ingre_rec_name_validity(name, 'meal') == 'False':
                        print('That name is already in use.\nPlease try again.')
                        continue
                    break
                edit_meal = {'name': name, 'recipies': [], 'nutes': {'calories': 0, 'protein': 0, 'fat': 0}}
            while True:
                self.meal_readjuster_dic(edit_meal)
                self.print_meal_individual(edit_meal, day_nute_dic)
                print('How would you like to edit this meal')
                if len(edit_meal['recipies']) == 0:
                    print('1:\tEdit name.\n2:\tAdd recipe.\nb:\tFinish editing meal.')
                else:
                    print('1:\tEdit name.\n2:\tRemove/add recipies.\nb:\tFinish editing meal.')
                while True:
                    meal_input = input_check(input('Please select an option.\t'), 'both', [[0,2],['b']])
                    if meal_input == 'False':
                        continue
                    break
                if meal_input == 'b':
                    return edit_meal
                elif meal_input == 1:
                    while True:
                        name = input('What would you like to rename this meal to?\t')
                        if self.meal_ingre_rec_name_validity(name, 'meal') == 'False':
                            print('That name is already in use.\nPlease try again.')
                            continue
                        break
                    edit_meal['name'] = name
                elif meal_input == 2:
                    if len(edit_meal['recipies']) == 0:
                        recipi_choice = 1
                    else:
                        while True:
                            recipi_choice = input_check(input('What would you like to do.\n1:\tAdd recipy.\n2:\tRemove recipy.\nb:\tBack.\t'), 'both', [[0,2],['b']])
                            if recipi_choice == 'False':
                                continue
                            break
                        if recipi_choice == 'b':
                            break
                    if recipi_choice == 2:
                        it_lst = []
                        for items in edit_meal['recipies']:
                            it_lst.append(items['name'])
                        choice = lst_interation(it_lst)
                        if choice == 'False':
                            continue
                        else:
                            rec = edit_meal['recipies']
                            for items in rec:
                                if items['name'] == choice:
                                    del rec[rec.index(items)]
                            edit_meal['recipies'] = rec
                            continue
                    if recipi_choice == 1:
                        while True:
                            if self.check_meal_fillers('recipies') == 'False':
                                while True:
                                    re_ch = input_check(input('Please select an option.\n1:\tCreate new recipie.\n2:\tLoad recipe.\nb:\tBack.\t'), 'both', [[0,2],['b']])
                                    if re_ch == 'False':
                                        continue
                                    break
                            else:
                                re_ch = 1
                            if re_ch == 'b':
                                break
                            if re_ch == 2:
                                rec_check = self.return_meal_option_input('recipies', 'in')
                                if rec_check == 'False':
                                    continue
                                vols = volume_of_rec_calc(rec_check)
                                print(f'This recipie is for {vols}g')
                                while True:
                                    vol_check = input_check(input('Is this the correct volume?\t'), 'other')
                                    if vol_check == 'False':
                                        print('Unrecognised input.')
                                        continue
                                    break
                                if vol_check in ['y', 'yes']:
                                    vol = vols
                                else:
                                    while True:
                                        vol = input_check(input('How much of this recipe did you have?\t'), 'num')
                                        if vol =='False':
                                            continue
                                        break
                                rec_check = self.recipe_adjuster(rec_check, 'old', vol)
                                self.print_recipe_individual(rec_check)
                                while True:
                                    rec_c = input_check(input('\nAre you happy with this recipe?'), 'other')
                                    if rec_c == 'False':
                                        continue
                                    break
                                if rec_c in ['y', 'yes']:
                                    edit_meal['recipies'].append(rec_check)
                                    break
                            if re_ch == 1:
                                rec_check = self.meal_dic_creator(typ='recipe')
                                rec_check = self.recipe_adjuster(rec_check, 'new')
                                self.print_recipe_individual(rec_check)
                                while True:
                                    rec_c = input_check(input('\nAre you happy with this recipe?'), 'other')
                                    if rec_c == 'False':
                                        continue
                                    break
                                if rec_c in ['y', 'yes']:
                                    self.save_recipe_meal_ingredient(rec_check, 'recipe')
                                    edit_meal['recipies'].append(rec_check)
                                    break

# still need to work on this, so the problem is with the section that keeps the protein shakes when the meal adjusts with protein shakes it throws off the calculations for the rest of the rec nutes
    def meal_meal_recalc(self, meal_plan_day, on= 0):
        while True:
            check_dic = True
            p_shake_num = 0
            if on == 0:
                prot_value = meal_plan_day['rec meal nutes']['protein']
                cal_value = meal_plan_day['rec meal nutes']['calories']
                fat_value = meal_plan_day['rec meal nutes']['fat']
            else:
                if meal_plan_day['on_off'] == 'on':
                    prot_value = self.required_protein
                    cal_value = self.required_calories
                    fat_value = self.required_fat
                elif meal_plan_day['on_off'] == 'off':
                    prot_value = self.required_protein
                    cal_value = self.required_calories_off_day
                    fat_value = self.required_fat_day_off
            new_prot_value = 0
            new_cal_value = 0
            new_fat_value = 0  
            calc_prot = 0
            calc_fat = 0
            calc_cals = 0
            prot_lst = []
            cal_lst = []
            fat_lst = []
            opt_lst =['protein', 'calories', 'fat']
            for meals in meal_plan_day:
                if meals in ['on_off', 'rec meal nutes', 'meal nutes']:
                    pass
                else:
                    if meal_plan_day[meals]['name'] == 'Protein Shake':
                        p_shake_num = meal_plan_day[meals]['rec meal nutes']['scoop_num']
                    for opts in opt_lst:
                        chec = meal_plan_day[meals]['meal nutes'][opts]
                        if opts == 'protein':
                            new_prot_value += meal_plan_day[meals]['meal nutes'][opts]
                            if meal_plan_day[meals]['meal nutes'][opts] >= meal_plan_day[meals]['rec meal nutes'][opts] and meal_plan_day[meals]['meal nutes'][opts] != 0:
                                meal_plan_day[meals]['rec meal nutes'][opts] = meal_plan_day[meals]['meal nutes'][opts]
                                prot_lst.append(meals)
                                calc_prot += meal_plan_day[meals]['rec meal nutes'][opts]
                            
                        elif opts == 'calories':
                            new_cal_value += meal_plan_day[meals]['meal nutes'][opts]
                            if meal_plan_day[meals]['meal nutes'][opts] >= meal_plan_day[meals]['rec meal nutes'][opts] and meal_plan_day[meals]['meal nutes'][opts] != 0:
                                meal_plan_day[meals]['rec meal nutes'][opts] = meal_plan_day[meals]['meal nutes'][opts]
                                calc_cals += meal_plan_day[meals]['rec meal nutes'][opts]
                                cal_lst.append(meals)
                        else:
                            new_fat_value += meal_plan_day[meals]['meal nutes'][opts]
                            if meal_plan_day[meals]['meal nutes'][opts] >= meal_plan_day[meals]['rec meal nutes'][opts] and meal_plan_day[meals]['meal nutes'][opts] != 0:
                                meal_plan_day[meals]['rec meal nutes'][opts] = meal_plan_day[meals]['meal nutes'][opts]
                                calc_fat += meal_plan_day[meals]['meal nutes'][opts]
                                fat_lst.append(meals)
            new_values_dic = {'protein': new_prot_value, 'calories': new_cal_value, 'fat': new_fat_value}
            meal_plan_day['meal nutes'] = new_values_dic
            p_dic = {'main meals': 0, 'snacks': 0, 'protein shakes': 0}
            c_dic = {'main meals': 0, 'snacks': 0, 'protein shakes': 0}
            f_dic = {'main meals': 0, 'snacks': 0, 'protein shakes': 0}
            opt_dic = {'required protein': prot_value - calc_prot, 'required calories': cal_value - calc_cals, 'required calories off day': cal_value - calc_cals, 'required fat': fat_value - calc_fat, 'required fat off day': fat_value - calc_fat}            
            for meals in meal_plan_day:
                check = 0
                if meals in ['on_off', 'rec meal nutes', 'meal nutes']:
                    check = 1
                if meals not in cal_lst and check != 1:
                    if meal_plan_day[meals]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                        c_dic['main meals'] += 1
                    elif meal_plan_day[meals]['name'] == 'Snack':
                        c_dic['snacks'] += 1
                        
                    elif meal_plan_day[meals]['name'] == 'Protein Shake':
                        c_dic['protein shakes'] += 1
                        
                if meals not in prot_lst and check != 1:
                    if meal_plan_day[meals]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                        p_dic['main meals'] += 1
                    elif meal_plan_day[meals]['name'] == 'Snack':
                        p_dic['snacks'] += 1
                        
                    elif meal_plan_day[meals]['name'] == 'Protein Shake':
                        p_dic['protein shakes'] += 1
                        
                if meals not in fat_lst and check != 1:
                    if meal_plan_day[meals]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                        f_dic['main meals'] += 1
                    elif meal_plan_day[meals]['name'] == 'Snack':
                        f_dic['snacks'] += 1
                    elif meal_plan_day[meals]['name'] == 'Protein Shake':
                        f_dic['protein shakes'] += 1      
            prot_re = self.rejig_calc(p_dic['snacks'], p_dic['main meals'], p_shake_num, p_dic['protein shakes'], opt_dic)
            cal_re = self.rejig_calc(c_dic['snacks'], c_dic['main meals'], p_shake_num, c_dic['protein shakes'], opt_dic)
            fat_re = self.rejig_calc(f_dic['snacks'], f_dic['main meals'], p_shake_num, f_dic['protein shakes'], opt_dic) 
            for meals in meal_plan_day:
                if meals in ['on_off', 'rec meal nutes', 'meal nutes']:
                    pass
                else:
                    if meals not in prot_lst:
                        if meal_plan_day[meals]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                            meal_plan_day[meals]['rec meal nutes']['protein'] = prot_re['mm_prot']
                        elif meal_plan_day[meals]['name'] == 'Snack':
                            meal_plan_day[meals]['rec meal nutes']['protein'] = prot_re['s_prot']
                        elif meal_plan_day[meals]['name'] == 'Protein Shake':
                            
                            meal_plan_day[meals]['rec meal nutes']['protein'] = prot_re['pp_prot']
                            
                    if meals not in cal_lst:
                        if meal_plan_day[meals]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                            meal_plan_day[meals]['rec meal nutes']['calories'] = cal_re['mm_cal']
                        elif meal_plan_day[meals]['name'] == 'Snack':
                            meal_plan_day[meals]['rec meal nutes']['calories'] = cal_re['s_cal']
                        elif meal_plan_day[meals]['name'] == 'Protein Shake':
                            
                            meal_plan_day[meals]['rec meal nutes']['calories'] = cal_re['pp_cal']
                            
                    if meals not in fat_lst:
                        if meal_plan_day[meals]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                            meal_plan_day[meals]['rec meal nutes']['fat']= fat_re['mm_fat']
                        elif meal_plan_day[meals]['name'] == 'Snack':
                            meal_plan_day[meals]['rec meal nutes']['fat'] = fat_re['s_fat']
                        elif meal_plan_day[meals]['name'] == 'Protein Shake':
                            meal_plan_day[meals]['rec meal nutes']['fat'] = 0
            if check_dic == True:
                return meal_plan_day
            
        
    # need to insert this into athe part of the program that lets you edit meal plans
    def full_update_saved_ingredents(self):
        if len(self.shop_lst) == 1:
            shop = self.shop_lst[0]
        else:
            while True:
                for shop in self.shop_lst:
                    print(f"{self.shop_lst.index(shop)+1}:\t{shop}")
                print('b:\tback.')
                shop_choice = input_check(input('Please select a shop.\t'), 'both', [[1, len(self.shop_lst)+1], ['b']])
                if shop_choice == 'False':
                    print('Unrecognised imput.')
                    continue
                break
            if shop_choice.lower() == 'b':
                return False
            shop = self.shop_lst[int(shop_choice+1)]
        if shop == 'Asda':
            with open('asda_data_nut.txt', 'r')as file:
                data = file.read()
            data = json.loads(data)
        # here3 put other supermarkets with their dictionary values == data
        for it in data:
            for items in self.user_saved_data['foods database']['supermarket products'][shop]['store nute']:
                if it == items['name']:
                    price = data[it]['price']
                    key_nutes = supermarket_search_data_sort(data[it]['nute'])
                    package_volume = gram_converter(data[it]['volume'])
                    if key_nutes == 'Fail':
                        key_nutes = supermarket_search_data_sort(data[it]['nute'], data[it]['volume'])
                    save_dic = {'name': it, 'key_nutes': key_nutes, 'price': price, 'package volume': package_volume, 'date': items['date']}
                    if save_dic['price'] != items['price']:
                        items['price'] = save_dic['price']
                    if save_dic['package volume'] != items['package volume']:
                        items['package volume'] = save_dic['package volume']
                    key_nutes_pass = True
                    for obs in save_dic['key_nutes']:
                        if obs == 'key':
                            try:
                                if save_dic['key_nutes'][obs] != items['key_nutes'][obs]:
                                    key_nutes_pass = False
                            except Exception:
                                key_nutes_pass = False
                        elif obs == 'data':
                            try:
                                for tts in save_dic['key_nutes'][obs]:
                                    if save_dic['key_nutes'][obs][tts] != items['key_nutes'][obs][tts]:
                                        key_nutes_pass = False
                            except Exception:
                                key_nutes_pass = False
                    if key_nutes_pass == False:
                        self.user_saved_data['foods database']['supermarket products'][shop]['store nute'].remove(items)
                        self.user_saved_data['foods database']['supermarket products'][shop]['store nute'].append(save_dic)
        self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)
    
    def delete_meals_rec_ingre(self, oject, typ = 'meals', store = 0):
        if typ == 'meals':
            for objs in self.user_saved_data['meals database']:
                if oject['name'] == objs['name']:
                    self.user_saved_data['meals database'].remove(objs)
        elif typ == 'recipies':
            for objs in self.user_saved_data['recipies database']:
                if oject['name'] == objs['name']:
                    self.user_saved_data['recipies database'].remove(objs)
        else:
            if store == 0:
                for objs in self.user_saved_data['foods database']['user products']:
                    if oject['name'] == objs['name']:
                        self.user_saved_data['foods database']['user products'].remove(objs)
            else:
                for objs in self.user_saved_data['foods database']['supermarket products'][store[0]][store[1]]:
                    if oject['name'] == objs['name']:
                        self.user_saved_data['foods database']['supermarket products'][store[0]][store[1]].remove(objs)
        self.user_saved_data = save_data(self.user_saved_data, self.used_foods_database_path)

    def print_ingre_indiv(self, key_nutes):
        vol = gram_converter(key_nutes['key_nutes']['key'])
        nutes = nute_sorter_ingredients_to_recipes(vol, key_nutes['key_nutes'])   
        print(f"\n{key_nutes['name']}:\t\t{vol}\n\n")  
        for ttt in nutes:
            try:
                print(f"\t{ttt}:\t{round(nutes[ttt])}")   
            except Exception:
                print(f"\t{ttt}:\t{nutes[ttt]}")   
            
    def update_meal_plan_biometrics(self, temp):
        for days in temp:
            if days not in ['name', 'date']:
                temp[days]['rec meal nutes']['protein'] = self.required_protein
                if temp[days]['on_off'] == 'on':
                    temp[days]['rec meal nutes']['calories'] = self.required_calories
                    temp[days]['rec meal nutes']['fat'] = self.required_fat
                else:
                    temp[days]['rec meal nutes']['calories'] = self.required_calories_off_day
                    temp[days]['rec meal nutes']['fat'] = self.required_fat_day_off
                mm_num = 0
                ps_num = 0
                sn_num = 0
                for objs in temp[days]:
                    if objs not in ['meal nutes', 'rec meal nutes', 'on_off']:                        
                        if temp[days][objs]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                            mm_num += 1
                        elif temp[days][objs]['name'] == 'Snack':
                            sn_num += 1
                        else:
                            scoop_num = temp[days][objs]['rec meal nutes']['scoop_num']
                            ps_num += 1
                rejig_dic = self.rejig_calc(sn_num, mm_num, scoop_num, ps_num) 
                for objs in temp[days]:
                    if objs not in ['meal nutes', 'rec meal nutes', 'on_off']: 
                        if temp[days]['on_off'] == 'on':
                            if temp[days][objs]['name'] in ['Breakfast', 'Lunch', 'Dinner']:
                                temp[days][objs]['rec meal nutes'] = {'calories': rejig_dic['mm_cal'], 'protein': rejig_dic['mm_prot'], 'fat': rejig_dic['mm_fat']}
                            elif temp[days][objs]['name'] == 'Snack':
                                temp[days][objs]['rec meal nutes'] = {'calories': rejig_dic['s_cal'], 'protein': rejig_dic['s_prot'], 'fat': rejig_dic['s_fat']}
                            else:
                                temp[days][objs]['rec meal nutes'] = {'scoop_num': scoop_num, 'calories': rejig_dic['pp_cal'], 'fat': 0, 'protein': rejig_dic['pp_prot']}
        return temp
    
    def meal_plan_price_calculator(self, temp):
        ingre_lst = {}
        for days in temp:
            if days not in ['name', 'date']:
                for meals in temp[days]:
                    if meals not in ['meal nutes', 'rec meal nutes', 'on_off']:
                        try:
                            for recipes in temp[days][meals]['meal']['recipies']:
                                for ingredients in recipes['ingredients']:
                                    ingred_dic = {'name': ingredients['name'], 'price': ingredients['price'], 'volume': ingredients['volume'], 'package volume': ingredients['package volume']}
                                    try:
                                        ingre_lst[ingred_dic['name']].append(ingred_dic)
                                    except Exception:
                                        ingre_lst[ingred_dic['name']] = [ingred_dic]                 
                        except Exception:
                            pass    
        return_lst = []
        for items in ingre_lst:
            price = None
            volume = 0
            package_volume = None
            for objects in ingre_lst[items]:
                volume += float(objects['volume'])
                obj_price = float(objects['price'].replace('£', ''))
                obj_package_volume = float(objects['package volume'])
                if price == None:
                    price = obj_price
                    package_volume = obj_package_volume
                else:
                    if obj_price/obj_package_volume < price/package_volume:
                        price = obj_price
                        package_volume = obj_package_volume
            check = False
            if volume % package_volume != 0:
                check = True
            number_of_packages_required = volume/package_volume
            if check == True:
                number_of_packages_required = str(number_of_packages_required).split('.')
                number_of_packages_required = int(number_of_packages_required[0]) + 1
            return_lst.append({'name': items, 'price': price, 'volume': volume, 'package volume': package_volume, 'number_of_packages_required': number_of_packages_required})
        cost = 0
        number_of_items = 0
        for items in return_lst:
            cost += (items['price'] * items['number_of_packages_required'])
            number_of_items += items['number_of_packages_required']
        cost = round(cost, 2)
        cost = '%.2f' % cost
        print(f"\n\n\tShopping List\n\nMeal plan:\t\t{temp['name']}\nCost:\t\t\t£{cost}\nNumber of items:\t{number_of_items}\n")
        num = 1
        for items in return_lst:
            print(f"{num}:\t{items['name']}\n\tQt:\t{items['number_of_packages_required']}\tPrice:\t£{'%.2f' % items['price']}")
            num += 1
        print('\n\n')

            
            

                    




                










# grim = {'name': 'gim', 'Monday': {'on_off': 'on', 'rec meal nutes': {'calories': 466, 'protein': 178, 'fat': 13}, '1': {'name': 'Breakfast', 'meal': {'name': 'meal', 'recipies': [{'name': 'recrec', 'nutes': {'calories': 4370, 'protein': 674, 'fat': 151}, 'ingredients': [{'name': 'Glorious! Warming Carrot', 'price': '£2.60', 'volume': 1000.0, 'nutes': {'calories': 370, 'protein': 7, 'fat': 18}, 'key_nutes': {'key': 100.0, 'data': {'Energy kcal': 37.0, 'Fat': 1.8, 'of which saturates': 0.7, 'Carbohydrate': 4.1, 'of which sugars': 2.5, 'Fibre': 0.9, 'Protein': 0.7, 'Salt': 0.56, '*RI = of your reference intake': '', 'Pot contains 2 portions': ''}}, 'package volume': 560.0}, {'name': 'Birds Eye 4 Breaded Haddock Fish Fillets', 'price': '£4.00', 'volume': 100.0, 'nutes': {'calories': 4000, 'protein': 667, 'fat': 133}, 'key_nutes': {'key': 3.0, 'data': {'Energy kcal': 120.0, 'Energy kJ': 506.0, 'Fat': 4.0, 'Carbohydrate': 1.0, 'of which sugars': '', 'Protein': 20.0, 'Salt': 410.0}}, 'package volume': 440.0}], 'serving size': 1100.0, 'date': '2023-03-09 13:02:32.186170'}, {'name': 'ct', 'nutes': {'calories': 510, 'protein': 21, 'fat': 40}, 'ingredients': [{'name': 'ASDA Pumpkin Seeds', 'price': '£1.20', 'volume': 88.0, 'nutes': {'calories': 510, 'protein': 21, 'fat': 40}, 'key_nutes': {'key': 100.0, 'data': {'Energy kJ': 2403.0, 'Energy kcal': 579.0, 'Fat': 46.0, 'of which saturates': 7.0, 'Carbohydrate': 15.0, 'of which sugars': 1.1, 'Fibre': 5.3, 'Protein': 24.0, 'Salt': 0.05}}, 'package volume': 150.0}], 'serving size': 88.0, 'date': '2023-03-09 13:10:32.432086'}], 'nutes': {'calories': 4880, 'protein': 695, 'fat': 191}, 'date': '2023-03-09 13:10:35.107886'}, 'meal nutes': {'calories': 4880, 'protein': 695, 'fat': 191}, 'rec meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}}, '2': {'name': 'Lunch', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}}, '3': {'name': 'Dinner', 'meal': {'name': 'meal', 'recipies': [{'name': 'recrec', 'nutes': {'calories': 4370, 'protein': 674, 'fat': 151}, 'ingredients': [{'name': 'Glorious! Warming Carrot', 'price': '£2.60', 'volume': 1000.0, 'nutes': {'calories': 370, 'protein': 7, 'fat': 18}, 'key_nutes': {'key': 100.0, 'data': {'Energy kcal': 37.0, 'Fat': 1.8, 'of which saturates': 0.7, 'Carbohydrate': 4.1, 'of which sugars': 2.5, 'Fibre': 0.9, 'Protein': 0.7, 'Salt': 0.56, '*RI = of your reference intake': '', 'Pot contains 2 portions': ''}}, 'package volume': 560.0}, {'name': 'Birds Eye 4 Breaded Haddock Fish Fillets', 'price': '£4.00', 'volume': 100.0, 'nutes': {'calories': 4000, 'protein': 667, 'fat': 133}, 'key_nutes': {'key': 3.0, 'data': {'Energy kcal': 120.0, 'Energy kJ': 506.0, 'Fat': 4.0, 'Carbohydrate': 1.0, 'of which sugars': '', 'Protein': 20.0, 'Salt': 410.0}}, 'package volume': 440.0}], 'serving size': 1100.0, 'date': '2023-03-09 13:02:32.186170'}, {'name': 'ct', 'nutes': {'calories': 510, 'protein': 21, 'fat': 40}, 'ingredients': [{'name': 'ASDA Pumpkin Seeds', 'price': '£1.20', 'volume': 88.0, 'nutes': {'calories': 510, 'protein': 21, 'fat': 40}, 'key_nutes': {'key': 100.0, 'data': {'Energy kJ': 2403.0, 'Energy kcal': 579.0, 'Fat': 46.0, 'of which saturates': 7.0, 'Carbohydrate': 15.0, 'of which sugars': 1.1, 'Fibre': 5.3, 'Protein': 24.0, 'Salt': 0.05}}, 'package volume': 150.0}], 'serving size': 88.0, 'date': '2023-03-09 13:10:32.432086'}], 'nutes': {'calories': 4880, 'protein': 695, 'fat': 191}, 'date': '2023-03-09 14:36:26.270778'}, 'meal nutes': {'calories': 4880, 'protein': 695, 'fat': 191}, 'rec meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}}, '4': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, '5': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, 'meal nutes': {'protein': 1390, 'calories': 9760, 'fat': 382}}, 'Tuesday': {'on_off': 'on', 'rec meal nutes': {'calories': 466, 'protein': 178, 'fat': 13}, '1': {'name': 'Breakfast', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '2': {'name': 'Lunch', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '3': {'name': 'Dinner', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '4': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, '5': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}}, 'Wednesday': {'on_off': 'on', 'rec meal nutes': {'calories': 466, 'protein': 178, 'fat': 13}, '1': {'name': 'Breakfast', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '2': {'name': 'Lunch', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '3': {'name': 'Dinner', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '4': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, '5': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}}, 'Thursday': {'on_off': 'off', 'rec meal nutes': {'calories': 266, 'protein': 178, 'fat': 7}, '1': {'name': 'Breakfast', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 4, 'protein': 38, 'fat': 2}}, '2': {'name': 'Lunch', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 4, 'protein': 38, 'fat': 2}}, '3': {'name': 'Dinner', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 4, 'protein': 38, 'fat': 2}}, '4': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, '5': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}}, 'Friday': {'on_off': 'on', 'rec meal nutes': {'calories': 466, 'protein': 178, 'fat': 13}, '1': {'name': 'Breakfast', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '2': {'name': 'Lunch', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '3': {'name': 'Dinner', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '4': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, '5': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}}, 'Saturday': {'on_off': 'on', 'rec meal nutes': {'calories': 466, 'protein': 178, 'fat': 13}, '1': {'name': 'Breakfast', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '2': {'name': 'Lunch', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '3': {'name': 'Dinner', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 72, 'protein': 38, 'fat': 4}}, '4': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, '5': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}}, 'Sunday': {'on_off': 'off', 'rec meal nutes': {'calories': 266, 'protein': 178, 'fat': 7}, '1': {'name': 'Breakfast', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 4, 'protein': 38, 'fat': 2}}, '2': {'name': 'Lunch', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 4, 'protein': 38, 'fat': 2}}, '3': {'name': 'Dinner', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 4, 'protein': 38, 'fat': 2}}, '4': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}, '5': {'name': 'Protein Shake', 'meal': {'name': '0_none_0'}, 'meal nutes': {'calories': 0, 'protein': 0, 'fat': 0}, 'rec meal nutes': {'calories': 126.0, 'protein': 31.5, 'fat': 0, 'scoop_num': 3}}}, 'date': '2023-03-17 12:18:46.907151'}















# opt_dic = {'required protein': self.required_protein, 'required calories': self.required_calories, 'required calories off day': self.required_calories_off_day, 'required fat': self.required_fat, 'required fat off day': self.required_fat_day_off}
# def rejig_calc(self, snack_num, main_meal_num, scoop_num, p_shake_num, opt_dic = 0):           
# re = {'pp_prot': pp_prot, 'pp_cal': pp_cal, 's_prot': s_prot, 's_cal': s_cal, 's_cal_off': s_cal_off, 's_fat': s_fat, 's_fat_off': s_fat_off, 'mm_prot': mm_prot, 'mm_cal': mm_cal, 'mm_cal_off': mm_cal_off, 'mm_fat': mm_fat, 'mm_fat_off': mm_fat_off, 'scoop_num': scoop_num}                                         
            


# cm = biomentric(2134765816585215521762738344818, 'Geo', 'male', 99.0, 99.0, 99.0, 99.0, 1, 1, 1)

# cm.update_meal_plan_biometrics(grim)
# print(cm.check_meal_fillers('ingredients'))
# tree =cm.meal_dic_creator('meal')


# # if no ingredients it returns just the name unless 'in'
# crack = cm.return_meal_option_input('ingredients', 'in', 'in')
# cm.print_ingre_indiv(crack[0])



# print(tree)
# cm.save_recipe_meal_ingredient(tree, 'meal')

# cm.nute_ingre_test_print()
# cm.full_update_saved_ingredents()
# cm.nute_ingre_test_print()
                    
                
            
            

            
                
        
        
                    
                    
            
        
# in meal: name (0_none_0) == empty registry     
# meal_plan = {'name': 'Example name', 'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}, 'Sunday': {'on_off': 'on/off', 'meal nutes': {'calories': 000, 'protein': 000, 'fat': 000}, 'rec meal nutes': {'calories': 000, 'protein': 000, 'fat': 000}, '1': {}, '2': {}, '3': {}, '4': {}, '5': {'name': 'meal name', 'nutes': {'calories': 000, 'protein': 000, 'fat': 000}, 'meal': {'name': '', 'recipies': [{'name': '', 'nutes': {'calories': 000, 'protein': 000, 'fat': 000}, 'ingredients': [{insert ingredient data}], 'serving size': 0}], 'nutes': {'calories': 000, 'protein': 000, 'fat': 000} }}}      
            