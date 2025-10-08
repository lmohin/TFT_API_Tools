import json
from quickstart import *
import asyncio

# List of lists
data = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]

# Convert into JSON
# File name is mydata.json
with open("mydata.json", "w") as final:
    json.dump(data, final)

with open("mydata.json", "r") as final:
    test = json.load(final)
    print(test)
    
async def Save(page):
    if page == 1:
        PageName = "Liste Joueurs"
    elif page == 2:
        PageName = "Phase 1 : Rondes Suisse (Samedi)"
    elif page == 3:
        PageName = "Units Stats"
    else :
        return
    values = get_cell_value(f"{PageName}!A:ZZ")
    with open(f"page{page}.json", "w") as final:
        json.dump(values, final)


if __name__ == "__main__":
    asyncio.run(Save(1))
