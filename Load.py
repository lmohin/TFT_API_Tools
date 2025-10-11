import json
from quickstart import *
import asyncio

async def Load(page):
    if page == 1:
        PageName = "Liste Joueurs"
    elif page == 2:
        PageName = "Phase 1 : Rondes Suisse (Samedi)"
    elif page == 3:
        PageName = "Units Stats"
    else :
        return
    with open(f"page{page}.json", "r") as final:
        Values = json.load(final)
    write_cells(f"{PageName}!A1", Values)
    
if __name__ == "__main__":
    asyncio.run(Load(1))
