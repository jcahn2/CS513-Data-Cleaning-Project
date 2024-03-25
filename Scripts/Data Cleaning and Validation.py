#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')


# In[19]:


#read cleaned CSV (output of OpenRefine)
clean_df = pd.read_csv('Food-Inspections-07182023.csv', sep=',')
print(len(clean_df.index))


# In[21]:


#separate business data
fldlist = ['License # - Clean','DBA Name - Clean','AKA Name - Clean','Facility Type - Clean','Inspection Date','License # - Flag']
renfldlist = ['License #','DBA Name','AKA Name','Facility Type','Inspection Date','License # - Flag']
business_df = clean_df
business_df = business_df[fldlist]
#standardize field names
counter = 0
for item in fldlist:
    business_df = business_df.rename(columns={item: renfldlist[counter]})
    counter += 1

print("Before cleaning:"+str(len(business_df.index)))
business_df = business_df[business_df['License # - Flag']!='Incorrect']
business_df['License #'] = business_df['License #'].map(int)
business_df = business_df.drop_duplicates()
print("After Incorrect cleaning:"+str(len(business_df.index)))

#pick latest DBA/AKA name based on last Inspection date
business_df['Dt'] = pd.to_datetime(business_df['Inspection Date']).dt.date
business_dt_df = business_df.groupby(['License #']).agg(Dt=('Dt', np.max)).reset_index()
#print("Before cleaning:"+str(len(business_df.index)))
business_df = business_dt_df.merge(business_df, on=['License #','Dt'], how='inner')
business_df = business_df.drop_duplicates(subset=['License #'], keep='first')
print("After Deduplication cleaning:"+str(len(business_df.index)))

#pick latest location ID based on last Inspection date
#might not need here, since it would be in inspection

#export final clean data into a csv
business_df.to_csv('business.csv',index=False)
print('Business file is created.')


# In[56]:


#separate locations data
fldlist = ['Inspection ID','License # - Clean','Address - Clean','City - Clean','State',           'Zip','Latitude','Longitude','Location','Address - Flag','City - Flag','Location - Flag']
renfldlist = ['Inspection ID','License #','Address','City','State','Zip','Latitude','Longitude','Location',             'Address - Flag','City - Flag','Location - Flag']
locations_df = clean_df
locations_df = locations_df[fldlist]
#standardize field names
counter = 0
for item in fldlist:
    locations_df = locations_df.rename(columns={item: renfldlist[counter]})
    counter += 1

locations_df['Address'] = locations_df['Address'].fillna('')
locations_df['City'] = locations_df['City'].fillna('')
locations_df['Location'] = locations_df['Location'].fillna('-,-')
locations_df['Zip'] = locations_df['Zip'].fillna(0)
locations_df['Zip'] = locations_df['Zip'].map(int)
locations_df.loc[(locations_df['City']=='') & (locations_df['Zip']>0), 'City'] = 'CHICAGO'
locations_df.loc[(locations_df['City']=='CHICAGO') & (locations_df['Address']=='2324 N FREMONT ST'), 'Zip'] = 60614
locations_df.loc[(locations_df['City']=='CHICAGO') & (locations_df['Address']=='7545 N PAULINA ST'), 'Zip'] = 60626
locations_df.loc[(locations_df['City']=='BRIDEVIEW') & (locations_df['Address']=='7451 W 100TH ST'), 'Zip'] = 60455

locations_df.loc[locations_df['Location']=='41.90376892189224, -87.62853223878038', 'Address'] = '1165 North State Street'
locations_df.loc[locations_df['Location']=='41.775402337592375, -87.72282206289516', 'Address'] = '6450 South Pulaski Road'
locations_df.loc[locations_df['Location']=='41.87828615621557, -87.62780446623054', 'Address'] = '10 West Jackson Boulevard'
locations_df.loc[locations_df['Location']=='41.88406738126699, -87.63373557888185', 'Address'] = '181 West Randolph Street'
locations_df.loc[locations_df['Location']=='41.92118550519079, -87.6640136808923', 'Address'] = '2170 North Clybourn Avenue'
locations_df.loc[locations_df['Location']=='41.937929647019295, -87.65389286931712', 'Address'] = '3055 North Sheffield Avenue'
locations_df.loc[locations_df['Location']=='41.94915322312433, -87.64939586983472', 'Address'] = 'West Waveland Avenue'
locations_df.loc[locations_df['Location']=='41.69066950675008, -87.6085186509516', 'Address'] = '11208 S St Lawrence Avenue'
locations_df.loc[locations_df['Location']=='41.99020232648958, -87.71486611653422', 'Address'] = '3419 West Peterson Avenue'
locations_df.loc[locations_df['Location']=='41.92859664532255, -87.65338817338453', 'Address'] = '2574 North Lincoln Avenue'
locations_df.loc[locations_df['Location']=='41.97580062815588, -87.71349867231145', 'Address'] = '5205-5209 North Kimball Avenue'
locations_df.loc[locations_df['Location']=='41.91716536920397, -87.63620087405286', 'Address'] = '1919 North Lincoln Park West'
locations_df.loc[locations_df['Location']=='41.75905514352224, -87.57025265057769', 'Address'] = '2224 East 75th Street'
locations_df.loc[locations_df['Location']=='41.850453739981155, -87.62389126353149', 'Address'] = '2328 South Michigan Avenue'
locations_df.loc[locations_df['Location']=='41.971216840373906, -87.65958204538089', 'Address'] = '4845-4881 North Broadway Street'
locations_df.loc[locations_df['Location']=='41.87739707385008, -87.63504341455305', 'Address'] = '321 South Franklin Street'
locations_df.loc[locations_df['Location']=='41.8907467911109, -87.62851094403574', 'Address'] = '15, West Illinois Street'
locations_df.loc[locations_df['Location']=='41.89650357363852, -87.6327844082446', 'Address'] = 'West Chicago Avenue - River North'
locations_df.loc[locations_df['Location']=='41.75103049992091, -87.61364868855419', 'Address'] = '433 East 79th Street'
locations_df.loc[locations_df['Location']=='41.85104667463312, -87.62209308455373', 'Address'] = '1 Mccormick Place'
locations_df.loc[locations_df['Location']=='41.862628294037634, -87.61503109411332', 'Address'] = '1502 South Special Olympics Drive'
locations_df.loc[locations_df['Location']=='41.86580003172552, -87.67607360607634', 'Address'] = '1956 West Washburne Avenue'
locations_df.loc[locations_df['Location']=='41.96586490126624, -87.69387055820421', 'Address'] = '2608 West Eastwood Avenue'
locations_df.loc[locations_df['Location']=='41.89631758778245, -87.63584025366825', 'Address'] = '750 North Franklin Street'
locations_df.loc[locations_df['Location']=='41.948004550829744, -87.66418623070139', 'Address'] = '3636 N Southport Ave'
locations_df.loc[locations_df['Location']=='41.923575855788215, -87.78498537215225', 'Address'] = '6349 W Fullerton Ave'
locations_df.loc[locations_df['Location']=='41.93310552130911, -87.64530294150725', 'Address'] = '2808 N Clark St'
locations_df.loc[locations_df['Location']=='41.958548345644644, -87.78691898876937', 'Address'] = '4305 N Narragansett Ave'
locations_df.loc[locations_df['Location']=='41.96521193313759, -87.66326005651248', 'Address'] = '1325 W Wilson Ave'
locations_df.loc[locations_df['Location']=='41.968490719713, -87.65981645066375', 'Address'] = '4744 N Broadway St'
locations_df.loc[locations_df['Location']=='41.77896336682326, -87.63516942804449', 'Address'] = '6350 S Stewart Ave'
locations_df.loc[locations_df['Location']=='41.7515920243175, -87.56860603613539', 'Address'] = '2301 E 79th St'
locations_df.loc[locations_df['Location']=='41.85155346052472, -87.715059286164', 'Address'] = '3601 W Cermak Rd'

locations_df.loc[locations_df['Location']=='41.90376892189224, -87.62853223878038', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.775402337592375, -87.72282206289516', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.87828615621557, -87.62780446623054', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.88406738126699, -87.63373557888185', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.92118550519079, -87.6640136808923', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.937929647019295, -87.65389286931712', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.94915322312433, -87.64939586983472', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.69066950675008, -87.6085186509516', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.99020232648958, -87.71486611653422', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.92859664532255, -87.65338817338453', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.97580062815588, -87.71349867231145', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.91716536920397, -87.63620087405286', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.75905514352224, -87.57025265057769', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.850453739981155, -87.62389126353149', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.971216840373906, -87.65958204538089', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.87739707385008, -87.63504341455305', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.8907467911109, -87.62851094403574', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.89650357363852, -87.6327844082446', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.75103049992091, -87.61364868855419', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.85104667463312, -87.62209308455373', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.862628294037634, -87.61503109411332', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.86580003172552, -87.67607360607634', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.96586490126624, -87.69387055820421', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.89631758778245, -87.63584025366825', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.948004550829744, -87.66418623070139', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.923575855788215, -87.78498537215225', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.93310552130911, -87.64530294150725', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.958548345644644, -87.78691898876937', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.96521193313759, -87.66326005651248', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.968490719713, -87.65981645066375', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.77896336682326, -87.63516942804449', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.7515920243175, -87.56860603613539', 'City'] = 'Chicago'
locations_df.loc[locations_df['Location']=='41.85155346052472, -87.715059286164', 'City'] = 'Chicago'

locations_df.loc[locations_df['Location']=='41.90376892189224, -87.62853223878038', 'Zip'] = 60610
locations_df.loc[locations_df['Location']=='41.775402337592375, -87.72282206289516', 'Zip'] = 60629
locations_df.loc[locations_df['Location']=='41.87828615621557, -87.62780446623054', 'Zip'] = 60604
locations_df.loc[locations_df['Location']=='41.88406738126699, -87.63373557888185', 'Zip'] = 60602
locations_df.loc[locations_df['Location']=='41.92118550519079, -87.6640136808923', 'Zip'] = 60614
locations_df.loc[locations_df['Location']=='41.937929647019295, -87.65389286931712', 'Zip'] = 60657
locations_df.loc[locations_df['Location']=='41.94915322312433, -87.64939586983472', 'Zip'] = 60613
locations_df.loc[locations_df['Location']=='41.69066950675008, -87.6085186509516', 'Zip'] = 60628
locations_df.loc[locations_df['Location']=='41.99020232648958, -87.71486611653422', 'Zip'] = 60659
locations_df.loc[locations_df['Location']=='41.92859664532255, -87.65338817338453', 'Zip'] = 60614
locations_df.loc[locations_df['Location']=='41.97580062815588, -87.71349867231145', 'Zip'] = 60625
locations_df.loc[locations_df['Location']=='41.91716536920397, -87.63620087405286', 'Zip'] = 60614
locations_df.loc[locations_df['Location']=='41.75905514352224, -87.57025265057769', 'Zip'] = 60649
locations_df.loc[locations_df['Location']=='41.850453739981155, -87.62389126353149', 'Zip'] = 60616
locations_df.loc[locations_df['Location']=='41.971216840373906, -87.65958204538089', 'Zip'] = 60640
locations_df.loc[locations_df['Location']=='41.87739707385008, -87.63504341455305', 'Zip'] = 60606
locations_df.loc[locations_df['Location']=='41.8907467911109, -87.62851094403574', 'Zip'] = 60654
locations_df.loc[locations_df['Location']=='41.89650357363852, -87.6327844082446', 'Zip'] = 60654
locations_df.loc[locations_df['Location']=='41.75103049992091, -87.61364868855419', 'Zip'] = 60619
locations_df.loc[locations_df['Location']=='41.85104667463312, -87.62209308455373', 'Zip'] = 60616
locations_df.loc[locations_df['Location']=='41.862628294037634, -87.61503109411332', 'Zip'] = 60605
locations_df.loc[locations_df['Location']=='41.86580003172552, -87.67607360607634', 'Zip'] = 60608
locations_df.loc[locations_df['Location']=='41.96586490126624, -87.69387055820421', 'Zip'] = 60625
locations_df.loc[locations_df['Location']=='41.89631758778245, -87.63584025366825', 'Zip'] = 60654
locations_df.loc[locations_df['Location']=='41.948004550829744, -87.66418623070139', 'Zip'] = 60613
locations_df.loc[locations_df['Location']=='41.923575855788215, -87.78498537215225', 'Zip'] = 60639
locations_df.loc[locations_df['Location']=='41.93310552130911, -87.64530294150725', 'Zip'] = 60657
locations_df.loc[locations_df['Location']=='41.958548345644644, -87.78691898876937', 'Zip'] = 60634
locations_df.loc[locations_df['Location']=='41.96521193313759, -87.66326005651248', 'Zip'] = 60640
locations_df.loc[locations_df['Location']=='41.968490719713, -87.65981645066375', 'Zip'] = 60640
locations_df.loc[locations_df['Location']=='41.77896336682326, -87.63516942804449', 'Zip'] = 60621
locations_df.loc[locations_df['Location']=='41.7515920243175, -87.56860603613539', 'Zip'] = 60649
locations_df.loc[locations_df['Location']=='41.85155346052472, -87.715059286164', 'Zip'] = 60623

locations_df.loc[locations_df['Address']=='5235-5237 N BROARDWAY', 'City'] = 'Chicago'
locations_df.loc[locations_df['Address']=='5235-5237 N BROARDWAY', 'Zip'] = 60640
locations_df.loc[locations_df['Address']=='5235-5237 N BROARDWAY', 'Address'] = '5235 N BROARDWAY'

locations_df.loc[locations_df['Address']=='1332 W DRIVING PARK ROAD BSMT', 'City'] = 'Wheaton'
locations_df.loc[locations_df['Address']=='1332 W DRIVING PARK ROAD BSMT', 'Zip'] = 60187
locations_df.loc[locations_df['Address']=='1332 W DRIVING PARK ROAD BSMT', 'Address'] = '1332 DRIVING PARK ROAD'

#locations_df.head(2)

locations_df['Loc'] = locations_df['Address'] + '-' + locations_df['City'] + '-' + locations_df['State'] + '-' + locations_df['Zip'].map(str)
locations_df['Loc'] = locations_df['Loc'].str.upper()

print('Inspection data:'+str(len(locations_df.index)))
loc_df = locations_df[['Loc']]
loc_df = loc_df.drop_duplicates()
loc_df = loc_df.sort_values(by='Loc', ascending=True)
loc_df.insert(0, 'Location ID', range(0, 0 + len(loc_df)))
inspc_loc_df = loc_df.merge(locations_df, on=['Loc'], how='right')
#inspc_loc_df.head(2)
print('Inspection data after creating location id:'+str(len(locations_df.index)))

locations_df = inspc_loc_df[['Location ID','Address','City','State','Zip','Latitude','Longitude','Location']]
locations_df = locations_df.drop_duplicates(subset=['Location ID'], keep='first')
print('Location data:'+str(len(locations_df.index)))

#export final clean data into a csv
locations_df.to_csv('locations.csv',index=False)
print('Locations file is created.')

inspc_loc_df = inspc_loc_df[['Inspection ID','Location ID']].drop_duplicates()
print('Inspection Location data:'+str(len(inspc_loc_df.index)))


# In[57]:


#separate inspections data
fldlist = ['License # - Clean','Inspection ID','Inspection Date','Inspection Type - Clean','Risk Category - Clean','Risk - Flag','Results','License # - Flag']
renfldlist = ['License #','Inspection ID','Inspection Date','Inspection Type','Risk Category','Risk - Flag','Results','License # - Flag']
inspection_df = clean_df
inspection_df = inspection_df[fldlist]
#standardize field names
counter = 0
for item in fldlist:
    inspection_df = inspection_df.rename(columns={item: renfldlist[counter]})
    counter += 1

print("Before cleaning:"+str(len(inspection_df.index)))
inspection_df = inspection_df[inspection_df['License # - Flag']!='Incorrect']
inspection_df = inspection_df[inspection_df['Risk - Flag']!='Incorrect']
inspection_df['License #'] = inspection_df['License #'].map(int)

inspection_df = inspection_df.merge(business_df[['License #']], on=['License #'], how='inner')
print("After cleaning:"+str(len(inspection_df.index)))
inspection_df = inspection_df.drop(columns=['Risk - Flag','License # - Flag'])

inspection_df = inspection_df.merge(inspc_loc_df, on=['Inspection ID'], how='left')
print("After brining location ID:"+str(len(inspection_df.index)))

#inspection_df.head(2)
#export final clean data into a csv
inspection_df.to_csv('inspections.csv',index=False)
print('Inspection file is created.')


# In[82]:


#separate violations data
#violation id, inspection id, violation code (1-44,70), violation flag\
#violation order (1-23), violation text (whole text), violation type(critical, serious, other)
fldlist = ['Inspection ID','Results',           'Violations 1','Violations 2','Violations 3','Violations 4','Violations 5','Violations 6',           'Violations 7','Violations 8','Violations 9','Violations 10','Violations 11','Violations 12',           'Violations 13','Violations 14','Violations 15','Violations 16','Violations 17','Violations 18',           'Violations 19','Violations 20','Violations 21','Violations 22','Violations 23']
renfldlist = ['Inspection ID','Results',             'Violation 1','Violation 2','Violation 3','Violation 4','Violation 5','Violation 6',              'Violation 7','Violation 8','Violation 9','Violation 10','Violation 11','Violation 12',              'Violation 13','Violation 14','Violation 15','Violation 16','Violation 17','Violation 18',              'Violation 19','Violation 20','Violation 21','Violation 22','Violation 23']
violations_df = clean_df
violations_df = violations_df[fldlist]
#standardize field names
counter = 0
for item in fldlist:
    violations_df = violations_df.rename(columns={item: renfldlist[counter]})
    counter += 1

#violations_df = violations_df.loc[violations_df['Inspection ID']==120273]
violations_df.head(2)
violations_df = pd.melt(violations_df, id_vars=['Inspection ID','Results'], value_vars=['Violation 1','Violation 2',              'Violation 3','Violation 4','Violation 5','Violation 6',              'Violation 7','Violation 8','Violation 9','Violation 10','Violation 11','Violation 12',              'Violation 13','Violation 14','Violation 15','Violation 16','Violation 17','Violation 18',              'Violation 19','Violation 20','Violation 21','Violation 22','Violation 23'])
violations_df = violations_df.rename(columns={'variable': 'Violation Order'})
violations_df = violations_df.rename(columns={'value': 'Violation Text'})
violations_df['Violation Order'] = violations_df['Violation Order'].fillna('')
violations_df['Violation Text'] = violations_df['Violation Text'].fillna('')

print("Before cleaning:"+str(len(violations_df.index)))
violations_df = violations_df.loc[violations_df['Violation Text']!='']
print("After first cleaning:"+str(len(violations_df.index)))
violations_df.insert(0, 'Violation ID', range(0, 0 + len(violations_df)))
violations_df['Violation Code'] = violations_df['Violation Text'].str[:3].str.replace('.','',regex=False).map(int)

violations_df['Violation Type'] = 'Other'
violations_df.loc[(violations_df['Violation Code']>=1) & (violations_df['Violation Code']<=14), 'Violation Type'] = 'Critical'
violations_df.loc[(violations_df['Violation Code']>=15) & (violations_df['Violation Code']<=29), 'Violation Type'] = 'Serious'

violations_df['Violation Flag'] = 'Correct'
violations_df.loc[(violations_df['Results']=='Pass') & (violations_df['Violation Type']!='Other'), 'Violation Flag'] = 'Incorrect'
violations_df = violations_df.loc[violations_df['Violation Flag']=='Correct']
print("After cleaning:"+str(len(violations_df.index)))
#violations_df.head(2)

#export final clean data into a csv
violations_df.to_csv('violations.csv',index=False)
print('Violations file is created.')


# In[ ]:


#validation and count check scripts start from here


# In[62]:


chk = clean_df.loc[clean_df['License # - Flag']=='Incorrect']#.drop_duplicates()
print(len(chk.index))


# In[63]:


chk = clean_df.loc[clean_df['Risk - Flag']=='Incorrect']#.drop_duplicates()
print(len(chk.index))


# In[66]:


chk = clean_df.loc[clean_df['Zip'].isnull()]#.drop_duplicates()
print(len(chk.index))


# In[70]:


chk = clean_df.loc[clean_df['Zip'].isnull()]#.drop_duplicates()
print(len(chk.index))


# In[71]:


locations_df = clean_df
locations_df['Loc'] = locations_df['Address'] + '-' + locations_df['City'] + '-' + locations_df['State'] + '-' + locations_df['Zip'].map(str)
locations_df['Loc'] = locations_df['Loc'].str.upper()
chk = locations_df[['Loc']].drop_duplicates()
print(len(chk.index))


# In[38]:


# functional dependency <License # -> DBA Name>
chk = business_df[['License #','DBA Name']]
chk = chk.drop_duplicates()
chk1 = chk.groupby("License #", as_index=False)["DBA Name"].count()
chk1['DBA Name'] = chk1['DBA Name'].astype(int)
chk1 = chk1.sort_values(by='DBA Name', ascending=False)
chk2 = chk1[chk1['DBA Name']>1]['License #'].values.tolist()
chk3 = clean_df[clean_df['License #'].isin(chk2)][['License #','DBA Name','Inspection ID']]#.drop_duplicates()
chk4 = chk3.groupby(["License #",'DBA Name'], as_index=False)["Inspection ID"].count()
#chk4['host'] = chk4['License #'].map(str) + ', ' + chk4['host_name']
#chk5 = dict(zip(chk4['host'], chk4['id']))
l1 = chk4['License #'].values.tolist()
l2 = chk4['DBA Name'].values.tolist()
l3 = chk4['Inspection ID'].values.tolist()
chk5 = {k: v for k, v in zip(zip(l1,l2), l3)}
#print(len(chk5))
chk5


# In[ ]:





# In[59]:


#chk = locations_df.loc[locations_df['Zip']==0][['Zip','City','Address']].drop_duplicates()
chk = locations_df.loc[locations_df['Address']==''][['Location','City','Address','Zip']]
chk


# In[79]:


#check for invalid violations data
chk = violations_df.loc[(violations_df['Results']=='Pass') & (violations_df['Violation Type']!='Other')][['Inspection ID','Violation Type']].drop_duplicates()
chk = chk.groupby("Violation Type", as_index=False)["Inspection ID"].count()
#violations_df[['Results','Violation Type']].drop_duplicates()
#chk = chk.sort_values(by='Results', ascending=True)
chk


# In[61]:


# functional dependency <License # -> DBA Name>
chk = clean_df[['License #','DBA Name']]
chk = chk.drop_duplicates()
chk1 = chk.groupby("License #", as_index=False)["DBA Name"].count()
chk1['DBA Name'] = chk1['DBA Name'].astype(int)
chk1 = chk1.sort_values(by='DBA Name', ascending=False)
chk2 = chk1[chk1['DBA Name']>1]['License #'].values.tolist()
chk3 = clean_df[clean_df['License #'].isin(chk2)][['License #','DBA Name','Inspection ID']]#.drop_duplicates()
chk4 = chk3.groupby(["License #",'DBA Name'], as_index=False)["Inspection ID"].count()
#chk4['host'] = chk4['License #'].map(str) + ', ' + chk4['host_name']
#chk5 = dict(zip(chk4['host'], chk4['id']))
l1 = chk4['License #'].values.tolist()
l2 = chk4['DBA Name'].values.tolist()
l3 = chk4['Inspection ID'].values.tolist()
chk5 = {k: v for k, v in zip(zip(l1,l2), l3)}
print(len(chk5))


# In[ ]:


print('<License # -> DBA Name> Functional Dependency Violations: '+str(len(chk5)))
print('Total Number of Records with <License # -> DBA Name> Functional Dependency: '+str(sum(chk5.values())))


# In[ ]:


raw_df[["Results", "Risk", "Zip"]].describe()


# In[91]:


#chk1 = business_df.groupby("DBA Name", as_index=False)["License #"].count()
#chk1['DBA Name'] = chk1['DBA Name'].astype(int)
#chk1 = chk1.sort_values(by='DBA Name', ascending=False)
chk2 = clean_df[chk1['DBA Name']>1]['Inspection ID'].values.tolist()
print(len(chk1.index))


# In[ ]:


chk1 = raw_df[["Results","Violations"]]
chk1['Violation Code'] = chk1['Violations'].str[:2]
chk1['Violation Code'] = chk1['Violation Code'].fillna('0').str.strip()
chk1['Violation Code1'] = chk1['Violation Code'].str.replace('.','').map(int)

chk1 = chk1.drop(columns=['Violations','Violation Code'])
chk1 = chk1.drop_duplicates()
chk1 = chk1[(chk1['Results']=='Pass') & (chk1['Violation Code1'] > 29)]
chk1 = chk1.sort_values(by=["Results","Violation Code1"], ascending=False)
chk1


# In[ ]:


chk2 = chk1[['Results']].drop_duplicates()
chk2


# In[4]:


chk = clean_df[clean_df['Inspection ID'].isnull()]
print(len(chk.index))


# In[ ]:




