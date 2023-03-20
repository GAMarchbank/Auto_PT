from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

# scraping program to extract the product data from the supermarket ASDA's website.

# begin by defining some key variables and error lists
un_nutted = []
error_lst = []
url_1s = 'https://groceries.asda.com/sitemap'

# function that will show me wherever errors appear in the code while allowing program to remain runing
def error_report(er):
    global error_lst
    error_lst.append(er)

# function that shows which products do not have nutrtional information attached to them 
def un_nuted(url):
    global un_nutted
    un_nutted.append(url)    

# funciton to load the modual seleium, allows the input of a url
def sel_load(url):
    location = "C:\\Users\\ommo\\Desktop\\chromedriver.exe"
    chromeOptions = Options()
    chromeOptions.headless = False
    driver = webdriver.Chrome(executable_path=location, options= chromeOptions)
    driver.get(url)
    driver.implicitly_wait(30)
    consent_button = driver.find_element(by = By.ID, value= "onetrust-accept-btn-handler")
    driver.implicitly_wait(30)
    consent_button.click()
    driver.implicitly_wait(30)
    return driver

# funciton to scaping the urls for the subcatigories shelves from the site map catigories
def pro_scrape(url_1):
    product_lst = {}
    used_urls = []
    while True:
        print(url_1)
        print(used_urls)
        used_urls.append(url_1)
        driver = sel_load(url_1)
        try:
            products = driver.find_element(By.CLASS_NAME, 'co-product-list')
            products = products.find_elements(By.CLASS_NAME, 'co-item')
            for items in products:
                try:
                    inn_dic = {}
                    ob = items.find_element(By.CLASS_NAME, 'co-item__col2')
                    ob = ob.find_element(By.CSS_SELECTOR, 'a')
                    urls = ob.get_attribute('href')
                    title = ob.text
                    obs = items.find_element(By.CLASS_NAME, 'co-item__col1')
                    amount = obs.find_element(By.CLASS_NAME, 'co-item__volume-container').text
                    obbs = items.find_element(By.CLASS_NAME, 'co-item__col3')
                    price = obbs.find_element(By.CLASS_NAME, 'co-product__price').text
                    price = price.replace('\n', '')
                    pric = ''
                    for letters in price:
                        if letters == 'n' or letters == 'o' or letters == 'w':
                            pass
                        else:
                            pric = pric + letters
                    sub_cat = urls.split('product/')
                    sub_cat = sub_cat[1].split('/', 1)
                    sub_cat = sub_cat[0]
                    asiles = url_1.split('aisle/')
                    asiles = asiles[1].split('/', 1)
                    asile = asiles[0]
                    cat= asiles[1].split('/', 1)
                    cat = cat[0]
                    inn_dic['url'] = urls
                    inn_dic['volume'] = amount
                    inn_dic['price'] = pric
                    inn_dic['sub cat'] = [sub_cat]
                    inn_dic['asile'] = [asile]
                    inn_dic['cat'] = [cat]
                    product_lst[title] = inn_dic
                except Exception as e:
                    error_report(e)
                    print('1: noooo')
                    pass
        except Exception as e:
            error_report(e)
            pass
        kil_lst = []
        try:
            next_page = driver.find_element(By.CLASS_NAME, 'page-navigation')
            next_page = next_page.find_element(By.CLASS_NAME, 'co-pagination')
            pages = next_page.find_elements(By.CLASS_NAME, 'asda-btn')
            for page in pages:
                n_url = page.get_attribute('href')
                kil_lst.append(n_url)
        except Exception as e:
            print('end')
            driver.quit()
            break
        driver.quit()
        time.sleep(5)
        num = 0
        for url_t in kil_lst:
            if url_t in used_urls:
                pass
            else:
                url_1 = url_t
                num += 1
        if num == 0:
            break    
    print(len(product_lst))
    return product_lst

def nut_sort(full_dic):
    no_nut_asile = ['big-night-in', 'price-match','health-wellness', 'toiletries-beauty', 'laundry-household', 'baby-toddler-kids', 'back-to-school', 'beer-wine-spirits', 'home-entertainment', 'pet-food-accessories', 'drinks']
    no_nut_cat =['vegan-alcohol', 'vegan-health-beauty', 'vegan-toiletries-beauty', 'bath-shower-soap', 'skin-care', 'top-toiletries-deals', 'make-up-nails', 'pamper-night', 'deodorants-body-sprays', 'baby-toiletries-healthcare', 'newborn-mum-to-be', 'vitamins-supplements', 'kids-health', 'organic-toiletries-baby-food', 'beer-lager-ales', 'cider', 'wine', 'no-low-alcohol', 'pre-mixed-drinks-cocktails', 'alcohol-gifts', 'spirits', 'disposable-tableware-gift-wrap', 'accessories', 'flowers'] 
    no_nut_sub_cat = ['big-pot', 'pale-ales', 'ip-as', 'stout', 'childrens-vitamins', 'roasting-tins-dishes', 'oven-trays', 'disposable-drinkware', 'disposable-tableware', 'serverware-condiments', 'cocktail-mixer-shot-glasses', 'party-tableware', 'energy-drinks', 'drinks', 'storage', 'lunch-boxes-bags', 'storage-containers', 'spices', 'salt-pepper', 'sweetener', 'brown-baking-sugars', 'baking-tins-trays', 'adult-multivitamins', 'pouches', 'joints-bone-care-vitamins', 'womens-vitamins', 'aptamil-first-milk', 'baby-childrens-cough-and-cold', 'gluten-free-baking-ingredients', 'bottled-lagers', 'all-other-grapes', 'ale', 'flavoured-spiced-rum', 'fruity-beers', 'apple-cider', 'pilsners-lagers', 'canned-lagers', 'fruit-flavoured-cider', 'vegan-wine', 'no-low-alcohol-beer', 'rose-wine', 'mini-wines', 'multipacks-cider', 'pre-mixed-drinkes', 'champagne', 'cabernet-sauvignon', 'sauvignon-blanc', 'irish-whiskey', 'world-lager', 'pinot-grigio', 'gluten-free-beer-lager-spirits', 'tequila', 'chardonnay', 'boxed-white-wine', 'port', 'shiraz', 'no-low-alcohol-cider', 'merlot', 'no-low-alcohol-wine', 'health-wellbeing', 'sparking-water', 'rioja', 'malbec', 'extra-special-wine', 'pinot-noir', 'prosecco', 'classic-gin', 'frying-pans-woks', 'chopping-boards', 'herbs', 'flavoured-water', 'cava', 'sparkling-wine', 'ground-coffee', 'coffee-beans', 'scotch-malt-whisky', 'speciality-earl-grey-tea']
    nut_lsts = []
    nut_lst = []
    nut_ls = []
    ls = []
    for keys in full_dic.keys():
        for obs in full_dic[keys]['asile']:
            if obs not in no_nut_asile:
                nut_lsts.append(keys)
    for keys in nut_lsts:
        for obs in full_dic[keys]['cat']:
            if obs not in no_nut_cat:
                nut_lst.append(keys)            
    for obs in nut_lst:
        for ob in full_dic[obs]['sub cat']:
            if ob not in no_nut_sub_cat:
                nut_ls.append(obs)
        
    return nut_ls

def nut_output(dic_name, dic_section, sort_lst):
    inn_dic = {}
    nute_out = {}
    url = dic_section['url']
    if dic_name in sort_lst:
        try:
            print(1)
            driver = sel_load(url)
            print(1)
            segs = driver.find_element(By.CLASS_NAME, 'layout__section')
            deets = segs.find_element(By.CLASS_NAME, 'product-detail-page__main-cntr')
            nute = deets.find_element(By.CLASS_NAME, "pdp-description-reviews__nutrition-table-cntr")
            nute = nute.find_elements(By.CLASS_NAME, 'pdp-description-reviews__nutrition-row')
            by_value = nute[0].find_elements(By.CSS_SELECTOR, 'div')
            by_value = by_value[1]
            del nute[0]
            for nutes in nute:
                nut = nutes.find_elements(By.CSS_SELECTOR, 'div')
                key = nut[0]
                value = nut[1]
                inn_dic[key.text] = value.text
            nute_out['key'] = by_value.text 
            nute_out['data'] = inn_dic
            driver.quit()
            time.sleep(5)
            return nute_out
        except Exception:
            nute_out['key'] = 'None'
            nute_out['data'] = 'None'
            un_nuted([dic_name, url])
            return nute_out
    else:
        nute_out['key'] = 'None'
        nute_out['data'] = 'None'
        return nute_out
    
driver = sel_load(url_1s)
catigories = driver.find_elements(By.CLASS_NAME, 'cat__taxonomy')
cat_page_lst = []
print(len(catigories))
num = 1
for items in catigories:
    items = items.find_elements(By.CLASS_NAME, 'aisle')
    try:
        for objs in items:
            item = objs.find_element(By.CSS_SELECTOR, 'a')
            urls = item.get_attribute('href')
            cat_page_lst.append(urls)
            print(f'{num}/240:\t{urls}')
            num += 1
    except Exception:
        print(f'{num}/240:\t{urls}')
        num += 1
        pass

driver.quit()
time.sleep(10)
full_prod_dic = {}
for shelves in cat_page_lst:
    number = cat_page_lst.index(shelves)
    number += 1
    print(f'{number}/{len(cat_page_lst)}')
    prod_lst = pro_scrape(shelves)
    for k in prod_lst:
        if k in full_prod_dic.keys():
            for cat in prod_lst[k]['cat']:
                if cat not in full_prod_dic[k]['cat']:
                    full_prod_dic[k]['cat'].append(cat)
            for sub_cat in prod_lst[k]['sub cat']:
                if sub_cat not in full_prod_dic[k]['sub cat']:
                    full_prod_dic[k]['sub cat'].append(sub_cat)
            for asile in prod_lst[k]['asile']:
                if asile not in full_prod_dic[k]['asile']:
                    full_prod_dic[k]['asile'].append(asile)
        else:
            full_prod_dic[k] = prod_lst[k]

nut_lst = nut_sort(full_prod_dic)
print(nut_lst)
num = 1
for keys in full_prod_dic.keys():
    print(f'{num}/{len(full_prod_dic.keys())}')
    them = nut_output(keys, full_prod_dic[keys], nut_lst)
    print(them)
    full_prod_dic[keys]['nute'] = them
    num +=1
    
print(len(nut_lst))
print(len(full_prod_dic.keys()))

dic = json.dumps(full_prod_dic)
nut = json.dumps(un_nutted)

with open('unnutted_2.txt', 'w')as file:
    file.write(nut)

with open('asda_data_2.txt', 'w')as file:
    file.write(dic)

print(len(full_prod_dic.keys()))
print(error_lst)
