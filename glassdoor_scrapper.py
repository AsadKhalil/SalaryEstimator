# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:32:36 2020
author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:
        # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)
        # gdGrid
        try:
            driver.find_element_by_class_name("eigr9kq0").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element_by_css_selector(
                '[alt="Close"]').click()  # clicking to the X.
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed')
            pass
        # Test for the "Sign Up" prompt and get rid of it.
        print("HERE")
        # Going through each job in this page
        # eigr9kq0
        #//*[@id="MainCol"]/div[1]/ul
        #// *[ @ id = "MainCol"] / div[1] / ul / li[1]
        job_buttons = driver.find_elements_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[*]')

            # jl for Job Listing. These are the buttons we're going to click.
        i = 1
        for job_button in job_buttons:

            print(len(job_buttons))
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            # job_button.click()  # You might
            driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{i}]').click()
            print("this")
            time.sleep(5)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{i}]/div[2]/div[1]/a/span').text
                    location = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{i}]/div[2]/div[2]/span').text
                    job_title = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{i}]/div[2]/a/span').text
                    # job_description = driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[*]/div[2]/div[4]').text
                    collected_successfully = True
                    print("h")
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{i}]/div[2]/div[3]/div[1]/span').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{i}]/div[1]/span').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            # if verbose:
            print("Job Title: {}".format(job_title))
            print("Salary Estimate: {}".format(salary_estimate))
            # print("Job Description: {}".format(job_description[:500]))
            print("Rating: {}".format(rating))
            print("Company Name: {}".format(company_name))
            print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            print("hh")

            i += 1
            print(i)

            try:
                # driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[{i}]').click()

                try:
                    size = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
                except NoSuchElementException:
                    revenue = -1
            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            print("Size: {}".format(size))
            print("Founded: {}".format(founded))
            print("Type of Ownership: {}".format(type_of_ownership))
            print("Industry: {}".format(industry))
            print("Sector: {}".format(sector))
            print("Revenue: {}".format(revenue))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('//*[@id="MainCol"]/div[2]/div/div[1]/button[7]').click()
        except NoSuchElementException:
            print(
                "Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                    num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.