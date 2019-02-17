####### PANDAS

#drop rows where selected columns contain nan
df.dropna(subset=['city','state','job_description','job_type'])

#return count of occurences of a valuable in a given column (series)
df['category'].value_counts()
