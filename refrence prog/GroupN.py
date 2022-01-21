"""
Preface:
This project is created as group assignment for "MSCI530: Data Sourcing, Handling and Programming [1]"

Summary: 

This project is designed to view, add, update and analyze hospital's Accident and Emergency
Department's (AEDs) patient database in England.

The interface has 5 main classes:
    (i) Inquiry Face: This window can be used to access and filter the patient database.
    (ii) Record Face: This window facilitates the user to view the filtered records.
    (iii) Add Face: This window enables the user to add new patient records.
    (iv) Update Face: This window to update information about existing 
    patients regarding investigations, treatments and discharge.
    (v) Summary Face: This window returns a summary report of the patient database including 
    summary statistics and graphs. 
    
"""
# Installing packages
# pip install pandastable
# pip install tkcalendar
# pip install seaborn

# Importing necessary packages
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import re
from tkinter import messagebox
from pandastable import Table
from tkcalendar import *
from tkinter.colorchooser import askcolor
from tkinter.tix import *
import warnings
import numpy as np
import pandas as pd
import requests
import datetime
import calendar
from os import getcwd
import io
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns
import matplotlib.pyplot as plt

'''Following are the code for database'''
class CriteriaQuery():
    '''
    This class interacts with interface.py.
    It receives a dataframe that stores all the user inputs and 
    returns all the records that meet the criteria.
    '''    
    
    patient_count = 0


    def __init__(self):
        '''
        This function does the following :
        (i) Tries to read the file that the user has specified
        (ii) Checks if the file is in the local directory and reads it
        (iii) If the the file is not present in the local directory, it pulls it
        from git hub, reads it and saves it in the local directory.
        
        Input: The path of the filename specified by the user
        '''

        directory = getcwd()
        filename =  directory + '\\AED4weeks.csv'
        try:
            self.record = pd.read_csv(filename) # Reading the file
            self.record = pd.DataFrame(self.record) # Converting it into a dataframe
        except:
            url = "https://raw.githubusercontent.com/DivyaSherwani/MSCI530/main/AED4weeks.csv"
            r = requests.get(url).content # Sends a request to the specified URL
            
            self.record = pd.read_csv(io.StringIO(r.decode('utf-8')))
            self.record = pd.DataFrame(self.record)
            # Creating a file in the local directory
            f = open(filename,'wb')
            f.write(r)
            f.close()
        
        self.patient_count = self.record.iloc[-1,self.record.shape[1]-1]  
        # print(self.patient_count)


    def condition_matching(self, index):
        '''
        This function is called by the RecordFace in interface.py. It receives a dataframe
        which has the user inputs for filters and then filters the patients records in the
        database (self.record) and returns it (self.subset).
        '''
        
        self.index = index # The dataframe containing user inputs
        self.subset = self.record # Creating a copy of the main database which would contain 
        # the filtered records
        
        # Filter on the basis of ID
        # self.index.iloc[0,2] contains the ID 'from' value
        # self.index.iloc[0,3] contains the ID 'to' value
        if self.index.iloc[0,2] == "" and self.index.iloc[0,3] == "":
            pass
        elif self.index.iloc[0,2] == "" and self.index.iloc[0,3] != "":
            self.subset = self.subset[self.subset.iloc[:,0] <= self.index.iloc[0,3]]
        elif self.index.iloc[0,2] != "" and self.index.iloc[0,3] == "":
            self.subset = self.subset[self.subset.iloc[:,0] >= self.index.iloc[0,2]]
        else:
            self.subset = self.subset[(self.subset.iloc[:,0] >= self.index.iloc[0,2]) & (self.subset.iloc[:,0] <= self.index.iloc[0,3])]
        
        # Loop to filter data on the basis of age and day
        # self.index.iloc[i,2] contains the 'from' value
        # self.index.iloc[i,3] contains the 'to' value
        for i in range(1,3):
            if self.index.iloc[i,2] == "" and self.index.iloc[i,3] == "":
                pass
            elif self.index.iloc[i,2] == "" and self.index.iloc[i,3] != "":
                self.subset = self.subset[self.subset.iloc[:,i] <= int(self.index.iloc[i,3])]
            elif self.index.iloc[i,2] != "" and self.index.iloc[i,3] == "":
                self.subset = self.subset[self.subset.iloc[:,i] >= int(self.index.iloc[i,2])]
            else:
                self.subset = self.subset[(self.subset.iloc[:,i] >= int(self.index.iloc[i,2])) & (self.subset.iloc[:,i] <= int(self.index.iloc[i,3]))]
                    
        # Filters data on the basis of HRG
        if self.index.iloc[3,2] == "":
            self.subset = self.subset
        else:
            self.subset = self.subset[self.subset["HRG"] == self.index.iloc[3,2]]
               
        # Filters data to show records of only breached patients or non breached patients 
        # or both depending on the option chosen by the user in the radio button
        if self.index.iloc[4,2] == 1 and self.index.iloc[4,3] == 0: # return info of breach patients
            self.subset = self.subset[self.subset["Breachornot"] == "breach"] 
        elif self.index.iloc[4,2] == 0 and self.index.iloc[4,3] == 1: # return info of non breach patients
            self.subset = self.subset[self.subset["Breachornot"] == "non-breach"]
        else:
            self.subset = self.subset
            
        # Sorts the data on the basis of variable and order (ascending or descending) chosen 
        # by the user
        # If user selects ascending, the variable 'order' will be True
        if self.index.iloc[6,2] == "Ascending":
            order = True
        else:
            order = False
        # If user does not specify any variable, patient records are sorted on the basis
        # of ID
        if self.index.iloc[5,2] == "":
            self.subset.sort_values("ID", inplace = True, ascending = order)
        else:
            self.subset.sort_values(self.index.iloc[5,2], inplace = True, ascending = order)
        
        # Error message is printed if none of the records match the filters
        if len(self.subset) == 0:
            print("Sorry could not find records.")
        else:
            pass
        
        return self.subset
    
class CatalogData(CriteriaQuery):
    '''
    This class is called by the Inquiry Face in the interface.py to display the options
    that need to be shown in the drop down list for HRG and 'Sort by'. This class inherits
    the database from the CriteriaQuery class to get access to the patient records 
    from which it can extract the unique values of HRG. This connection is made so that 
    every time the patient database is updated with a new HRG, the drop down list in 
    the Inquiry face is also updated.
    '''  
    
    def __init__(self,index):
        '''
        This function defines the index variable for the instance and calls the init operator
        of the parent class.
        '''
        self.index = index
        super().__init__()

    def condition_list(self):
        '''
        This function is called by the InquiryFace in interface.py.
        return a list of all the values of a filter conditon received
    '''
       
        if self.index =="HRG":
            self.cdtn_list = list(self.record["HRG"].dropna().unique())
        elif self.index == "Sort_by":
            self.cdtn_list = ["ID", "Age", "Day", "HRG"]

        return self.cdtn_list  

class AddRecord(CriteriaQuery):
    '''
    This class is defined by the Add Record Face to get the details of the new patient entered
    by the user and insert the new record in the existing database.
    '''
    
    def __init__(self, new_record):
        '''
        This function defines the new record as self.new_record and calls the init operator
        of the parent class.
        '''
        self.new_record = new_record
        super().__init__()

    
    def insert_record(self):
        '''
        This function does the following:
        (i) Initializes the noofinvestigation and nooftreatment as 0 for the new patient
        (ii) Extracts the Day, Dayofweek and Period from the Arrival Date and Arrival Time
        (iii) Calulates the noofpatients for the new patient as the noofpatients for the 
        previous patient plus any admissions minus any discharges
        (iv) Append the existing dataframe with the new record
        '''
        # Initiliazing variables
        # print(CriteriaQuery.patient_count)
        self.noofinvestigation = 0
        self.nooftreatment = 0
        self.new_record["nooftreatment"] = self.nooftreatment
        self.new_record["noofinvestigation"] = self.noofinvestigation
        # Extracting Day, Dayofweek and Period from Arrival Date and Arrival Time
        self.new_record["Day"] = self.new_record["Arrival Date"].day + 1
        self.new_record["DayofWeek"] = calendar.day_name[self.new_record["Arrival Date"].weekday()]
        self.new_record["Period"] = datetime.datetime.strptime(self.new_record["Arrival Time"],"%H:%M").hour
        # Adding 1 to the class variable patient count 
        CriteriaQuery.patient_count += 1
        # Creating a dictionary which will be added to the database
        self.new_record["noofpatients"] = CriteriaQuery.patient_count + self.patient_count
        self.new_patient = {key: self.new_record[key] for key in self.new_record.keys()
                               & {'ID', 'Age', 'Day', 'DayofWeek','Period', 
                                  'noofpatients', 'noofinvestigation', 'nooftreatment'}}
        # Appending the dataframe
        self.record = self.record.append(self.new_patient, ignore_index = True)
        # Writing the updated file to the local directory
        directory = getcwd()
        filename =  directory + '\\AED4weeks.csv'
        # print(CriteriaQuery.patient_count)
        self.record.to_csv(filename, index = False)
        
        
    def id_checker(self, new_id):
        '''
        This function checks if the ID entered by the user exists in the patient database. 
        If yes, it sets the variable self.proceed as 0 which goes to the interface.
        The user is then automatically redirected to the 'Update Patient Database' page.
        If no, it sets the variable self.proceed as 1 which is used by the interface to
        return a message box saying that 'Record has been added successfully.'
        '''
        if new_id not in self.record["ID"].values:
            self.proceed = 1
        else:
            self.proceed = 0
        return self.proceed
    
class UpdateRecord(CriteriaQuery):
    '''
    This class is defined to update information for already existing patient records.
    This may be with regard to investigation , treatment or discharge of a patient.
    '''
    def __init__(self, update_record):
        '''
        This function defines the new record as self.update_record and calls the init operator
        of the parent class.
        '''
        self.new_record = update_record
        super().__init__()

    
    def update_record(self):
        '''
        This function does the following:
        (i) If diagnosis is selected by the user, noofinvestigation is updated
        (ii) If treatment is selected by the user, nooftreatment and HRG is updated
        (iii) If discharge is selected, LOS is updated and patient is classified as 
        breach or non-breach
        '''
        
        if self.new_record["noofinvestigation"] != "":
            # Updates noofinvestigation
            self.record.iloc[self.record.index[self.record['ID'] == self.new_record["ID"]].tolist(),8] += 1
        elif self.new_record["HRG"] != "":
            self.record.iloc[self.record.index[self.record['ID'] == self.new_record["ID"]].tolist(),9] += 1
            new_code = self.new_record["HRG"]
            self.record.iloc[self.record.index[self.record['ID'] == self.new_record["ID"]].tolist(),7] = new_code
        elif self.new_record["LOS"] != "":
            CriteriaQuery.patient_count = CriteriaQuery.patient_count - 1
            self.record.iloc[self.record.index[self.record['ID'] == self.new_record["ID"]].tolist(),5] = int(self.new_record["LOS"])
            # Classifies patients as breach or non breach depending on LOS
            if int(self.new_record["LOS"]) >= 240:
                self.record.iloc[self.record.index[self.record['ID'] == self.new_record["ID"]].tolist(),6] = "breach"
            else:
                self.record.iloc[self.record.index[self.record['ID'] == self.new_record["ID"]].tolist(),6] = "non-breach"
        else:
            pass
        
        
        # Writing the updated dataframe to a csv
        directory = getcwd()
        filename =  directory + '\\AED4weeks.csv'
        self.record.to_csv(filename, index = False)
        
        
    def id_checker(self, new_id):
        '''
        This function checks if the ID entered by the user exists in the patient database. 
        If yes, it sets the variable self.proceed as 1 which is used by the interface to
        return a message box saying that 'Record has been updated successfully.' 
        If no, it sets the variable self.proceed as 0 which then goes to the interface. 
        The user is then automatically redirected to the 'New Patient Registration' page.
        '''
        if new_id not in self.record["ID"].values:
            self.proceed = 0
        else:
            self.proceed = 1
        return self.proceed
    
class SumryFace(CriteriaQuery):
    '''
    This class is designed to power the summary dashboard in the interface with appropriate
    tables and plots which will help the user to have an understanding about the patient
    records in a simple and comprehensive manner.
    '''
    def plot_data(self):
        '''
        There are 5 pages in total in the graphical part of the summary tab. Plots are designed
        separately for each of the 5 pages and there are buttons on the interface to help the user
        browse through these pages.
        '''
        
        '''
        Page 1
        This page is an overview of the patient records mainly focussed at looking at each of the 
        variables separately (univariate analysis).
        Plot 1: Count of patients vs Breach or not
        Plot 2: Count of patients vs HRG
        Plot 3: Count of patients vs Number of investigations
        Plot 4: Count of patients vs Number of treatments
        Plot 5: Count of patients vs Day of week
        Plot 6: Count of patients vs Period
        '''
        # Defines figure dimensions and subplots
        fig1=plt.figure(figsize=(21.5,10))
        axes30=fig1.add_subplot(2,3,1)
        axes31=fig1.add_subplot(2,3,2)
        axes32=fig1.add_subplot(2,3,3)
        axes33=fig1.add_subplot(2,3,4)
        axes34=fig1.add_subplot(2,3,5)
        axes35=fig1.add_subplot(2,3,6)
        
        # Rotates the x axis labels of the plots by 20 degrees
        axes31.tick_params(axis = 'x', rotation = 20)
        axes34.tick_params(axis = 'x', rotation = 20)
        
        # Plot 1: Breach or not
        breachpie = pd.DataFrame(self.record.groupby("Breachornot").count()["ID"])
        breachpie.plot.pie(y = "ID", colors = ["grey", "#6d3657"], ax = axes30, title = "Breach and Non Breach", legend = None)
        circle = plt.Circle((0,0), 0.7, color='white')
        p=plt.gcf()
        p.gca().add_artist(circle)
        axes30.set_ylabel(" ")
         
        # Plot 2: HRG
        sns.countplot(x="HRG", palette="ch:.25", data=self.record,ax=axes31).set(title='HRG', xlabel = None, ylabel = 'Count of patients')
        
        # Plot 3: Number of investigations
        sns.countplot(x="noofinvestigation", palette="ch:.25", data=self.record,ax=axes32).set(title='Number of investigations', xlabel = None, ylabel = 'Count of patients')
        
        # Plot 4: Number of treatments
        sns.countplot(x="nooftreatment", palette="ch:.25", data=self.record,ax=axes33).set(title='Number of treatments', xlabel = None, ylabel = 'Count of patients')

        # Plot 5: Day of Week
        sns.countplot(x="DayofWeek", palette="ch:.25", data=self.record,ax=axes34).set(title='Day of Week',xlabel = None, ylabel = 'Count of patients')
        
        # Plot 6: Period
        sns.countplot(x="Period", palette="ch:.25", data=self.record,ax=axes35,).set(title='Period', xlabel = None, ylabel = 'Count of patients')
        
        # Sets overall title for the plot
        fig1.suptitle("Overview", fontsize = 18, fontweight="bold")
        
        '''
        Page 2
        This page shows the correlation matrix which would help the user to understand
        interrelationships between various Hospital KPI's.'
        '''
        # Defines figure dimensions and subplots
        fig2 = plt.figure(figsize=(21.5,10))
        # Sets the colour palette
        cmap = sns.cubehelix_palette(as_cmap=False)
        # Plots the heatmap
        sns.heatmap(self.record.corr(),annot=True,linewidths=1,cmap=cmap)
        # Rotates x tick labels by 20 degrees
        plt.xticks(rotation=12)
        # Sets title for the plot
        plt.suptitle("AED KPI's Correlation Matrix", fontsize = 18, fontweight = "bold")
        
        
        '''
        Page 3
        This page provides an analysis of patients who have breached and those who have not 
        breached. It provides a comparative analysis of metrics for the breach and non breach
        category. (bivariate analysis)
        Plot 1: Boxplot of all patients
        Plot 2: Boxplot of breached patients
        Plot 3: Boxplot of non breached patients
        Plot 4: Number of investigations vs Breach or not
        Plot 5: Number of treatments vs Breach or not
        '''
        # Defines figure dimensions and subplots
        fig3=plt.figure(figsize=(21.5,10))
        axes30=fig3.add_subplot(2,3,1)
        axes31=fig3.add_subplot(2,3,2)
        axes32=fig3.add_subplot(2,3,3)
        axes33=fig3.add_subplot(2,2,3)
        axes34=fig3.add_subplot(2,2,4)

        # Rotates the x axis labels of the plots by 12 degrees
        axes30.tick_params(axis='x', rotation=12)
        axes31.tick_params(axis='x', rotation=12)
        axes32.tick_params(axis='x', rotation=12)
        
        # Filters the main data for breach and non breach patients and creates two subsets
        self.record_breach = self.record[self.record["Breachornot"] == "breach"]
        self.record_nonbreach = self.record[self.record["Breachornot"] == "non-breach"]

        # Plot 1: Box plot for all the patients
        sns.set_theme(style="whitegrid")
        sns.boxplot(data=self.record,palette="ch:.25", ax = axes30).set(title = 'Overview of Patients', ylim = (0,650))
        
        # Plot 2: Box plot for breached patients
        sns.boxplot(data=self.record_breach,palette="ch:.25",ax=axes31).set(title = 'Overview of Breached Patients', ylim = (0,650))
        
        # Plot 3: Box plot for non breached patients
        sns.boxplot(data=self.record_nonbreach,palette="ch:.25",ax=axes32).set(title = 'Overview of Non Breached Patients', ylim = (0,650))
        
        # Plot 4: Number of investigations vs Breach or not
        sns.boxplot(x="Breachornot", y="noofinvestigation",palette="ch:.25",
        data = self.record,ax=axes33).set(title='No of investigations vs Breach')
        
        # Plot 5: Number of treatments vs Breach or not
        sns.boxplot(x="Breachornot", y="nooftreatment",palette="ch:.25",
        data = self.record,ax=axes34).set(title='No of treatments vs Non Breach')
        
        # Sets the title for the overall plot
        fig3.suptitle("KPI's by Breach and Non Breach", fontsize = 18, fontweight = 'bold')
        
        
        '''
        Page 4
        This page provides an analysis of the breached patients with respect to HRG.
        Plot 1: Count of breaches vs HRG
        Plot 2: Count of breaches vs Day of Week
        Plot 3: Count of breaches vs Period
        Plot 4: Treatment to Investigation Ratio by HRG
        PLot 5: Treatment to Investigation Ratio and Breaches by HRG
        ''' 
        # Defines figure dimensions and subplots
        fig4=plt.figure(figsize=(21.5, 10))
        axes30=fig4.add_subplot(2,2,1)
        axes31=fig4.add_subplot(2,2,2)
        axes32=fig4.add_subplot(2,3,4)
        axes33=fig4.add_subplot(2,3,5)
        axes34=fig4.add_subplot(2,3,6)
        
        # Plot 1: Count of breaches vs HRG
        sns.set_theme(style="whitegrid")
        sns.countplot(x="HRG", palette="ch:.25", data=self.record_breach,ax=axes30,
                      order = self.record_breach['HRG'].value_counts(ascending=True).index).set(title='HRG', ylabel = "Count of patients")
        
        # Plot 2: Count of breaches vs Day of Week
        sns.countplot(x="DayofWeek", palette="ch:.25", data=self.record_breach,ax=axes31,
                     order = self.record_breach['DayofWeek'].value_counts(ascending=True).index ).set(title='Day Of Week', xlabel = None)
        
        # Plot 3: Count of breaches vs Period
        sns.countplot(x="Period", palette="ch:.25", data=self.record_breach,
                      ax=axes32,order = self.record_breach['Period'].value_counts(ascending=True).index).set(title='Period')
        
        # Plot 4 : Treatment to Investigation Ratio by HRG
        af = self.record.groupby(["HRG"]).sum()
        af['Result'] = (af['nooftreatment']/af['noofinvestigation'])*100
        af["Result"] = af["Result"].replace([np.inf, -np.inf], np.nan)
        af=af.reset_index()
        
        sns.barplot(x="HRG",y="Result",data=af,ax = axes33, palette="ch:.25").set(ylabel = 'Treatment to Investigation Ratio', title = "Treatment to Investigation Ratio")        
        
        # Plot 5:Treatment to Investigation Ratio and Breaches by HRG
        af["Result"] = round(af["Result"].replace(np.NaN, 620))
        af = af.set_index("HRG")
        df_breaches = self.record.pivot_table(index = "HRG", columns = "Breachornot", values = "ID", aggfunc = lambda x: len(x))
        df_breaches["breach"] = df_breaches["breach"].replace(np.NaN, 0)
        df_breaches["Treatment Investigation Ratio"] = af["Result"]
        
        sns.set_style("whitegrid", {'axes.grid' : False})
        sns.scatterplot(x="breach", y="Treatment Investigation Ratio", palette="ch:.25", hue = "HRG", data=df_breaches,ax = axes34).set(title = "Treatment Investigation Ratio vs Breaches", xlabel = "Number of breaches")
        
        
        fig4.suptitle("Analysis of Breaches by HRG", fontsize = 18, fontweight = 'bold')
        
        '''
        Page 5
        This page analysis the number and percntage of breaches by day and period.
        Plot 1: Percentage of patients who breached vs Day of Week
        Plot 2: Number of patients and Number of breaches by Period
        '''
        # Defines figure dimensions and subplots
        fig5=plt.figure(figsize=(21.5,10))
        axes30=fig5.add_subplot(2,1,1)
        axes31=fig5.add_subplot(2,1,2)
        
        # Plot 1: Percentage of Patients who breached by Day of Week
        data = self.record.pivot_table(index = "DayofWeek", columns = "Breachornot", values = "ID", aggfunc = lambda x: len(x))
        data = data.reset_index()
        # Sorts the values by day of week
        data["DayofWeek"] = data["DayofWeek"].astype("category")
        sorter = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        data["DayofWeek"].cat.set_categories(sorter, inplace=True)
        data = data.sort_values(["DayofWeek"])
        # Magnifiying the percnatage to be displayed
        data["Rate"] = round((data["breach"]/data["non-breach"]),2)
        data["Rate*60"] = data["Rate"]*1500
        data["Percentage Breached"] = round((data["breach"]/data["non-breach"])*100,2)
        data.reset_index(inplace = True)
        data.sort_index()
        
        # Plots the line chart
        data[['DayofWeek', 'Rate*60']].plot(x='DayofWeek', linestyle='-', marker='o', ax=axes30, color="black", grid = False)
        
        # Plots the bar chart
        data[['DayofWeek', 'non-breach', 'breach']].plot(x='DayofWeek', kind='bar', ax=axes30, color=["#6d3657", "#d3ab99"], rot = 20,
                                                         title = "Percentage of Patients who Breached vs Day of Week", grid = False)
        
        axes30.set_xlabel('')
        
        # Plot 2: Number of patients and Number of breaches vs Period
        data = self.record.pivot_table(index = "Period", columns = "Breachornot", values = "ID", aggfunc = lambda x: len(x))
        data["Number of breaches"] = data["breach"].replace([np.NaN],0)
        data["Number of breaches"] = data["Number of breaches"].astype(int)
        data.reset_index(inplace = True)
        data.sort_index()
        
        # Sets the y-axis color and label
        axes31.set_ylabel('Number of patients', fontsize=12) 
        axes31.tick_params(axis='y')
        
        # Plots the line chart
        data[['Period', 'Number of breaches']].plot(x='Period', linestyle='-', marker='o', ax=axes31, color="black", rot = 45, 
                                                   title = "Number of Patients and Number of Breaches by Period")
        
        # Setting the line chart marker labels
        x = list(range(0,24)) #Getting the x-axis ticks to plot the label
        for a,b, c in zip(x,data['Number of breaches'], data['Number of breaches']):
            plt.text(a-.1,b+25,c, color='white', fontsize=8)
        
        # Plots the bar chart
        data[['Period', 'non-breach', 'breach']].plot(x='Period', kind='bar', ax=axes31, color=["#6d3657", "#d3ab99"],stacked=True,grid=False)
        
        # Sets the y-axis color and label
        axes31.set_xlabel("Period", fontsize=12) 
        
        # Sets the title for the overall plot
        fig5.suptitle("Day of Arrival and Arrival Time", fontsize = 18, fontweight="bold")     
        
        '''
        Page 6
        This page provides a comparative analysis of patients falling in different age groups.
        Plot 1: Age and Number of Investigations
        Plot 2: Age Group
        Plot 3: Age Group vs Breach or not
        Plot 4: LoS by Age Group
        '''
        fig6=plt.figure(figsize=(21.5,10))
        axes30=fig6.add_subplot(2,1,1)
        axes31=fig6.add_subplot(2,3,4)
        axes32=fig6.add_subplot(2,3,5)
        axes33=fig6.add_subplot(2,3,6)

        axes30.grid(False)
        
        
        # Plot 1: Age vs Number of investigations
        sns.scatterplot(x="Age", y="noofinvestigation", hue="Breachornot",palette="ch:.25", 
                        data=self.record, size="Age",sizes=(40, 250), ax = axes30).legend(loc='upper right',fontsize='9')
        axes30.set_xlabel('')
        
        # Plot 2: Age Group
        df_1 = self.record
        # Creates age group buckets
        bins = [-1,18,66,120]
        labels = ['0-17 ','18-65', '>65']
        df_1['Age_Bin']=pd.cut(df_1['Age'], bins=bins, labels=labels)
        # Plots pie chart of patients under different age groups
        df_1.groupby("Age_Bin").count()["ID"].plot.pie(y ="ID", colors = ['#e5d7c2','#9b586c','#371a36'], ax = axes31, title = "Age Group", xlabel = None, ylabel = None)
        axes31.set_ylabel("")
        
        # Plot 3: Age Group vs Breach or not
        df_1["Count_Age_bin"] = df_1['Age_Bin'].count()
        df_2 = df_1[["ID", "Age","Breachornot", "Age_Bin"]]
        
        sns.countplot(x="Age_Bin",data=df_2, hue = "Breachornot", palette="ch:.25", dodge = False, ax = axes32).set(title = "Age Group vs Breach or not", ylabel = "Count of patients")
             
        # Plot 4: LoS by Age Group
        sns.boxplot(x="Age_Bin", y="LoS",palette="ch:.25", data = df_1, ax = axes33).set(title='LoS vs Age Group', xlabel = None, ylabel = "Length of Stay")
        axes33.set_xlabel('')
        
        # Sets overall title for the plot
        fig6.suptitle("Analysis by Age", fontsize = 18, fontweight="bold")

        return fig1,fig2,fig3, fig4, fig5, fig6

'''Following is the code for interface'''
class Basedesk():
    '''Initialize window properties'''   
    
    def __init__(self, master = None):
        self.root = master
        self.root.config()
        self.root.title('Accident and Emergency Departments (AEDs) System')
        
        # Set up window dimension
        self.width = root.winfo_screenwidth()         # Get the screen width and use it as the window width
        self.height = root.winfo_screenheight()       # Get the screen height and use it as the window height
        self.root.geometry('{}x{}'.format(self.width,self.height))  # Set window size 
        self.root.attributes('-topmost', True)        # Make the window full screen
        InitFace(self.root)                           # Calling the initial face to enter main window

class InitFace(object):
    '''
    This class is used to create the initial interface window.
    The Init face has four buttons: 
    (i) Patient Database: Used to access the existing database and extract required information.
    (ii) New Patient Registration: Used to register a new patient, mainly during admission.
    (iii) Update Existing Database: Used to update records of an admitted patient, 
    can be used to enter updates regarding diagnosis or treatment or discharge.
    (iv) Summary: Used to generate summary report of the database for easy and quick analysis.  
    '''    
    
    def __init__(self,master):
        '''
        Receives the root(master) and sets the size of the frame.
        
        Input : The main window, i.e., master
        
        '''
        self.master = master # Specifying the root of the frame as master
        try:
            self.master.config(bg = self.master.background_colour)
        except:
           pass
       
        
        self.initface = tk.Frame(self.master)
        # self.initface = tk.Frame(self.master,width = 1000, height = 800) # Creates a frame in the main window
        try:
            self.initface.configure(bg = self.master.background_colour)
        except:
            pass

        self.initface.pack(expand=True) # Places the frame in the window
        self.createwidget() # Calling the initial face to enter main window
        

    def createwidget(self):
        '''
        Sets the layout and creates all the widgets in the initial interface window.
        '''
       
        # Create greeting line on the initial window
        self.greeting = tk.Label(self.initface,
                                 text='Welcome to \n Accident and Emergency Departments \n (AEDs) System', 
                                 font=('Helvetica', 35), 
                                 fg='black')
        try:
            self.greeting.config(bg = self.master.background_colour)
        except:
           pass
       
        '''
        Creates all the buttons for the initial window
        Import button(Import .csv file) : Allows the user to import a csv file of their choice
        Inquiry button(Patient Database) : Allows the user to access records from the patient 
        database
        Add Button(New Patient Registration) : Allows the user to add a new patient record
        Update Button(Update Patient Database) : Allows user to input additional information and 
        updates it in the existing database
        Summary Button(Summary) : Returns summary analytics of the data in the database 
        Color Button(Change Background Colour) : Changes the background colour of the window
                                
        '''
        height = 3
        width = 10
        helv20 = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        # Defining the buttons and specifying the properties to 
        # Customise the appearance of the buttons
        warnings.filterwarnings('ignore')
        tip = Balloon(self.initface) # Adds the tooltip for the buttons
        self.import_btn = tk.Button(self.initface,
                                 text="Import .csv file",
                                 bg='#89c4f4', 
                                 font=helv20, 
                                 height=1, 
                                 width=width + 7,
                                 wraplength = 1000,
                                 command=lambda: [self.import_table()],
                                 justify="center")
        tip.bind_widget(self.import_btn,balloonmsg="Import a csv file of your choice to view patient records.")
        self.iqrybtn = tk.Button(self.initface,
                                 text="Patient\nDatabase",
                                 bg='#89c4f4', 
                                 font=helv20, 
                                 height=height, 
                                 width=width,
                                 command=lambda: self.change('InquiryFace'),
                                 justify="center")
        tip.bind_widget(self.iqrybtn,balloonmsg="View patient records")
        self.add_btn = tk.Button(self.initface,
                                 text='New Patient\nRegistration',
                                 bg='#89c4f4',
                                 font=helv20,
                                 height=height,
                                 width=width,
                                 command=lambda: self.change('AddFace'),
                                 justify="center")
        tip.bind_widget(self.add_btn,balloonmsg="Add new patient records")
        self.update_btn = tk.Button(self.initface,
                                 text='Update\nPatient\nDatabase',
                                 bg='#89c4f4',
                                 font=helv20,
                                 height=height,
                                 width=width,
                                 command=lambda: self.change('UpdateFace'),
                                 justify="center")
        tip.bind_widget(self.update_btn,balloonmsg="Update information about existing patients")
        self.smry_btn = tk.Button(self.initface,
                                  text='Summary',
                                  bg='#89c4f4',
                                  font=helv20,
                                  height=height,
                                  width=width,
                                  command=lambda: self.change('SummaryFace'))
        tip.bind_widget(self.smry_btn,balloonmsg="View summary statistics and visual graphics of patient records")
        self.ccolor_button = tk.Button(self.initface,
                                  text='Choose Background\nColour',
                                   bg='#89c4f4',
                                   font=helv20,
                                   height=3-1,
                                   width=width+7,
                                  command=self.getColor,
                                  justify="center")
        tip.bind_widget(self.ccolor_button, balloonmsg="Change background colour")



        '''
        Place all widgets in the initial face
        Grid places widgets in row and columnwise 
        Row : Specifies the row number
        Column : Specifies the column number
        Columnspan : Specifies the number of columns across which the widget should spread
        Padx : Specifies the horizontal spacing between the widgets
        Pady : Specifies the vertical spacing between the widgets
        Stick : Aligns the widget
        '''
        self.greeting.grid(row=0, column=0, columnspan=5, padx = 40, pady=60, stick='EW')
        self.import_btn.grid(row=3, column=0,columnspan = 5,pady = 20)
        self.iqrybtn.grid(row=1, column=0, pady=50, padx = 10)
        self.add_btn.grid(row=1, column=1, pady=50, padx = 10)
        self.update_btn.grid(row=1, column=2, pady=50, padx = 10)
        self.smry_btn.grid(row=1, column=3, pady=50, padx = 10)
        self.ccolor_button.grid(row=2,column=0,columnspan = 5,padx=10,pady=50)
        
        
    def getColor(self):
        '''
        Asks the user to select a background colour for the interface. The colour selected is applied
        to all the frames in the window.
        '''
        colors = askcolor(title="Tkinter Color Chooser")
        self.master.background_colour = colors[1]
        self.master.config(bg = self.master.background_colour)
        self.greeting.config(bg = self.master.background_colour)
        self.initface.configure(bg = self.master.background_colour)
        
        
    def import_table(self):
        '''
        Allows the user to import a csv file which would be used by the 'Patient Database' frame
        
        '''
        
        self.file_name = tk.filedialog.askopenfilename(initialdir = '/Desktop',
        title = 'Select a CSV file',
        filetypes = (('csv file','*.csv'),
        ('csv file','*.csv')))
        # Defines the file name as a master variable which can be accessed by other frames
        self.master.file_name = self.file_name
        # Creating a copy of the file selected by the user in the working directory
        directory = getcwd()
        filename =  directory + '\\AED4weeks.csv'
        r = pd.read_csv(self.file_name)
        f = open(filename,'wb')
        r.to_csv(f, index = False)
        f.close()
        print("Getting records from: ", self.file_name)

        
    def change(self, choice):  
        '''
        Change to the next level interface based on the button selection
        Inquiry button redirects the user to the inquiry face
        Add button redirects the user to the add face
        Update button redirects the user to the update face
        Summary button redirects the user to the summary face
        '''
        
        self.initface.destroy()      # Close current window
        eval(choice)(self.master)    # Call next level window class
        

class InquiryFace():
    '''
    This class is defined for the inquiry face which allows the user to access and filter
    the patient database. This class does the following:
    1) Creates the inquiry interface window
    2) Creates and design the window layout components
    3) Defines the widgets to get user inputs
    4) Interacts with aeddatabase to get unique values for the drop down lists
    5) Validates the user inputs and clear the entry cells in case of wrong inputs
    6) Gets the user input and stores it in a dataframe named self.conditions
    7) Reset button clear all existing input
    8) Allows the user to go to home page, exit or apply the entered filters
    
    The inquiry face has four buttons:
    (i) Reset button : Clears all the inputs
    (ii) Apply button : Applies all the filters and returns the filtered patient records
    (iii) Home button : Redirects user to the Initial face
    (iv) Exit button : Closes all the windows and exit the program
    '''     
    
    def __init__(self,master):
        '''
        Receives the root(master) and sets the size of the frame.
        
        Input : The main window, i.e., master
        
        '''
        self.master = master 
        self.master.config()
        
        # Creates inquiry window as a frame in the root window
        self.iqryface = tk.Frame(self.master,)
        # Sets background colour of the frame to the colour chosen by the user
        try:
            self.iqryface.config(bg = self.master.background_colour)
        except:
            pass
        
        self.iqryface.pack(expand=True)
        self.createwidget()    # Calling the createwidget function to begin layout setting
    

    def validate_id(self,ipt):
        '''
        Checks the input format for ID value
        '''
        
        value_form = re.compile(r'[P][\d]{5}')      # Set ID input value format
        value_form1 = re.compile(r'[p][\d]{5}') 
        if value_form.match(ipt) or value_form1.match(ipt) or ipt == '':
            return True
        else:                                       
            tk.messagebox.showinfo(title='Warning',
                                   message="Patient ID should be in P00000 format.")
            self.input_id_from.delete(0, tk.END)         # Clear input values 
            self.input_id_to.delete(0, tk.END)
            return False  
          
    
    def validate_age_day(self,ipt):
        '''
        Checks the input format for Age and day value
        '''
        
        if ipt.isdigit() or ipt == '':
            return True
        else:
            tk.messagebox.showinfo(title='Warning',
                                   message="Age and day value should be a number.")
            self.input_age_from.delete(0, tk.END)         # Clear input values
            self.input_age_to.delete(0, tk.END)
            self.input_day_from.delete(0, tk.END)
            self.input_day_to.delete(0, tk.END)
            return False      

    def validation(self):
        valid_list = [self.validate_id(self.id_from.get()),self.validate_id(self.id_to.get()),\
                      self.validate_age_day(self.age_from.get()), self.validate_age_day(self.age_to.get()),\
                          self.validate_age_day(self.day_from.get()), self.validate_age_day(self.day_to.get()) ]
        outcome = []
        for i in valid_list:
            outcome.append(i)
        if False not in outcome:
            self.change('RecordFace')
        else:
            pass
    
    
    def createwidget(self):    
        '''
        Designs a layout for the inquiry face
        '''
        
        # Create widget variables
        # self.id_from and self.id_to sets the range for filtering ID
        self.id_from, self.id_to = tk.StringVar(),tk.StringVar() 
        # self.age_from, self.age_to sets the range for filtering Age
        self.age_from, self.age_to = tk.StringVar(),tk.StringVar()
        # self.day_from, self.day_to sets the range for filtering Day
        self.day_from, self.day_to = tk.StringVar(),tk.StringVar()
        # self.hrg_from, self.hrg_to sets the range for filtering HRG
        self.hrg_from, self.hrg_to = tk.StringVar(),tk.StringVar()
        # Gives the user the option to filter based on breach or not
        self.breach_yes, self.breach_no = tk.IntVar(),tk.IntVar()
        # Gives the user the option to sort the data based on ID,Age,Day and HRG
        self.sortby1, self.sortby2 = tk.StringVar(),tk.StringVar()
        # Gives the user the option to display the data 
        # in ascending or descending order
        self.ascending, self.descending = tk.StringVar(),tk.StringVar()
        self.ascending.set('Ascending') # Default is ascending order  
 
        
        '''
        Creates a dataframe which stores all the entered inputs and 
        sends it to aeddatabase.py as condition input
        '''
        self.conditions = pd.DataFrame()   
        
        # Creates two columns in the dataframe named 'conditions' and 'type'
        # 'Conditions' contains the variable names for which user would enter inputs
        # 'Type' column specifies the type of the particular input, string or integer
        self.conditions['Conditions'] = ['ID','Age','Day','HRG','Breachornot','Sort_by','Order']
        self.conditions['Type'] = ['string', 'int', 'int', 'string', 'string', 'string', 'string']

        # Sets the font for the labels and widgets
        helv_title = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        helv_fill = tkFont.Font(family='Helvetica', size=15)
        helv_act = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)        
        
        # Creates all the widgets in the inquiry interface window, i.e., the input boxes 
         
        # Creates the 'From' and 'To' labels and 
        # Specifiesthe aesthetic properties of the labels
        heightD = 2 # height of the label
        widthD = 20 # weight of the label
        self.from_label = tk.Label(self.iqryface,
                                   text='From',
                                   font=helv_title,
                                   fg='black',
                                   height=heightD,
                                   width=widthD)
        self.to_label = tk.Label(self.iqryface,
                                 text='To',
                                 font=helv_title,
                                 fg='black',
                                 height=heightD,
                                 width=widthD) 

        # Creates condition labels on the left which indicates the user what each input box 
        # stands for. The labels are taken from the self.conditions dataframe
        
        labels = ["Patient ID", "Age", "Day", "HRG", "Breach", "Sort by"]
        for i in range(len(labels)):
            tk.Label(self.iqryface,
                     text=labels[i],
                     font=helv_title,
                     height=2,
                     width=15,
                     anchor='e').grid(row=i+1, column=0, padx=50, stick='ew')
        
        # Create entry widgets for ID, Age, Day
        # Creates 'from' widget for ID and assigns the value to the corresponding variable
        self.input_id_from = ttk.Entry(self.iqryface, textvariable=self.id_from,
                                  font=helv_fill, justify='center')

        # Creates 'to' widget for ID and assigns the value to the corresponding variable
        self.input_id_to = ttk.Entry(self.iqryface, textvariable=self.id_to,
                                  font=helv_fill, justify='center')

        # Creates 'from' widget for Age and assigns the value to the corresponding variable
        self.input_age_from = ttk.Entry(self.iqryface, textvariable=self.age_from,
                                  font=helv_fill, justify='center')

        # Creates ‘to’ widget for Age and assigns the value to the corresponding variable
        self.input_age_to = ttk.Entry(self.iqryface, textvariable=self.age_to,
                                  font=helv_fill, justify='center')
      
          # Creates ‘from’ widget for Day and assigns the value to the corresponding variable
        self.input_day_from = ttk.Entry(self.iqryface, textvariable=self.day_from,
                                  font=helv_fill, justify='center')

        # Creates ‘to’ widget for Day and assigns the value to the corresponding variable
        self.input_day_to = ttk.Entry(self.iqryface, textvariable=self.day_to,
                                  font=helv_fill, justify='center')

        '''
        Creates drop down list widget for HRG which interactes with the database to get the
        unique records of a column to display as options in the drop down menu
        '''         
        # Pass the condition name to the database to return the list 
        # which would appear in the drop down menu
        self.list = CatalogData(self.conditions.iloc[3,0])  
        # Get return value of the list of the condition
        self.list = self.list.condition_list()  

        # Creates combobox to store and show return HRG list               
        self.input_hrg = ttk.Combobox(self.iqryface,
                                     textvariable=self.hrg_from,
                                     state="readonly")
        self.input_hrg['values']=self.list 
       
        # Creates checkbox widget to allow the user to filter for patients who have breached   
        self.input_breach_yes = ttk.Checkbutton(self.iqryface,
                                        text="Yes",
                                        variable=self.breach_yes,
                                        onvalue=1,
                                        offvalue=0)
        # Creates checkbox widget to allow the user to filter for patients who have not breached
        self.input_breach_no = ttk.Checkbutton(self.iqryface,
                                        text="No",
                                        variable=self.breach_no,
                                        onvalue=1,
                                        offvalue=0)
        
        '''
        Creates drop down list widget for Sort_by such that multiple options can be selected 
        simultaneously. It allows the user to select on the basis of
        which variable they would like to sort the patient records 
        '''
        self.list = CatalogData(self.conditions.iloc[5,0]) # Defines an instance
        self.list = self.list.condition_list() # Calls the method from the database 
        self.input_sort_by = ttk.Combobox(self.iqryface,
                                     textvariable=self.sortby1,
                                     state="readonly") 
        self.input_sort_by['values']=self.list

        # Creates Radiobutton widget for Order such that only one box can be selected 
        self.input_ascending = ttk.Radiobutton(self.iqryface, text='Ascending',
                                        variable=self.ascending, value='Ascending')      
        self.input_descending = ttk.Radiobutton(self.iqryface, text='Descending',
                                        variable=self.ascending, value='Descending')

        # Creates action buttons for reset, apply, home and exit
        warnings.filterwarnings('ignore')
        tip = Balloon(self.iqryface) # Adds tootip for the buttons
        self.reset_btn = tk.Button(self.iqryface, text='Reset', width=10,
                                   font=helv_act, bg='#fcd670',
                                   command=self.reset_all)
        tip.bind_widget(self.reset_btn,balloonmsg="Clear all the input fields")
        self.apply_btn = tk.Button(self.iqryface, text='Apply', width=10,
                                   font=helv_act, bg='#fcd670',
                                   command=lambda: [self.get_value(), self.validation()])
        tip.bind_widget(self.apply_btn,balloonmsg="View the filtered patient records")
        self.home_btn = tk.Button(self.iqryface, text='Home',
                                  font=helv_act, bg='#89c4f4',
                                  command=lambda: self.change('InitFace'))
        tip.bind_widget(self.home_btn,balloonmsg="Go to Home Page")
        self.exit_btn = tk.Button(self.iqryface, text='Exit',
                                  font=helv_act, bg='#89c4f4',
                                  command=CloseWindow)
        tip.bind_widget(self.exit_btn,balloonmsg="Exit this program")

        '''
        Place all widgets in the inquiry face
        Grid places widgets in row and columnwise 
        Row : Specifies the row number
        Column : Specifies the column number
        Columnspan : Specifies the number of columns across which the widget should spread
        Padx : Specifies the horizontal spacing between the widgets
        Pady : Specifies the vertical spacing between the widgets
        Stick : Aligns the widget
        ''' 
        self.from_label.grid(row=0, column=1, pady= 5, stick='EW')        
        self.to_label.grid(row=0, column=2, pady=5, stick='EW')
        self.input_id_from.grid(row=1, column=1, pady=10, stick='NSEW') 
        self.input_id_to.grid(row=1, column=2, pady=10, stick='NSEW') 
        self.input_age_from.grid(row =2, column=1, pady=10, stick='NSEW') 
        self.input_age_to.grid(row=2, column=2, pady=10, stick='NSEW')        
        self.input_day_from.grid(row=3, column=1, pady=10, stick='NSEW') 
        self.input_day_to.grid(row=3, column=2, pady=10, stick='NSEW')        
        self.input_hrg.grid(row=4, column=1, pady=10, columnspan=2, stick='NSEW')
        self.input_breach_yes.grid(row=5, column=1, pady=10, stick='NSEW')
        self.input_breach_no.grid(row=5, column=2, pady=10, stick='NSEW')        
        self.input_sort_by.grid(row=6, column=1, pady=10, columnspan=2, stick='NSEW')               
        self.input_ascending.grid(row=7, column=1, pady=10, padx=50, stick='NSEW')
        self.input_descending.grid(row=7, column=2, pady=10, padx=50, stick='NSEW')
        self.reset_btn.grid(row=1, column=3, rowspan=2, padx=150, pady=10, stick='NSEW')
        self.apply_btn.grid(row=3, column=3, rowspan=2, padx=150, pady=10, stick='NSEW')
        self.home_btn.grid(row=6, column=3, padx=150, stick='EW')
        self.exit_btn.grid(row=7, column=3, padx=150, stick='EW')
     
        for widget in self.iqryface.winfo_children():
            if isinstance(widget, tk.Label):
                try:
                    widget.config(bg = self.master.background_colour)
                except:
                    pass
    
    def get_value(self):           
        '''
        Gets all input values and stores them in a dataframe named self.conditions
        '''
        
        self.conditions['From'] = [self.id_from.get().upper(),
                                   self.age_from.get(),
                                   self.day_from.get(),
                                   self.hrg_from.get(),
                                   self.breach_yes.get(),
                                   self.sortby1.get(),
                                   self.ascending.get()]
        self.conditions['To'] = [self.id_to.get().upper(),
                                 self.age_to.get(),
                                 self.day_to.get(),
                                 self.hrg_to.get(),
                                 self.breach_no.get(),
                                 self.sortby2.get(),
                                 self.descending.get()] 
        print(self.conditions)
        
    def reset_all(self):
        '''
        When clicked, it resets all the conditions
        '''
        
        self.iqryface.destroy()
        self.iqryface = tk.Frame(self.master,)
        self.iqryface.pack(expand=True)
        self.createwidget()
        
    def change(self, choice): 
        '''
        When clicked, changes to the next level depending on what is selected.
        It is used to redirect the user to the next page based on the selection.
        '''
        
        self.iqryface.destroy()
        if choice == 'RecordFace':
            eval(choice)(self.master, self.conditions)        
        else:
            eval(choice)(self.master)           
            

class RecordFace():
    '''
    This class is defined for the record face which allows the user to view records from
    the patient database based on the inputs given on the inquiry face. 
    This class does the following:
    1) Creates the record interface window
    2) Creates and design the window layout components
    3) Sends entered conditions to aeddatabase to get the filtered records based on entered inputs
    4) Allows the user to go to home page, exit or apply the entered filters
        
    The record face has four buttons:
    (i) Home button : Redirects user to the Initial face
    (ii) Return button : Redirects user to the Inquiry face
    (iii) Exit button : Closes all the windows and exit the program
    '''  
    
    def __init__(self,master,index):
        '''
        Receives the root(master) and sets the size of the frame.
        
        Input : The main window, i.e., master
        '''
        
        self.master = master 
        self.master.config()
        
        # Creates record window as a frame in the root window
        self.rcdface = tk.Frame(self.master)
        self.rcdface.pack(side='top', expand=1, fill=tk.BOTH)

        # Creates a frame in the root window to store action buttons
        self.contolbtns = tk.Frame(self.master)
        self.contolbtns.pack(side='bottom')
        # Sets background colour of the frame to the colour chosen by the user
        try:
            self.rcdface.config(bg = self.master.background_colour)
            self.contolbtns.config(bg = self.master.background_colour)
        except: 
            pass
        
        # The conditions dataframe which contains all the filters inputted by the user
        self.condition = index 
        
        '''
        Gets the path of the csv file imported from the user. If no file is imported, 
        the file name is an empty string. Interacts with the aeddatabase 
        to get the patient records. This is assigned to the variable self.record.
        '''
       
        self.record = CriteriaQuery()
        self.record = self.record.condition_matching(self.condition)
        
    
        # Calling createwidget functions which defines the labels and widgets to be placed
        # on the record face
        self.createwidget()  

    def createwidget(self):
        '''
        Creates all the widgets in the record interface window
        '''  
        
        # Creates Pandas Table to show the filtered records
        self.rcdtable = Table(self.rcdface, dataframe=self.record, editable=False)
        self.rcdtable.autoResizeColumns()
        self.rcdtable.show()
        
        # Sets the font for the buttons
        act_font = tkFont.Font(family='Helvetica', size=13, weight=tkFont.BOLD)

        
        # Creates a button to return to the Initial Face
        tk.Button(self.contolbtns,
                  text='Home',
                  width=30,
                  bg='#89c4f4',
                  font=act_font,
                  command=lambda:self.change('InitFace')).grid(row=1,
                                                               column=1,
                                                               padx=50,
                                                               pady=40)
        
        # Creates a button to return to the Inquiry Face
        tk.Button(self.contolbtns,
                  text='Return',
                  width=30,
                  bg='#89c4f4',
                  font=act_font,
                  command=lambda:self.change('InquiryFace')).grid(row=1,
                                                                  column=2,
                                                                  padx=50,
                                                                  pady=40)
              
        # Creates a button to exit from the program
        tk.Button(self.contolbtns,
                  text='Exit',
                  width=30,
                  bg='#89c4f4',
                  font =act_font,
                  command=CloseWindow).grid(row=1, column=3, padx=50, pady=40)
        
    def change(self, choice):  
        '''
        When clicked, changes to the next level depending on what is selected.
        It is used to redirect the user to the next page based on the selection.
        '''
        self.rcdface.destroy()
        self.contolbtns.destroy()
        eval(choice)(self.master)        
                     


class AddFace():
    '''
    This class is defined for the Add Face which allows the user to add new patient records. 
    This would be mainly useful at the time of admitting a patient. It takes the ID, Age, 
    Arrival Date and Arrival Time from the user.
    
    This class does the following:
    1) Creates the adds interface window
    2) Creates and designs the window layout components
    3) Defines the widgets to get user inputs
    4) Interacts with aeddatabase to add the new record in the database
    5) Validates the user inputs and clears the entry cells in case of wrong inputs
    6) Gets the user input and stores it in a dataframe named self.conditions
    7) Allows the user to reset, go to home page or exit.
    
    The add face has four buttons:
    (i) Reset button : Clears all the inputs
    (ii) Add button : Adds the new patient record to the database
    (iii) Home button : Redirects user to the Initial face
    (iv) Exit button : Closes all the windows and exits the program
    '''  
    
    def __init__(self,master):
        '''
        Receives the root(master) and sets the size of the frame.
        
        Input : The main window, i.e., master
        '''
        self.master = master 
        self.master.config()
        self.add = tk.Frame(self.master,)
        # Creates add window as a frame in the root window
        self.addface = tk.Frame(self.master,)
        # Sets background colour of the frame to the colour chosen by the user
        try:
            self.addface.config(bg = self.master.background_colour)
        except: 
            pass
        self.addface.pack(expand=True)
        self.createwidget()    # Calling the createwidget function to begin layout setting
    
 
    
    def validate_id(self,ipt):
        '''
        Checks the input format for ID value
        '''
        
        value_form = re.compile(r'[P][\d]{5}')      # Set ID input value format
        if value_form.match(ipt):
            return True
        else:                                       
            tk.messagebox.showinfo(title='Warning',
                                   message="You should follow the format: P00000")
            self.input_id.delete(0, tk.END)         # Clear input values      
            return False  
    
    def validate_age(self,ipt):
        '''
        Checks the input format for ID value
        '''
        
        if ipt.isdigit():
            return True
        else:
            tk.messagebox.showinfo(title='Warning',
                                   message="You should enter a number")
            self.input_age.delete(0, tk.END)         # Clear input values           
            return False      
        
    def onClick(self):
        '''
        Checks whether the user has completed all the fields. Further, it checks if 
        entered ID already exists in the entire database. If it exists, this function 
        throws an error message. 
        This function is called every time the Add button is clicked on the AddRecord face. 
        Once clicked, this function interacts with the database and adds the 
        record to the database if all the fields are completed and the 
        entered ID is not already there in the database.
        '''
        
        if self.new_record["ID"] != "" and self.new_record["Age"] != "" and self.new_record["Arrival Date"] != "" and self.new_record["Arrival Time"] != "" :
            self.add_record = AddRecord(self.new_record)
            if self.add_record.id_checker(self.new_record["ID"]) == 1:
                self.add_record = self.add_record.insert_record()
                tk.messagebox.showinfo(title='Success Message', 
                                   message="Record has been added successfully.")
                self.input_id.delete(0, tk.END)         # Clear input values 
                self.input_age.delete(0, tk.END)         # Clear input values 
            else:
                tk.messagebox.showinfo(title='Failure Message', 
                                   message="Entered ID found in patient records. You will now be redirected to the 'Update Existing Database' page.") 
                self.change('UpdateFace')
        else:
            tk.messagebox.showinfo(title='Warning',
               message="Record could not be added. Please complete all the fields.")
            self.new_record = {}
            print(self.new_record)
            
    def get_value(self):           
        '''
        Gets all input values and stores them in a dictionary named self.new_record
        '''
        
        # An empty dictionary is created in which details 
        # of the new record will be added
        
        self.new_record = {}
        
        '''
        The keys of the dictionary are the names of different inputs entered by the user.
        The values of the dictionary are the actual values inputted by the user.
        The inputs are:
            (i) Patient ID: "P0000" format (string)
            (ii) Age: integer
            (iii) Arrival Date: "DD-MM-YYYY" (date)
            (iv) Arrival Time: "HH:MM" format
        '''
        
        self.new_record["ID"] = self.id.get()
        self.new_record["Age"] = self.age.get()
        self.new_record["Arrival Date"] = self.input_arrival_date.get_date()
        self.new_record["Arrival Time"] = self.arrival_time.get()
        
        print(self.new_record)  
        
    def validate_id(self,ipt):
        '''
        Checks the input format for ID value
        '''
        
        value_form = re.compile(r'[P][\d]{5}')      # Set ID input value format
        value_form1 = re.compile(r'[p][\d]{5}') 
        if value_form.match(ipt) or value_form1.match(ipt) or ipt == '':
            return True
        else:                                       
            tk.messagebox.showinfo(title='Warning',
                                   message="Patient ID should be in P00000 format.")
            self.input_id.delete(0, tk.END)         # Clear input values      
            return False 

    def validate_age(self,ipt):
        '''
        Checks the input format for Age value
        '''
        
        if ipt.isdigit() or ipt == '':
            return True
        else:
            tk.messagebox.showinfo(title='Warning',
                                   message="Age value should be a number.")
            self.input_age.delete(0, tk.END)         # Clear input values           
            return False  
        
    def validation(self):      
        valid_list = [self.validate_id(self.input_id.get()),\
                      self.validate_age(self.input_age.get())]
        outcome = []
        for i in valid_list:
            outcome.append(i)
        if False not in outcome:
            self.onClick()
        else:
            pass    
    
    
    
    def createwidget(self):    
        '''
        Sets the layout and creates all the widgets in the initial interface window.
        '''
        
        # Creates widget variables
        self.id = tk.StringVar() # ID
        self.age = tk.StringVar() # Age
        self.arrival_date = tk.StringVar() # Arrival Date
        now = datetime.datetime.now() # Sets current time as the default value for the current time
        self.arrival_time = tk.StringVar(value = now.strftime("%H:%M")) # Arrival Time
        

        # Sets the font for the labels and widgets
        helv_title = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        helv_fill = tkFont.Font(family='Helvetica', size=15)
        helv_fill2 = tkFont.Font(family='Helvetica', size=10)
        helv_act = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
        
        
        # Creates all widgets in the Add Record window        
        
        # Creates the labels for input variables
        heightD = 2
        widthD = 20

        self.record_vars = ["ID", "Age", "Arrival Date", "Arrival Time"]
        # create condition label on the far left
        for i in range(len(self.record_vars)):
            tk.Label(self.addface,
                     text=self.record_vars[i],
                     font=helv_title,
                     height=2,
                     width=15,
                     anchor='e').grid(row=i+1, column=0, padx=50, stick='ew')
        
        # Calls the functions which validate the inputs entered by the user
        # self.reg_id = self.addface.register(self.validate_id)
        # self.reg_age = self.addface.register(self.validate_age)
        
        # Create entry widgets for ID, Age, Arrival Date and Arrival Time
        # Creates widget for ID and assigns the value to the corresponding variable
        self.input_id = ttk.Entry(self.addface, textvariable=self.id,
                                  font=helv_fill, justify='center')
        # self.input_id.config(validate='focusout',
        #                      validatecommand=(self.reg_id, '%P'))
        # Creates widget for Age and assigns the value to the corresponding variable
        self.input_age = ttk.Entry(self.addface, textvariable=self.age,
                                  font=helv_fill, justify='center')
        # self.input_age.config(validate='focusout',
        #                      validatecommand=(self.reg_age, '%P'))
        # Creates widget for Arroval Date and assigns the value to the corresponding variable
        today = datetime.date.today() # setting current time as default value for arrival date
        self.input_arrival_date = DateEntry(self.addface,width=30,bg="darkblue",fg="white",
                                  year=today.year, month=today.month, day=today.day, 
                                  date_pattern = "DD/MM/yyyy")
        # Creates widget for Arrival Time and assigns the value to the corresponding variable
        self.input_arrival_time = ttk.Entry(self.addface, textvariable=self.arrival_time,
                                  font=helv_fill, justify='center')
        
        # Creates action buttons for reset, apply, home and exit
        warnings.filterwarnings('ignore')
        tip = Balloon(self.addface) # Adds the tooltip for the buttons
        self.reset_btn = tk.Button(self.addface, text='Reset', width=10,
                                   font=helv_act, bg='#fcd670',
                                   command=self.reset_all)
        tip.bind_widget(self.reset_btn,balloonmsg="Clear all the input fields")
        self.add_btn = tk.Button(self.addface, text='Add', width=10,
                                   font=helv_act, bg='#fcd670',
                                   command=lambda: [self.get_value(),self.validation()])
        tip.bind_widget(self.add_btn,balloonmsg="Insert the new patient record in the database")
        self.home_btn = tk.Button(self.addface, text='Home',
                                  font=helv_act, bg='#89c4f4',
                                  command=lambda: self.change('InitFace'))
        tip.bind_widget(self.home_btn,balloonmsg="Go to Home Page")
        self.exit_btn = tk.Button(self.addface, text='Exit',
                                  font=helv_act, bg='#89c4f4',
                                  command=CloseWindow)
        tip.bind_widget(self.exit_btn,balloonmsg="Exit this program")
        
        directory = getcwd()
        filename = directory + '\\AED4weeks.csv'
        label_msg = "The updated files are available in \n " + filename + "."
        tk.Label(self.addface, text=label_msg, font=helv_fill2, height=2, width=70,
        anchor='e', fg="blue").grid(row=15, column=1, padx=10, stick='ew')
        '''
        Place all widgets in the add record face
        Grid places widgets in row and columnwise 
        Row : Specifies the row number
        Column : Specifies the column number
        Columnspan : Specifies the number of columns across which the widget should spread
        Padx : Specifies the horizontal spacing between the widgets
        Pady : Specifies the vertical spacing between the widgets
        Stick : Aligns the widget
        ''' 
        self.input_id.grid(row=1, column=1, pady=10, stick='NSEW') 
        self.input_age.grid(row =2, column=1, pady=10, stick='NSEW') 
        self.input_arrival_date.grid(row=3, column=1, pady=10, stick='NSEW')        
        self.input_arrival_time.grid(row=4, column=1, pady=10, stick='NSEW')
        self.reset_btn.grid(row=1, column=3, rowspan=2, padx=150, pady=10, stick='NSEW')
        self.add_btn.grid(row=3, column=3, rowspan=2, padx=150, pady=10, stick='NSEW')
        self.home_btn.grid(row=6, column=3, padx=150, pady = 10, stick='EW')
        self.exit_btn.grid(row=7, column=3, padx=150, stick='EW')
 
        for widget in self.addface.winfo_children():
            if isinstance(widget, tk.Label):
                try:
                    widget.config(bg = self.master.background_colour)
                except:
                    pass
        
    def reset_all(self):
        '''
        When clicked, it resets all the conditions
        '''
        
        self.addface.destroy()
        self.addface = tk.Frame(self.master,)
        self.addface.pack(expand=True)
        self.createwidget()
        
    def change(self, choice): 
        '''
        When clicked, changes to the next level depending on what is selected.
        It is used to redirect the user to the next page based on the selection.
        '''
        
        self.addface.destroy()
        if choice == 'RecordFace':
            eval(choice)(self.master, self.conditions)        
        else:
            eval(choice)(self.master)     

class UpdateFace():
    '''
    This class is defined to update existing patient records at the time of a new diagnosis,
    treatment administer or at the time of discharge. It has a drop down menu which allows 
    the user to update one of the above details, once selected, it displays the appropriate 
    entry widgets. 
    When a new diagnosis is performed, the noofinvestigations for the patient is updated.
    When a new treatment is conducted, the nooftreatments and HRG is updated for the patient.
    When a patient is disharged, the length of stay(LOS) is entered by the user and calculations
    are performed to determine if the patient breached or not, i.e., LOS > 240 minutes.
    '''  
    
    def __init__(self,master):
        '''
        Receives the root(master) and sets the size of the frame.
        
        Input : The main window, i.e., master
        
        '''
        self.master = master 
        self.master.config()
        self.update = tk.Frame(self.master,)
        # Creates update window as a frame in the root window
        self.updateface = tk.Frame(self.master,)
        # Sets background colour of the frame to the colour chosen by the user
        try:
            self.updateface.config(bg = self.master.background_colour)
        except: 
            pass
        self.updateface.pack(expand=True)
        self.createwidget()    # Calling the createwidget function to begin layout setting
    
    
    def validate_id(self,ipt):
        '''
        Checks the input format for ID value
        '''
           
        value_form = re.compile(r'[P][\d]{5}') # Set ID input value format
        if value_form.match(ipt) or ipt == '':
            return True
        else:                                       
            tk.messagebox.showinfo(title='Warning',
                                   message="You should follow the format: P00000")
            self.input_id.delete(0, tk.END)  # Clear input values  

            return False  
        
    def validate_los(self,ipt):
        '''
        Checks the input format for Discharge value
        '''
        
        if ipt.isdigit() or ipt == '':
            return True
        else:
            tk.messagebox.showinfo(title='Warning',
                                   message="You should enter a number")
            self.input_los.delete(0, tk.END) # Clear input values           
            return False  
        
        
    def validate_treatment(self,ipt):
        '''
        Checks the input format for ID value
        '''
           
        value_form = re.compile(r'[V][B][\d]{2}[Z]') # Set ID input value format
        if value_form.match(ipt) or ipt == '':
            return True
        else:                                       
            tk.messagebox.showinfo(title='Warning',
                                    message="You should follow the format: VB00Z")
            self.input_treatment.delete(0, tk.END)  # Clear input values      
            return False  


    def validation(self):
        valid1 = True
        valid2 = True
        valid1 = self.validate_id(self.input_id.get())
        if self.update_type.get() == self.list[2]:
            valid2 = self.validate_los(self.input_los.get())
        elif self.update_type.get() == self.list[1]:
            valid2 = self.validate_treatment(self.input_treatment.get())
        else:
            pass
        if valid1 != False and valid2 != False:
            self.onClick()
        else:
            pass          
    
 
    def onClick(self):
        '''
        Checks whether the user has entered an ID that already exists in the patient database.
        If entered ID does not exist, it throws an error message.
        This function is called every time the Update button is clicked on the UpdateRecord face. 
        Once clicked, this function interacts with the database and updates the 
        database if records for the entered ID exists in the database.
        '''
          
        self.up_record = UpdateRecord(self.update_record)    
        # Runs only if atleast one of the input fields are non-empty

        if ((self.diagnosis.get() != "") or (self.treatment.get() != "") or (self.los.get() != "")) and (self.up_record.id_checker(self.update_record["ID"]) == 1):
            
            self.up_record = self.up_record.update_record()
            tk.messagebox.showinfo(title='Success Message', 
                                   message="Record has been updated successfully.")  
            self.change('InitFace')
        else:
            tk.messagebox.showinfo(title='Warning',
               message="Entered ID not found in patient records. You will now be redirected to the 'New Patient Registration' page.")    
            self.change('AddFace')
            self.update_record = {}
            print(self.update_record)
            
    def callback(self, *args):  
        '''
        This function displays entry widgets to allow users to enter details to update patient records
        depending on what they choose in the drop down menu. The drop down menu has three options:
            (i) Diagnosis : If selected, it allows the user to enter the type of diagnosis done.
            (ii) Treatment : If selected, it allows the user to enter the HRG (treatment code).
            (iii) Discharge : If chosen, it asks user to enter the length of stay.
        '''
        
        # Sets the font for the labels and widgets
        helv_title = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        helv_fill = tkFont.Font(family='Helvetica', size=15)
        try:
            self.minutes_msg.grid_forget()
        except:
            pass
        if self.update_type.get() == self.list[0]:
            self.input_diagnosis = ttk.Entry(self.updateface, textvariable = self.diagnosis,
                                      font = helv_fill, justify = 'center')
            self.input_diagnosis.grid(row=4, column=1, pady=10, stick='NSEW')
            tk.Label(self.updateface,
                     text=["Diagnosis"],
                     font=helv_title,
                     height=2,
                     width=15,
                     anchor='e').grid(row=4, column=0, padx=50, stick='ew')
            self.input_diagnosis.delete(0, tk.END)
        elif self.update_type.get() == self.list[1]:
            self.input_treatment = ttk.Entry(self.updateface, textvariable = self.treatment,
                                      font = helv_fill, justify = 'center')
            self.input_treatment.grid(row=4, column=1, pady=10, stick='NSEW')
            tk.Label(self.updateface,
                     text=["HRG"],
                     font=helv_title,
                     height=2,
                     width=15,
                     anchor='e').grid(row=4, column=0, padx=50, stick='ew')
            self.input_treatment.delete(0, tk.END)
        elif self.update_type.get() == self.list[2]:
            self.input_los = ttk.Entry(self.updateface, textvariable = self.los,
                                      font = helv_fill, justify = 'center')
            self.input_los.grid(row=4, column=1, pady=10, stick='NSEW')
            tk.Label(self.updateface,
                     text="Length of Stay",
                     font=helv_title,
                     height=2,
                     width=15,
                     anchor='e').grid(row=4, column=0, padx=50, stick='ew')
            self.minutes_msg = tk.Label(self.updateface,
                     text="(in minutes)",
                     font=helv_fill,
                     height=2,
                     width=15,
                     anchor='e')
            self.minutes_msg.grid(row=5, column=0, padx=50, stick='ew')
            self.input_los.delete(0, tk.END)
        for widget in self.updateface.winfo_children():
            if isinstance(widget, tk.Label):
                try:
                    widget.config(bg = self.master.background_colour)
                except:
                    pass

                     
    def createwidget(self):    
        '''
        Sets the layout and creates all the widgets in the UpdateFace window
        '''
        
        # Creates widget variables
        self.id = tk.StringVar() # ID
        self.update_type = tk.StringVar() # What would you like to update?
        self.diagnosis = tk.StringVar() # Diagnosis
        self.treatment = tk.StringVar() # Treatment
        self.los = tk.StringVar() # Length of Stay
        
        # Sets the font for the labels and widgets
        helv_title = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        helv_fill = tkFont.Font(family='Helvetica', size=15)
        helv_fill2 = tkFont.Font(family='Helvetica', size=10)
        helv_act = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)        
        

        tk.Label(self.updateface,
                 text="ID",
                 font=helv_title,
                 height=2,
                 width=15,
                 anchor='e').grid(row=1, column=0, padx=50, stick='ew')

        # Create entry widgets for ID
        self.input_id = ttk.Entry(self.updateface, textvariable=self.id,
                                  font=helv_fill, justify='center')
        # Create entry widgets for update type
        self.list = ["Diagnosis", "Treatment", "Discharge"]
        self.input_update_type = ttk.Combobox(self.updateface,
                                     textvariable=self.update_type,
                                     state="readonly" )
        self.input_update_type['values']=self.list
        self.update_type.trace("w", self.callback)

        # Create action buttons for reset, apply, home and exit
        warnings.filterwarnings('ignore')
        tip = Balloon(self.updateface) # Adds tootip for the buttons
        self.reset_btn = tk.Button(self.updateface, text='Reset', width=10,
                                   font=helv_act, bg='#fcd670',
                                   command=self.reset_all)
        tip.bind_widget(self.reset_btn,balloonmsg="Clear all the input fields")
        self.update_btn = tk.Button(self.updateface, text='Update', width=10,
                                   font=helv_act, bg='#fcd670',
                                   command=lambda: [self.get_value(),
                                                    self.validation()])
        tip.bind_widget(self.update_btn,balloonmsg="Update the patient records")
        self.home_btn = tk.Button(self.updateface, text='Home',
                                  font=helv_act, bg='#89c4f4',
                                  command=lambda: self.change('InitFace'))
        tip.bind_widget(self.home_btn,balloonmsg="Go to Home Page")
        self.exit_btn = tk.Button(self.updateface, text='Exit',
                                  font=helv_act, bg='#89c4f4',
                                  command=CloseWindow)
        tip.bind_widget(self.exit_btn,balloonmsg="Exit this program")

        directory = getcwd()
        filename = directory + '\\AED4weeks.csv'
        label_msg = "The updated files are available in \n " + filename + "."
        tk.Label(self.updateface, text=label_msg, font=helv_fill2, height=2, width=70,
        anchor='e', fg="blue").grid(row=15, column=1, padx=10, stick='ew')
        
        '''
        Place all widgets in the add record face
        Grid places widgets in row and columnwise 
        Row : Specifies the row number
        Column : Specifies the column number
        Columnspan : Specifies the number of columns across which the widget should spread
        Padx : Specifies the horizontal spacing between the widgets
        Pady : Specifies the vertical spacing between the widgets
        Stick : Aligns the widget
        ''' 
        self.input_id.grid(row=1, column=1, pady=10, stick='NSEW') 
        self.input_update_type.grid(row =3, column=1, pady=10, stick='NSEW') 
        self.reset_btn.grid(row=1, column=3, rowspan=2, padx=150, pady=10, stick='NSEW')
        self.update_btn.grid(row=3, column=3, rowspan=2, padx=150, pady=10, stick='NSEW')
        self.home_btn.grid(row=6, column=3, padx=150, pady=10, stick='EW')
        self.exit_btn.grid(row=7, column=3, padx=150, stick='EW')
         
        # Creates the update type line
        self.reminder_word = 'What would you like to update?'
        self.reminder = tk.Label(self.updateface,
                                 text=self.reminder_word,
                                 font = helv_act,
                                 fg='#34495e')
        self.reminder.grid(row=2, column=1, pady=10, stick='NSEW')  
        
        for widget in self.updateface.winfo_children():
            if isinstance(widget, tk.Label):
                try:
                    widget.config(bg = self.master.background_colour)
                except:
                    pass
   

    def get_value(self):           
        '''
        Gets all input values and stores them in a dictionary named self.new_record
        '''
        
        # Creates a dictionary where the keys are different variables 
        # are values are different inputs by the user
        
        self.update_record = {}
        
        self.update_record["ID"] = self.id.get()
        self.update_record["noofinvestigation"] = self.diagnosis.get()
        self.update_record["HRG"] = self.treatment.get()
        self.update_record["LOS"] = self.los.get()
        
    def reset_all(self):
        '''
        When clicked, it resets all the conditions
        '''  
        self.updateface.destroy()
        self.updateface = tk.Frame(self.master,)
        self.updateface.pack(expand=True)
        self.createwidget()   
        
    def change(self, choice): 
        '''
        When clicked, changes to the next level depending on what is selected.
        It is used to redirect the user to the next page based on the selection.
        '''
        self.updateface.destroy()
        if choice == 'RecordFace':
            eval(choice)(self.master, self.conditions)        
        else:
            eval(choice)(self.master)     
            
            
class SummaryFace():
    '''
    This class is defined to display a summary analysis of the data.
    ''' 
    
    def __init__(self,master):
        '''
        Receives the root(master) and sets the size of the frame. Defines the plot frame.
        
        Input : The main window, i.e., master
        
        '''
       
        self.master = master 
        # Creates record window as a frame in the root window
        self.width = root.winfo_screenwidth()         # Get the screen width and use it as the window width
        self.height = root.winfo_screenheight()
        self.sumryface = tk.Frame(self.master, width = self.width, height = self.height)
        self.sumryface.grid(row = 3, stick = "NSEW")
        
        # Creates a frame in the root window to store action buttons
        self.contolbtns = tk.Frame(self.master, width = 500, height = 100)
        self.contolbtns.grid(row = 1, stick = "NSEW")
        
        # Sets background colour of the frame to the colour chosen by the user
        try:
            self.sumryface.config(bg = self.master.background_colour)
            self.contolbtns.config(bg = self.master.background_colour)
        except: 
            pass
        
        self.records = CriteriaQuery()
        self.record = self.records.record
        
        self.sumrytable = Table(self.sumryface, dataframe=self.record.describe(include = "all").reset_index(), editable=False)
        self.sumrytable.autoResizeColumns()
        self.sumrytable.show()
        
        self.createwidget()
    
    def createwidget(self):
              
       
        # Sets the font for the labels and widgets
        helv_title = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        helv_fill = tkFont.Font(family='Helvetica', size=15)
        helv_act = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)        
        button_width = 20
        
        
        '''
        Place all widgets in the add record face
        Grid places widgets in row and columnwise 
        Row : Specifies the row number
        Column : Specifies the column number
        Columnspan : Specifies the number of columns across which the widget should spread
        Padx : Specifies the horizontal spacing between the widgets
        Pady : Specifies the vertical spacing between the widgets
        Stick : Aligns the widget
        ''' 
        
        # Creates a button to return to the Initial Face
        warnings.filterwarnings('ignore')
        tip = Balloon(self.contolbtns) # Adds tootip for the buttons
        self.home_btn = tk.Button(self.contolbtns,
                  text='Home',
                  width=button_width,
                  bg='#89c4f4',
                  font=helv_act,
                  command=lambda:self.change('InitFace'))
        self.home_btn.grid(row=1,column=1,padx=50,pady=60)   
        tip.bind_widget(self.home_btn,balloonmsg="Go to Home Page")
        # Creates a button to generate summary statistics of the data
        self.summary_stats_btn = tk.Button(self.contolbtns,
                  text='Summary statistics',
                  width=button_width,
                  bg='#89c4f4',
                  font=helv_act,
                  command=self.display_table, relief = SUNKEN)
        self.summary_stats_btn.grid(row=1, column=2, padx=50, pady=60)
        tip.bind_widget(self.summary_stats_btn,balloonmsg="View summary statistics of the patient records")
        # Creates a button to view plots of the patient records
        self.graphics_btn = tk.Button(self.contolbtns,
                  text='Graphics',
                  width=button_width,
                  bg='#89c4f4',
                  font=helv_act,
                  command=self.display_graphics_page1)
        self.graphics_btn.grid(row=1, column=3, padx=50, pady=60)
        tip.bind_widget(self.graphics_btn,balloonmsg="View summary plots of the patient records")
        # Creates a button to exit from the program
        self.exit_btn = tk.Button(self.contolbtns,
                  text='Exit',
                  width=button_width,
                  bg='#89c4f4',
                  font =helv_act,
                  command=CloseWindow)
        self.exit_btn.grid(row=1, column=4, padx=50, pady=60)
        tip.bind_widget(self.exit_btn,balloonmsg="Exit the program")
        

        for widget in self.sumryface.winfo_children():
            if isinstance(widget, Label):
                try:
                    widget.config(bg = self.master.background_colour)
                except:
                    pass
        
    def display_table(self):
        for widget in self.sumryface.winfo_children():
            widget.destroy()
        helv_act = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)        
        button_width = 20
        # Changes the configuration of the summary stats and graphics button
        self.summary_stats_btn.config(relief = SUNKEN)
        self.graphics_btn.config(relief = RAISED)
        # Destroys all the labels in the graphics face
        try:
            self.page_msg.destroy()
            self.page1_btn.place_forget()
            self.page2_btn.place_forget()
            self.page3_btn.place_forget()
            self.page4_btn.place_forget()
            self.page5_btn.place_forget()
            self.page6_btn.place_forget()
        except: 
            pass
        # Displays the summary statistics tabel for patient records
        self.sumrytable = Table(self.sumryface, dataframe=self.record.describe(include = "all").reset_index(), editable=False)
        self.sumrytable.autoResizeColumns()
        self.sumrytable.show()
     
    def display_graphics_page1(self):
        # Sets up hover tip for all the buttons on the graphics page
        tip = Balloon(self.contolbtns)
        self.page_msg = tk.Label(text = 'Navigation:')
        self.page_msg.place(x = 1100 , y = 130) 
        try:
            self.page_msg.config(bg = self.master.background_colour)
        except:
           pass
        # Sets button attributes
        helv_act = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)        
        button_width = 20
        # Changes the way the button looks depending on what is clicked
        self.summary_stats_btn.config(relief = RAISED)
        self.graphics_btn.config(relief = SUNKEN)
        # Creates a button a which redirects the user to page 1
        self.page1_btn = tk.Button(self.contolbtns,
                  text='1',
                  width=2,
                  bg='white',
                  command=self.display_graphics_page1, relief = SUNKEN)
        self.page1_btn.place(x = 1200, y = 130)
        tip.bind_widget(self.page1_btn,balloonmsg="Go to Page 1")
        # Creates a button a which redirects the user to page 2
        self.page2_btn = tk.Button(self.contolbtns,
                  text='2',
                  width=2,
                  bg='white',
                  command=self.display_graphics_page2)
        self.page2_btn.place(x = 1225, y = 130)
        tip.bind_widget(self.page2_btn,balloonmsg="Go to Page 2")
        # Creates a button a which redirects the user to page 3
        self.page3_btn = tk.Button(self.contolbtns,
                  text='3',
                  width=2,
                  bg='white',
                  command=self.display_graphics_page3)
        self.page3_btn.place(x = 1250, y = 130)
        tip.bind_widget(self.page3_btn,balloonmsg="Go to Page 3")
        # Creates a button a which redirects the user to page 4
        self.page4_btn = tk.Button(self.contolbtns,
                  text='4',
                  width=2,
                  bg='white',
                  command=self.display_graphics_page4)
        self.page4_btn.place(x = 1275, y = 130)
        tip.bind_widget(self.page4_btn,balloonmsg="Go to Page 4")
        # Creates a button a which redirects the user to page 5
        self.page5_btn = tk.Button(self.contolbtns,
                  text='5',
                  width=2,
                  bg='white',
                  command=self.display_graphics_page5)
        self.page5_btn.place(x = 1300, y = 130)
        tip.bind_widget(self.page5_btn,balloonmsg="Go to Page 5")
        # Creates a button a which redirects the user to page 6
        self.page6_btn = tk.Button(self.contolbtns,
                  text='6',
                  width=2,
                  bg='white',
                  command=self.display_graphics_page6)
        self.page6_btn.place(x = 1325, y = 130)
        tip.bind_widget(self.page6_btn,balloonmsg="Go to Page 6")
        for widget in self.sumryface.winfo_children():
            widget.destroy()
        self.plot = SumryFace()
        self.plot = self.plot.plot_data()
        canvas = FigureCanvasTkAgg(self.plot[0],
                                master = self.sumryface)  
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        tk.Label(text = "Page 1").place(x = 3000, y = 130)
        
    def display_graphics_page2(self):     
        # Changes the way the button looks depending on which page the user is on
        self.summary_stats_btn.config(relief = RAISED)
        self.graphics_btn.config(relief = SUNKEN)
        self.page1_btn.config(relief = RAISED)
        self.page2_btn.config(relief = SUNKEN)
        self.page3_btn.config(relief = RAISED)
        self.page4_btn.config(relief = RAISED)
        self.page5_btn.config(relief = RAISED)
        self.page6_btn.config(relief = RAISED)       
        for widget in self.sumryface.winfo_children():
            widget.destroy()
        self.plot = SumryFace()
        self.plot = self.plot.plot_data()
        canvas = FigureCanvasTkAgg(self.plot[1],
                                master = self.sumryface)  
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        
        
        
    def display_graphics_page3(self):  
        # Changes the way the button looks depending on which page the user is on
        self.summary_stats_btn.config(relief = RAISED)
        self.graphics_btn.config(relief = SUNKEN)
        self.page1_btn.config(relief = RAISED)
        self.page2_btn.config(relief = RAISED)
        self.page3_btn.config(relief = SUNKEN)
        self.page4_btn.config(relief = RAISED)
        self.page5_btn.config(relief = RAISED)
        self.page6_btn.config(relief = RAISED)
        # Destroys all the widgets in the summary face
        for widget in self.sumryface.winfo_children():
            widget.destroy()
        self.plot = SumryFace()
        self.plot = self.plot.plot_data()
        canvas = FigureCanvasTkAgg(self.plot[2],
                                master = self.sumryface)  
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        
        
    def display_graphics_page4(self):       
        # Changes the way the button looks depending on which page the user is on
        self.summary_stats_btn.config(relief = RAISED)
        self.graphics_btn.config(relief = SUNKEN)
        self.page1_btn.config(relief = RAISED)
        self.page2_btn.config(relief = RAISED)
        self.page3_btn.config(relief = RAISED)
        self.page4_btn.config(relief = SUNKEN)
        self.page5_btn.config(relief = RAISED)
        self.page6_btn.config(relief = RAISED)
        # Destroys all the widgets in the summary face
        for widget in self.sumryface.winfo_children():
            widget.destroy()
        self.plot = SumryFace()
        self.plot = self.plot.plot_data()
        canvas = FigureCanvasTkAgg(self.plot[3],
                                master = self.sumryface)  
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    
    def display_graphics_page5(self):  
        # Changes the way the button looks depending on which page the user is on
        self.summary_stats_btn.config(relief = RAISED)
        self.graphics_btn.config(relief = SUNKEN)
        self.page1_btn.config(relief = RAISED)
        self.page2_btn.config(relief = RAISED)
        self.page3_btn.config(relief = RAISED)
        self.page4_btn.config(relief = RAISED)
        self.page5_btn.config(relief = SUNKEN)
        self.page6_btn.config(relief = RAISED)
        # Destroys all the widgets in the summary face
        for widget in self.sumryface.winfo_children():
            widget.destroy()
        self.plot = SumryFace()
        self.plot = self.plot.plot_data()
        canvas = FigureCanvasTkAgg(self.plot[4],
                                master = self.sumryface)  
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        
    def display_graphics_page6(self):
        # Changes the way the button looks depending on which page the user is on
        self.summary_stats_btn.config(relief = RAISED)
        self.graphics_btn.config(relief = SUNKEN)
        self.page1_btn.config(relief = RAISED)
        self.page2_btn.config(relief = RAISED)
        self.page3_btn.config(relief = RAISED)
        self.page4_btn.config(relief = RAISED)
        self.page5_btn.config(relief = RAISED)
        self.page6_btn.config(relief = SUNKEN)
        # Destroys all the widgets in the summary face
        for widget in self.sumryface.winfo_children():
            widget.destroy()
        self.plot = SumryFace()
        self.plot = self.plot.plot_data()
        canvas = FigureCanvasTkAgg(self.plot[5],
                                master = self.sumryface)  
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        
    def change(self, choice):  
        '''
        Change to the next level interface based on the button selection
        Inquiry button redirects the user to the inquiry face
        Add button redirects the user to the add face
        Update button redirects the user to the update face
        Summary button redirects the user to the summary face
        '''
        try:
            self.page_msg.destroy()
            self.page1_btn.place_forget()
            self.page2_btn.place_forget()
            self.page3_btn.place_forget()
            self.page4_btn.place_forget()
            self.page5_btn.place_forget()
            self.page6_btn.place_forget()
        except:
            pass
        self.sumryface.destroy()      # Close current window
        self.contolbtns.destroy()
        eval(choice)(self.master)    # Call next level window class


    
class CloseWindow():
    def __init__(self):
        root.destroy()



if __name__ == '__main__':
    root = tk.tix.Tk()
    app = Basedesk(root)
    root.title("Accidents and Emergency Department")
    root.attributes('-fullscreen')
    root.mainloop()
        
  
