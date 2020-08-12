For this scraper to run you will need installed Google chrome browser and selenium, webdriver_manager, and scrapy packages.
Google Chrome and selenium are used due to hight interactivity of webpage, having large part of data provided by javascript code. 
Later can be install via pip:
 
 or from requirements.txt:
 - pip install -r requirements.txt
 
 After you finishes installations, run it by running in terminal from top folder "people":
 - scrapy crawl aws -a file=<path_to_file>
 
