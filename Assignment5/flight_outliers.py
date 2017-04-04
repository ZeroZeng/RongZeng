import bs4
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from unidecode import unidecode
import pandas as pd
import datetime
from dateutil.parser import parse
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt

########### task 1 ##########
def scrape_data(start_date, from_place, to_place, city_name):

    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/')
    time.sleep(1.5)
    #input to_place
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.5)
    #input from_place
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.5)
    #input start_date
    driver.get(driver.current_url[:-10]+start_date)
    time.sleep(0.5)
    #find the city_name
    data = []
    city_name0=unicode(city_name,'utf-8')
    city_name_unicode=unidecode(city_name0)
    city_name1=city_name_unicode.lower().split(' ')
    city_name2=''
    for i in range(len(city_name1)):
        city_name2=city_name2+city_name1[i][0].upper()+city_name1[i][1:]+' '
    city_name2=city_name2.strip()
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for result in results:
        if city_name2 in result.text:
            bars = result.find_elements_by_class_name('LJTSM3-w-x')

            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.0001)
                data.append((result.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                             result.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
        else:
            pass
    time.sleep(0.01)
    driver.quit()
    return data

########### task 2 ##########
def scrape_data_90(start_date, from_place, to_place, city_name):

    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/')
    time.sleep(1.5)
    #input to_place
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[4]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(to_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.5)
    #input from_place
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[3]/div/div[2]/div/div')
    to_input.click()
    actions = ActionChains(driver)
    actions.send_keys(from_place)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(0.5)
    #input start_date
    driver.get(driver.current_url[:-10]+start_date)
    time.sleep(0.5)
    #find the city_name
    data = []
    city_name0=unicode(city_name,'utf-8')
    city_name_unicode=unidecode(city_name0)
    city_name1=city_name_unicode.lower().split(' ')
    city_name2=''
    for i in range(len(city_name1)):
        city_name2=city_name2+city_name1[i][0].upper()+city_name1[i][1:]+' '
    city_name2=city_name2.strip()
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for result in results:
        if city_name2 in result.text:
            bars = result.find_elements_by_class_name('LJTSM3-w-x')

            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.0001)
                data.append((result.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                             result.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
        else:
            pass
    time.sleep(0.5)
    to_input = driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/div[5]/div')
    to_input.click()
    time.sleep(0.5)
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    for result in results:
        if city_name2 in result.text:
            bars = result.find_elements_by_class_name('LJTSM3-w-x')

            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.0001)
                data.append((result.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,
                             result.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))
        else:
            pass

    data=data[:60]+data[-30:]
    driver.quit()
    return data

########## task 3 part 1 ##########

def task_3_dbscan(flight_data):
    clean_data = [(float(d[0].replace('$', '').replace(',', '')),
                   (parse(d[1].split('-')[0].strip()) - parse(flight_data[0][1].split('-')[0].strip())).days,
                   reduce(lambda x, y: y - x, [parse(x.strip()) for x in d[1].split('-')]).days) for d in flight_data]
    df = pd.DataFrame(clean_data, columns=['Price', 'Start_Date', 'Trip_Length'])

    X = StandardScaler().fit_transform(df[['Start_Date', 'Price']])
    db = DBSCAN(eps=.5, min_samples=3).fit(X)

    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    plt.subplots(figsize=(12, 8))

    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                 markeredgecolor='k', markersize=14)

    plt.title("Total Clusters: {}".format(clusters), fontsize=14, y=1.01)
    df['dbscan_labels'] = db.labels_
    plt.savefig('task_3_dbscan.png')
    outliers = df[df['dbscan_labels'] == -1].copy()
    outliers_1 = zip(outliers.Start_Date, outliers.Price)
    clusters = df[df['dbscan_labels'] != -1].copy()
    clusters_1 = zip(clusters.Start_Date, clusters.Price, clusters.dbscan_labels)
    outliers_label = []
    for outlier in outliers_1:
        min_cluster_label = -1
        min_dist = 9999
        for cluster in clusters_1:
            dist = (float(outlier[0]) - float(cluster[0])) ** 2 + ((float(outlier[1]) - float(cluster[1])) / 100) ** 2
            # I think the weight of date in distance is more important than weight of price. Therefore, I did not use Euclidean distance.
            if dist < min_dist:
                min_dist = dist
                min_cluster_label = cluster[2]
        outliers_label.append(min_cluster_label)
    outliers_2 = zip(outliers.Start_Date, outliers.Price, outliers_label)
    agg = df[df['dbscan_labels'] != -1].groupby('dbscan_labels')['Start_Date', 'Price'].agg(
        ['std', 'mean', 'count']).copy()
    outliers_3 = []
    for outlier in outliers_2:
        mean = agg[agg.index == outlier[2]]['Price']['mean']
        std = max(float(agg[agg.index == outlier[2]]['Price']['std']), 10)
        line = max(float(mean - 2 * std), 50)
        if outlier[1] < line:
            outliers_3.append(outlier[0])
    if len(outliers_3) == 0:
        return 'There is no low price outlier.'
    else:
        return df.loc[outliers_3]

########## task 3 part 2 ##########

def task_3_IQR(flight_data):
    clean_data = [(float(d[0].replace('$', '').replace(',', '')),
               (parse(d[1].split('-')[0].strip()) - parse(flight_data[0][1].split('-')[0].strip())).days,
               reduce(lambda x,y: y-x, [parse(x.strip()) for x in d[1].split('-')]).days) for d in flight_data]
    df = pd.DataFrame(clean_data, columns=['Price', 'Start_Date', 'Trip_Length'])
    plt.boxplot(df['Price']);
    plt.savefig('task_3_iqr.png')
    Q1 = df.Price.describe()['25%']
    Q3 = df.Price.describe()['75%']
    IQR = Q3 - Q1
    low_line = Q1 - 1.5 * IQR
    result = df[df['Price'] < low_line]
    if len(result) == 0:
        return 'No outliers'
    else:
        return result

########## task 4 ##########

def task_4_dbscan(flight_data):
    clean_data = [(float(d[0].replace('$', '').replace(',', '')),
                   (parse(d[1].split('-')[0].strip()) - parse(flight_data[0][1].split('-')[0].strip())).days,
                   reduce(lambda x, y: y - x, [parse(x.strip()) for x in d[1].split('-')]).days) for d in flight_data]
    df = pd.DataFrame(clean_data, columns=['Price', 'Start_Date', 'Trip_Length'])
    X = df[['Start_Date', 'Price']].values * np.array([20, 1])
    radius = np.sqrt(np.square(20.00) + np.square(20.00))
    db = DBSCAN(eps=radius, min_samples=3).fit(X)

    df['dbscan_labels'] = db.labels_

    clusters = df.dbscan_labels.unique()
    clusters_5 = []
    for cluster in clusters:
        if cluster != -1 and len(df[df['dbscan_labels'] == cluster]) > 4:
            for i in range(len(df[df['dbscan_labels'] == cluster]) - 4):
                clusters_5.append(df[df['dbscan_labels'] == cluster]['Start_Date'].values[i:i + 5])
    mean_min = 9999
    cluster_mean_min = []
    for cluster_5 in clusters_5:
        df_5 = df.loc[cluster_5][['Start_Date', 'Price']]
        cluster_max = df_5['Price'].max()
        cluster_min = df_5['Price'].min()
        cluster_mean = df_5['Price'].mean()
        if cluster_max - cluster_min <= 20 and cluster_mean < mean_min:
            mean_min = cluster_mean
            cluster_mean_min = cluster_5
        else:
            pass
    if len(cluster_mean_min) == 0:
        return 'No required value'
    else:
        return df.loc[cluster_mean_min]