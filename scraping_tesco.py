from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from copy import deepcopy
import time
import json

# an error list that will contain all of the main product pages that fail to fully scrape
error_list = []

# a function that loads a selenium instance with the selected options at the url entered into the arugment
def selenium_load(url):
    webdriver_location = "C:\\Users\\ommo\\Desktop\\chromedriver.exe"
    chromeOptions = Options()
    chromeOptions.headless = False
    driver = webdriver.Chrome(executable_path=webdriver_location, options=chromeOptions)
    driver.get(url)
    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, 'main__content'))    
    return driver

# a function to extract the url attached to each products image on the shelves sub catagory sub-page.
# constructing the scraper like this is mostly an artifact of a previous verion of the program where seleium would navigate into the product page and then back out again.
# this proved too memory intensive for the webdriver, so ive sectioned the programs into seperate selenium instances.
def product_scraper(driver, item_index, check_opt = False):
    product_lst = driver.find_element(By.CLASS_NAME, 'main__content')
    product_lst = product_lst.find_element(By.CLASS_NAME, 'product-list-view')
    product_lst = product_lst.find_element(By.CLASS_NAME, 'product-lists')
    product_lst = product_lst.find_element(By.CLASS_NAME, 'category.product-list--page.product-list--current-page')
    products = product_lst.find_element(By.CLASS_NAME, 'product-list')
    products = products.find_elements(By.CLASS_NAME, 'product-list--list-item')
    if check_opt == True:
        return (len(products))
    items = products[item_index]
    try:
        link = items.find_element(By.CSS_SELECTOR, 'a')
        url = link.get_attribute('href')
        return url
    except Exception:
        return False

# this function scrapes the main page of the tesco's website for their shelves catagory subpages. it then moves through these pages to find the products.
def menu_find(main_url, num, fun_num):
    global error_list
    # this section moves though the drop down menu attached to teh groceries tag to select different pages
    url_lst = []
    menu_tag = 'menu-superdepartment-'
    driver = selenium_load(main_url)
    buttons = driver.find_element(By.CLASS_NAME, 'menu-tree')
    WebDriverWait(driver, timeout=3).until(lambda buttons: buttons.find_element(By.CLASS_NAME, menu_tag + str(num)))  
    buttons = buttons.find_element(By.CLASS_NAME, menu_tag + str(num))
    buttons.click()
    # when navigating to the correct page it tries to locate products, if none are found it exits the browser and moves to the next option
    try:
        menu_string = 'menu-department-'
        WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, 'menu'))  
        buttons = buttons.find_element(By.CLASS_NAME, 'menu')
        items = buttons.find_element(By.CLASS_NAME, menu_string + str(fun_num))
        items.click()
        items = items.find_element(By.CLASS_NAME, 'menu')
        items = items.find_element(By.CLASS_NAME, 'menu-aisle-0')
        items.click()
        time.sleep(10)
    except Exception:
        return False
    # this instance of the product scraper returns the number of products on the page
    product_index = product_scraper(driver, 0, True)
    page_num = 1
    # this next section searches for the number of products the website says it displays on each page to check against the number the program found
    check_num = driver.find_element(By.CLASS_NAME, 'main__content')
    check_num = check_num.find_element(By.CLASS_NAME, 'product-list-view')
    check_num = check_num.find_element(By.CLASS_NAME, 'product-list-container')
    check_num = check_num.find_element(By.CLASS_NAME, 'pagination__items-displayed')
    check_num = check_num.find_element(By.CSS_SELECTOR, 'strong').text
    check_num = check_num.split(' to ')
    check_num = int(check_num[1]) - (int(check_num[0]) -1) 
    # this section is used to find the number of pages in each isle
    new_page = driver.find_element(By.CLASS_NAME, 'main__content')
    new_page = new_page.find_element(By.CLASS_NAME, 'pagination-component')
    arrows = new_page.find_elements(By.CSS_SELECTOR, 'li')
    pages_num = arrows[-2].find_element(By.CSS_SELECTOR, 'span').text
    check = 0
    # this next section scrapes the urls for all the products found on the page and appends them to teh url_lst list
    for numbers in range(0, product_index):
        print(f"page:\t{page_num}/{pages_num}\nFound Items:\t{numbers+1}/{product_index}\nRelevant Items:\t{check_num}")
        out = product_scraper(driver, numbers, False) 
        if out == False:
            check += 1
        else:
            url_lst.append(out)
    # if less products are scraped then appear on the page the pageurl is insered into teh error list
    if product_index - check != check_num:
        error_list.append(driver.current_url)
    # here the page looks for the last page arrow in the next page list and clicks it
    new_page = driver.find_element(By.CLASS_NAME, 'main__content')
    new_page = new_page.find_element(By.CLASS_NAME, 'pagination-component')
    arrows = new_page.find_elements(By.CSS_SELECTOR, 'li')
    # here it checks if there is only one page to scrape
    if len(arrows) == 3:
        pass
    else: 
        # if there are more then one page, it moves to teh last page on the page list and then moves backwards to make sure it scrapes the entire section
        next_page = arrows[-2]
        next_page.click()
        time.sleep(5)
        page_num +=1
        while True:
            driver.refresh
            product_index = product_scraper(driver, 0, True)
            check_num = driver.find_element(By.CLASS_NAME, 'main__content')
            check_num = check_num.find_element(By.CLASS_NAME, 'product-list-view')
            check_num = check_num.find_element(By.CLASS_NAME, 'product-list-container')
            check_num = check_num.find_element(By.CLASS_NAME, 'pagination__items-displayed')
            check_num = check_num.find_element(By.CSS_SELECTOR, 'strong').text
            check_num = check_num.split(' to ')
            check_num = int(check_num[1]) - (int(check_num[0]) -1) 
            check = 0
            for numbers in range(0, product_index):
                print(f"page:\t{page_num}/{pages_num}\nFound Items:\t{numbers+1}/{product_index}\nRelevant Items:\t{check_num}")
                out = product_scraper(driver, numbers,  False)
                if out == False:
                    check += 1
                else:
                    url_lst.append(out)
            if product_index - check != check_num:
                error_list.append(driver.current_url)
            new_page = driver.find_element(By.CLASS_NAME, 'main__content')
            new_page = new_page.find_element(By.CLASS_NAME, 'pagination-component')
            arrows = new_page.find_elements(By.CSS_SELECTOR, 'li')
            next_page = arrows[0]
            next_page.click()
            time.sleep(5)
            # ther only difference is here when the program checks the page number located at the end of the url, if the number is 1 it has returned to the starting page and exits the seleniun instance.
            end_check = driver.current_url.split('&')
            if len(end_check) == 1:
                end_check = driver.current_url.split('?')
            if end_check[-1] == 'page=1':
                break
            page_num += 1
    return url_lst

# a function to scrape the product info directly off each products individual products page.
def data_dump(driver):
    WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, 'main__content'))
    # this first section exctracts the product name
    page = driver.find_element(By.CLASS_NAME, 'main__content')
    page = page.find_element(By.CLASS_NAME, 'product-details-page')
    title_price = page.find_element(By.CLASS_NAME, 'product-details-tile')
    title = title_price.find_element(By.CLASS_NAME, 'product-details-tile__title-wrapper')
    title = title.find_element(By.CLASS_NAME, 'product-details-tile__title').text
    try:
        price = title_price.find_element(By.CLASS_NAME, 'product-controls__wrapper')
    except Exception:
        driver.quit
        return False
    # this section extracts the product price
    price = price.find_element(By.CLASS_NAME, 'controls')
    price = price.find_element(By.CLASS_NAME, 'price-control-wrapper')
    price = price.find_element(By.CLASS_NAME, 'value').text
    try:
        # this section extracts the product nutrition data from the table at teh bottom of the page
        nutes = page.find_element(By.CLASS_NAME, 'grocery-product')
        nutes_weight = nutes.find_element(By.CLASS_NAME, 'product-blocks')
        weight = nutes_weight.find_element(By.CLASS_NAME, 'product-info-block.product-info-block--net-contents')
        weight = weight.find_element(By.CSS_SELECTOR, 'p').text
        weight_lst = []
        weight_str = ''
        letter_check = False
        for letters in weight:
            try:
                int(letters)
                weight_str = weight_str + letters
            except Exception:
                if letters == ' ':
                    weight_lst.append(weight_str)
                    weight_str = ''
                elif letters == 'g':
                    if weight_str != '':
                        if letter_check == True:
                            weight_str = weight_str + 'kg'
                        else:
                            weight_str = weight_str + 'g'
                elif letters == 'k' and weight_str != '':
                    letter_check = True
                else:
                    letter_check = False
        re_weight_lst = deepcopy(weight_lst)
        weight_lst = []
        for objects in re_weight_lst:
            if objects != '':
                weight_lst.append(objects)
        if len(weight_lst) == 1:
            check = False
            for letters in weight_lst[0]:
                if letters == 'g':
                    check = True
            if check == True:
                weight = weight_lst[0]
            else:
                weight = weight_lst[0] + ' servings'
        try:
            nutes = nutes_weight.find_element(By.CLASS_NAME, 'tabularContent')
            key_nutes = nutes.find_element(By.CSS_SELECTOR, 'thead')
            key_nutes = key_nutes.find_elements(By.CSS_SELECTOR, 'th')
            key = key_nutes[1].text
            try:
                keys = key.split(' ')[1].replace('g', '')
            except Exception:
                try:
                    keys = key.split(' ')[1].replace('kg', '')
                except Exception:
                    keys = key
            try:
                key = int(keys)
            except Exception:
                key = '1 serving'
            nutes = nutes.find_element(By.CSS_SELECTOR, 'tbody')
            nutes = nutes.find_elements(By.CSS_SELECTOR, 'tr')
            nute_dic = {'key': key, 'nutes': {}}
            for sessions in nutes:
                nut = sessions.find_elements(By.CSS_SELECTOR, 'td')
                name = nut[0].text
                data = nut[1].text
                nute_dic['nutes'][name] = data
        except Exception:
            # if that table does not exist it extracts it from the table at the top of the page
            nute_dic = {'key': 'per serving', 'nutes': {}}
            nutes = nutes_weight.find_element(By.CLASS_NAME, 'gda')
            nutes = nutes.find_elements(By.CLASS_NAME, 'styled__Item-llkqfd-1')
            for items in nutes:
                items = items.find_element(By.CLASS_NAME, 'styled__NutritionContainer-llkqfd-2')
                name = items.find_element(By.CSS_SELECTOR, 'dt').text
                data = items.find_elements(By.CSS_SELECTOR, 'dd')
                data_string = ''
                for items in data:
                    items = items.text
                    if items in ['', ' ']:
                        pass
                    else:
                        data_string = data_string + '/' + items
                nute_dic['nutes'][name] = data_string  
    except Exception:
        # if nither of these tables exist then there is no nutritional data to extract
        nute_dic = {'key': None, 'nutes': None}
        weight = None
    driver.quit
    time.sleep(5)
    return [title, price, weight, nute_dic]

# this function counts the number of items in the drop down menu attached to teh grocery button, allowing the program to fully scrape the page.
def menu_superdepartment_count(main_url):
    driver = selenium_load(main_url)
    items = driver.find_element(By.CLASS_NAME, 'menu-tree') 
    items = items.find_element(By.CLASS_NAME, 'menu.menu-superdepartment')
    items = items.find_elements(By.CSS_SELECTOR, 'li')
    return len(items)
    

# the main section of the code the loads each function. 
url_lst = []
# the varibles num and fun_num selection selection which elements of the grocesies drop down menu will be selected
num = 0
fun_num = 1
scrape = True
main_url = "https://www.tesco.com/groceries/?icid=dchp_groceriesshopgroceries"
numbers = menu_superdepartment_count(main_url)
print(numbers)
check = False
while scrape == True:
    if num == numbers:
        break
    else:
        try:
            urls = menu_find(main_url, num, fun_num)
        except Exception:
            if check == True:
                check = False
                break
            else:
                check = True
                continue
        if urls == False:
            num += 1
            fun_num = 1
            pass
        else:
            for url in urls:
                if url in url_lst:
                    pass
                else:
                    url_lst.append(url)
            fun_num += 1
    # except:
    #     scrape = False

print(url_lst)

# here i write the url data to a txt file
j_dumped_urls = json.dumps(url_lst)
with open('tesco_scrape_urls.txt', 'w')as file:
    file.write(j_dumped_urls)



# here it loads every url in the url_lst and scapes the product pages for information
results_out = []
for items in url_lst:
    print(f"{url_lst.index(items)+1}/{len(url_lst)}")
    percentage = round((int(url_lst.index(items)+1)/len(url_lst)) * 100, 1)
    print(f"{percentage}% of products scraped.\n")
    print(items)
    while True:
        try:
            driver = selenium_load(items)
            break
        except Exception:
            try:
                driver.quit
                time.sleep(5)
            except Exception:
                pass
            continue
    product_info = data_dump(driver)
    if product_info != False:
        results_out.append(product_info)

# here it write that data to a txt file
j_dumped_data = json.dumps(results_out)
with open('tesco_scape_data.txt', 'w')as file:
    file.write(j_dumped_data)

# finally it prints teh results
print(results_out)
