"""

Hi Brion! 

This is Group 1's submission. Enjoy! 

Contributors: 
    Ashley Sequeira, 
    Lisa D, 
    Carrie Pratt,
    Nelson Colon,
    Chris Fiorillo

    
DOCUMENTATION: 
The Consumer Complaint Database is a collection of complaints about consumer financial products and services that we sent to companies for response. 
Complaints are published after the company responds, confirming a commercial relationship with the consumer, or after 15 days, whichever comes first. 
Complaints referred to other regulators, such as complaints about depository institutions with less than $10 billion in assets, are not published 
in the Consumer Complaint Database. The database generally updates daily. 

Hello Group 1! 

I have added some comments to the group code below! 

Here is the URL that will assist in generating our API call URL: https://cfpb.github.io/api/ccdb/api.html

If we get ambitious, we can have the user select a state and append it to the end of the URL, as seen below. (I did this, but dont understand 'state')
Orrrrr we can have them pick a date range. The sky is the limit! 


Progress for the day:
1. selected an API, and it is a good and useful one: CFPB's consumer complaints! 
2. tested the API, reviewed the data dictionary and what some of these terms mean
  a. The 'schemas' section down near the bottom has more information on each field.
3. created an OUTPUT file to review, and determine what should be our xls objects and attributes
4. created shells for required functions! 
5.  I am done! For now! 
6. I refactored and organized a smidge.

BONUS:
1. connected to the kanye api and pulled a random quote for our worksheet title. (NVM)
    a. I think we should change this to a rick and morty character. we can choose a random URL and pull a name.
    b. okay I changed this.
"""
# imports
import json, requests
from openpyxl import Workbook # setup for things 
from random import randint as ri # for the rick character selection! 

wb = Workbook() #this block sets up our workbook and sheet! 
ws = wb.active

def check_state(user_state):
    """
    This validates user input.

    params:
        user_state - should eb a two character state input.

    returns:
        checker - boolean, True if valid.
    """
    good_states = set([ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'])
    
    if user_state in good_states:
        return True
    else:
        print("\nNOPE! Try again...\n")
        return False



def ws_titler(): #creative title for our ws
    """ 
    STATUS: COMPLETED, but maybe we should change it?
    EDIT: I did! It is now R&M
    This function calls the Kanye REST API and returns the first 12 chars of the string to be ws title heheheh (ignore that)

    If all else fails, we will have succeeded at this!

    params:
        None

    returns:
        title (str)
    """
    char_num = ri(1,820) #820~ chars to pick from.
    char_url = 'https://api.kanye.rest/'
    rm = requests.get(char_url) #changed to RM
    quote = json.loads(rm.text)
    
    title = (quote['quote'])
    # print(f"the title of your sheet is: {title}") #for testing; comment out... if you want to

    return title


def headers(main_dict): #pulls headers. These are important due to structure of json return
    """
    STATUS: Completed! NICE.
    
    This should take in a main dictionary (converted from the json)
    and return a list of headers.
    
    params:
        main_dict - main dictionary full of converted json text
        
    returns:
        headers (list)
    """
    # print(main_dict['aggregations']['state']['state']['buckets'][0])


    heads = set() # okay this is a set, which allows only one per item in it! it will ignore dupes
    for state in main_dict['aggregations']['state']['state']['buckets']:
        heads.add(state['product']['buckets'][0]['key'])

    headers = list(heads) # converts a set into a list, because we want State to be our first col.
    headers.insert(0, 'State') #inserts 'State' as the first list item

    return(headers)

def content(main_dict, headers): 
    """
    This takes in a main dict, and returns a list of lists comprised of values associated with headers, which are keys.
    
    params:
        main_dict - main dictionary full of converted json text
        headers - these are our keys, used to pull values

    returns:
        sheet_content - this is the content of our sheet (list of lists)    
    """

    rows = [headers]

    states = []

    for item in main_dict['aggregations']['state']['state']['buckets']: #gets all our states! 
        states.append(item['key'])


    for state in states: #alright.. this was a total PITA because of the API return syntax. made an intermediary dict for search.
        row = [] #blank row!
        row.append(state) # state comes first.

        source_dict = {}
        source_proc={}

        for dict in main_dict['aggregations']['state']['state']['buckets']: #Look at this nonsense! what a joke! 

            if dict['key'] == state:
                source_dict = dict['product']['buckets']
                for d in source_dict:
                    source_proc[d['key']] = d['doc_count'] #WHAT A HEADACHE, CFPB
        

        for header in headers[1:]: #source proc is our processed dictionary for these, with keys and values rearranged. 
            if header in source_proc: #if the header is present in our processed dict, we drop the value into our row list.
                row.append(str(source_proc[header]))
            else:
                row.append('0') #if not, it's a zero
        
        rows.append(row) # drop the row list into our rows list of lists. 

    return(rows)


def sheet_maker(all_data):
    """
    This takes in a list of lists, where each sublist is a row of data.
    The first one should be comprised of headers.
    It then puts it into an xls sheet and saves it!
    
    params:
        all_data - list of lists where the first is headers and each following is row data
    
    returns:
        None
    """
    for r in enumerate(all_data): # for each row in our list of list.
        for i in enumerate(r[1]): # for each item in the row.. 
            ws.cell(row=r[0] + 1, column = i[0]+1, value = i[1])


def goodbye(): # the other CFPB api doesnt work (see comment) so we used kanye again...
    """
    This uses another varition of the CFPB's API to generate a goodbye phrase. It's either broken or I don't get it.
    """

    # url="https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/_suggest?size=60&text=" + str(search_term)
    # rm = requests.get(url) #changed to RM
    quote = ws_titler()

    print(f"Goodbye, and never forget the importance of {quote}")


def abbr_lookup(abbr): #just an abbreviation lookup dict
    """
    This one is self-explanatory!
    """

    states_lookup = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }
    return states_lookup[abbr]

def main():

    print("\nWelcome to CFPB Complaint Investigator Tool!\n\n")



    checker = False # sentinel; runs validation until match realized
    while checker == False:
        state_in = input("What state (xx)?: ").upper() #yep, letting people pick their state! or not! 
        checker = check_state(state_in) #check_state validates entry against a list.

    search_term = input("What search term?: ").lower() #and their search term

    search_term.replace(" ", "%20") #replaces whitespace with blank characters for the search

    if state_in: #users can also choose to not input a state, to get all states.
        state_url = '&state=' + state_in # builds the portion of the URL for state lookup


    url = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/geo/states?search_term=" + search_term + \
    "&field=complaint_what_happened&company_received_min=2022-09-26&date_received_min=2022-09-26" + state_url
    
    ws.title = ws_titler() + " in " + abbr_lookup(state_in) # looks up appreviation, gets full state name!

    x = requests.get(url) # our api call. 

    p_dict = json.loads(x.text) #loads json to a dict

    d_dict = json.dumps(p_dict, indent=2, sort_keys=True) #makes it readable!

    with open('OUTPUT.txt', 'w') as f:  # this block creates a document called OUTPUT in the same directory as this .py file.
        f.write(d_dict)                 # this is just to be used to create a file to explore and see the json text. it's complicated.
        f.close()

    full_sheet = [] # master list that will contain all data
    cols = headers(p_dict) #list of headers (keys)
    all_rows = content(p_dict, cols) # should be a list of lists, values of keys

    sheet_maker(all_rows) #sends all rows of data to our sheet maker function

    wb.save("group1_project.xlsx")

    goodbye() # Fixed! YAY.

main()