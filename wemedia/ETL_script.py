#setup
import pandas as pd
import os
import django
import traceback

os.environ["DJANGO_SETTINGS_MODULE"] = 'wemedia.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from discuss.models import Topic, content


#user input
filename = input("Please input filename inside data folder (without extention) : ")

'''
#File pick test
try:
    print(os.listdir())
    df_input = pd.read_excel('wemedia\\data\\' + filename + '.xlsx')
    print("file found")
    exit()
except:
    print("file not found")
    print(traceback.format_exc())
    exit()
'''

df_input = pd.read_excel('wemedia\\data\\' + filename + '.xlsx')

#helper functions
def convert_string_to_list(text):
    '''
    Converts comma separated string to list
    '''
    if pd.isna(text):
        return []
    
    lst = text.split(',')
    
    return [x.strip() for x in lst]

def parse_text(text):
    '''
    If nan, returns blank. Else returns text.
    '''
    if pd.isna(text):
        return ""
    else:
        return text

def extract_books_from_row(row):
    '''
    Returns list of contents extracted for this row
    '''
    content_list = []
    if pd.isna(row["Book_1"]) == False or pd.isna(row["Author_1"]) == False:
        #print("Book_1 found")
        content_list.append(content(title = parse_text(row["Book_1"]), creator = parse_text(row["Author_1"]))) 

    if pd.isna(row["Book_2"]) == False or pd.isna(row["Author_2"]) == False:
        #print("Book_2 found")
        content_list.append(content(title = parse_text(row["Book_2"]), creator = parse_text(row["Author_2"])))
        
    if pd.isna(row["Book_3"]) == False or pd.isna(row["Author_3"]) == False:
        #print("Book_3 found")
        content_list.append(content(title = parse_text(row["Book_3"]), creator = parse_text(row["Author_3"])))
        
    if pd.isna(row["Book_4"]) == False or pd.isna(row["Author_4"]) == False:
        #print("Book_4 found")
        content_list.append(content(title = parse_text(row["Book_4"]), creator = parse_text(row["Author_4"])))
        
    if pd.isna(row["Book_5"]) == False or pd.isna(row["Author_5"]) == False:
        #print("Book_5 found")
        content_list.append(content(title = parse_text(row["Book_5"]), creator = parse_text(row["Author_5"])))
        
    return content_list

def persist_objects(object_list):
    '''
    persists list of contents to database
    '''
    for obj in object_list:
        obj.save()
        
def connect_content(parent_content_list, child_content_list):
    '''
    Establishes relationships between content
    '''
    for parent_content in parent_content_list:
        for child_content in child_content_list:
            parent_content.related_content.add(child_content)
            
def extract_topics_from_cell(cell):
    '''
    Returns list of contents extracted for this cell
    '''
    list_of_topic_strings = convert_string_to_list(row["Topics"])
    
    topic_list = []
    for topic_string in list_of_topic_strings:
        topic_list.append(parse_into_topic_object(topic_string))
        
    return topic_list

def parse_into_topic_object(topic_string):
    '''
    Returns existing or else newly created topic object 
    '''
    try:
        topic_object = Topic.objects.get(title=topic_string)
        return topic_object
    except topic.DoesNotExist:
        #persist new entry into db
        topic_object = Topic(title = topic_string)
        topic_object.save()
        return topic_object

def connect_topic(topic_list, content_list):
    '''
    Establishes relationships between topic and content
    '''
    for content in content_list:
        for topic in topic_list:
            content.topics.add(topic)


#Process file
for i, row in df_input.iterrows():    
    if row["is_op"] == True:
        #reset all lists
        parent_topic_list = []
        parent_content_list = []
        child_topic_list = []
        child_content_list = []
        
        #parent (OP)
        parent_topic_list = extract_topics_from_cell(row["Topics"])
        
        parent_content_list = extract_books_from_row(row)
        persist_objects(parent_content_list)
        
        connect_topic(parent_topic_list, parent_content_list)
    else:
        #child (Comments)
        child_topic_list = extract_topics_from_cell(row["Topics"])
        
        child_content_list = extract_books_from_row(row)
        persist_objects(child_content_list)
        connect_content(parent_content_list, child_content_list) 
        
        connect_topic(child_topic_list, child_content_list)
        connect_topic(parent_topic_list, child_content_list)