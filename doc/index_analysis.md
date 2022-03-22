SQL Query 1:

Index 1: We created an index on the first ten characters of the group name field in the group table. 
This caused the cost of filtering by group name to decrease from 50.99 to 5.66 because it had to scan fewer rows
and the nested inner join also became faster because it had fewer rows to scan and the cost had decreased. 

Index 2: We created an index on the first character of the group name field in the group table. 
This caused the cost of filtering by group name to only scan 66 rows instead of 499 and decrease the cost from 50.99 to 29.96. 
This index is not as efficient because it starts with the first character and there are multiple courses that start with “C” other than CS for our query. 

Index 3: We created an index on the first 3 characters of the group name field in the group table. 
This caused the cost of filtering by group name to decrease from 50.99 to 5.66 because it had to scan fewer rows
and the nested inner join also became faster because it had fewer rows to scan and the cost had decreased. This index had the same outcome as the first index we created with an index on the first ten characters of the group name field in the group table because the filter was only looking for the first 3 characters of the group name thus an index with more then 3 characters will be the same. 
