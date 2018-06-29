# -*- coding:utf8 -*-

from selenium import webdriver
import pandas as pd
import numpy as np
import time
import os

plat_files = [i.split('.')[0].decode('gb18030') for i in os.listdir('plat')]

result = pd.DataFrame()

plat_company = pd.read_csv('plat_company.csv', encoding='gb18030')

miss_plat = []

#url = 'https://www.qichacha.com/search?key=%E7%BD%91%E8%B4%B7%E4%B9%8B%E5%AE%B6'

driver = webdriver.Firefox()
time.sleep(np.random.randint(3, 9))
driver.get("https://www.wdzj.com/")
time.sleep(np.random.randint(3, 9))
driver.get("https://www.qichacha.com/")
#time.sleep(np.random.randint(3, 9))
#driver.get(url)
#time.sleep(np.random.randint(3, 9))

time.sleep(90)

for row in plat_company.iterrows():
    if row[1]['plat_name'] not in plat_files:
        try:
            headerKey = driver.find_element_by_xpath("//input[@id='headerKey']")
            time.sleep(np.random.randint(1, 5))
            headerKey.clear()
            time.sleep(np.random.randint(1, 5))
            headerKey.send_keys(row[1]['company'])
            time.sleep(np.random.randint(1, 5))
            driver.find_element_by_xpath("//button[@class='btn btn-primary top-searchbtn']").click()
            time.sleep(np.random.randint(6, 9))
            srch_list = driver.find_elements_by_xpath("//table[@class='m_srchList']/tbody/tr[1]/td[2]/a")
            if srch_list and srch_list[0].text == row[1]['company']:
                #driver.get(srch_list[0].get_attribute('href'))
                srch_list[0].click()
                time.sleep(np.random.randint(6, 9))

                win_hds = driver.window_handles
                if len(win_hds) == 2:
                    STR_READY_STATE = ''
                    while STR_READY_STATE != 'complete':
                        time.sleep(np.random.random())
                        STR_READY_STATE = driver.execute_script('return document.readyState')
                    
                    driver.switch_to_window(driver.window_handles[1])
                    time.sleep(np.random.randint(1, 5))
                    driver.execute_script("window.scrollTo(0, %d)" % np.random.randint(520, 1314))
                    time.sleep(np.random.randint(1, 5))
                    driver.execute_script("window.scrollBy(0, %d)" % np.random.randint(520, 1314))
                    time.sleep(np.random.randint(1, 5))
                    change_info = pd.DataFrame([[tr.get_attribute('data-pname'), tr.find_element_by_xpath("td[1]").text,
                                                 tr.find_element_by_xpath("td[2]").text, tr.find_element_by_xpath("td[3]").text,
                                                 tr.find_element_by_xpath("td[4]").text,tr.find_element_by_xpath("td[5]").text]
                                                for tr in driver.find_elements_by_xpath("//section[@id='Changelist']/table/tbody/tr[position()>1]")],
                                               columns=['data_pname'] + [th.text for th in driver.find_elements_by_xpath("//section[@id='Changelist']/table/tbody/tr[1]/th")])
                    change_info['plat_name'] = row[1]['plat_name']
                    change_info['company'] = row[1]['company']
                    change_info.to_csv('plat/%s.csv' % row[1]['plat_name'], index=False, encoding='gb18030')
                    result = pd.concat([result, change_info])
                    np.random.randint(1, 5)
                    driver.close()
                    np.random.randint(1, 5)
                    time.sleep(np.random.random())
                    win_hds = driver.window_handles
                    if len(win_hds) == 1:
                        driver.switch_to_window(win_hds[0])
                    else:
                        driver.quit()
                        time.sleep(np.random.randint(6, 9))
                        driver = webdriver.Firefox()
                        time.sleep(np.random.randint(6, 9))
                        driver.get("https://www.wdzj.com/")
                        time.sleep(np.random.randint(6, 9))
                        driver.get("https://www.qichacha.com/")
                        #time.sleep(np.random.randint(6, 9))
                        #driver.get(url)
                        #time.sleep(np.random.randint(6, 9))
                        time.sleep(90)
                    if (row[0] + 1) % 30 == 0:
                        time.sleep(np.random.randint(300, 600))
                else:
                    miss_plat.append([row[1]['plat_name'], row[1]['company']])
            else:
                miss_plat.append([row[1]['plat_name'], row[1]['company']])
        except Exception, e:
            miss_plat.append([row[1]['plat_name'], row[1]['company']])
        
driver.quit()

result.to_csv('qichacha.csv', index=False, mode='a', encoding='gb18030')

if __name__ == "__main__":
    pass
