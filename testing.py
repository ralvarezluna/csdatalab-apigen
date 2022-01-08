import re
joined_sdgs = "SDG_11,SDG_16,SDG_3"
print(re.findall(r'\d+', joined_sdgs))
#print([int(s) for s in joined_sdgs.split() if s.isdigit()])