from django.shortcuts import render, HttpResponse
from . import requests

# Create your views here.
login_page = 'http://office.mediaobserver-me.com:882/checkuser.php'
# client = orange (customers=173)
credentials = {'username':'*****','password':'*****'}
accounts = {'LG':166, 'Orange':173}
#'ACT':167, 'Emaar':177, 'AIG4':288, 'Crescent':307, 'Pearl':334, 'HBKU':366, 'Total':624, 'Westin':658, 'Bein':856, 'Fine':910, 'Alan':1050, 'DB':1052, 'DCCI-tr':1132, 'AIG_clips':1352, 'Danube':1750, 'USAID':1826, 'Memac':2060, 'Disney':211}

def overview(request):  
    # create session, enter credentials, get and render cookies
    session = requests.Session()
    login = session.post(login_page, credentials)
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    results = {}
    
    for account_name, account_number in zip(accounts.keys(), accounts.values()):
        # counter flag
        untranslated_arts = 0
        
        get_items = 'http://office.mediaobserver-me.com:882/json/translate_articles/get_articles_datatable.php?country=&publication_type=&langs=Arabic&publication=&issue_from=&issue_to=&create_from=2018-07-18&create_to=&artcile_status=&keywords_id=&translate_status=4&artcile_status=&customers=%d' % account_number
        arts_list = session.post(get_items, cookies=cookies)
        
        # contents
        content = str(arts_list.content)
        text = content.split(',')
        
        # search for untranslated items, update counter flag
        #if account_name in ['Crescent', 'Pearl', 'Total', 'Westin', 'Bein', 'DB', 'DCCI-tr', 'AIG_clips', 'Danube', 'Memac', 'Disney']:
            #for word in text:
                #if word in ['"headline_translated":""', '"headline_translated":null', '"text_translated":""'] and word != '"check_body":null':
                    #untranslated_arts += 1            
        #else:
        if '"check_body":null' in text: #check if headline
            for word in text:
                if word in ['"headline_translated":""', '"headline_translated":null']:
                    untranslated_arts += 1
        else: #else its headline and body
            for word in text:
                if word in ['"text_translated":""', '"text_translated":null']:
                    untranslated_arts += 1
            
        results[account_name] = untranslated_arts
    
    return render(request, 'unstranslated_counter/overview.html', {'results':results})
