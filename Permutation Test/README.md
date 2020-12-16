# Do employee referrals last longer on the Job?

For this notebook, I will be exploring the question of "whether employee referrals tend to last longer on the job than non-employee referrals". The data that I am working with has 1644 observations of 'hourly' employee turnover data from a 2 year period of employees who were either referred by other employees or not.

Each observation is labeled either as an employee referral (1) or non-referral (0). The attributes I will be measuring against are whether an employee has hit or missed a milestone in their tenure at 30 days, 60 days, and 90 days. If an employee has not been hired long enough to hit a milestone, then that milestone will be a null value, otherwise it is counted as 1 for successfully hitting the milestone and 0 for failing to hit the milestone.

My null hypothesis is that there is NO difference between tenure of referrals vs non-referrals.

To answer these questions, I will be using permutation tests which produce histograms that test statistical significance of the initial observations. A permutation test will randomly sample and reallocate the groups 1000 times to test against the actual observation. This will help to show whether the initial observations fall within the distribution that chance has randomly produced. If the actual or "observed difference" falls outside of most of the permutation distribution, then we can conclude that "chance is not responsible" (Bruce et all, 2020). 

Using histograms as a visual aid really has helped me to better understand the meaning behind the term "statistically significant". I was inspired to create this project after reading about it and seeing it demonstrated in the book **Practical Statistics for Data Scientists** (Bruce et all, 2020). 

<br>
<br>
Reference:<br>
*Bruce, P. C., Bruce, A. G., &amp; Gedeck, P. (2020). Practical statistics for data scientists: 50+ essential concepts using R and Python. Sebastopol, CA: O'Reilly.*
