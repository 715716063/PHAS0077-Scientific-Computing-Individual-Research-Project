#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib
from urllib import parse
from urllib.request import urlopen
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession
import time
import pandas as pd


# In[2]:


html = requests.get("https://www.exomol.com/data/molecules/").content.decode()
soup = BeautifulSoup(html,'html.parser')
molecules_url_element_list = soup.find_all("a",class_="list-group-item link-list-group-item molecule_link")
molecules_url_list = []
base_url = "https://www.exomol.com/data/molecules/"
for items in molecules_url_element_list:
    part_url = items.get("href")
    full_url = base_url + part_url+str("/")
    molecules_url_list.append(full_url)
###gained the url for every molecules 


# In[3]:


isotopologues_url_list = []
for url in molecules_url_list:
    html = requests.get(url).content.decode()
    soup = BeautifulSoup(html,'html.parser')
    isotopologues_url_element_list = soup.find_all("a",class_="list-group-item link-list-group-item")
    for items in isotopologues_url_element_list:
        part_url = items.get("href")
        full_url = url + part_url + str("/")
        isotopologues_url_list.append(full_url)
###gained the url for every isotopologues


# In[4]:


dataset_url_list = []
for url in isotopologues_url_list:
    html = requests.get(url).content.decode()
    soup = BeautifulSoup(html,'html.parser')
    
    dataset_url_element_list = soup.find_all("a",class_="list-group-item link-list-group-item")
    for items in dataset_url_element_list:
        part_url = items.get("href")
        full_url = url + part_url + str("/")
        dataset_url_list.append(full_url)
        
    dataset_url_element_list_recommended = soup.find_all("a",class_="list-group-item link-list-group-item recommended")
    for items in dataset_url_element_list_recommended:
        part_url = items.get("href")
        full_url = url + part_url + str("/")
        dataset_url_list.append(full_url)

###gained the url for every dataset


# In[5]:


full_reference_url_list = []
for url in dataset_url_list:
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'lxml')
    reference_url_list = []
    tag = soup.find_all("span",class_="noprint")
    for i in tag:
        reference_url = i.find("a").get("href")
        reference_url_list.append(reference_url)
    reference_url_list = list(set(reference_url_list))
    for k in reference_url_list:
        full_reference_url_list.append([url]+[k])
###Stored the crawler result into full_reference_url_list, the saved format is [[Original data set url],[the reference paper url]]


# In[6]:


for i in full_reference_url_list:
    if i[1] == 'http://dx,doi,org/10.1093/mnras/stu944':
        i[1] = 'http://dx.doi.org/10.1093/mnras/stu944'
    if i[1] == 'http://http://dx.doi.org/10.1093/mnras/stu326':
        i[1] = 'http://dx.doi.org/10.1093/mnras/stu326'
        
###the orginal web page gives wrong links, here we append the modified url into the gerenal_url_list.


# In[7]:


paper_url_list = []
for i in full_reference_url_list:
    paper_url = i[1]
    paper_url_list.append(paper_url)
paper_url_set = set(paper_url_list)
###remove duplicate paper url


# In[265]:


len(paper_url_set)


# In[8]:


genernal_url_list = []
for k in paper_url_set:
    url_parts = parse.urlparse(k)
    if url_parts[1] == 'doi.org' or url_parts[1] == 'dx.doi.org':
        genernal_url_list.append(k)
###Stored the genernal naming format url into genernal_url_list


# In[9]:


screened_reference_url_list = []
for i in full_reference_url_list:
    if i[1] in genernal_url_list:
        screened_reference_url_list.append(i)
main_data = pd.DataFrame(screened_reference_url_list,columns = ['database link','reference paper url'])
###add the modified data into the main_data


# In[10]:


def dict_to_list(dictionary):
    trans_list = []
    for i in dictionary.keys():
        trans = trans_list.append([i] + [dictionary[i]]) 
    return trans_list


# In[11]:


dataset_url_list = []
database_url = list(main_data['database link'])
for i in database_url:
    dataset = i.split("/")[-2]
    dataset_url_list.append([i]+[dataset])
dataset_url_data = pd.DataFrame(dataset_url_list,columns = ['database url','dataset'])
main_data = pd.concat([dataset_url_data,main_data,], axis=1)
main_data = main_data.drop("database link", axis=1, inplace=False)

###add data set name into main_data

url_doi = dict()
reference_paper_url = list(set(list(main_data['reference paper url'])))
for i in reference_paper_url:
    doi = parse.urlparse(i)[2][1:]
    url_doi[i] = doi
doi_list = list(url_doi.values())
doi_list.remove("10.5194/acp-2020-286")
url_doi["https://doi.org/10.5194/acp-2020-286"]="10.5194/acp-2020-286(not available)"
###remove unavilable DOI from doi_list and update the url_doi dictionary
doi_data = pd.DataFrame(dict_to_list(url_doi),columns = ["reference paper url","DOI"])
main_data = pd.merge(main_data,doi_data,how = "left")
###add reference paper DOI into main_data


# In[266]:


main_data


# In[12]:


Account_information = {
    "school account username" : "ucapadx",
    "school account password" : "Myc970403!!",
    "personal account username" : '715716063@qq.com',
    "personal account password" : "myc970403~~~"
}
###stored personnal account information


# In[92]:


options = webdriver.ChromeOptions()
options.add_experimental_option('prefs',  {
    "download.default_directory": "D:\\test",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True 
    }
) 
driver = webdriver.Chrome(chrome_options=options) 
WOS_url = 'https://www.webofknowledge.com'
driver.get(WOS_url)
driver.maximize_window()
driver.find_element_by_id("mat-select-0").click()
time.sleep(1)
driver.find_element_by_id("mat-option-48").click()
time.sleep(1)
driver.find_element_by_xpath('/html/body/microui-app/div/section/microui-base/div[1]/div/base-login/div/div[3]/div[3]/app-shibboleth-login/div/form/button').click()
driver.find_element_by_id('SearchInput').send_keys("UCL")
driver.find_element_by_id('submit-btn').click()
driver.find_element_by_link_text("UCL (University College London)").click()
driver.find_element_by_id('username').send_keys(Account_information['school account username'])
driver.find_element_by_id('password').send_keys(Account_information["school account password"])
driver.find_element_by_name("_eventId_proceed").click()
driver.find_element_by_xpath('/html/body/app-wos/div/div/header/app-header/div[2]/button[1]').click()
driver.find_element_by_xpath('''//*[@id="mat-menu-panel-3"]/div/div/a[1]''').click()
time.sleep(5)
driver.find_element_by_xpath('''//*[@id="mat-input-0"]''').send_keys(Account_information["personal account username"])
driver.find_element_by_xpath('''//*[@id="mat-input-1"]''').send_keys(Account_information["personal account password"])
driver.find_element_by_xpath('''//*[@id="signIn-btn"]''').click()
time.sleep(2)


# In[93]:


def get_title():
    title = driver.find_element_by_id("FullRTa-fullRecordtitle-0").text
    return title


# In[94]:


def get_cited_times():
    try:
        xpath = "/html/body/app-wos/div/div/main/div/app-input-route/app-full-record-home/div[2]/div[1]/app-full-record-right-panel/div/div[1]/div[1]/div[1]/a"
        cited_times = driver.find_element_by_xpath(xpath).text
    except:
        cited_times = "0"
    return cited_times


# In[95]:


def get_author():
    author_list = []
    try:
        driver.find_element_by_id("SumAuthTa-FrToggle-author-en").click()
    except:
        pass
    for i in range(2000):
        try:
            path = "SumAuthTa-DisplayName-author-en-"+str(i)
            author = driver.find_element_by_id(path).text
            author_list.append(author)
        except:
            break

    return author_list


# In[96]:


cited_times_dict = dict()
author_dict = dict()
title_dict = dict()
doi_record_dict = dict()

for doi in doi_list:
        driver.find_element_by_xpath("""//*[@id="snSearchType"]/div[1]/app-search-row/div[1]/div[1]/app-select-search-field/wos-select""").click()
        time.sleep(1)
        driver.find_element_by_xpath("""//*[@id="global-select"]/div[1]/div[2]/div[18]""").click()

        driver.find_element_by_name("search-main-box").send_keys(doi)
        driver.find_element_by_xpath('//*[@id="snSearchType"]/div[3]/button[2]/span[1]').click()
        time.sleep(2)
        record_href = driver.find_element_by_xpath('/html/body/app-wos/div/div/main/div/app-input-route/app-base-summary-component/div/div[2]/app-records-list/app-record/div[2]/div[1]/app-summary-title/h3/a').get_attribute("href")
        driver.find_element_by_xpath('/html/body/app-wos/div/div/main/div/app-input-route/app-base-summary-component/div/div[2]/app-records-list/app-record/div[2]/div[1]/app-summary-title/h3/a').click()
        doi_record_dict[doi] = record_href
        time.sleep(2)
        title_dict[doi] = get_title()       
        cited_times_dict[doi] = get_cited_times()
        author_dict[doi] = get_author()
        time.sleep(1)
        driver.find_element_by_xpath('''//*[@id="breadcrumb"]/ul/li[1]/a/span''').click()
        driver.find_element_by_xpath('''//*[@id="snSearchType"]/div[1]/app-search-row/div[1]/div[2]/button''').click()
        time.sleep(1)


# In[107]:


cited_data = pd.DataFrame(dict_to_list(cited_times_dict),columns = ['DOI','cited times'])
author_data = pd.DataFrame(dict_to_list(author_dict),columns = ['DOI','author'])
df1 = pd.merge(cited_data,author_data,how = "inner")
###stored the DOI, author, cited time, named df1 for temporary
title_data = pd.DataFrame(dict_to_list(title_dict),columns = ['DOI','title'])
df2 = pd.merge(df1,title_data,how = "inner")
###append the title into df1
record_doi_data = pd.DataFrame(dict_to_list(doi_record_dict),columns = ['DOI',"record link"])
df3 = pd.merge(df2,record_doi_data,how ="inner")
###append the record link into df2
url_doi_data = pd.DataFrame(dict_to_list(url_doi),columns = ['reference paper url','DOI'])
df4 = pd.merge(url_doi_data,df3,how="left")
###append the reference paper into df3, which is used to connect the main_data
main_data = pd.merge(main_data,df4, how="left")
###merge all the information into main_data


# In[ ]:





# In[19]:


def initialize_search_box():
    try:
        driver.find_element_by_xpath("""//*[@id="snSearchType"]/div[3]/button[1]/span[1]""").click()
    except:
        pass


# In[20]:


WOS_url = 'https://www.webofknowledge.com'
driver.get(WOS_url)
time.sleep(2)
driver.find_element_by_xpath("""//*[@id="snSearchType"]/div[1]/app-search-row/div/div[1]/app-select-search-field/wos-select/button""").click()
driver.find_element_by_xpath("""//*[@id="global-select"]/div[1]/div[2]/div[1]""").click()
initialize_search_box()
###initialize the main search page
keyword = "exomol"
driver.find_element_by_name("search-main-box").send_keys(keyword)
driver.find_element_by_xpath('//*[@id="snSearchType"]/div[3]/button[2]/span[1]').click()
time.sleep(5)
###search the relavent paper


# In[21]:


def get_page_number():
    numbers_of_paper = driver.find_element_by_css_selector("body > app-wos > div > div > main > div > app-input-route > app-base-summary-component > app-search-friendly-display > div.search-display > app-general-search-friendly-display > h1 > span").text
    numbers_of_page = int((int(numbers_of_paper)-1)/50)+1
    return numbers_of_page


# In[22]:


def scroll_down():
    for i in range(12):
        time.sleep(2)
        driver.execute_script("window.scrollBy(0,1000)")


# In[23]:


def get_url():
    part_url_list = []
    for i in range(50):
        try:
            selector = "body > app-wos > div > div > main > div > app-input-route > app-base-summary-component > div > div.results.ng-star-inserted > app-records-list > app-record:nth-child("+str(i+1)+") > div.data-section.ng-star-inserted > div:nth-child(1) > app-summary-title > h3 > a"
            webpage_element = driver.find_element_by_css_selector(selector)
            paper_url = webpage_element.get_attribute('href')
            part_url_list.append(paper_url)
        except:
            pass
    return part_url_list


# In[24]:


def traverse_searched_result():
    url_list=[]
    page_number = get_page_number()
    for i in range(page_number):
        scroll_down()
        part_url_list = get_url()
        for url in part_url_list:
            url_list.append(url)
        next_page = driver.find_element_by_css_selector("body > app-wos > div > div > main > div > app-input-route > app-base-summary-component > div > div.results.ng-star-inserted > app-page-controls:nth-child(4) > div > form > div > button:nth-child(4) > span.mat-button-wrapper > mat-icon > svg")
        try:    
            next_page.click()
        except:
            break
    return url_list


# In[25]:


def get_doi():
    try:
        doi = driver.find_element_by_id("FullRTa-DOI").text
    except:
        doi = ''
    return doi


# In[26]:


def get_paper_link():
    try:
        driver.find_element_by_xpath("/html/body/app-wos/div/div/main/div/app-input-route/app-full-record-home/div[1]/app-page-controls/div/div[1]/div[1]/app-full-record-links/div/button").click()
        paper_href = driver.find_element_by_id("FRLinkTa-link-grouped-0").get_attribute("href")
    except:
        paper_href = ""
    return paper_href


# In[27]:


doi_title_dict = dict()
doi_link_dict = dict()
url_list = traverse_searched_result()
for url in url_list:
    driver.get(url)
    time.sleep(4)
    doi = get_doi()
    title = get_title()
    paper_link = get_paper_link()
    if len(paper_link) != 0 and len(doi) != 0:
        doi_title_dict[doi] = title
        doi_link_dict[doi] = paper_link


# In[28]:


title_data = pd.DataFrame(dict_to_list(doi_title_dict),columns = ['doi','title'])
link_data = pd.DataFrame(dict_to_list(doi_link_dict),columns = ['doi','paper link'])
Searched_data = pd.merge(title_data,link_data,how = "inner")


# In[43]:


filtered_doi = []
for doi in Searched_data["doi"]:
    if doi not in list(main_data['DOI']):
        filtered_doi.append(doi)
filtered_doi = list(set(list(filtered_doi)))


# In[44]:


len(filtered_doi)


# In[31]:


def get_page_number_for_reference():
    numbers_of_paper = driver.find_element_by_css_selector("#GenericFD-search-searchInfo-parent > span").text
    numbers_of_page = int((int(numbers_of_paper)-1)/50)+1
    return numbers_of_page


# In[32]:


def traverse_reference_result():
    url_list = []
    page_numbers = get_page_number_for_reference()
    for page in range(page_numbers):
        scroll_down()
        for i in range(50):
            try:
                selector = "body > app-wos > div > div > main > div > app-input-route > app-base-summary-component > div > div.results.ng-star-inserted > app-records-list > app-record:nth-child("+str(i+1)+") > div.data-section.ng-star-inserted > div:nth-child(1) > app-summary-title > h3 > a"
                webpage_element = driver.find_element_by_css_selector(selector)
                paper_url = webpage_element.get_attribute('href')
                url_list.append(paper_url)
            except:
                pass
        next_page = driver.find_element_by_css_selector("body > app-wos > div > div > main > div > app-input-route > app-base-summary-component > div > div.results.ng-star-inserted > app-page-controls:nth-child(4) > div > form > div > button:nth-child(4) > span.mat-button-wrapper > mat-icon > svg")
        try:    
            next_page.click()
        except:
            break
    return url_list


# In[33]:


driver.get(WOS_url)
initialize_search_box()
driver.find_element_by_xpath("""//*[@id="snSearchType"]/div[1]/app-search-row/div[1]/div[1]/app-select-search-field/wos-select""").click()
time.sleep(1)
driver.find_element_by_xpath("""//*[@id="global-select"]/div[1]/div[2]/div[18]""").click()


# In[35]:


refer_link_list = []
for doi in filtered_doi:
    initialize_search_box()
    driver.find_element_by_xpath("""//*[@id="snSearchType"]/div[1]/app-search-row/div[1]/div[1]/app-select-search-field/wos-select""").click()
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="global-select"]/div[1]/div[2]/div[18]""").click()
    driver.find_element_by_name("search-main-box").send_keys(doi)
    driver.find_element_by_xpath('//*[@id="snSearchType"]/div[3]/button[2]/span[1]').click()
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/app-wos/div/div/main/div/app-input-route/app-base-summary-component/div/div[2]/app-records-list/app-record/div[2]/div[1]/app-summary-title/h3/a').click()
    time.sleep(2)
    driver.find_element_by_xpath("""//*[@id="FullRRPTa-wos-citation-network-refCountLink"]""").click()
    driver.find_element_by_xpath("""//*[@id="FRMiniCrlTa-viewCitedRefLink"]""").click()
    paper_refer_url_list = traverse_reference_result()
    refer_link_list.append(paper_refer_url_list)
    driver.find_element_by_xpath("""//*[@id="breadcrumb"]/ul/li[1]/a""").click()


# In[36]:


filtered_result = dict()
for i in range(len(refer_link_list)):
    duplication_counter = 0
    refer_link = refer_link_list[i]
    for k in refer_link:
        if k in list(main_data['record link']):
            duplication_counter = duplication_counter + 1
    if duplication_counter == 0:
        filtered_result[filtered_doi[i]] = "cite data by other way"
    else:
        filtered_result[filtered_doi[i]] = "cite data by paper"
filtered_data = pd.DataFrame(dict_to_list(filtered_result),columns = ['doi','filtered result'])


# In[ ]:





# In[38]:


filtered_data[filtered_data["filtered result"] == 'cite data by other way']


# In[270]:


filtered_data[filtered_data["filtered result"] == 'cite data by paper']


# In[ ]:





# In[256]:


def lineage_method(data):
    dataset_contributor = [str("Contributor of ")+main_data['dataset'][data]]
    author_list = main_data["author"][data]
    total_contributor_number = int(len(dataset_contributor)) + int(len(author_list))
    cited_times = int(main_data['cited times'][data])
    title = main_data['title'][i]
    repeat_times = len(main_data[main_data['title'] == title])
    average_credit = cited_times / total_contributor_number / repeat_times
    return average_credit


# In[ ]:





# In[257]:


dataset_contributor_dictionary = dict()
for i in range(len(main_data)):
    dataset_contributor = str("Contributor of ")+main_data['dataset'][i]
    dataset_contributor_dictionary[dataset_contributor] = 0


# In[258]:


author_dictionary = dict()
for i in range(len(main_data)):
    try:
        current_author_list = main_data["author"][i]
        for k in current_author_list:
            author_dictionary[k] = 0
    except:
        pass


# In[259]:


for i in range(len(main_data)):
    try:
        average_credit = lineage_method(i)
        dataset_contributor = str("Contributor of ")+main_data['dataset'][i]
        current_d_credit = dataset_contributor_dictionary[dataset_contributor]
        current_d_credit = current_d_credit + average_credit
        dataset_contributor_dictionary[dataset_contributor] = current_d_credit
        
        current_author_list = main_data["author"][i]
        for k in current_author_list:
            current_a_credit = author_dictionary[k]
            current_a_credit = current_a_credit + average_credit
            author_dictionary[k] = current_a_credit
    except:
        pass


# In[260]:


sorted(dataset_contributor_dictionary.items(), key = lambda x:x[1],reverse = True)


# In[262]:


sorted(author_dictionary.items(), key = lambda x:x[1],reverse = True)

