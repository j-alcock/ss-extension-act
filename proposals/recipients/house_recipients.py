"""
US House of Representatives Recipient List — 119th Congress (2025-2027)
Maps each representative to their stance classification and proposal assignment.

CLASSIFICATION METHODOLOGY:
  RECEPTIVE: Likely to support SS expansion + billionaire taxation
  SKEPTICAL: Open to SS solvency reform but cautious on M2M tax / scale
  HOSTILE: Opposed to new taxes and/or expanded benefits

PROPOSAL ASSIGNMENTS:
  RECEPTIVE → Letter (receptive) + Executive Brief + Policy Brief
  SKEPTICAL → Letter (skeptical) + Executive Brief + Fiscal Summary
  HOSTILE   → Letter (hostile) + Executive Brief (solvency-focused)

Data compiled from: house.gov, committee pages, caucus memberships,
voting records, public statements. See caveats at bottom regarding
data freshness (based on early-mid 2025 known composition).

CONTACT INFORMATION:
  Full contact details (DC offices, phone numbers, websites, district offices)
  are in house_contact_directory.py — import and cross-reference by name.

  Usage:
    from proposals.recipients.house_contact_directory import (
        HOUSE_CONTACTS, format_contact_block, get_contacts_by_district
    )
    contact = HOUSE_CONTACTS['John Larson']
    print(format_contact_block('John Larson'))
"""

# ═══════════════════════════════════════════════════════════════════════
#  HOUSE ROSTER — 435 MEMBERS
# ═══════════════════════════════════════════════════════════════════════

REPRESENTATIVES = [
    # ── ALABAMA (7 districts: 6R, 1D) ────────────────────────────────
    {'name': 'Jerry Carl', 'district': 'AL-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Barry Moore', 'district': 'AL-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Mike Rogers', 'district': 'AL-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Armed Services'], 'notes': 'Armed Services Chair'},
    {'name': 'Robert Aderholt', 'district': 'AL-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Dale Strong', 'district': 'AL-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Gary Palmer', 'district': 'AL-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': ''},
    {'name': 'Terri Sewell', 'district': 'AL-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; CBC'},

    # ── ALASKA (1 at-large: R) ───────────────────────────────────────
    {'name': 'Mary Peltola', 'district': 'AK-AL', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Lost 2024 — replaced by Nick Begich (R) HOSTILE'},

    # ── ARIZONA (9 districts) ────────────────────────────────────────
    {'name': 'David Schweikert', 'district': 'AZ-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Eli Crane', 'district': 'AZ-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Raul Grijalva', 'district': 'AZ-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'May have retired; replaced by D'},
    {'name': 'Greg Stanton', 'district': 'AZ-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Andy Biggs', 'district': 'AZ-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary'], 'notes': 'Freedom Caucus'},
    {'name': 'Juan Ciscomani', 'district': 'AZ-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Ruben Gallego', 'district': 'AZ-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Left for Senate; replaced by D'},
    {'name': 'Debbie Lesko', 'district': 'AZ-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Paul Gosar', 'district': 'AZ-9', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},

    # ── ARKANSAS (4 districts: 4R) ───────────────────────────────────
    {'name': 'Rick Crawford', 'district': 'AR-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'French Hill', 'district': 'AR-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': 'Financial Services Chair'},
    {'name': 'Steve Womack', 'district': 'AR-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Bruce Westerman', 'district': 'AR-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Natural Resources'], 'notes': 'Natural Resources Chair'},

    # ── CALIFORNIA (52 districts) ────────────────────────────────────
    {'name': 'Doug LaMalfa', 'district': 'CA-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Jared Huffman', 'district': 'CA-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'Kevin Kiley', 'district': 'CA-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Mike Thompson', 'district': 'CA-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Tom McClintock', 'district': 'CA-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Ami Bera', 'district': 'CA-6', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Doris Matsui', 'district': 'CA-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': ''},
    {'name': 'John Garamendi', 'district': 'CA-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services'], 'notes': ''},
    {'name': 'Josh Harder', 'district': 'CA-9', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D; competitive district'},
    {'name': 'Mark DeSaulnier', 'district': 'CA-10', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Nancy Pelosi', 'district': 'CA-11', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Former Speaker; enormous influence'},
    {'name': 'Lateefah Simon', 'district': 'CA-12', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New member; Progressive'},
    {'name': 'John Duarte', 'district': 'CA-13', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'May have lost 2024; swing district'},
    {'name': 'Eric Swalwell', 'district': 'CA-14', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Kevin Mullin', 'district': 'CA-15', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Anna Eshoo', 'district': 'CA-16', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Retired; replaced by D (Sam Liccardo)'},
    {'name': 'Ro Khanna', 'district': 'CA-17', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive; tech/labor crossover'},
    {'name': 'Zoe Lofgren', 'district': 'CA-18', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Jimmy Panetta', 'district': 'CA-19', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Kevin McCarthy', 'district': 'CA-20', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Resigned; replaced by Vince Fong (R)'},
    {'name': 'Jim Costa', 'district': 'CA-21', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Blue Dog; moderate D'},
    {'name': 'David Valadao', 'district': 'CA-22', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': 'Moderate R'},
    {'name': 'Jay Obernolte', 'district': 'CA-23', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Salud Carbajal', 'district': 'CA-24', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Raul Ruiz', 'district': 'CA-25', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': 'CHC Chair'},
    {'name': 'Julia Brownley', 'district': 'CA-26', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Mike Garcia', 'district': 'CA-27', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'May have lost 2024; swing district'},
    {'name': 'Judy Chu', 'district': 'CA-28', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; Progressive'},
    {'name': 'Tony Cardenas', 'district': 'CA-29', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Adam Schiff', 'district': 'CA-30', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Left for Senate; replaced by D'},
    {'name': 'Grace Napolitano', 'district': 'CA-31', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Retired; replaced by D'},
    {'name': 'Brad Sherman', 'district': 'CA-32', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Financial Services'},
    {'name': 'Pete Aguilar', 'district': 'CA-33', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'House Dem Caucus Chair'},
    {'name': 'Jimmy Gomez', 'district': 'CA-34', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; Progressive'},
    {'name': 'Norma Torres', 'district': 'CA-35', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Ted Lieu', 'district': 'CA-36', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Sydney Kamlager-Dove', 'district': 'CA-37', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Linda Sanchez', 'district': 'CA-38', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Mark Takano', 'district': 'CA-39', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Veterans Affairs'], 'notes': 'Progressive'},
    {'name': 'Young Kim', 'district': 'CA-40', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Ken Calvert', 'district': 'CA-41', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Robert Garcia', 'district': 'CA-42', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'Maxine Waters', 'district': 'CA-43', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Financial Services Ranking'},
    {'name': 'Nanette Barragan', 'district': 'CA-44', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': 'CHC'},
    {'name': 'Michelle Steel', 'district': 'CA-45', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Lou Correa', 'district': 'CA-46', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Katie Porter', 'district': 'CA-47', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Ran for Senate; seat may have flipped; progressive champion'},
    {'name': 'Darrell Issa', 'district': 'CA-48', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Mike Levin', 'district': 'CA-49', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Scott Peters', 'district': 'CA-50', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D; New Dem Coalition'},
    {'name': 'Sara Jacobs', 'district': 'CA-51', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services'], 'notes': ''},
    {'name': 'Juan Vargas', 'district': 'CA-52', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': ''},

    # ── COLORADO (8 districts) ───────────────────────────────────────
    {'name': 'Diana DeGette', 'district': 'CO-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': ''},
    {'name': 'Joe Neguse', 'district': 'CO-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': 'Asst Dem Leader'},
    {'name': 'Jeff Crank', 'district': 'CO-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New member; replaced Boebert'},
    {'name': 'Lauren Boebert', 'district': 'CO-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Switched districts; Freedom Caucus'},
    {'name': 'Jeff Hurd', 'district': 'CO-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New member'},
    {'name': 'Jason Crow', 'district': 'CO-6', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Armed Services'], 'notes': 'Moderate D'},
    {'name': 'Brittany Pettersen', 'district': 'CO-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Yadira Caraveo', 'district': 'CO-8', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D; swing district; may have lost 2024'},

    # ── CONNECTICUT (5 districts: 5D) ────────────────────────────────
    {'name': 'John Larson', 'district': 'CT-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'SS 2100 Act sponsor; TOP CHAMPION'},
    {'name': 'Joe Courtney', 'district': 'CT-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services'], 'notes': ''},
    {'name': 'Rosa DeLauro', 'district': 'CT-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': 'Appropriations Ranking; CTC champion'},
    {'name': 'Jim Himes', 'district': 'CT-4', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Financial Services'], 'notes': 'New Dem Coalition; Financial Services'},
    {'name': 'Jahana Hayes', 'district': 'CT-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},

    # ── DELAWARE (1 at-large: D) ─────────────────────────────────────
    {'name': 'Sarah McBride', 'district': 'DE-AL', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New member'},

    # ── FLORIDA (28 districts) ───────────────────────────────────────
    {'name': 'Matt Gaetz', 'district': 'FL-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Resigned; replaced by R in special election'},
    {'name': 'Neal Dunn', 'district': 'FL-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Energy and Commerce'], 'notes': ''},
    {'name': 'Kat Cammack', 'district': 'FL-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Aaron Bean', 'district': 'FL-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Education and Workforce'], 'notes': ''},
    {'name': 'John Rutherford', 'district': 'FL-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Michael Waltz', 'district': 'FL-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Left for NSA; replaced by R'},
    {'name': 'Cory Mills', 'district': 'FL-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Bill Posey', 'district': 'FL-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Darren Soto', 'district': 'FL-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': 'CHC'},
    {'name': 'Maxwell Frost', 'district': 'FL-10', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive; youngest member'},
    {'name': 'Daniel Webster', 'district': 'FL-11', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Gus Bilirakis', 'district': 'FL-12', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Energy and Commerce'], 'notes': ''},
    {'name': 'Anna Paulina Luna', 'district': 'FL-13', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Kathy Castor', 'district': 'FL-14', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': ''},
    {'name': 'Laurel Lee', 'district': 'FL-15', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Vern Buchanan', 'district': 'FL-16', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Greg Steube', 'district': 'FL-17', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Scott Franklin', 'district': 'FL-18', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Byron Donalds', 'district': 'FL-19', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': 'Freedom Caucus'},
    {'name': 'Sheila Cherfilus-McCormick', 'district': 'FL-20', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC; supports UBI concepts'},
    {'name': 'Brian Mast', 'district': 'FL-21', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Lois Frankel', 'district': 'FL-22', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Jared Moskowitz', 'district': 'FL-23', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Frederica Wilson', 'district': 'FL-24', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Debbie Wasserman Schultz', 'district': 'FL-25', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Mario Diaz-Balart', 'district': 'FL-26', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Maria Elvira Salazar', 'district': 'FL-27', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Carlos Gimenez', 'district': 'FL-28', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── GEORGIA (14 districts) ───────────────────────────────────────
    {'name': 'Buddy Carter', 'district': 'GA-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Sanford Bishop', 'district': 'GA-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': 'CBC'},
    {'name': 'Drew Ferguson', 'district': 'GA-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Hank Johnson', 'district': 'GA-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': 'CBC; Progressive'},
    {'name': 'Nikema Williams', 'district': 'GA-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Rich McCormick', 'district': 'GA-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Lucy McBath', 'district': 'GA-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Austin Scott', 'district': 'GA-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Andrew Clyde', 'district': 'GA-9', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': 'Freedom Caucus'},
    {'name': 'Mike Collins', 'district': 'GA-10', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Barry Loudermilk', 'district': 'GA-11', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Rick Allen', 'district': 'GA-12', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'David Scott', 'district': 'GA-13', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Marjorie Taylor Greene', 'district': 'GA-14', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},

    # ── HAWAII (2 districts: 2D) ─────────────────────────────────────
    {'name': 'Ed Case', 'district': 'HI-1', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Appropriations'], 'notes': 'Moderate D'},
    {'name': 'Jill Tokuda', 'district': 'HI-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},

    # ── IDAHO (2 districts: 2R) ──────────────────────────────────────
    {'name': 'Russ Fulcher', 'district': 'ID-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Mike Simpson', 'district': 'ID-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},

    # ── ILLINOIS (17 districts) ──────────────────────────────────────
    {'name': 'Jonathan Jackson', 'district': 'IL-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Robin Kelly', 'district': 'IL-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': 'CBC'},
    {'name': 'Delia Ramirez', 'district': 'IL-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'Jesus "Chuy" Garcia', 'district': 'IL-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Progressive'},
    {'name': 'Mike Quigley', 'district': 'IL-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Sean Casten', 'district': 'IL-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Danny Davis', 'district': 'IL-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; CBC'},
    {'name': 'Raja Krishnamoorthi', 'district': 'IL-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Jan Schakowsky', 'district': 'IL-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': 'Progressive'},
    {'name': 'Brad Schneider', 'district': 'IL-10', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; moderate D'},
    {'name': 'Bill Foster', 'district': 'IL-11', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Physicist; quantitative'},
    {'name': 'Mike Bost', 'district': 'IL-12', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Veterans Affairs'], 'notes': ''},
    {'name': 'Nikki Budzinski', 'district': 'IL-13', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Lauren Underwood', 'district': 'IL-14', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Mary Miller', 'district': 'IL-15', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Darin LaHood', 'district': 'IL-16', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Eric Sorensen', 'district': 'IL-17', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},

    # ── INDIANA (9 districts: 7R, 2D) ────────────────────────────────
    {'name': 'Frank Mrvan', 'district': 'IN-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Rudy Yakym', 'district': 'IN-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Budget'], 'notes': ''},
    {'name': 'Jim Banks', 'district': 'IN-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Left for Senate; replaced by R'},
    {'name': 'Jim Baird', 'district': 'IN-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Victoria Spartz', 'district': 'IN-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Greg Pence', 'district': 'IN-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Andre Carson', 'district': 'IN-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Mark Messmer', 'district': 'IN-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New member'},
    {'name': 'Erin Houchin', 'district': 'IN-9', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── IOWA (4 districts) ───────────────────────────────────────────
    {'name': 'Mariannette Miller-Meeks', 'district': 'IA-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Ashley Hinson', 'district': 'IA-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Zach Nunn', 'district': 'IA-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; may have lost 2024'},
    {'name': 'Randy Feenstra', 'district': 'IA-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},

    # ── KANSAS (4 districts: 3R, 1D) ─────────────────────────────────
    {'name': 'Tracey Mann', 'district': 'KS-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Jake LaTurner', 'district': 'KS-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Sharice Davids', 'district': 'KS-3', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D; New Dem Coalition'},
    {'name': 'Ron Estes', 'district': 'KS-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},

    # ── KENTUCKY (6 districts: 5R, 1D) ───────────────────────────────
    {'name': 'James Comer', 'district': 'KY-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Oversight'], 'notes': 'Oversight Chair'},
    {'name': 'Brett Guthrie', 'district': 'KY-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Energy and Commerce'], 'notes': 'Energy and Commerce Chair'},
    {'name': 'Morgan McGarvey', 'district': 'KY-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Thomas Massie', 'district': 'KY-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Libertarian-leaning'},
    {'name': 'Hal Rogers', 'district': 'KY-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': 'Dean of the House'},
    {'name': 'Andy Barr', 'district': 'KY-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},

    # ── LOUISIANA (6 districts: 5R, 1D) ──────────────────────────────
    {'name': 'Steve Scalise', 'district': 'LA-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'House Majority Leader'},
    {'name': 'Troy Carter', 'district': 'LA-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Clay Higgins', 'district': 'LA-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Mike Johnson', 'district': 'LA-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'SPEAKER OF THE HOUSE — critical gatekeeper'},
    {'name': 'Julia Letlow', 'district': 'LA-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Garret Graves', 'district': 'LA-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},

    # ── MAINE (2 districts) ──────────────────────────────────────────
    {'name': 'Chellie Pingree', 'district': 'ME-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': 'Progressive'},
    {'name': 'Jared Golden', 'district': 'ME-2', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Problem Solvers; very moderate D'},

    # ── MARYLAND (8 districts: 7D, 1R) ───────────────────────────────
    {'name': 'Andy Harris', 'district': 'MD-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Dutch Ruppersberger', 'district': 'MD-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Retired; replaced by D'},
    {'name': 'John Sarbanes', 'district': 'MD-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Retired; replaced by D'},
    {'name': 'Glenn Ivey', 'district': 'MD-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Steny Hoyer', 'district': 'MD-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Retired; replaced by D'},
    {'name': 'David Trone', 'district': 'MD-6', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Ran for Senate; replaced by D'},
    {'name': 'Kweisi Mfume', 'district': 'MD-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Jamie Raskin', 'district': 'MD-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': 'Judiciary Ranking; Progressive; champion potential'},

    # ── MASSACHUSETTS (9 districts: 9D) ──────────────────────────────
    {'name': 'Richard Neal', 'district': 'MA-1', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means Ranking Member; key gatekeeper'},
    {'name': 'Jim McGovern', 'district': 'MA-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Rules'], 'notes': 'Progressive'},
    {'name': 'Lori Trahan', 'district': 'MA-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Jake Auchincloss', 'district': 'MA-4', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Centrist D'},
    {'name': 'Katherine Clark', 'district': 'MA-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'House Minority Whip'},
    {'name': 'Seth Moulton', 'district': 'MA-6', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Ayanna Pressley', 'district': 'MA-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Progressive; CBC'},
    {'name': 'Stephen Lynch', 'district': 'MA-8', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Financial Services'], 'notes': 'Moderate-labor D'},
    {'name': 'Bill Keating', 'district': 'MA-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},

    # ── MICHIGAN (13 districts) ──────────────────────────────────────
    {'name': 'Jack Bergman', 'district': 'MI-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'John Moolenaar', 'district': 'MI-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Hillary Scholten', 'district': 'MI-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Bill Huizenga', 'district': 'MI-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Tim Walberg', 'district': 'MI-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Debbie Dingell', 'district': 'MI-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': 'Progressive'},
    {'name': 'Curtis Hertel', 'district': 'MI-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New member'},
    {'name': 'Kristen McDonald Rivet', 'district': 'MI-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New member; replaced Dan Kildee'},
    {'name': 'Lisa McClain', 'district': 'MI-9', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'John James', 'district': 'MI-10', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Haley Stevens', 'district': 'MI-11', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Rashida Tlaib', 'district': 'MI-12', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Progressive'},
    {'name': 'Shri Thanedar', 'district': 'MI-13', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},

    # ── MINNESOTA (8 districts) ──────────────────────────────────────
    {'name': 'Brad Finstad', 'district': 'MN-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Angie Craig', 'district': 'MN-2', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Kelly Morrison', 'district': 'MN-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New member; replaced Dean Phillips'},
    {'name': 'Betty McCollum', 'district': 'MN-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Ilhan Omar', 'district': 'MN-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive; CBC'},
    {'name': 'Tom Emmer', 'district': 'MN-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'House Majority Whip'},
    {'name': 'Michelle Fischbach', 'district': 'MN-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Pete Stauber', 'district': 'MN-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── MISSISSIPPI (4 districts: 3R, 1D) ────────────────────────────
    {'name': 'Trent Kelly', 'district': 'MS-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Bennie Thompson', 'district': 'MS-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Michael Guest', 'district': 'MS-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Mike Ezell', 'district': 'MS-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── MISSOURI (8 districts: 6R, 2D) ───────────────────────────────
    {'name': 'Wesley Bell', 'district': 'MO-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Replaced Cori Bush'},
    {'name': 'Ann Wagner', 'district': 'MO-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Blaine Luetkemeyer', 'district': 'MO-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Mark Alford', 'district': 'MO-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Emanuel Cleaver', 'district': 'MO-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Sam Graves', 'district': 'MO-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Eric Burlison', 'district': 'MO-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Jason Smith', 'district': 'MO-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'WAYS AND MEANS CHAIR — critical gatekeeper'},

    # ── MONTANA (2 districts: 2R) ────────────────────────────────────
    {'name': 'Ryan Zinke', 'district': 'MT-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Troy Downing', 'district': 'MT-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'May have replaced Rosendale'},

    # ── NEBRASKA (3 districts: 3R) ───────────────────────────────────
    {'name': 'Mike Flood', 'district': 'NE-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Don Bacon', 'district': 'NE-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Problem Solvers; most moderate NE Republican'},
    {'name': 'Adrian Smith', 'district': 'NE-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},

    # ── NEVADA (4 districts) ─────────────────────────────────────────
    {'name': 'Dina Titus', 'district': 'NV-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Mark Amodei', 'district': 'NV-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Susie Lee', 'district': 'NV-3', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Steven Horsford', 'district': 'NV-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; CBC'},

    # ── NEW HAMPSHIRE (2 districts: 2D) ──────────────────────────────
    {'name': 'Chris Pappas', 'district': 'NH-1', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Annie Kuster', 'district': 'NH-2', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Retired or may still serve; moderate D'},

    # ── NEW JERSEY (12 districts) ────────────────────────────────────
    {'name': 'Donald Norcross', 'district': 'NJ-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Jeff Van Drew', 'district': 'NJ-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Switched D to R'},
    {'name': 'Herb Conaway', 'district': 'NJ-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New; replaced Andy Kim (Senate)'},
    {'name': 'Chris Smith', 'district': 'NJ-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Josh Gottheimer', 'district': 'NJ-5', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Financial Services'], 'notes': 'Problem Solvers; may have left for Gov race'},
    {'name': 'Frank Pallone', 'district': 'NJ-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': 'E&C Ranking'},
    {'name': 'Tom Kean Jr.', 'district': 'NJ-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Moderate R'},
    {'name': 'Rob Menendez Jr.', 'district': 'NJ-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Bill Pascrell Jr.', 'district': 'NJ-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Deceased; replaced by D'},
    {'name': 'LaMonica McIver', 'district': 'NJ-10', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New; CBC'},
    {'name': 'Mikie Sherrill', 'district': 'NJ-11', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'May have run for Governor'},
    {'name': 'Bonnie Watson Coleman', 'district': 'NJ-12', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive; CBC'},

    # ── NEW MEXICO (3 districts: 3D) ─────────────────────────────────
    {'name': 'Melanie Stansbury', 'district': 'NM-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'Gabe Vasquez', 'district': 'NM-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Teresa Leger Fernandez', 'district': 'NM-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},

    # ── NEW YORK (26 districts) ──────────────────────────────────────
    {'name': 'Nick LaLota', 'district': 'NY-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Andrew Garbarino', 'district': 'NY-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Tom Suozzi', 'district': 'NY-3', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Problem Solvers; moderate'},
    {'name': 'Laura Gillen', 'district': 'NY-4', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'New; won 2024 flip; moderate D'},
    {'name': 'Gregory Meeks', 'district': 'NY-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Grace Meng', 'district': 'NY-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Nydia Velazquez', 'district': 'NY-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Progressive'},
    {'name': 'Hakeem Jeffries', 'district': 'NY-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'HOUSE MINORITY LEADER — most important D in House'},
    {'name': 'Yvette Clarke', 'district': 'NY-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Dan Goldman', 'district': 'NY-10', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Nicole Malliotakis', 'district': 'NY-11', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Jerry Nadler', 'district': 'NY-12', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': ''},
    {'name': 'Adriano Espaillat', 'district': 'NY-13', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'Alexandria Ocasio-Cortez', 'district': 'NY-14', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive star; wealth tax champion; TOP CHAMPION'},
    {'name': 'Ritchie Torres', 'district': 'NY-15', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'Moderate-progressive'},
    {'name': 'George Latimer', 'district': 'NY-16', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate; replaced Bowman'},
    {'name': 'Mike Lawler', 'district': 'NY-17', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'May have lost 2024'},
    {'name': 'Pat Ryan', 'district': 'NY-18', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Marc Molinaro', 'district': 'NY-19', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'May have lost 2024'},
    {'name': 'Paul Tonko', 'district': 'NY-20', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Energy and Commerce'], 'notes': ''},
    {'name': 'Elise Stefanik', 'district': 'NY-21', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Left for UN Ambassador; replaced by R'},
    {'name': 'Brandon Williams', 'district': 'NY-22', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'May have lost 2024'},
    {'name': 'Nick Langworthy', 'district': 'NY-23', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Claudia Tenney', 'district': 'NY-24', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Joseph Morelle', 'district': 'NY-25', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Timothy Kennedy', 'district': 'NY-26', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New; replaced Higgins'},

    # ── NORTH CAROLINA (14 districts) ────────────────────────────────
    {'name': 'Don Davis', 'district': 'NC-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Deborah Ross', 'district': 'NC-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Greg Murphy', 'district': 'NC-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Valerie Foushee', 'district': 'NC-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Virginia Foxx', 'district': 'NC-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Education and Workforce'], 'notes': 'Education & Workforce Chair'},
    {'name': 'Kathy Manning', 'district': 'NC-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Redistricted; may not be in Congress'},
    {'name': 'David Rouzer', 'district': 'NC-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Dan Bishop', 'district': 'NC-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Ran for AG; replaced by R'},
    {'name': 'Richard Hudson', 'district': 'NC-9', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Patrick McHenry', 'district': 'NC-10', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Chuck Edwards', 'district': 'NC-11', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Alma Adams', 'district': 'NC-12', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Jeff Jackson', 'district': 'NC-13', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Redistricted; status uncertain'},
    {'name': 'Tim Moore', 'district': 'NC-14', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New district from redistricting; former NC House Speaker'},

    # ── NORTH DAKOTA (1 at-large: R) ─────────────────────────────────
    {'name': 'Julie Fedorchak', 'district': 'ND-AL', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Replaced Armstrong (became Governor)'},

    # ── OHIO (15 districts) ──────────────────────────────────────────
    {'name': 'Greg Landsman', 'district': 'OH-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Brad Wenstrup', 'district': 'OH-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Retired; replaced by R'},
    {'name': 'Joyce Beatty', 'district': 'OH-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Jim Jordan', 'district': 'OH-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary'], 'notes': 'Judiciary Chair'},
    {'name': 'Bob Latta', 'district': 'OH-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Energy and Commerce'], 'notes': ''},
    {'name': 'Michael Rulli', 'district': 'OH-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New; won special for Bill Johnson seat'},
    {'name': 'Max Miller', 'district': 'OH-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Warren Davidson', 'district': 'OH-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': 'Freedom Caucus'},
    {'name': 'Marcy Kaptur', 'district': 'OH-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': 'May have lost 2024'},
    {'name': 'Mike Turner', 'district': 'OH-10', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Intelligence'], 'notes': ''},
    {'name': 'Shontel Brown', 'district': 'OH-11', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Troy Balderson', 'district': 'OH-12', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Emilia Sykes', 'district': 'OH-13', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'May have lost 2024'},
    {'name': 'Dave Joyce', 'district': 'OH-14', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Moderate R'},
    {'name': 'Mike Carey', 'district': 'OH-15', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},

    # ── OKLAHOMA (5 districts: 5R) ───────────────────────────────────
    {'name': 'Kevin Hern', 'district': 'OK-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; RSC Chair'},
    {'name': 'Josh Brecheen', 'district': 'OK-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Frank Lucas', 'district': 'OK-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Tom Cole', 'district': 'OK-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': 'Appropriations Chair; pragmatic dealmaker'},
    {'name': 'Stephanie Bice', 'district': 'OK-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── OREGON (6 districts) ─────────────────────────────────────────
    {'name': 'Suzanne Bonamici', 'district': 'OR-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'Cliff Bentz', 'district': 'OR-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Maxine Dexter', 'district': 'OR-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New; replaced Earl Blumenauer'},
    {'name': 'Val Hoyle', 'district': 'OR-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'Lori Chavez-DeRemer', 'district': 'OR-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Left for Secretary of Labor; special election'},
    {'name': 'Andrea Salinas', 'district': 'OR-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},

    # ── PENNSYLVANIA (17 districts) ──────────────────────────────────
    {'name': 'Brian Fitzpatrick', 'district': 'PA-1', 'party': 'R', 'stance': 'SKEPTICAL',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; Problem Solvers co-chair; MOST MODERATE HOUSE R'},
    {'name': 'Brendan Boyle', 'district': 'PA-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Budget'], 'notes': 'BUDGET RANKING MEMBER — key position'},
    {'name': 'Dwight Evans', 'district': 'PA-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Resigned; replaced by D'},
    {'name': 'Madeleine Dean', 'district': 'PA-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Mary Gay Scanlon', 'district': 'PA-5', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Chrissy Houlahan', 'district': 'PA-6', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Susan Wild', 'district': 'PA-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'May have lost 2024'},
    {'name': 'Matt Cartwright', 'district': 'PA-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'May have lost 2024'},
    {'name': 'Dan Meuser', 'district': 'PA-9', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Scott Perry', 'district': 'PA-10', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Lloyd Smucker', 'district': 'PA-11', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Summer Lee', 'district': 'PA-12', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},
    {'name': 'John Joyce', 'district': 'PA-13', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Guy Reschenthaler', 'district': 'PA-14', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Glenn Thompson', 'district': 'PA-15', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Agriculture'], 'notes': 'Agriculture Chair'},
    {'name': 'Mike Kelly', 'district': 'PA-16', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Chris Deluzio', 'district': 'PA-17', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},

    # ── RHODE ISLAND (2 districts: 2D) ───────────────────────────────
    {'name': 'Gabe Amo', 'district': 'RI-1', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Seth Magaziner', 'district': 'RI-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},

    # ── SOUTH CAROLINA (7 districts: 6R, 1D) ────────────────────────
    {'name': 'Nancy Mace', 'district': 'SC-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Joe Wilson', 'district': 'SC-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Jeff Duncan', 'district': 'SC-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'William Timmons', 'district': 'SC-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Ralph Norman', 'district': 'SC-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Jim Clyburn', 'district': 'SC-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Senior Democratic leader; CBC'},
    {'name': 'Russell Fry', 'district': 'SC-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── SOUTH DAKOTA (1 at-large: R) ─────────────────────────────────
    {'name': 'Dusty Johnson', 'district': 'SD-AL', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Pragmatic; Problem Solvers adjacent'},

    # ── TENNESSEE (9 districts: 8R, 1D) ──────────────────────────────
    {'name': 'Diana Harshbarger', 'district': 'TN-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Tim Burchett', 'district': 'TN-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Chuck Fleischmann', 'district': 'TN-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Scott DesJarlais', 'district': 'TN-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Andy Ogles', 'district': 'TN-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': 'Freedom Caucus'},
    {'name': 'John Rose', 'district': 'TN-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Mark Green', 'district': 'TN-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'David Kustoff', 'district': 'TN-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Steve Cohen', 'district': 'TN-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': 'Progressive'},

    # ── TEXAS (38 districts) ─────────────────────────────────────────
    {'name': 'Nathaniel Moran', 'district': 'TX-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Dan Crenshaw', 'district': 'TX-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Keith Self', 'district': 'TX-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Pat Fallon', 'district': 'TX-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Lance Gooden', 'district': 'TX-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Jake Ellzey', 'district': 'TX-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Lizzie Fletcher', 'district': 'TX-7', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Morgan Luttrell', 'district': 'TX-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Al Green', 'district': 'TX-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Financial Services'], 'notes': 'CBC'},
    {'name': 'Michael McCaul', 'district': 'TX-10', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Foreign Affairs'], 'notes': 'Foreign Affairs Chair'},
    {'name': 'August Pfluger', 'district': 'TX-11', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Craig Goldman', 'district': 'TX-12', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New; replaced Kay Granger'},
    {'name': 'Ronny Jackson', 'district': 'TX-13', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Randy Weber', 'district': 'TX-14', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Monica De La Cruz', 'district': 'TX-15', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'May have lost 2024'},
    {'name': 'Veronica Escobar', 'district': 'TX-16', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Pete Sessions', 'district': 'TX-17', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Christian Menefee', 'district': 'TX-18', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Replaced Sheila Jackson Lee (deceased); CBC'},
    {'name': 'Jodey Arrington', 'district': 'TX-19', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Budget'], 'notes': 'BUDGET CHAIR — critical gatekeeper'},
    {'name': 'Joaquin Castro', 'district': 'TX-20', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Chip Roy', 'district': 'TX-21', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Troy Nehls', 'district': 'TX-22', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Tony Gonzales', 'district': 'TX-23', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Moderate R on immigration; conservative on fiscal'},
    {'name': 'Beth Van Duyne', 'district': 'TX-24', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Roger Williams', 'district': 'TX-25', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},
    {'name': 'Michael Burgess', 'district': 'TX-26', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Retired; replaced by R'},
    {'name': 'Michael Cloud', 'district': 'TX-27', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Henry Cuellar', 'district': 'TX-28', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Blue Dog; very conservative D; likely hostile to wealth tax'},
    {'name': 'Sylvia Garcia', 'district': 'TX-29', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Jasmine Crockett', 'district': 'TX-30', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive; CBC'},
    {'name': 'John Carter', 'district': 'TX-31', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Colin Allred', 'district': 'TX-32', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Ran for Senate; replaced by D'},
    {'name': 'Marc Veasey', 'district': 'TX-33', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'Vicente Gonzalez', 'district': 'TX-34', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D'},
    {'name': 'Greg Casar', 'district': 'TX-35', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive Caucus'},
    {'name': 'Brian Babin', 'district': 'TX-36', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Lloyd Doggett', 'district': 'TX-37', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; Progressive; champion potential'},
    {'name': 'Wesley Hunt', 'district': 'TX-38', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── UTAH (4 districts: 4R) ───────────────────────────────────────
    {'name': 'Blake Moore', 'district': 'UT-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Celeste Maloy', 'district': 'UT-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'John Curtis', 'district': 'UT-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Left for Senate; replaced by R'},
    {'name': 'Burgess Owens', 'district': 'UT-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},

    # ── VERMONT (1 at-large: D) ──────────────────────────────────────
    {'name': 'Becca Balint', 'district': 'VT-AL', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Progressive'},

    # ── VIRGINIA (11 districts) ──────────────────────────────────────
    {'name': 'Rob Wittman', 'district': 'VA-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Jen Kiggans', 'district': 'VA-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Bobby Scott', 'district': 'VA-3', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Education and Workforce'], 'notes': 'E&W Ranking; CBC'},
    {'name': 'Jennifer McClellan', 'district': 'VA-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},
    {'name': 'John McGuire', 'district': 'VA-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Replaced Bob Good'},
    {'name': 'Ben Cline', 'district': 'VA-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Freedom Caucus'},
    {'name': 'Abigail Spanberger', 'district': 'VA-7', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Left for Governor race; status uncertain'},
    {'name': 'Don Beyer', 'district': 'VA-8', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; supports wealth tax; champion potential'},
    {'name': 'Morgan Griffith', 'district': 'VA-9', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Suhas Subramanyam', 'district': 'VA-10', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New; replaced Jennifer Wexton'},
    {'name': 'Gerry Connolly', 'district': 'VA-11', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Oversight'], 'notes': ''},

    # ── WASHINGTON (10 districts) ────────────────────────────────────
    {'name': 'Suzan DelBene', 'district': 'WA-1', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; DCCC Chair; moderate D'},
    {'name': 'Rick Larsen', 'district': 'WA-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': ''},
    {'name': 'Marie Gluesenkamp Perez', 'district': 'WA-3', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Most moderate D; rural; Problem Solvers'},
    {'name': 'Dan Newhouse', 'district': 'WA-4', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Voted to impeach Trump'},
    {'name': 'Michael Baumgartner', 'district': 'WA-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Replaced McMorris Rodgers (retired)'},
    {'name': 'Emily Randall', 'district': 'WA-6', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New; replaced Derek Kilmer'},
    {'name': 'Pramila Jayapal', 'district': 'WA-7', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'PROGRESSIVE CAUCUS CHAIR — TOP CHAMPION'},
    {'name': 'Kim Schrier', 'district': 'WA-8', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'Moderate D; swing district'},
    {'name': 'Adam Smith', 'district': 'WA-9', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services'], 'notes': 'Armed Services Ranking'},
    {'name': 'Marilyn Strickland', 'district': 'WA-10', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'CBC'},

    # ── WEST VIRGINIA (2 districts: 2R) ──────────────────────────────
    {'name': 'Carol Miller', 'district': 'WV-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means'},
    {'name': 'Alex Mooney', 'district': 'WV-2', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Financial Services'], 'notes': ''},

    # ── WISCONSIN (8 districts) ──────────────────────────────────────
    {'name': 'Bryan Steil', 'district': 'WI-1', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Administration Chair'},
    {'name': 'Mark Pocan', 'district': 'WI-2', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations'], 'notes': 'Progressive Caucus'},
    {'name': 'Derrick Van Orden', 'district': 'WI-3', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Gwen Moore', 'district': 'WI-4', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Ways and Means'], 'notes': 'Ways and Means; CBC'},
    {'name': 'Scott Fitzgerald', 'district': 'WI-5', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Glenn Grothman', 'district': 'WI-6', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Tom Tiffany', 'district': 'WI-7', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
    {'name': 'Mike Gallagher', 'district': 'WI-8', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Resigned; replaced by R'},

    # ── WYOMING (1 at-large: R) ──────────────────────────────────────
    {'name': 'Harriet Hageman', 'district': 'WY-AL', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': ''},
]


# ═══════════════════════════════════════════════════════════════════════
#  CLASSIFICATION SUMMARY
# ═══════════════════════════════════════════════════════════════════════

def classify_house():
    """Classify all representatives and generate statistics."""
    receptive = [r for r in REPRESENTATIVES if r['stance'] == 'RECEPTIVE']
    skeptical = [r for r in REPRESENTATIVES if r['stance'] == 'SKEPTICAL']
    hostile = [r for r in REPRESENTATIVES if r['stance'] == 'HOSTILE']

    return {
        'receptive': receptive,
        'skeptical': skeptical,
        'hostile': hostile,
        'counts': {
            'receptive': len(receptive),
            'skeptical': len(skeptical),
            'hostile': len(hostile),
            'total': len(REPRESENTATIVES),
        }
    }


# ═══════════════════════════════════════════════════════════════════════
#  CRITICAL GATEKEEPERS
# ═══════════════════════════════════════════════════════════════════════

CRITICAL_GATEKEEPERS = [
    {'name': 'Mike Johnson', 'role': 'Speaker of the House', 'district': 'LA-4',
     'stance': 'HOSTILE', 'why': 'Controls floor schedule; nothing gets a vote without him'},
    {'name': 'Jason Smith', 'role': 'Ways and Means Chair', 'district': 'MO-8',
     'stance': 'HOSTILE', 'why': 'All tax legislation must pass through Ways and Means'},
    {'name': 'Jodey Arrington', 'role': 'Budget Chair', 'district': 'TX-19',
     'stance': 'HOSTILE', 'why': 'Controls budget resolution and reconciliation'},
    {'name': 'French Hill', 'role': 'Financial Services Chair', 'district': 'AR-2',
     'stance': 'HOSTILE', 'why': 'Oversees sovereign wealth fund and M2M tax implementation'},
    {'name': 'Tom Cole', 'role': 'Appropriations Chair', 'district': 'OK-4',
     'stance': 'HOSTILE', 'why': 'Controls funding; pragmatic dealmaker'},
]

TOP_CHAMPIONS = [
    {'name': 'John Larson', 'role': 'Ways and Means', 'district': 'CT-1',
     'stance': 'RECEPTIVE', 'why': 'SS 2100 Act sponsor; has literally spent years on this'},
    {'name': 'Pramila Jayapal', 'role': 'Progressive Caucus Chair', 'district': 'WA-7',
     'stance': 'RECEPTIVE', 'why': 'Can mobilize entire Progressive Caucus (~100 members)'},
    {'name': 'Hakeem Jeffries', 'role': 'House Minority Leader', 'district': 'NY-8',
     'stance': 'RECEPTIVE', 'why': 'Most important D in the House; controls floor strategy'},
    {'name': 'Alexandria Ocasio-Cortez', 'role': 'Progressive', 'district': 'NY-14',
     'stance': 'RECEPTIVE', 'why': 'Wealth tax champion; massive public platform'},
    {'name': 'Brendan Boyle', 'role': 'Budget Ranking', 'district': 'PA-2',
     'stance': 'RECEPTIVE', 'why': 'Key position for revenue-constrained benefit structure'},
    {'name': 'Don Beyer', 'role': 'Ways and Means', 'district': 'VA-8',
     'stance': 'RECEPTIVE', 'why': 'Supports wealth tax concepts; W&M position'},
    {'name': 'Lloyd Doggett', 'role': 'Ways and Means', 'district': 'TX-37',
     'stance': 'RECEPTIVE', 'why': 'Progressive on W&M; tax expertise'},
    {'name': 'Rosa DeLauro', 'role': 'Appropriations Ranking', 'district': 'CT-3',
     'stance': 'RECEPTIVE', 'why': 'CTC champion; understands benefit delivery'},
    {'name': 'Katherine Clark', 'role': 'House Minority Whip', 'district': 'MA-5',
     'stance': 'RECEPTIVE', 'why': 'Can whip Democratic votes'},
]

BRIDGE_REPRESENTATIVES = [
    {'name': 'Brian Fitzpatrick', 'role': 'Ways and Means; Problem Solvers co-chair',
     'district': 'PA-1', 'stance': 'SKEPTICAL',
     'why': 'Only R classified as SKEPTICAL; bipartisan credibility on W&M'},
    {'name': 'Richard Neal', 'role': 'Ways and Means Ranking',
     'district': 'MA-1', 'stance': 'SKEPTICAL',
     'why': 'Key gatekeeper for D side; cautious establishment but protects SS'},
    {'name': 'Jared Golden', 'role': 'Problem Solvers',
     'district': 'ME-2', 'stance': 'SKEPTICAL',
     'why': 'Very moderate D; bipartisan credibility'},
    {'name': 'Jim Himes', 'role': 'Financial Services',
     'district': 'CT-4', 'stance': 'SKEPTICAL',
     'why': 'Financial sector expertise; New Dem Coalition'},
    {'name': 'Suzan DelBene', 'role': 'Ways and Means; DCCC Chair',
     'district': 'WA-1', 'stance': 'SKEPTICAL',
     'why': 'W&M position and DCCC role give her outsized influence'},
]


# ═══════════════════════════════════════════════════════════════════════
#  PROPOSAL ASSIGNMENTS (same framework as Senate)
# ═══════════════════════════════════════════════════════════════════════

PROPOSAL_ASSIGNMENTS = {
    'RECEPTIVE': {
        'letter': 'political_letters/letter_receptive.py',
        'enclosures': [
            'short_format/executive_brief.py',
            'medium_format/policy_brief.py',
            'Key Model Outputs (1 page)',
        ],
        'follow_up': 'medium_format/white_paper.py (upon request)',
        'academic': 'long_format/working_paper.py (for staff economists)',
    },
    'SKEPTICAL': {
        'letter': 'political_letters/letter_skeptical.py',
        'enclosures': [
            'short_format/executive_brief.py',
            'Fiscal Impact Summary (1 page)',
        ],
        'follow_up': 'medium_format/policy_brief.py (upon request)',
        'academic': None,
    },
    'HOSTILE': {
        'letter': 'political_letters/letter_hostile.py',
        'enclosures': [
            'short_format/executive_brief.py (solvency-focused)',
            'Alaska PFD Comparison (1 page)',
        ],
        'follow_up': None,
        'academic': None,
    },
}


# ═══════════════════════════════════════════════════════════════════════
#  COMMITTEE-SPECIFIC TARGETING
# ═══════════════════════════════════════════════════════════════════════

COMMITTEE_TARGETS = {
    'Ways and Means': {
        'why': 'All tax legislation originates here; FICA reform and M2M tax require W&M markup',
        'chair': 'Jason Smith (R-MO-8)',
        'ranking': 'Richard Neal (D-MA-1)',
        'receptive_members': [
            'Terri Sewell (D-AL-7)', 'Mike Thompson (D-CA-4)',
            'Judy Chu (D-CA-28)', 'Jimmy Gomez (D-CA-34)',
            'Linda Sanchez (D-CA-38)', 'John Larson (D-CT-1)',
            'Danny Davis (D-IL-7)', 'Steven Horsford (D-NV-4)',
            'Don Beyer (D-VA-8)', 'Lloyd Doggett (D-TX-37)',
            'Gwen Moore (D-WI-4)', 'Jimmy Panetta (D-CA-19)',
        ],
        'skeptical_members': [
            'Brad Schneider (D-IL-10)', 'Suzan DelBene (D-WA-1)',
            'Brian Fitzpatrick (R-PA-1)',
        ],
    },
    'Budget': {
        'why': 'Revenue-constrained framework requires budget resolution; reconciliation path',
        'chair': 'Jodey Arrington (R-TX-19)',
        'ranking': 'Brendan Boyle (D-PA-2)',
    },
    'Financial Services': {
        'why': 'Sovereign wealth fund governance; M2M tax on investment income',
        'chair': 'French Hill (R-AR-2)',
        'ranking': 'Maxine Waters (D-CA-43)',
        'receptive_members': [
            'Maxine Waters (D-CA-43)', 'Nikema Williams (D-GA-5)',
            'Ayanna Pressley (D-MA-7)', 'Gregory Meeks (D-NY-5)',
            'Nydia Velazquez (D-NY-7)', 'Ritchie Torres (D-NY-15)',
            'Joyce Beatty (D-OH-3)', 'Alma Adams (D-NC-12)',
            'Rashida Tlaib (D-MI-12)', 'Emanuel Cleaver (D-MO-5)',
            'Al Green (D-TX-9)',
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════
#  CAUCUS-BASED OUTREACH STRATEGY
# ═══════════════════════════════════════════════════════════════════════

CAUCUS_STRATEGY = {
    'Congressional Progressive Caucus': {
        'chair': 'Pramila Jayapal (D-WA-7)',
        'estimated_members': '~100',
        'stance': 'RECEPTIVE',
        'strategy': 'Present full package; emphasize wealth tax + inequality reduction + SS expansion',
        'letter': 'letter_receptive.py',
    },
    'Congressional Black Caucus': {
        'chair': 'Steven Horsford (D-NV-4)',
        'estimated_members': '~60',
        'stance': 'RECEPTIVE',
        'strategy': 'Emphasize racial wealth gap closure; disproportionate benefit to Black workers; equity fund',
        'letter': 'letter_receptive.py',
    },
    'Congressional Hispanic Caucus': {
        'chair': 'Raul Ruiz (D-CA-25)',
        'estimated_members': '~40',
        'stance': 'RECEPTIVE',
        'strategy': 'Emphasize living wage threshold benefits; working poor demographics; SS solvency',
        'letter': 'letter_receptive.py',
    },
    'New Democrat Coalition': {
        'estimated_members': '~100',
        'stance': 'SKEPTICAL',
        'strategy': 'Emphasize fiscal discipline; revenue-constrained design; no deficit spending; GDP growth',
        'letter': 'letter_skeptical.py',
    },
    'Blue Dog Coalition': {
        'estimated_members': '~10-15',
        'stance': 'SKEPTICAL',
        'strategy': 'Lead with SS solvency; deficit neutrality; revenue-constrained formula; bipartisan potential',
        'letter': 'letter_skeptical.py',
    },
    'Problem Solvers Caucus': {
        'co_chairs': 'Brian Fitzpatrick (R-PA-1) and Josh Gottheimer (D-NJ-5)',
        'estimated_members': '~50 (bipartisan)',
        'stance': 'SKEPTICAL',
        'strategy': 'Present as bipartisan SS solvency solution; de-emphasize wealth tax; emphasize FICA reform',
        'letter': 'letter_skeptical.py',
    },
    'Republican Study Committee': {
        'chair': 'Kevin Hern (R-OK-1)',
        'estimated_members': '~160',
        'stance': 'HOSTILE',
        'strategy': 'Lead with SS solvency crisis for 67M retirees; Alaska PFD model; market-based returns',
        'letter': 'letter_hostile.py',
    },
    'House Freedom Caucus': {
        'estimated_members': '~40-50',
        'stance': 'HOSTILE',
        'strategy': 'Minimal engagement; focus only on SS solvency crisis affecting their constituents',
        'letter': 'letter_hostile.py',
    },
}


# ═══════════════════════════════════════════════════════════════════════
#  DATA CAVEATS
# ═══════════════════════════════════════════════════════════════════════

CAVEATS = """
IMPORTANT DATA FRESHNESS NOTES:

1. Based on training data through early-mid 2025. The 119th Congress was
   just organizing at that time. Committee assignments, caucus memberships,
   and even which members are serving may have changed due to:
   - Special elections (seats vacated for administration roles)
   - Deaths or resignations
   - Committee reassignments

2. Several 2024 races were extremely close and winners may be incorrect:
   NY-17, NY-19, NY-22, OH-9, OH-13, CA-13, CA-27, IA-3, CO-8, PA-7, PA-8

3. Classification is inherently approximate. A member classified as
   SKEPTICAL on the full package might be RECEPTIVE on SS solvency alone
   and HOSTILE on the billionaire tax.

4. Cross-reference against current official sources:
   - house.gov/representatives
   - congress.gov/members
   - Committee websites for current membership
   - Caucus websites for current rosters
"""


if __name__ == '__main__':
    classification = classify_house()

    print("=" * 80)
    print("  HOUSE RECIPIENT LIST — 119th CONGRESS")
    print("=" * 80)

    print(f"\n  CLASSIFICATION SUMMARY:")
    print(f"  {'Stance':<12} {'Count':>6} {'Pct':>6}")
    print(f"  {'─' * 24}")
    for stance in ['receptive', 'skeptical', 'hostile']:
        count = classification['counts'][stance]
        total = classification['counts']['total']
        pct = count / total * 100
        print(f"  {stance.upper():<12} {count:>6} {pct:>5.0f}%")
    print(f"  {'─' * 24}")
    print(f"  {'TOTAL':<12} {classification['counts']['total']:>6}")

    print(f"\n  RECEPTIVE MEMBERS ({classification['counts']['receptive']}):")
    for r in classification['receptive'][:20]:
        print(f"    {r['name']:<30} ({r['party']}-{r['district']}) {r.get('notes', '')[:50]}")
    if classification['counts']['receptive'] > 20:
        print(f"    ... and {classification['counts']['receptive'] - 20} more")

    print(f"\n  SKEPTICAL MEMBERS ({classification['counts']['skeptical']}):")
    for r in classification['skeptical']:
        print(f"    {r['name']:<30} ({r['party']}-{r['district']}) {r.get('notes', '')[:50]}")

    print(f"\n  CRITICAL GATEKEEPERS:")
    for g in CRITICAL_GATEKEEPERS:
        print(f"    {g['name']:<25} {g['role']:<30} [{g['stance']}]")

    print(f"\n  TOP CHAMPIONS:")
    for c in TOP_CHAMPIONS:
        print(f"    {c['name']:<25} {c['role']:<30} {c['why'][:50]}")

    print(f"\n  BRIDGE REPRESENTATIVES (persuadable):")
    for b in BRIDGE_REPRESENTATIVES:
        print(f"    {b['name']:<25} {b['role']:<35} {b['why'][:45]}")

    print(f"\n  CAUCUS OUTREACH STRATEGY:")
    for caucus, info in CAUCUS_STRATEGY.items():
        print(f"    {caucus:<40} [{info['stance']}] → {info['letter']}")

    print(f"\n  COMMITTEE TARGETS:")
    for committee, info in COMMITTEE_TARGETS.items():
        print(f"    {committee}: {info['why'][:60]}")

    print(f"\n  PROPOSAL ASSIGNMENTS:")
    for stance, assignment in PROPOSAL_ASSIGNMENTS.items():
        print(f"\n    {stance}:")
        print(f"      Letter: {assignment['letter']}")
        print(f"      Enclosures: {', '.join(assignment['enclosures'][:2])}")
