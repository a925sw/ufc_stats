# UFC Fight Picks

#### Project Status: [Mostly Complete]

## Project Intro/Objective
The purpose of this project is to create a continuous pipeline for predicting UFC fights with machine learning models. With inspiration taken from Paul Gift of BloodyElbow.com and a project found at github.com/WarrierRajeev/UFC-Predictions, all the code for this projet was written from the ground up. Starting with scraping all past UFC event and fighter data from the UFC official website, cleaning the data, doing feature engineering, creating the ML models from historic train_test data, and finally predicting upcoming UFC fights with the saved models. After each event is completed, the Updater scraper grabs the new fight data into the pipeline and adds it to update the model with the new information. The goal is having a smooth pipeline to update the dataset every time there are new fights, and add these observations to the model for gradually improving accuracy.


### Requirements
* Python 3 or higher
* Pandas
* Numpy
* Selenium / Splinter
* BeautifulSoup
* Scikitlearn
* Jupyter Notebooks
* Pickle 

## Project Sections

### Part 1: Scraping
There are three scrapers used in this project, two initial srapers to be run if this is the first time collecting the data and an updater scraper to be run subsequently in order to add new observations.
#### fighter_scraper:
This scraper is used to collect fighter profile data from each fighter in the UFC's list of fighters who have competed in the UFC. The UFC keeps this data on their website at http://ufcstats.com/statistics/fighters listed alphabetically by last name. The scraper runs through each letter and grabs the URL for each fighter with a last name begining with that letter. It the visits each profile URL to collect the info contained on their profile (date of birth, height, reach, etc..). This data is loaded into a dataframe and cleaned a bit by stripping out unneccessary text in the fields (such as "HEIGHT: " before each fighters listed height). Once cleaned, the dataframe is saved as a CSV to be used later on. Time to complete is roughly 1 hour.
#### fight_scraper:
This scraper collects the fight stats data of each bout that has happened in the UFC (barring a handful of fights very early in the promotion's history that have no available data). This is done by visiting http://ufcstats.com/statistics/events/completed?page=all to loop through each event that has happened in the UFC (except the very first event, UFC 1), visiting the URL of the event, and then performing another nested loop on each fight URL that took place on that event. Each individual fight URL contains stats taken by FightMetric (bought and rebranded as UFCstats) about strikes, takedowns, control time, etc.. who won, and the exact outcome of the fight (e.g KO at 3:27 of round 2). Once all this data has been scraped into a dateframe of all fights, it is saved as a CSV to be used later. The events page also contains a URL for the next upcoming UFC event that has not yet taken place, and that data is also scraped into a sperate dataframe with placeholder values for the fight stats mirroring the format of past events and saved as "future event." As I will show in the next section, this makes the cleaning proccess easier and more streamlined. Time to complete is 3-4 hours
#### updater:
This scraper is used once the initial scrapers have been run and the data collected, but there are new fights to be added to the dataset. This scraper will check a list of past fight URLs and fighter profile URLs to only scrape data from fights/fighters that are not already in the dataset. This allows for quick scraping of only the new observations, and concats on top of the old data to be cleaned. The reason for this is that the cleaning proccess is very fast and can be run on the entire dataset in less than a minute, but the scraping takes quite a bit of time. This way allows the scraping of new data just once, while feeding everything into the same cleaning pipeline that can be completed rapidly. Time to complete depends on how much new data there is to add, but is usually 10-15 minutes if run after each event.

### Part 2: Cleaning
Cleaning the data is broken down into three notebooks. One for cleaning the fighter profile data, one for the fights data, and a final notbook that merges these together and prepares the dataset for being run through the models.
#### fighter_info:
This notebook is where fighter profile data is cleaned and prepared for use later. Most of the data here is not used in later notebooks, and the data that is kept must be transformed in order to be useful. First, we narrow down our columns to Name, date of birth, height, weight, reach, and stance (UFC record is also kept in current iteration of notebook, although it is not used). Height is then converted from its string format (e.g 6'1") into an int of inches, dropping the unused height columns. Reach is already listed in inches, but need to be stripped of the " marker and converted to int as well. Because so many of the fighters in the dataset are have no reach listed, it is important to get an aproximation from height values. Height and reach are highly corelated, so for fighters with no reach listed, we simply substitute height in inches for the null reach values. Any fighter with no height or reach listed is dropped. Next, we simplify the stances by narrowing down the possibilities to 3, Orthodox, Southpaw, and Switch. Fighters with some variation of switch, such as "Openstance," or "Sideways," are changed to switch. All nan values are converted to Orthodox. This is done because to the overwhelming majority of fighters are orthodox, and of the ~650 fighters with no stance listed, assigning them all to orthodox will be correct far more often than not. This is important because, while the top levels of combat sports have a much higher share of southpaw fighters than the general population, most fighters are right handed and fight out of an orthodox stance. These rough hueristics for filling in reach and stance info is more relevant for old fights/fighter data, as it is extremely rare to have a fighter in the modern era with no reach or stance listed. These things will continue to get more accurate over time as modern stat keeping continues to outweigh old data from before information was rigorously kept.     
#### cleaning_fights:
This notebook is where most of the raw data preproccessing happens for fights, and columns are broken out from their initial formats (e.g total_strike column listed as "57 of 104" into two seperate columns of total_strikes_landed: 57, and total_strikes_thrown: 104). This kind of reformating and preproccessing is done for red and blue fighters, creating many more columns than initially scraped into our first fight dataframe. In addition to this reformatting, we also get the flip side of all these stats (e.g 2 listed takedowns for red fighter also becomes 2 time TAKEN DOWN for blue fighter). The time and rounds gets turned into total fight seconds, and same with control time. For a full breakdown of cleaning and transformation done, there is step by step documentation in the notebook of what is done to prepare it for mergeing and feature engineering in the next notebook.
#### fight_stats:
This notebook is were all the fighter profile data is merged with fight stats and more complex feature calculations are done. 
