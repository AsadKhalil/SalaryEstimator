# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:47:44 2020
@author: Asad
"""

import glassdoor_scrapper as gs
import pandas as pd

if __name__ == '__main__':

    path = "C:/Users/LunchON/Desktop/Books/Projects/SalaryEstimator/chromedriver"

    df = gs.get_jobs('data scientist',1000, False, path, 5)

    df.to_csv('glassdoor_jobs.csv', index = False)