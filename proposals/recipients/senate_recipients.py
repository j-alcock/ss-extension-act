"""
US Senate Recipient List — 119th Congress (2025-2027)
Maps each senator to their stance classification and proposal assignment.

CLASSIFICATION METHODOLOGY:
  RECEPTIVE: Likely to support SS expansion + billionaire taxation
  SKEPTICAL: Open to SS solvency reform but cautious on M2M tax / scale
  HOSTILE: Opposed to new taxes and/or expanded benefits

PROPOSAL ASSIGNMENTS:
  RECEPTIVE → Letter (receptive) + Executive Brief + Policy Brief
  SKEPTICAL → Letter (skeptical) + Executive Brief + Fiscal Summary
  HOSTILE   → Letter (hostile) + Executive Brief (solvency-focused)

Data compiled from: senate.gov, committee pages, caucus memberships,
voting records, public statements. See caveats at bottom regarding
data freshness (based on early-mid 2025 known composition).

CONTACT INFORMATION:
  Full contact details (DC offices, phone numbers, websites, state offices)
  are in senate_contact_directory.py — import and cross-reference by name.

  Usage:
    from proposals.recipients.senate_contact_directory import (
        SENATE_CONTACTS, format_contact_block, get_mailing_address
    )
    contact = SENATE_CONTACTS['Ron Wyden']
    print(format_contact_block('Ron Wyden'))
"""

# ═══════════════════════════════════════════════════════════════════════
#  SENATE ROSTER
# ═══════════════════════════════════════════════════════════════════════

SENATORS = [
    # ── ALABAMA ───────────────────────────────────────────────────
    {'name': 'Tommy Tuberville', 'state': 'AL', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Armed Services', 'Agriculture'], 'notes': ''},
    {'name': 'Katie Britt', 'state': 'AL', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Banking', 'Appropriations'], 'notes': ''},

    # ── ALASKA ────────────────────────────────────────────────────
    {'name': 'Lisa Murkowski', 'state': 'AK', 'party': 'R', 'stance': 'SKEPTICAL',
     'committees': ['Appropriations', 'Energy'], 'notes': 'Most moderate R; Alaska PFD precedent'},
    {'name': 'Dan Sullivan', 'state': 'AK', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Armed Services', 'Commerce'], 'notes': ''},

    # ── ARIZONA ───────────────────────────────────────────────────
    {'name': 'Ruben Gallego', 'state': 'AZ', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services'], 'notes': 'New senator (2025)'},
    {'name': 'Mark Kelly', 'state': 'AZ', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Armed Services', 'Commerce'], 'notes': 'Moderate D'},

    # ── ARKANSAS ──────────────────────────────────────────────────
    {'name': 'John Boozman', 'state': 'AR', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Tom Cotton', 'state': 'AR', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Armed Services', 'Intelligence'], 'notes': ''},

    # ── CALIFORNIA ────────────────────────────────────────────────
    {'name': 'Adam Schiff', 'state': 'CA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary'], 'notes': 'New senator (2025)'},
    {'name': 'Alex Padilla', 'state': 'CA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary', 'Budget'], 'notes': ''},

    # ── COLORADO ──────────────────────────────────────────────────
    {'name': 'Michael Bennet', 'state': 'CO', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Finance', 'Intelligence'], 'notes': 'CTC champion; open to innovative benefits; Finance member'},
    {'name': 'John Hickenlooper', 'state': 'CO', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Commerce', 'HELP'], 'notes': 'Business-oriented D'},

    # ── CONNECTICUT ───────────────────────────────────────────────
    {'name': 'Richard Blumenthal', 'state': 'CT', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary', 'Commerce'], 'notes': ''},
    {'name': 'Chris Murphy', 'state': 'CT', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations', 'Foreign Relations'], 'notes': ''},

    # ── DELAWARE ──────────────────────────────────────────────────
    {'name': 'Chris Coons', 'state': 'DE', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Appropriations', 'Foreign Relations'], 'notes': 'Moderate D'},
    {'name': 'Lisa Blunt Rochester', 'state': 'DE', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New senator (2025), CBC member'},

    # ── FLORIDA ───────────────────────────────────────────────────
    {'name': 'Rick Scott', 'state': 'FL', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Budget', 'Finance'], 'notes': 'Finance member; proposed SS/Medicare sunset'},
    {'name': 'Ashley Moody', 'state': 'FL', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Replaced Rubio (became Sec of State); former FL AG'},

    # ── GEORGIA ───────────────────────────────────────────────────
    {'name': 'Jon Ossoff', 'state': 'GA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary', 'Banking'], 'notes': ''},
    {'name': 'Raphael Warnock', 'state': 'GA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance', 'Banking'], 'notes': 'Finance member; strong on equity'},

    # ── HAWAII ────────────────────────────────────────────────────
    {'name': 'Brian Schatz', 'state': 'HI', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations', 'Commerce'], 'notes': 'UBI-adjacent interest'},
    {'name': 'Mazie Hirono', 'state': 'HI', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary', 'Armed Services'], 'notes': ''},

    # ── IDAHO ─────────────────────────────────────────────────────
    {'name': 'Mike Crapo', 'state': 'ID', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance'], 'notes': 'FINANCE CHAIR — critical gatekeeper'},
    {'name': 'Jim Risch', 'state': 'ID', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Foreign Relations'], 'notes': ''},

    # ── ILLINOIS ──────────────────────────────────────────────────
    {'name': 'Dick Durbin', 'state': 'IL', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary', 'Appropriations'], 'notes': 'Senate Democratic Whip'},
    {'name': 'Tammy Duckworth', 'state': 'IL', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services', 'Commerce'], 'notes': ''},

    # ── INDIANA ───────────────────────────────────────────────────
    {'name': 'Jim Banks', 'state': 'IN', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New senator (2025)'},
    {'name': 'Todd Young', 'state': 'IN', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Commerce'], 'notes': 'Finance member'},

    # ── IOWA ──────────────────────────────────────────────────────
    {'name': 'Chuck Grassley', 'state': 'IA', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Judiciary'], 'notes': 'Finance member, longtime SS focus'},
    {'name': 'Joni Ernst', 'state': 'IA', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Armed Services'], 'notes': 'Finance member'},

    # ── KANSAS ────────────────────────────────────────────────────
    {'name': 'Jerry Moran', 'state': 'KS', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations', 'Banking'], 'notes': ''},
    {'name': 'Roger Marshall', 'state': 'KS', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['HELP', 'Budget'], 'notes': ''},

    # ── KENTUCKY ──────────────────────────────────────────────────
    {'name': 'Mitch McConnell', 'state': 'KY', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': 'Former leader; stepped back but still influential'},
    {'name': 'Rand Paul', 'state': 'KY', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['HELP', 'Foreign Relations'], 'notes': 'Libertarian-leaning'},

    # ── LOUISIANA ─────────────────────────────────────────────────
    {'name': 'Bill Cassidy', 'state': 'LA', 'party': 'R', 'stance': 'SKEPTICAL',
     'committees': ['Finance', 'HELP'], 'notes': 'Finance member; working on bipartisan SS solvency with King'},
    {'name': 'John Kennedy', 'state': 'LA', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary', 'Banking'], 'notes': ''},

    # ── MAINE ─────────────────────────────────────────────────────
    {'name': 'Susan Collins', 'state': 'ME', 'party': 'R', 'stance': 'SKEPTICAL',
     'committees': ['Appropriations', 'Aging'], 'notes': 'Most moderate R; Aging committee; protects SS'},
    {'name': 'Angus King', 'state': 'ME', 'party': 'I', 'stance': 'SKEPTICAL',
     'committees': ['Energy', 'Intelligence'], 'notes': 'Caucuses with D; SS reform partner with Cassidy'},

    # ── MARYLAND ──────────────────────────────────────────────────
    {'name': 'Chris Van Hollen', 'state': 'MD', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations', 'Budget'], 'notes': 'Budget member'},
    {'name': 'Angela Alsobrooks', 'state': 'MD', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Replaced Cardin (retired); former Prince Georges Co. Exec'},

    # ── MASSACHUSETTS ─────────────────────────────────────────────
    {'name': 'Elizabeth Warren', 'state': 'MA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance', 'Banking'], 'notes': 'Finance + Banking member; wealth tax champion'},
    {'name': 'Ed Markey', 'state': 'MA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Commerce', 'Environment'], 'notes': 'Progressive'},

    # ── MICHIGAN ──────────────────────────────────────────────────
    {'name': 'Gary Peters', 'state': 'MI', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Commerce', 'Armed Services'], 'notes': ''},
    {'name': 'Elissa Slotkin', 'state': 'MI', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': [], 'notes': 'New senator (2025); moderate D'},

    # ── MINNESOTA ─────────────────────────────────────────────────
    {'name': 'Amy Klobuchar', 'state': 'MN', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Judiciary', 'Commerce'], 'notes': 'Moderate-pragmatic D'},
    {'name': 'Tina Smith', 'state': 'MN', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance', 'Banking'], 'notes': 'Finance member'},

    # ── MISSISSIPPI ───────────────────────────────────────────────
    {'name': 'Roger Wicker', 'state': 'MS', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Armed Services'], 'notes': ''},
    {'name': 'Cindy Hyde-Smith', 'state': 'MS', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},

    # ── MISSOURI ──────────────────────────────────────────────────
    {'name': 'Josh Hawley', 'state': 'MO', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary', 'Commerce'], 'notes': 'Populist R — may have interest in some elements'},
    {'name': 'Eric Schmitt', 'state': 'MO', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary', 'Commerce'], 'notes': ''},

    # ── MONTANA ───────────────────────────────────────────────────
    {'name': 'Steve Daines', 'state': 'MT', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Banking'], 'notes': 'Finance member'},
    {'name': 'Tim Sheehy', 'state': 'MT', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New senator (2025)'},

    # ── NEBRASKA ──────────────────────────────────────────────────
    {'name': 'Deb Fischer', 'state': 'NE', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Armed Services', 'Commerce'], 'notes': ''},
    {'name': 'Pete Ricketts', 'state': 'NE', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Banking', 'Environment'], 'notes': ''},

    # ── NEVADA ────────────────────────────────────────────────────
    {'name': 'Jacky Rosen', 'state': 'NV', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Commerce', 'HELP'], 'notes': 'Moderate D'},
    {'name': 'Catherine Cortez Masto', 'state': 'NV', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance', 'Banking'], 'notes': 'Finance member'},

    # ── NEW HAMPSHIRE ─────────────────────────────────────────────
    {'name': 'Jeanne Shaheen', 'state': 'NH', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Appropriations', 'Foreign Relations'], 'notes': 'Moderate D'},
    {'name': 'Maggie Hassan', 'state': 'NH', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Finance', 'HELP'], 'notes': 'Finance member; moderate D'},

    # ── NEW JERSEY ────────────────────────────────────────────────
    {'name': 'Andy Kim', 'state': 'NJ', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'New senator (2025)'},
    {'name': 'Cory Booker', 'state': 'NJ', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance', 'Judiciary'], 'notes': 'Finance member; baby bonds champion'},

    # ── NEW MEXICO ────────────────────────────────────────────────
    {'name': 'Martin Heinrich', 'state': 'NM', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations', 'Energy'], 'notes': ''},
    {'name': 'Ben Ray Lujan', 'state': 'NM', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Commerce', 'Budget'], 'notes': ''},

    # ── NEW YORK ──────────────────────────────────────────────────
    {'name': 'Chuck Schumer', 'state': 'NY', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': [], 'notes': 'Senate Minority Leader'},
    {'name': 'Kirsten Gillibrand', 'state': 'NY', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services', 'Aging'], 'notes': 'Aging committee'},

    # ── NORTH CAROLINA ────────────────────────────────────────────
    {'name': 'Thom Tillis', 'state': 'NC', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary', 'Banking'], 'notes': ''},
    {'name': 'Ted Budd', 'state': 'NC', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Commerce'], 'notes': 'Finance member'},

    # ── NORTH DAKOTA ──────────────────────────────────────────────
    {'name': 'John Hoeven', 'state': 'ND', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations'], 'notes': ''},
    {'name': 'Kevin Cramer', 'state': 'ND', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Banking', 'Environment'], 'notes': ''},

    # ── OHIO ──────────────────────────────────────────────────────
    {'name': 'Bernie Moreno', 'state': 'OH', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Replaced Sherrod Brown (lost 2024)'},
    {'name': 'Jon Husted', 'state': 'OH', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Replaced Vance (became VP); former OH Lt. Gov'},

    # ── OKLAHOMA ──────────────────────────────────────────────────
    {'name': 'James Lankford', 'state': 'OK', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Appropriations'], 'notes': 'Finance member'},
    {'name': 'Markwayne Mullin', 'state': 'OK', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['HELP', 'Armed Services'], 'notes': ''},

    # ── OREGON ────────────────────────────────────────────────────
    {'name': 'Ron Wyden', 'state': 'OR', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance'], 'notes': 'FINANCE RANKING MEMBER — has M2M bill ready; TOP CHAMPION'},
    {'name': 'Jeff Merkley', 'state': 'OR', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations', 'Environment'], 'notes': 'Progressive'},

    # ── PENNSYLVANIA ──────────────────────────────────────────────
    {'name': 'John Fetterman', 'state': 'PA', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Banking', 'Agriculture'], 'notes': 'Populist but shifting rightward on some issues'},
    {'name': 'Dave McCormick', 'state': 'PA', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'Replaced Bob Casey (lost 2024); former Bridgewater CEO'},

    # ── RHODE ISLAND ──────────────────────────────────────────────
    {'name': 'Jack Reed', 'state': 'RI', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Armed Services', 'Banking'], 'notes': ''},
    {'name': 'Sheldon Whitehouse', 'state': 'RI', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance', 'Budget', 'Judiciary'], 'notes': 'Finance + Budget; wealth inequality champion'},

    # ── SOUTH CAROLINA ────────────────────────────────────────────
    {'name': 'Lindsey Graham', 'state': 'SC', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Budget', 'Judiciary'], 'notes': 'BUDGET CHAIR — critical gatekeeper'},
    {'name': 'Tim Scott', 'state': 'SC', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Banking'], 'notes': 'Finance + Banking'},

    # ── SOUTH DAKOTA ──────────────────────────────────────────────
    {'name': 'John Thune', 'state': 'SD', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance'], 'notes': 'SENATE MAJORITY LEADER — controls floor schedule'},
    {'name': 'Mike Rounds', 'state': 'SD', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Armed Services', 'Banking'], 'notes': ''},

    # ── TENNESSEE ─────────────────────────────────────────────────
    {'name': 'Marsha Blackburn', 'state': 'TN', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Commerce', 'Judiciary'], 'notes': ''},
    {'name': 'Bill Hagerty', 'state': 'TN', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Banking', 'Foreign Relations'], 'notes': ''},

    # ── TEXAS ─────────────────────────────────────────────────────
    {'name': 'John Cornyn', 'state': 'TX', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Judiciary'], 'notes': 'Finance member'},
    {'name': 'Ted Cruz', 'state': 'TX', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Commerce', 'Judiciary'], 'notes': ''},

    # ── UTAH ──────────────────────────────────────────────────────
    {'name': 'Mike Lee', 'state': 'UT', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Judiciary', 'Commerce'], 'notes': 'Libertarian-leaning'},
    {'name': 'John Curtis', 'state': 'UT', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New senator (2025); climate-moderate but fiscal conservative'},

    # ── VERMONT ───────────────────────────────────────────────────
    {'name': 'Bernie Sanders', 'state': 'VT', 'party': 'I', 'stance': 'RECEPTIVE',
     'committees': ['HELP', 'Budget'], 'notes': 'Budget/HELP; moral authority on SS expansion; TOP CHAMPION'},
    {'name': 'Peter Welch', 'state': 'VT', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Judiciary', 'Agriculture'], 'notes': ''},

    # ── VIRGINIA ──────────────────────────────────────────────────
    {'name': 'Mark Warner', 'state': 'VA', 'party': 'D', 'stance': 'SKEPTICAL',
     'committees': ['Finance', 'Banking', 'Intelligence'], 'notes': 'Finance member; centrist D with fiscal credibility'},
    {'name': 'Tim Kaine', 'state': 'VA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['HELP', 'Budget', 'Foreign Relations'], 'notes': ''},

    # ── WASHINGTON ────────────────────────────────────────────────
    {'name': 'Patty Murray', 'state': 'WA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations', 'HELP'], 'notes': 'Former Appropriations Chair'},
    {'name': 'Maria Cantwell', 'state': 'WA', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Finance', 'Commerce'], 'notes': 'Finance member'},

    # ── WEST VIRGINIA ─────────────────────────────────────────────
    {'name': 'Shelley Moore Capito', 'state': 'WV', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Appropriations', 'Banking'], 'notes': ''},
    {'name': 'Jim Justice', 'state': 'WV', 'party': 'R', 'stance': 'HOSTILE',
     'committees': [], 'notes': 'New senator (2025)'},

    # ── WISCONSIN ─────────────────────────────────────────────────
    {'name': 'Ron Johnson', 'state': 'WI', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Budget', 'HELP'], 'notes': ''},
    {'name': 'Tammy Baldwin', 'state': 'WI', 'party': 'D', 'stance': 'RECEPTIVE',
     'committees': ['Appropriations', 'Commerce'], 'notes': 'Lost 2024 — replaced by Eric Hovde (R) HOSTILE'},

    # ── WYOMING ───────────────────────────────────────────────────
    {'name': 'John Barrasso', 'state': 'WY', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Finance', 'Energy'], 'notes': 'Finance member; Senate Republican Conference Chair'},
    {'name': 'Cynthia Lummis', 'state': 'WY', 'party': 'R', 'stance': 'HOSTILE',
     'committees': ['Banking', 'Commerce'], 'notes': ''},
]


# ═══════════════════════════════════════════════════════════════════════
#  CLASSIFICATION SUMMARY
# ═══════════════════════════════════════════════════════════════════════

def classify_senate():
    """Classify all senators and generate statistics."""
    receptive = [s for s in SENATORS if s['stance'] == 'RECEPTIVE']
    skeptical = [s for s in SENATORS if s['stance'] == 'SKEPTICAL']
    hostile = [s for s in SENATORS if s['stance'] == 'HOSTILE']

    return {
        'receptive': receptive,
        'skeptical': skeptical,
        'hostile': hostile,
        'counts': {
            'receptive': len(receptive),
            'skeptical': len(skeptical),
            'hostile': len(hostile),
            'total': len(SENATORS),
        }
    }


# ═══════════════════════════════════════════════════════════════════════
#  CRITICAL GATEKEEPERS
# ═══════════════════════════════════════════════════════════════════════

CRITICAL_GATEKEEPERS = [
    {'name': 'John Thune', 'role': 'Senate Majority Leader', 'stance': 'HOSTILE',
     'why': 'Controls floor schedule; nothing gets a vote without him'},
    {'name': 'Mike Crapo', 'role': 'Finance Committee Chair', 'stance': 'HOSTILE',
     'why': 'No tax bill moves without Finance markup'},
    {'name': 'Lindsey Graham', 'role': 'Budget Committee Chair', 'stance': 'HOSTILE',
     'why': 'Controls budget resolution and reconciliation'},
]

TOP_CHAMPIONS = [
    {'name': 'Ron Wyden', 'role': 'Finance Ranking Member', 'stance': 'RECEPTIVE',
     'why': 'Has the Billionaires Income Tax bill ready; perfect alignment'},
    {'name': 'Bernie Sanders', 'role': 'Budget/HELP', 'stance': 'RECEPTIVE',
     'why': 'Moral authority on SS expansion; massive public platform'},
    {'name': 'Elizabeth Warren', 'role': 'Finance + Banking', 'stance': 'RECEPTIVE',
     'why': 'Wealth tax champion; academic credibility'},
    {'name': 'Sheldon Whitehouse', 'role': 'Finance + Budget', 'stance': 'RECEPTIVE',
     'why': 'Wealth inequality documentation; prosecutorial approach'},
    {'name': 'Cory Booker', 'role': 'Finance', 'stance': 'RECEPTIVE',
     'why': 'Baby bonds champion; understands sovereign fund concept'},
]

BRIDGE_SENATORS = [
    {'name': 'Bill Cassidy', 'role': 'Finance', 'stance': 'SKEPTICAL',
     'why': 'Already working on bipartisan SS solvency with King'},
    {'name': 'Angus King', 'role': 'Intelligence', 'stance': 'SKEPTICAL',
     'why': 'SS reform partner with Cassidy; independent'},
    {'name': 'Susan Collins', 'role': 'Appropriations, Aging', 'stance': 'SKEPTICAL',
     'why': 'Most moderate R; protects SS; Aging committee'},
    {'name': 'Lisa Murkowski', 'role': 'Appropriations', 'stance': 'SKEPTICAL',
     'why': 'Most moderate R; Alaska PFD proves sovereign fund works'},
    {'name': 'Mark Warner', 'role': 'Finance, Banking', 'stance': 'SKEPTICAL',
     'why': 'Centrist D with fiscal credibility; Finance member'},
    {'name': 'Michael Bennet', 'role': 'Finance', 'stance': 'SKEPTICAL',
     'why': 'CTC champion; open to innovative benefit structures'},
]


# ═══════════════════════════════════════════════════════════════════════
#  PROPOSAL ASSIGNMENTS
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


if __name__ == '__main__':
    classification = classify_senate()

    print("=" * 80)
    print("  SENATE RECIPIENT LIST — 119th CONGRESS")
    print("=" * 80)

    print(f"\n  CLASSIFICATION SUMMARY:")
    print(f"  {'Stance':<12} {'Count':>6} {'Pct':>6}")
    print(f"  {'─' * 24}")
    for stance in ['receptive', 'skeptical', 'hostile']:
        count = classification['counts'][stance]
        pct = count / classification['counts']['total'] * 100
        print(f"  {stance.upper():<12} {count:>6} {pct:>5.0f}%")
    print(f"  {'─' * 24}")
    print(f"  {'TOTAL':<12} {classification['counts']['total']:>6}")

    print(f"\n  RECEPTIVE SENATORS ({classification['counts']['receptive']}):")
    for s in classification['receptive']:
        print(f"    {s['name']:<25} ({s['party']}-{s['state']}) {s.get('notes', '')}")

    print(f"\n  SKEPTICAL SENATORS ({classification['counts']['skeptical']}):")
    for s in classification['skeptical']:
        print(f"    {s['name']:<25} ({s['party']}-{s['state']}) {s.get('notes', '')}")

    print(f"\n  CRITICAL GATEKEEPERS:")
    for g in CRITICAL_GATEKEEPERS:
        print(f"    {g['name']:<25} {g['role']:<30} [{g['stance']}]")

    print(f"\n  TOP CHAMPIONS:")
    for c in TOP_CHAMPIONS:
        print(f"    {c['name']:<25} {c['role']:<30} {c['why'][:50]}")

    print(f"\n  BRIDGE SENATORS (persuadable):")
    for b in BRIDGE_SENATORS:
        print(f"    {b['name']:<25} {b['role']:<30} {b['why'][:50]}")

    print(f"\n  PROPOSAL ASSIGNMENTS:")
    for stance, assignment in PROPOSAL_ASSIGNMENTS.items():
        print(f"\n    {stance}:")
        print(f"      Letter: {assignment['letter']}")
        print(f"      Enclosures: {', '.join(assignment['enclosures'][:2])}")
