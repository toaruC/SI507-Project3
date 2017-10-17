from bs4 import BeautifulSoup, Tag
import unittest
import requests
import re

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!

def get_from_requests(url, file_name):
    response = requests.get(url)
    html = response.text
    f = open(file_name, 'w')
    f.write(html)
    f.close()

    return html

######### PART 0 #########

# Write your code for Part 0 here.
try:
    gallery_html = open('gallery.html','r').read()
except:
    gallery_html = get_from_requests("http://newmantaylor.com/gallery.html", 'gallery.html')

gallery_soup = BeautifulSoup(gallery_html,'html.parser')
gallery_img_list = gallery_soup.find_all("img")

def print_alt_text(img_list):
    img_num = 1
    for bs_img in gallery_img_list:
        if bs_img.get('alt'):
            if bs_img.get('alt') == "Waving Kitty " + str(img_num):
                print(bs_img.get('alt'))
                img_num += 1
            else:
                print(bs_img.get('alt') + ": Wrong alternative text! Should be Waving Kitty {}.".format(img_num))
                img_num += 1
        else:
            print("No alternative text provided!")
            img_num += 1

print_alt_text(gallery_img_list)

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

# Create Nps Mainpage Soup
try:
    nps_gov_data_html = open('nps_gov_data.html', 'r').read()
except:
    nps_gov_data_html = get_from_requests("https://www.nps.gov/index.htm", 'nps_gov_data.html')

nps_gov_soup = BeautifulSoup(nps_gov_data_html, 'html.parser')


# Define Method get_state_url
def get_state_url(state_name, soup):
    state_list = soup.find("ul",{"class":"dropdown-menu"}).find_all("a")
    for state in state_list:
        if state_name == state.get_text():
            url = "https://www.nps.gov{}".format(state.get('href'))
            break

    return url

# Create Arkanasas Soup
try:
    arkansas_data_html = open('arkansas_data.html', 'r').read()
except:
    url_ar = get_state_url("Arkansas", nps_gov_soup)
    arkansas_data_html = get_from_requests(url_ar, 'arkansas_data.html')

arkansas_soup = BeautifulSoup(arkansas_data_html, 'html.parser')

# Create California Soup
try:
    california_data_html = open('california_data.html', 'r').read()
except:
    url_ca = get_state_url("California", nps_gov_soup)
    california_data_html = get_from_requests(url_ca, 'california_data.html')

california_soup = BeautifulSoup(california_data_html, 'html.parser')

# Create Michigan Soup
try:
    michigan_data_html = open('michigan_data.html', 'r').read()
except:
    url_mi = get_state_url("Michigan", nps_gov_soup)
    michigan_data_html = get_from_requests(url_mi, 'michigan_data.html')

michigan_soup = BeautifulSoup(michigan_data_html, 'html.parser')


# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.




######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...



## Define your class NationalSite here:
class NationalSite(object):
    def __init__(self, soup_park):
        self.soup = soup_park  # don't forget to add self.
        self.location = soup_park.find("h4").get_text()
        self.name = soup_park.find("h3").get_text()
        if soup_park.find("h2"):
            self.type = soup_park.find("h2").get_text()
        else:
            self.type = None

        if soup_park.find("p"):
            self.description = soup_park.find("p").get_text()
        else:
            self.description = ""

    def __str__(self):
        return "{0} | {1}".format(self.name, self.location)

    def get_mailing_address(self):
        csv_mailing_addr = ""
        for a in self.soup.find_all("a"):
            if "Basic Information" in a.get_text():
                child_url = a.get("href")
                break

        child_html = requests.get(child_url).text
        soup_basic_info = BeautifulSoup(child_html, 'html.parser')

        if soup_basic_info.find("div", {"class":"physical-address"}):
            mailing_addr = soup_basic_info.find("div", {"class":"physical-address"}).get_text()
            lines = mailing_addr.strip().replace(',', "").splitlines()
            lines_rm_br = []
            for line in lines:
                if line is not '':
                    lines_rm_br.append(line)
            csv_mailing_addr = "/".join(lines_rm_br)

        return csv_mailing_addr
        # else:
        #     return "abcde"




    def __contains__(self, input_name):
        return input_name in self.name


## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

f = open("sample_html_of_park.html",'r')
soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# print(soup_park_inst.prettify())
sample_inst = NationalSite(soup_park_inst)
f.close()
print(str(sample_inst))
print(sample_inst.get_mailing_address())



######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

def get_natl_sites(soup_state):
    state_natl_sites = []
    soup_park_list = soup_state.find("ul", {"id":"list_parks"}).find_all("li", {"class":"clearfix"})
    for park in soup_park_list:
        state_natl_sites.append(NationalSite(park))
    return state_natl_sites

arkansas_natl_sites = get_natl_sites(arkansas_soup)
california_natl_sites = get_natl_sites(california_soup)
michigan_natl_sites = get_natl_sites(michigan_soup)


##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!

def convert_to_csv(natl_site):
    natl_site_row_strings = [natl_site.name, natl_site.location, natl_site.type, natl_site.get_mailing_address(), natl_site.description.strip()]
    csv_row_strings = []

    # Q: is there any better/simpler solution?
    for i in natl_site_row_strings:
        if i:
            if '"' in i:
                result = i.replace('"', '""')
                if ',' in i:
                    csv_row_strings.append('"' + result + '"')
                else:
                    csv_row_strings.append(result)
            else:
                if ',' in i:
                    csv_row_strings.append('"' + i + '"')
                else:
                    csv_row_strings.append(i)
        else:
            csv_row_strings.append("None")

    return csv_row_strings


def write_csv_resources(natl_sites, dir):
    outfile = open(dir, "w")  # dir is the directory of csv file
    header_columns = ["Name", "Location", "Type", "Address", "Description"]  # define header
    outfile.write('{},{},{},{},{}\n'.format(*header_columns))  # no white space between attributes
    for site in natl_sites:
        outfile.write('{},{},{},{},{}\n'.format(*convert_to_csv(site)))
    outfile.close()


# write arkansas_natl_sites
write_csv_resources(arkansas_natl_sites, "arkansas.csv")

# write california_natl_sites
write_csv_resources(california_natl_sites, "california.csv")

# write michigan_natl_sites
write_csv_resources(michigan_natl_sites, "michigan.csv")
