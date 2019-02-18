####### PANDAS

#drop rows where selected columns contain nan
df.dropna(subset=['city','state','job_description','job_type'])

#return count of occurences of a valuable in a given column (series)
df['category'].value_counts()


PANDAS
import pandas as pd

#IMPORT
df = pd.read_csv('filename.csv')
df = pd.read_excel('filename.xlsx')
df.head(rows)  #show top x rows
In case of errors ry calling read_csv with encoding='latin1', encoding='iso-8859-1' or encoding='cp1252'; or 'utf-8' 

#CLEANING
removing $ and , from currency data
dataframe['column'] = dataframe['column'].str.replace("$","")


#EXPORT
df.to_csv('filename.csv')
df.to_excel('filename.xls')
#VIEW/INSPECT
df.head(x) #show x rows
df.tail()
df.shape()
df.describe() #summary stats for numerical fields
s.value_counts(dropna=False)
df.apply(pd.Series.value_counts) #unique values and counts for all columns
loc
df.apply(lambda x: sum(x.isnull()),axis=0)



https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Python_Pandas_Cheat_Sheet_2.pdf
https://www.dataquest.io/blog/large_files/pandas-cheat-sheet.pdf

https://github.com/pandas-dev/pandas/blob/master/doc/cheatsheet/Pandas_Cheat_Sheet.pdf






from worklaptop sticky notes 16/1/18

Python NoTES



import re #import the regex module

#Create a Regex object with the re.compile() function. (Remember to use a raw string.)

myregex = re.compile(r'regex goes here') 

#Pass the string you want to search into the Regex object’s search() method. This returns a Match object.

mymatchobject = myregex.search(mytext)  #use the search RE method on the regex variable to do do the matching

# or use #findall()

#Call the Match object’s group() method to return a string of the actual matched text.

#use VERBOSE argument and triple ''' to spread compile method over multiple lines (ignoring whitespace)

re.compile(r''''(

(\d)

(\s|-|\.)?,

re.VERBOSE)

#email regex from http://emailregex.com

r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"





import pyperclip #for copying/pasting - accessing the clip boad

pip install pyperclip #if the module is not installed

pip install gtk #if your linux does not have a copy/paste mechanism

To copy text to the clipboard, pass a string to pyperclip.copy(). To paste the text from the clipboard, call pyperclip.paste() and the text will be returned as a string value.

import pyperclip

pyperclip.copy('Hello world!')

pyperclip.paste()

'Hello world!'












import pandas as pd
df = pd.read_excel('file.xlsx',header=1,skiprows=1) (import excel to a pandas dataframe)

df.head(10) #show first 10 rows
df.describe #provide summary stats on numeric fields
df.


#DELETE LAST LINE IN A FILE!!!
#handy for the non-printable character created when compiling csv via cmd prompt

mylines = open('filename.txt', 'r').readlines()  #open file as readonly to get lines
print(mylines[-2:])  #print the last two lines
myfile = open('filename.txt' 'w') #open file i n write
myfile.writelines([item for item in lines[:-1]])
myfile.close()
mylines = open('filename.txt', 'r').readlines()  #open file as readonly to get lines
print(mylines[-2:])  #print the last two lines


import re #import the regex module

#Create a Regex object with the re.compile() function. (Remember to use a raw string.)

myregex = re.compile(r'regex goes here') 

#Pass the string you want to search into the Regex object’s search() method. This returns a Match object.

mymatchobject = myregex.search(mytext)  #use the search RE method on the regex variable to do do the matching

# or use #findall()

#Call the Match object’s group() method to return a string of the actual matched text.

#use VERBOSE argument and triple ''' to spread compile method over multiple lines (ignoring whitespace)

re.compile(r''''(

(\d)

(\s|-|\.)?,

re.VERBOSE)

#email regex from http://emailregex.com

r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"





import pyperclip #for copying/pasting - accessing the clip boad

pip install pyperclip #if the module is not installed

pip install gtk #if your linux does not have a copy/paste mechanism

To copy text to the clipboard, pass a string to pyperclip.copy(). To paste the text from the clipboard, call pyperclip.paste() and the text will be returned as a string value.

import pyperclip

pyperclip.copy('Hello world!')

pyperclip.paste()

'Hello world!'


on color analysis
http://mkweb.bcgsc.ca/brewer/talks/color-palettes-brewer.pdf
http://mkweb.bcgsc.ca/color-summarizer/?home
