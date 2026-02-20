"""
US Senate Contact Directory — 119th Congress (2025-2027)
Full contact information for all 100 senators.

SOURCE DATA:
  - Senate Suite & Telephone List (PDF), published July 11, 2025
    by the Senate Sergeant at Arms / CIO
  - senate.gov/senators/ official directory
  - Individual senator websites for state office details

BUILDING CODES:
  SR — Russell Senate Office Building, Constitution Ave & Delaware Ave NE
  SD — Dirksen Senate Office Building, Constitution Ave & 1st St NE
  SH — Hart Senate Office Building, Constitution Ave & 2nd St NE

All DC phone numbers use the (202) 224-XXXX format.
Capitol Switchboard: (202) 224-3121

CONTACT PREFERENCE (ranked):
  1. Contact form on senator's website (most responsive for constituents)
  2. DC office phone (for legislative staff / scheduling)
  3. State office phone (for constituent services)
  4. Written letter to DC office (for formal proposals)

EMAIL STATUS:
  Direct email addresses are NOT publicly listed for any senator.
  The old @SENATE.GOV direct email system (circa 1995-2005) was
  replaced by web-based contact forms. The historical QRD directory
  (qrd.org/qrd/www/usa/congress.html) lists 104th-Congress-era
  addresses like SENATOR@SENATE.GOV — these are ALL defunct.

  Modern equivalent: Every senator's contact_form URL below accepts
  electronic messages. These forms typically require:
    - Full name and mailing address (to verify constituent status)
    - Subject line and message body
    - Some accept file attachments (for enclosing briefs)

  For NON-CONSTITUENT outreach (e.g., national policy proposals):
    - Written letter via USPS to DC office is most reliable
    - DC phone call to legislative director is second-best
    - Contact forms may filter out non-constituent messages
    - Cc: the senator's staff email if known (staff directories
      at legistorm.com, though subscription required)

CROSS-REFERENCE: See senate_recipients.py for stance classifications,
committee memberships, and proposal assignments.
"""

# ═══════════════════════════════════════════════════════════════════════
#  BUILDING FULL ADDRESSES
# ═══════════════════════════════════════════════════════════════════════

BUILDING_ADDRESSES = {
    'SR': 'Russell Senate Office Building, 2 Constitution Avenue NE, Washington, DC 20510',
    'SD': 'Dirksen Senate Office Building, 44 1st Street NE, Washington, DC 20510',
    'SH': 'Hart Senate Office Building, 120 Constitution Avenue NE, Washington, DC 20510',
}

def expand_suite(suite_code):
    """Convert 'SH-311' to full mailing address."""
    building = suite_code[:2]
    room = suite_code[3:]
    building_name = {
        'SR': 'Russell Senate Office Building',
        'SD': 'Dirksen Senate Office Building',
        'SH': 'Hart Senate Office Building',
    }[building]
    return f'{room} {building_name}, Washington, DC 20510'


# ═══════════════════════════════════════════════════════════════════════
#  SENATE CONTACT DIRECTORY — ALL 100 SENATORS
#  Source: Senate Suite & Telephone List, July 11, 2025
# ═══════════════════════════════════════════════════════════════════════

SENATE_CONTACTS = {
    # ── ALABAMA ───────────────────────────────────────────────────────
    'Tommy Tuberville': {
        'state': 'AL', 'party': 'R',
        'suite': 'SR-455', 'dc_phone': '(202) 224-4124',
        'website': 'https://tuberville.senate.gov',
        'contact_form': 'https://tuberville.senate.gov/contact',
        'state_offices': [
            {'city': 'Birmingham', 'address': '2000 International Park Dr, Suite 107, Birmingham, AL 35243', 'phone': '(205) 760-5576'},
            {'city': 'Montgomery', 'address': '100 Commerce St, Suite 802, Montgomery, AL 36104', 'phone': '(334) 523-7424'},
            {'city': 'Huntsville', 'address': '200 Clinton Ave W, Suite 802, Huntsville, AL 35801', 'phone': '(256) 971-0044'},
        ],
    },
    'Katie Britt': {
        'state': 'AL', 'party': 'R',
        'suite': 'SR-416', 'dc_phone': '(202) 224-5744',
        'website': 'https://britt.senate.gov',
        'contact_form': 'https://britt.senate.gov/contact',
        'state_offices': [
            {'city': 'Montgomery', 'address': '100 Commerce St, Suite 608, Montgomery, AL 36104', 'phone': '(334) 230-0698'},
            {'city': 'Birmingham', 'address': '2005 University Blvd, Suite 105, Birmingham, AL 35233', 'phone': '(205) 731-2384'},
            {'city': 'Huntsville', 'address': '200 Clinton Ave W, Suite 712, Huntsville, AL 35801', 'phone': '(256) 355-0894'},
        ],
    },

    # ── ALASKA ────────────────────────────────────────────────────────
    'Lisa Murkowski': {
        'state': 'AK', 'party': 'R',
        'suite': 'SH-522', 'dc_phone': '(202) 224-6665',
        'website': 'https://murkowski.senate.gov',
        'contact_form': 'https://murkowski.senate.gov/contact',
        'state_offices': [
            {'city': 'Anchorage', 'address': '510 L St, Suite 600, Anchorage, AK 99501', 'phone': '(907) 271-3735'},
            {'city': 'Fairbanks', 'address': '101 12th Ave, Room 329, Fairbanks, AK 99701', 'phone': '(907) 456-0233'},
            {'city': 'Juneau', 'address': '709 W 9th St, Suite 967, Juneau, AK 99802', 'phone': '(907) 586-7277'},
        ],
    },
    'Dan Sullivan': {
        'state': 'AK', 'party': 'R',
        'suite': 'SH-706', 'dc_phone': '(202) 224-3004',
        'website': 'https://sullivan.senate.gov',
        'contact_form': 'https://sullivan.senate.gov/contact',
        'state_offices': [
            {'city': 'Anchorage', 'address': '510 L St, Suite 750, Anchorage, AK 99501', 'phone': '(907) 271-5915'},
            {'city': 'Fairbanks', 'address': '101 12th Ave, Suite 328, Fairbanks, AK 99701', 'phone': '(907) 456-0261'},
            {'city': 'Juneau', 'address': '800 Glacier Ave, Suite 101, Juneau, AK 99801', 'phone': '(907) 586-7277'},
        ],
    },

    # ── ARIZONA ───────────────────────────────────────────────────────
    'Ruben Gallego': {
        'state': 'AZ', 'party': 'D',
        'suite': 'SH-302', 'dc_phone': '(202) 224-4521',
        'website': 'https://gallego.senate.gov',
        'contact_form': 'https://gallego.senate.gov/contact',
        'state_offices': [
            {'city': 'Phoenix', 'address': '2200 E Camelback Rd, Suite 120, Phoenix, AZ 85016', 'phone': '(602) 598-7327'},
            {'city': 'Tucson', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },
    'Mark Kelly': {
        'state': 'AZ', 'party': 'D',
        'suite': 'SH-516', 'dc_phone': '(202) 224-2235',
        'website': 'https://kelly.senate.gov',
        'contact_form': 'https://kelly.senate.gov/contact',
        'state_offices': [
            {'city': 'Phoenix', 'address': '2201 E Camelback Rd, Suite 115, Phoenix, AZ 85016', 'phone': '(602) 671-7901'},
            {'city': 'Tucson', 'address': '20 E Ochoa St, Tucson, AZ 85701', 'phone': '(520) 475-5350'},
        ],
    },

    # ── ARKANSAS ──────────────────────────────────────────────────────
    'John Boozman': {
        'state': 'AR', 'party': 'R',
        'suite': 'SD-555', 'dc_phone': '(202) 224-4843',
        'website': 'https://boozman.senate.gov',
        'contact_form': 'https://boozman.senate.gov/contact',
        'state_offices': [
            {'city': 'Little Rock', 'address': '1401 W Capitol Ave, Suite 155, Little Rock, AR 72201', 'phone': '(501) 372-7153'},
        ],
    },
    'Tom Cotton': {
        'state': 'AR', 'party': 'R',
        'suite': 'SR-326', 'dc_phone': '(202) 224-2353',
        'website': 'https://cotton.senate.gov',
        'contact_form': 'https://cotton.senate.gov/contact',
        'state_offices': [
            {'city': 'Little Rock', 'address': '1108 S Old Missouri Rd, Suite B, Springdale, AR 72764', 'phone': '(479) 751-0879'},
        ],
    },

    # ── CALIFORNIA ────────────────────────────────────────────────────
    'Adam Schiff': {
        'state': 'CA', 'party': 'D',
        'suite': 'SH-112', 'dc_phone': '(202) 224-3841',
        'website': 'https://schiff.senate.gov',
        'contact_form': 'https://schiff.senate.gov/contact',
        'state_offices': [
            {'city': 'Los Angeles', 'address': 'TBD', 'phone': 'TBD'},
            {'city': 'San Francisco', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },
    'Alex Padilla': {
        'state': 'CA', 'party': 'D',
        'suite': 'SH-331', 'dc_phone': '(202) 224-3553',
        'website': 'https://padilla.senate.gov',
        'contact_form': 'https://padilla.senate.gov/contact',
        'state_offices': [
            {'city': 'Los Angeles', 'address': '11845 W Olympic Blvd, Suite 1250W, Los Angeles, CA 90064', 'phone': '(310) 231-4494'},
            {'city': 'Sacramento', 'address': '501 I St, Suite 7-800, Sacramento, CA 95814', 'phone': '(916) 448-2787'},
            {'city': 'San Diego', 'address': '600 B St, Suite 2240, San Diego, CA 92101', 'phone': '(619) 239-3884'},
            {'city': 'Fresno', 'address': '2500 Tulare St, Suite 5290, Fresno, CA 93721', 'phone': '(559) 497-5109'},
            {'city': 'San Francisco', 'address': '333 Bush St, Suite 3225, San Francisco, CA 94104', 'phone': '(415) 981-9369'},
        ],
    },

    # ── COLORADO ──────────────────────────────────────────────────────
    'Michael Bennet': {
        'state': 'CO', 'party': 'D',
        'suite': 'SR-261', 'dc_phone': '(202) 224-5852',
        'website': 'https://bennet.senate.gov',
        'contact_form': 'https://bennet.senate.gov/contact',
        'state_offices': [
            {'city': 'Denver', 'address': '1244 Speer Blvd, Suite 150, Denver, CO 80204', 'phone': '(303) 455-7600'},
        ],
    },
    'John Hickenlooper': {
        'state': 'CO', 'party': 'D',
        'suite': 'SH-316', 'dc_phone': '(202) 224-5941',
        'website': 'https://hickenlooper.senate.gov',
        'contact_form': 'https://hickenlooper.senate.gov/contact',
        'state_offices': [
            {'city': 'Denver', 'address': '1244 Speer Blvd, Suite 310, Denver, CO 80204', 'phone': '(303) 244-1628'},
        ],
    },

    # ── CONNECTICUT ───────────────────────────────────────────────────
    'Richard Blumenthal': {
        'state': 'CT', 'party': 'D',
        'suite': 'SH-503', 'dc_phone': '(202) 224-2823',
        'website': 'https://blumenthal.senate.gov',
        'contact_form': 'https://blumenthal.senate.gov/contact',
        'state_offices': [
            {'city': 'Hartford', 'address': '90 State House Square, 10th Floor, Hartford, CT 06103', 'phone': '(860) 258-6940'},
        ],
    },
    'Chris Murphy': {
        'state': 'CT', 'party': 'D',
        'suite': 'SH-136', 'dc_phone': '(202) 224-4041',
        'website': 'https://murphy.senate.gov',
        'contact_form': 'https://murphy.senate.gov/contact',
        'state_offices': [
            {'city': 'Hartford', 'address': '120 Huyshope Ave, Suite 401, Hartford, CT 06106', 'phone': '(860) 549-8463'},
        ],
    },

    # ── DELAWARE ──────────────────────────────────────────────────────
    'Chris Coons': {
        'state': 'DE', 'party': 'D',
        'suite': 'SR-218', 'dc_phone': '(202) 224-5042',
        'website': 'https://coons.senate.gov',
        'contact_form': 'https://coons.senate.gov/contact',
        'state_offices': [
            {'city': 'Wilmington', 'address': '1105 N Market St, Suite 100, Wilmington, DE 19801', 'phone': '(302) 573-6345'},
        ],
    },
    'Lisa Blunt Rochester': {
        'state': 'DE', 'party': 'D',
        'suite': 'SH-513', 'dc_phone': '(202) 224-2441',
        'website': 'https://bluntrochester.senate.gov',
        'contact_form': 'https://bluntrochester.senate.gov/contact',
        'state_offices': [
            {'city': 'Wilmington', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── FLORIDA ───────────────────────────────────────────────────────
    'Rick Scott': {
        'state': 'FL', 'party': 'R',
        'suite': 'SH-110', 'dc_phone': '(202) 224-5274',
        'website': 'https://rickscott.senate.gov',
        'contact_form': 'https://rickscott.senate.gov/contact',
        'state_offices': [
            {'city': 'Orlando', 'address': '225 E Robinson St, Suite 410, Orlando, FL 32801', 'phone': '(407) 872-7161'},
            {'city': 'Miami', 'address': '2000 PGA Blvd, Suite 5050, North Palm Beach, FL 33408', 'phone': '(561) 514-0189'},
            {'city': 'Tampa', 'address': '801 N Florida Ave, Suite 421, Tampa, FL 33602', 'phone': '(813) 225-7040'},
        ],
    },
    'Ashley Moody': {
        'state': 'FL', 'party': 'R',
        'suite': 'SR-387', 'dc_phone': '(202) 224-3041',
        'website': 'https://moody.senate.gov',
        'contact_form': 'https://moody.senate.gov/contact',
        'state_offices': [
            {'city': 'Tampa', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── GEORGIA ───────────────────────────────────────────────────────
    'Jon Ossoff': {
        'state': 'GA', 'party': 'D',
        'suite': 'SH-317', 'dc_phone': '(202) 224-3521',
        'website': 'https://ossoff.senate.gov',
        'contact_form': 'https://ossoff.senate.gov/contact',
        'state_offices': [
            {'city': 'Atlanta', 'address': '3280 Peachtree Rd NE, Suite 2640, Atlanta, GA 30305', 'phone': '(470) 786-7800'},
        ],
    },
    'Raphael Warnock': {
        'state': 'GA', 'party': 'D',
        'suite': 'SH-717', 'dc_phone': '(202) 224-3643',
        'website': 'https://warnock.senate.gov',
        'contact_form': 'https://warnock.senate.gov/contact',
        'state_offices': [
            {'city': 'Atlanta', 'address': '3280 Peachtree Rd NE, Suite 1000, Atlanta, GA 30305', 'phone': '(770) 694-7828'},
        ],
    },

    # ── HAWAII ────────────────────────────────────────────────────────
    'Brian Schatz': {
        'state': 'HI', 'party': 'D',
        'suite': 'SH-722', 'dc_phone': '(202) 224-3934',
        'website': 'https://schatz.senate.gov',
        'contact_form': 'https://schatz.senate.gov/contact',
        'state_offices': [
            {'city': 'Honolulu', 'address': '300 Ala Moana Blvd, Room 7-212, Honolulu, HI 96850', 'phone': '(808) 523-2061'},
        ],
    },
    'Mazie Hirono': {
        'state': 'HI', 'party': 'D',
        'suite': 'SH-109', 'dc_phone': '(202) 224-6361',
        'website': 'https://hirono.senate.gov',
        'contact_form': 'https://hirono.senate.gov/contact',
        'state_offices': [
            {'city': 'Honolulu', 'address': '300 Ala Moana Blvd, Room 3-106, Honolulu, HI 96850', 'phone': '(808) 522-8970'},
        ],
    },

    # ── IDAHO ─────────────────────────────────────────────────────────
    'Mike Crapo': {
        'state': 'ID', 'party': 'R',
        'suite': 'SD-239', 'dc_phone': '(202) 224-6142',
        'website': 'https://crapo.senate.gov',
        'contact_form': 'https://crapo.senate.gov/contact',
        'state_offices': [
            {'city': 'Boise', 'address': '251 E Front St, Suite 205, Boise, ID 83702', 'phone': '(208) 334-1776'},
            {'city': 'Idaho Falls', 'address': '410 Memorial Dr, Suite 204, Idaho Falls, ID 83402', 'phone': '(208) 522-9779'},
        ],
    },
    'Jim Risch': {
        'state': 'ID', 'party': 'R',
        'suite': 'SR-483', 'dc_phone': '(202) 224-2752',
        'website': 'https://risch.senate.gov',
        'contact_form': 'https://risch.senate.gov/contact',
        'state_offices': [
            {'city': 'Boise', 'address': '350 N 9th St, Suite 302, Boise, ID 83702', 'phone': '(208) 342-7985'},
        ],
    },

    # ── ILLINOIS ──────────────────────────────────────────────────────
    'Dick Durbin': {
        'state': 'IL', 'party': 'D',
        'suite': 'SH-711', 'dc_phone': '(202) 224-2152',
        'website': 'https://durbin.senate.gov',
        'contact_form': 'https://durbin.senate.gov/contact',
        'state_offices': [
            {'city': 'Chicago', 'address': '230 S Dearborn St, Suite 3892, Chicago, IL 60604', 'phone': '(312) 353-4952'},
            {'city': 'Springfield', 'address': '525 S 8th St, Springfield, IL 62703', 'phone': '(217) 492-4062'},
        ],
    },
    'Tammy Duckworth': {
        'state': 'IL', 'party': 'D',
        'suite': 'SH-524', 'dc_phone': '(202) 224-2854',
        'website': 'https://duckworth.senate.gov',
        'contact_form': 'https://duckworth.senate.gov/contact',
        'state_offices': [
            {'city': 'Chicago', 'address': '230 S Dearborn St, Suite 3900, Chicago, IL 60604', 'phone': '(312) 886-3506'},
        ],
    },

    # ── INDIANA ───────────────────────────────────────────────────────
    'Jim Banks': {
        'state': 'IN', 'party': 'R',
        'suite': 'SH-303', 'dc_phone': '(202) 224-4814',
        'website': 'https://banks.senate.gov',
        'contact_form': 'https://banks.senate.gov/contact',
        'state_offices': [
            {'city': 'Indianapolis', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },
    'Todd Young': {
        'state': 'IN', 'party': 'R',
        'suite': 'SD-185', 'dc_phone': '(202) 224-5623',
        'website': 'https://young.senate.gov',
        'contact_form': 'https://young.senate.gov/contact',
        'state_offices': [
            {'city': 'Indianapolis', 'address': '251 N Illinois St, Suite 120, Indianapolis, IN 46204', 'phone': '(317) 226-6700'},
        ],
    },

    # ── IOWA ──────────────────────────────────────────────────────────
    'Chuck Grassley': {
        'state': 'IA', 'party': 'R',
        'suite': 'SH-135', 'dc_phone': '(202) 224-3744',
        'website': 'https://grassley.senate.gov',
        'contact_form': 'https://grassley.senate.gov/contact',
        'state_offices': [
            {'city': 'Des Moines', 'address': '721 Federal Bldg, 210 Walnut St, Des Moines, IA 50309', 'phone': '(515) 288-1145'},
        ],
    },
    'Joni Ernst': {
        'state': 'IA', 'party': 'R',
        'suite': 'SR-260', 'dc_phone': '(202) 224-3254',
        'website': 'https://ernst.senate.gov',
        'contact_form': 'https://ernst.senate.gov/contact',
        'state_offices': [
            {'city': 'Des Moines', 'address': '733 Federal Bldg, 210 Walnut St, Des Moines, IA 50309', 'phone': '(515) 284-4574'},
        ],
    },

    # ── KANSAS ────────────────────────────────────────────────────────
    'Jerry Moran': {
        'state': 'KS', 'party': 'R',
        'suite': 'SD-521', 'dc_phone': '(202) 224-6521',
        'website': 'https://moran.senate.gov',
        'contact_form': 'https://moran.senate.gov/contact',
        'state_offices': [
            {'city': 'Olathe', 'address': '23600 College Blvd, Suite 201, Olathe, KS 66061', 'phone': '(913) 393-0711'},
        ],
    },
    'Roger Marshall': {
        'state': 'KS', 'party': 'R',
        'suite': 'SR-479A', 'dc_phone': '(202) 224-4774',
        'website': 'https://marshall.senate.gov',
        'contact_form': 'https://marshall.senate.gov/contact',
        'state_offices': [
            {'city': 'Topeka', 'address': '100 Military Plaza, Suite 203, Dodge City, KS 67801', 'phone': '(620) 227-2244'},
        ],
    },

    # ── KENTUCKY ──────────────────────────────────────────────────────
    'Mitch McConnell': {
        'state': 'KY', 'party': 'R',
        'suite': 'SR-317', 'dc_phone': '(202) 224-2541',
        'website': 'https://mcconnell.senate.gov',
        'contact_form': 'https://mcconnell.senate.gov/contact',
        'state_offices': [
            {'city': 'Louisville', 'address': '601 W Broadway, Suite 630, Louisville, KY 40202', 'phone': '(502) 582-6304'},
        ],
    },
    'Rand Paul': {
        'state': 'KY', 'party': 'R',
        'suite': 'SR-295', 'dc_phone': '(202) 224-4343',
        'website': 'https://paul.senate.gov',
        'contact_form': 'https://paul.senate.gov/contact',
        'state_offices': [
            {'city': 'Bowling Green', 'address': '1029 State St, Bowling Green, KY 42101', 'phone': '(270) 782-8303'},
        ],
    },

    # ── LOUISIANA ─────────────────────────────────────────────────────
    'Bill Cassidy': {
        'state': 'LA', 'party': 'R',
        'suite': 'SD-455', 'dc_phone': '(202) 224-5824',
        'website': 'https://cassidy.senate.gov',
        'contact_form': 'https://cassidy.senate.gov/contact',
        'state_offices': [
            {'city': 'Baton Rouge', 'address': '5555 Hilton Ave, Suite 100, Baton Rouge, LA 70808', 'phone': '(225) 929-7711'},
            {'city': 'Metairie', 'address': '3421 N Causeway Blvd, Suite 204, Metairie, LA 70002', 'phone': '(504) 838-0130'},
        ],
    },
    'John Kennedy': {
        'state': 'LA', 'party': 'R',
        'suite': 'SR-437', 'dc_phone': '(202) 224-4623',
        'website': 'https://kennedy.senate.gov',
        'contact_form': 'https://kennedy.senate.gov/contact',
        'state_offices': [
            {'city': 'Baton Rouge', 'address': '7932 Wrenwood Blvd, Suite A, Baton Rouge, LA 70809', 'phone': '(225) 926-8033'},
        ],
    },

    # ── MAINE ─────────────────────────────────────────────────────────
    'Susan Collins': {
        'state': 'ME', 'party': 'R',
        'suite': 'SD-413', 'dc_phone': '(202) 224-2523',
        'website': 'https://collins.senate.gov',
        'contact_form': 'https://collins.senate.gov/contact',
        'state_offices': [
            {'city': 'Bangor', 'address': '202 Harlow St, Suite 20100, Bangor, ME 04401', 'phone': '(207) 945-0417'},
            {'city': 'Portland', 'address': '1 Canal Plaza, Suite 802, Portland, ME 04101', 'phone': '(207) 780-3575'},
        ],
    },
    'Angus King': {
        'state': 'ME', 'party': 'I',
        'suite': 'SH-133', 'dc_phone': '(202) 224-5344',
        'website': 'https://king.senate.gov',
        'contact_form': 'https://king.senate.gov/contact',
        'state_offices': [
            {'city': 'Augusta', 'address': '4 Gabriel Dr, Suite 3, Augusta, ME 04330', 'phone': '(207) 622-8292'},
            {'city': 'Portland', 'address': '383 US Route 1, Suite 1C, Scarborough, ME 04074', 'phone': '(207) 883-1588'},
        ],
    },

    # ── MARYLAND ──────────────────────────────────────────────────────
    'Chris Van Hollen': {
        'state': 'MD', 'party': 'D',
        'suite': 'SH-730', 'dc_phone': '(202) 224-4654',
        'website': 'https://vanhollen.senate.gov',
        'contact_form': 'https://vanhollen.senate.gov/contact',
        'state_offices': [
            {'city': 'Rockville', 'address': '111 Rockville Pike, Suite 960, Rockville, MD 20850', 'phone': '(301) 545-1500'},
            {'city': 'Baltimore', 'address': '60 W St, Suite 107, Annapolis, MD 21401', 'phone': '(410) 263-1325'},
        ],
    },
    'Angela Alsobrooks': {
        'state': 'MD', 'party': 'D',
        'suite': 'SR-374', 'dc_phone': '(202) 224-4524',
        'website': 'https://alsobrooks.senate.gov',
        'contact_form': 'https://alsobrooks.senate.gov/contact',
        'state_offices': [
            {'city': 'Baltimore', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── MASSACHUSETTS ─────────────────────────────────────────────────
    'Elizabeth Warren': {
        'state': 'MA', 'party': 'D',
        'suite': 'SH-311', 'dc_phone': '(202) 224-4543',
        'website': 'https://warren.senate.gov',
        'contact_form': 'https://warren.senate.gov/contact',
        'state_offices': [
            {'city': 'Boston', 'address': '2400 JFK Federal Bldg, 15 New Sudbury St, Boston, MA 02203', 'phone': '(617) 565-3170'},
            {'city': 'Springfield', 'address': '1550 Main St, Suite 406, Springfield, MA 01103', 'phone': '(413) 788-2690'},
        ],
    },
    'Ed Markey': {
        'state': 'MA', 'party': 'D',
        'suite': 'SD-255', 'dc_phone': '(202) 224-2742',
        'website': 'https://markey.senate.gov',
        'contact_form': 'https://markey.senate.gov/contact',
        'state_offices': [
            {'city': 'Boston', 'address': '975 JFK Federal Bldg, 15 New Sudbury St, Boston, MA 02203', 'phone': '(617) 565-8519'},
        ],
    },

    # ── MICHIGAN ──────────────────────────────────────────────────────
    'Gary Peters': {
        'state': 'MI', 'party': 'D',
        'suite': 'SH-724', 'dc_phone': '(202) 224-6221',
        'website': 'https://peters.senate.gov',
        'contact_form': 'https://peters.senate.gov/contact',
        'state_offices': [
            {'city': 'Detroit', 'address': 'Patrick V. McNamara Federal Bldg, 477 Michigan Ave, Suite 1837, Detroit, MI 48226', 'phone': '(313) 226-6020'},
        ],
    },
    'Elissa Slotkin': {
        'state': 'MI', 'party': 'D',
        'suite': 'SR-291', 'dc_phone': '(202) 224-4822',
        'website': 'https://slotkin.senate.gov',
        'contact_form': 'https://slotkin.senate.gov/contact',
        'state_offices': [
            {'city': 'Lansing', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── MINNESOTA ─────────────────────────────────────────────────────
    'Amy Klobuchar': {
        'state': 'MN', 'party': 'D',
        'suite': 'SD-425', 'dc_phone': '(202) 224-3244',
        'website': 'https://klobuchar.senate.gov',
        'contact_form': 'https://klobuchar.senate.gov/contact',
        'state_offices': [
            {'city': 'Minneapolis', 'address': '1200 Washington Ave S, Suite 250, Minneapolis, MN 55415', 'phone': '(612) 727-5220'},
        ],
    },
    'Tina Smith': {
        'state': 'MN', 'party': 'D',
        'suite': 'SH-720', 'dc_phone': '(202) 224-5641',
        'website': 'https://smith.senate.gov',
        'contact_form': 'https://smith.senate.gov/contact',
        'state_offices': [
            {'city': 'St. Paul', 'address': '60 E Plato Blvd, Suite 220, St. Paul, MN 55107', 'phone': '(651) 221-1016'},
        ],
    },

    # ── MISSISSIPPI ───────────────────────────────────────────────────
    'Roger Wicker': {
        'state': 'MS', 'party': 'R',
        'suite': 'SR-425', 'dc_phone': '(202) 224-6253',
        'website': 'https://wicker.senate.gov',
        'contact_form': 'https://wicker.senate.gov/contact',
        'state_offices': [
            {'city': 'Jackson', 'address': '190 E Capitol St, Suite 550, Jackson, MS 39201', 'phone': '(601) 965-4644'},
        ],
    },
    'Cindy Hyde-Smith': {
        'state': 'MS', 'party': 'R',
        'suite': 'SH-528', 'dc_phone': '(202) 224-5054',
        'website': 'https://hydesmith.senate.gov',
        'contact_form': 'https://hydesmith.senate.gov/contact',
        'state_offices': [
            {'city': 'Jackson', 'address': '190 E Capitol St, Suite 550, Jackson, MS 39201', 'phone': '(601) 965-4459'},
        ],
    },

    # ── MISSOURI ──────────────────────────────────────────────────────
    'Josh Hawley': {
        'state': 'MO', 'party': 'R',
        'suite': 'SR-381', 'dc_phone': '(202) 224-6154',
        'website': 'https://hawley.senate.gov',
        'contact_form': 'https://hawley.senate.gov/contact',
        'state_offices': [
            {'city': 'Kansas City', 'address': '400 E 9th St, Suite 9350, Kansas City, MO 64106', 'phone': '(816) 960-4694'},
        ],
    },
    'Eric Schmitt': {
        'state': 'MO', 'party': 'R',
        'suite': 'SR-404', 'dc_phone': '(202) 224-5721',
        'website': 'https://schmitt.senate.gov',
        'contact_form': 'https://schmitt.senate.gov/contact',
        'state_offices': [
            {'city': 'St. Louis', 'address': '111 S 10th St, Suite 23.306, St. Louis, MO 63102', 'phone': '(314) 877-8706'},
        ],
    },

    # ── MONTANA ───────────────────────────────────────────────────────
    'Steve Daines': {
        'state': 'MT', 'party': 'R',
        'suite': 'SH-320', 'dc_phone': '(202) 224-2651',
        'website': 'https://daines.senate.gov',
        'contact_form': 'https://daines.senate.gov/contact',
        'state_offices': [
            {'city': 'Billings', 'address': '222 N 32nd St, Suite 100, Billings, MT 59101', 'phone': '(406) 245-6822'},
        ],
    },
    'Tim Sheehy': {
        'state': 'MT', 'party': 'R',
        'suite': 'SR-124', 'dc_phone': '(202) 224-2644',
        'website': 'https://sheehy.senate.gov',
        'contact_form': 'https://sheehy.senate.gov/contact',
        'state_offices': [
            {'city': 'Helena', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── NEBRASKA ──────────────────────────────────────────────────────
    'Deb Fischer': {
        'state': 'NE', 'party': 'R',
        'suite': 'SR-448', 'dc_phone': '(202) 224-6551',
        'website': 'https://fischer.senate.gov',
        'contact_form': 'https://fischer.senate.gov/contact',
        'state_offices': [
            {'city': 'Lincoln', 'address': '440 N 8th St, Suite 120, Lincoln, NE 68508', 'phone': '(402) 441-4600'},
        ],
    },
    'Pete Ricketts': {
        'state': 'NE', 'party': 'R',
        'suite': 'SR-139', 'dc_phone': '(202) 224-4224',
        'website': 'https://ricketts.senate.gov',
        'contact_form': 'https://ricketts.senate.gov/contact',
        'state_offices': [
            {'city': 'Omaha', 'address': '4811 S 132nd St, Suite 301, Omaha, NE 68137', 'phone': '(402) 933-7088'},
        ],
    },

    # ── NEVADA ────────────────────────────────────────────────────────
    'Jacky Rosen': {
        'state': 'NV', 'party': 'D',
        'suite': 'SH-713', 'dc_phone': '(202) 224-6244',
        'website': 'https://rosen.senate.gov',
        'contact_form': 'https://rosen.senate.gov/contact',
        'state_offices': [
            {'city': 'Las Vegas', 'address': '333 Las Vegas Blvd S, Suite 8016, Las Vegas, NV 89101', 'phone': '(702) 388-0205'},
        ],
    },
    'Catherine Cortez Masto': {
        'state': 'NV', 'party': 'D',
        'suite': 'SH-309', 'dc_phone': '(202) 224-3542',
        'website': 'https://cortezmasto.senate.gov',
        'contact_form': 'https://cortezmasto.senate.gov/contact',
        'state_offices': [
            {'city': 'Las Vegas', 'address': '333 Las Vegas Blvd S, Suite 8203, Las Vegas, NV 89101', 'phone': '(702) 388-5020'},
            {'city': 'Reno', 'address': '400 S Virginia St, Suite 902, Reno, NV 89501', 'phone': '(775) 686-5750'},
        ],
    },

    # ── NEW HAMPSHIRE ─────────────────────────────────────────────────
    'Jeanne Shaheen': {
        'state': 'NH', 'party': 'D',
        'suite': 'SH-506', 'dc_phone': '(202) 224-2841',
        'website': 'https://shaheen.senate.gov',
        'contact_form': 'https://shaheen.senate.gov/contact',
        'state_offices': [
            {'city': 'Manchester', 'address': '1589 Elm St, Suite 3, Manchester, NH 03101', 'phone': '(603) 647-7500'},
        ],
    },
    'Maggie Hassan': {
        'state': 'NH', 'party': 'D',
        'suite': 'SH-324', 'dc_phone': '(202) 224-3324',
        'website': 'https://hassan.senate.gov',
        'contact_form': 'https://hassan.senate.gov/contact',
        'state_offices': [
            {'city': 'Manchester', 'address': '1200 Elm St, Suite 2, Manchester, NH 03101', 'phone': '(603) 622-2204'},
        ],
    },

    # ── NEW JERSEY ────────────────────────────────────────────────────
    'Andy Kim': {
        'state': 'NJ', 'party': 'D',
        'suite': 'SH-520', 'dc_phone': '(202) 224-4744',
        'website': 'https://kim.senate.gov',
        'contact_form': 'https://kim.senate.gov/contact',
        'state_offices': [
            {'city': 'Newark', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },
    'Cory Booker': {
        'state': 'NJ', 'party': 'D',
        'suite': 'SH-306', 'dc_phone': '(202) 224-3224',
        'website': 'https://booker.senate.gov',
        'contact_form': 'https://booker.senate.gov/contact',
        'state_offices': [
            {'city': 'Newark', 'address': 'One Gateway Center, Suite 1100, Newark, NJ 07102', 'phone': '(973) 639-8700'},
            {'city': 'Camden', 'address': 'One Port Center, 2 Riverside Dr, Suite 505, Camden, NJ 08101', 'phone': '(856) 338-8922'},
        ],
    },

    # ── NEW MEXICO ────────────────────────────────────────────────────
    'Martin Heinrich': {
        'state': 'NM', 'party': 'D',
        'suite': 'SH-709', 'dc_phone': '(202) 224-5521',
        'website': 'https://heinrich.senate.gov',
        'contact_form': 'https://heinrich.senate.gov/contact',
        'state_offices': [
            {'city': 'Albuquerque', 'address': '400 Gold Ave SW, Suite 1080, Albuquerque, NM 87102', 'phone': '(505) 346-6601'},
        ],
    },
    'Ben Ray Lujan': {
        'state': 'NM', 'party': 'D',
        'suite': 'SR-498', 'dc_phone': '(202) 224-6621',
        'website': 'https://lujan.senate.gov',
        'contact_form': 'https://lujan.senate.gov/contact',
        'state_offices': [
            {'city': 'Albuquerque', 'address': '400 Gold Ave SW, Suite 680, Albuquerque, NM 87102', 'phone': '(505) 346-6791'},
        ],
    },

    # ── NEW YORK ──────────────────────────────────────────────────────
    'Chuck Schumer': {
        'state': 'NY', 'party': 'D',
        'suite': 'SH-322', 'dc_phone': '(202) 224-6542',
        'website': 'https://schumer.senate.gov',
        'contact_form': 'https://schumer.senate.gov/contact',
        'state_offices': [
            {'city': 'New York', 'address': '780 Third Ave, Suite 2301, New York, NY 10017', 'phone': '(212) 486-4430'},
        ],
    },
    'Kirsten Gillibrand': {
        'state': 'NY', 'party': 'D',
        'suite': 'SR-478', 'dc_phone': '(202) 224-4451',
        'website': 'https://gillibrand.senate.gov',
        'contact_form': 'https://gillibrand.senate.gov/contact',
        'state_offices': [
            {'city': 'New York', 'address': '780 Third Ave, Suite 2601, New York, NY 10017', 'phone': '(212) 688-6262'},
        ],
    },

    # ── NORTH CAROLINA ────────────────────────────────────────────────
    'Thom Tillis': {
        'state': 'NC', 'party': 'R',
        'suite': 'SD-113', 'dc_phone': '(202) 224-6342',
        'website': 'https://tillis.senate.gov',
        'contact_form': 'https://tillis.senate.gov/contact',
        'state_offices': [
            {'city': 'Charlotte', 'address': '9300 Harris Corners Pkwy, Suite 170, Charlotte, NC 28269', 'phone': '(704) 509-9087'},
        ],
    },
    'Ted Budd': {
        'state': 'NC', 'party': 'R',
        'suite': 'SR-354', 'dc_phone': '(202) 224-3154',
        'website': 'https://budd.senate.gov',
        'contact_form': 'https://budd.senate.gov/contact',
        'state_offices': [
            {'city': 'Winston-Salem', 'address': '251 N Main St, Suite 630, Winston-Salem, NC 27101', 'phone': '(336) 998-1998'},
        ],
    },

    # ── NORTH DAKOTA ──────────────────────────────────────────────────
    'John Hoeven': {
        'state': 'ND', 'party': 'R',
        'suite': 'SR-338', 'dc_phone': '(202) 224-2551',
        'website': 'https://hoeven.senate.gov',
        'contact_form': 'https://hoeven.senate.gov/contact',
        'state_offices': [
            {'city': 'Bismarck', 'address': '220 E Rosser Ave, Room 312, Bismarck, ND 58501', 'phone': '(701) 250-4618'},
        ],
    },
    'Kevin Cramer': {
        'state': 'ND', 'party': 'R',
        'suite': 'SH-313', 'dc_phone': '(202) 224-2043',
        'website': 'https://cramer.senate.gov',
        'contact_form': 'https://cramer.senate.gov/contact',
        'state_offices': [
            {'city': 'Bismarck', 'address': '220 E Rosser Ave, Room 228, Bismarck, ND 58501', 'phone': '(701) 232-8030'},
        ],
    },

    # ── OHIO ──────────────────────────────────────────────────────────
    'Jon Husted': {
        'state': 'OH', 'party': 'R',
        'suite': 'SR-304', 'dc_phone': '(202) 224-3353',
        'website': 'https://husted.senate.gov',
        'contact_form': 'https://husted.senate.gov/contact',
        'state_offices': [
            {'city': 'Columbus', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },
    'Bernie Moreno': {
        'state': 'OH', 'party': 'R',
        'suite': 'SR-284', 'dc_phone': '(202) 224-2315',
        'website': 'https://moreno.senate.gov',
        'contact_form': 'https://moreno.senate.gov/contact',
        'state_offices': [
            {'city': 'Cleveland', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── OKLAHOMA ──────────────────────────────────────────────────────
    'James Lankford': {
        'state': 'OK', 'party': 'R',
        'suite': 'SH-731', 'dc_phone': '(202) 224-5754',
        'website': 'https://lankford.senate.gov',
        'contact_form': 'https://lankford.senate.gov/contact',
        'state_offices': [
            {'city': 'Oklahoma City', 'address': '1015 N Broadway Ave, Suite 310, Oklahoma City, OK 73102', 'phone': '(405) 231-4941'},
        ],
    },
    'Markwayne Mullin': {
        'state': 'OK', 'party': 'R',
        'suite': 'SH-330', 'dc_phone': '(202) 224-4721',
        'website': 'https://mullin.senate.gov',
        'contact_form': 'https://mullin.senate.gov/contact',
        'state_offices': [
            {'city': 'Tulsa', 'address': '1 W 3rd St, Suite 305, Tulsa, OK 74103', 'phone': '(918) 748-5111'},
        ],
    },

    # ── OREGON ────────────────────────────────────────────────────────
    'Ron Wyden': {
        'state': 'OR', 'party': 'D',
        'suite': 'SD-221', 'dc_phone': '(202) 224-5244',
        'website': 'https://wyden.senate.gov',
        'contact_form': 'https://wyden.senate.gov/contact',
        'state_offices': [
            {'city': 'Portland', 'address': '911 NE 11th Ave, Suite 630, Portland, OR 97232', 'phone': '(503) 326-7525'},
            {'city': 'Eugene', 'address': '405 E 8th Ave, Suite 2020, Eugene, OR 97401', 'phone': '(541) 431-0229'},
            {'city': 'Salem', 'address': '707 13th St SE, Suite 285, Salem, OR 97301', 'phone': '(503) 589-4555'},
            {'city': 'Bend', 'address': '131 NW Hawthorne Ave, Suite 107, Bend, OR 97703', 'phone': '(541) 330-9142'},
        ],
    },
    'Jeff Merkley': {
        'state': 'OR', 'party': 'D',
        'suite': 'SH-531', 'dc_phone': '(202) 224-3753',
        'website': 'https://merkley.senate.gov',
        'contact_form': 'https://merkley.senate.gov/contact',
        'state_offices': [
            {'city': 'Portland', 'address': '121 SW Salmon St, Suite 1400, Portland, OR 97204', 'phone': '(503) 326-3386'},
        ],
    },

    # ── PENNSYLVANIA ──────────────────────────────────────────────────
    'John Fetterman': {
        'state': 'PA', 'party': 'D',
        'suite': 'SR-142', 'dc_phone': '(202) 224-4254',
        'website': 'https://fetterman.senate.gov',
        'contact_form': 'https://fetterman.senate.gov/contact',
        'state_offices': [
            {'city': 'Philadelphia', 'address': 'TBD', 'phone': 'TBD'},
            {'city': 'Pittsburgh', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },
    'Dave McCormick': {
        'state': 'PA', 'party': 'R',
        'suite': 'SH-702', 'dc_phone': '(202) 224-6324',
        'website': 'https://mccormick.senate.gov',
        'contact_form': 'https://mccormick.senate.gov/contact',
        'state_offices': [
            {'city': 'Philadelphia', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── RHODE ISLAND ──────────────────────────────────────────────────
    'Jack Reed': {
        'state': 'RI', 'party': 'D',
        'suite': 'SH-728', 'dc_phone': '(202) 224-4642',
        'website': 'https://reed.senate.gov',
        'contact_form': 'https://reed.senate.gov/contact',
        'state_offices': [
            {'city': 'Providence', 'address': '1000 Chapel View Blvd, Suite 290, Cranston, RI 02920', 'phone': '(401) 943-3100'},
        ],
    },
    'Sheldon Whitehouse': {
        'state': 'RI', 'party': 'D',
        'suite': 'SH-530', 'dc_phone': '(202) 224-2921',
        'website': 'https://whitehouse.senate.gov',
        'contact_form': 'https://whitehouse.senate.gov/contact',
        'state_offices': [
            {'city': 'Providence', 'address': '170 Westminster St, Suite 1100, Providence, RI 02903', 'phone': '(401) 453-5294'},
        ],
    },

    # ── SOUTH CAROLINA ────────────────────────────────────────────────
    'Lindsey Graham': {
        'state': 'SC', 'party': 'R',
        'suite': 'SR-211', 'dc_phone': '(202) 224-5972',
        'website': 'https://lgraham.senate.gov',
        'contact_form': 'https://lgraham.senate.gov/contact',
        'state_offices': [
            {'city': 'Greenville', 'address': '130 S Main St, Suite 700, Greenville, SC 29601', 'phone': '(864) 250-1417'},
            {'city': 'Columbia', 'address': '508 Hampton St, Suite 202, Columbia, SC 29201', 'phone': '(803) 933-0112'},
        ],
    },
    'Tim Scott': {
        'state': 'SC', 'party': 'R',
        'suite': 'SH-104', 'dc_phone': '(202) 224-6121',
        'website': 'https://scott.senate.gov',
        'contact_form': 'https://scott.senate.gov/contact',
        'state_offices': [
            {'city': 'Columbia', 'address': '1301 Gervais St, Suite 825, Columbia, SC 29201', 'phone': '(803) 771-6112'},
            {'city': 'North Charleston', 'address': '2500 City Hall Lane, Suite 1, North Charleston, SC 29406', 'phone': '(843) 727-4525'},
        ],
    },

    # ── SOUTH DAKOTA ──────────────────────────────────────────────────
    'John Thune': {
        'state': 'SD', 'party': 'R',
        'suite': 'SD-511', 'dc_phone': '(202) 224-2321',
        'website': 'https://thune.senate.gov',
        'contact_form': 'https://thune.senate.gov/contact',
        'state_offices': [
            {'city': 'Sioux Falls', 'address': '5015 S Bur Oak Place, Sioux Falls, SD 57108', 'phone': '(605) 334-9596'},
            {'city': 'Rapid City', 'address': '246 Founders Park Dr, Suite 102, Rapid City, SD 57701', 'phone': '(605) 348-7551'},
        ],
    },
    'Mike Rounds': {
        'state': 'SD', 'party': 'R',
        'suite': 'SH-716', 'dc_phone': '(202) 224-5842',
        'website': 'https://rounds.senate.gov',
        'contact_form': 'https://rounds.senate.gov/contact',
        'state_offices': [
            {'city': 'Sioux Falls', 'address': '1313 W Main St, Rapid City, SD 57701', 'phone': '(605) 343-5035'},
        ],
    },

    # ── TENNESSEE ─────────────────────────────────────────────────────
    'Marsha Blackburn': {
        'state': 'TN', 'party': 'R',
        'suite': 'SD-357', 'dc_phone': '(202) 224-3344',
        'website': 'https://blackburn.senate.gov',
        'contact_form': 'https://blackburn.senate.gov/contact',
        'state_offices': [
            {'city': 'Nashville', 'address': '10 W MLK Blvd, 6th Floor, Chattanooga, TN 37402', 'phone': '(423) 541-2939'},
        ],
    },
    'Bill Hagerty': {
        'state': 'TN', 'party': 'R',
        'suite': 'SR-251', 'dc_phone': '(202) 224-4944',
        'website': 'https://hagerty.senate.gov',
        'contact_form': 'https://hagerty.senate.gov/contact',
        'state_offices': [
            {'city': 'Nashville', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── TEXAS ─────────────────────────────────────────────────────────
    'John Cornyn': {
        'state': 'TX', 'party': 'R',
        'suite': 'SH-517', 'dc_phone': '(202) 224-2934',
        'website': 'https://cornyn.senate.gov',
        'contact_form': 'https://cornyn.senate.gov/contact',
        'state_offices': [
            {'city': 'Houston', 'address': '5300 Memorial Dr, Suite 980, Houston, TX 77007', 'phone': '(713) 572-3337'},
            {'city': 'Dallas', 'address': '5001 Spring Valley Rd, Suite 1125E, Dallas, TX 75244', 'phone': '(972) 239-1310'},
            {'city': 'San Antonio', 'address': '600 Navarro St, Suite 210, San Antonio, TX 78205', 'phone': '(210) 224-7485'},
            {'city': 'Austin', 'address': '221 W 6th St, Suite 1530, Austin, TX 78701', 'phone': '(512) 469-6034'},
        ],
    },
    'Ted Cruz': {
        'state': 'TX', 'party': 'R',
        'suite': 'SR-167', 'dc_phone': '(202) 224-5922',
        'website': 'https://cruz.senate.gov',
        'contact_form': 'https://cruz.senate.gov/contact',
        'state_offices': [
            {'city': 'Houston', 'address': '808 Travis St, Suite 1420, Houston, TX 77002', 'phone': '(713) 718-3057'},
            {'city': 'Dallas', 'address': 'Lee Park Tower II, 3626 N Hall St, Suite 410, Dallas, TX 75219', 'phone': '(214) 599-8749'},
            {'city': 'San Antonio', 'address': '9901 IH-10W, Suite 950, San Antonio, TX 78230', 'phone': '(210) 340-2885'},
        ],
    },

    # ── UTAH ──────────────────────────────────────────────────────────
    'Mike Lee': {
        'state': 'UT', 'party': 'R',
        'suite': 'SR-363', 'dc_phone': '(202) 224-5444',
        'website': 'https://lee.senate.gov',
        'contact_form': 'https://lee.senate.gov/contact',
        'state_offices': [
            {'city': 'Salt Lake City', 'address': '125 S State St, Suite 4225, Salt Lake City, UT 84138', 'phone': '(801) 524-5933'},
        ],
    },
    'John Curtis': {
        'state': 'UT', 'party': 'R',
        'suite': 'SH-502', 'dc_phone': '(202) 224-5251',
        'website': 'https://curtis.senate.gov',
        'contact_form': 'https://curtis.senate.gov/contact',
        'state_offices': [
            {'city': 'Salt Lake City', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── VERMONT ───────────────────────────────────────────────────────
    'Bernie Sanders': {
        'state': 'VT', 'party': 'I',
        'suite': 'SD-332', 'dc_phone': '(202) 224-5141',
        'website': 'https://sanders.senate.gov',
        'contact_form': 'https://sanders.senate.gov/contact',
        'state_offices': [
            {'city': 'Burlington', 'address': '1 Church St, 3rd Floor, Burlington, VT 05401', 'phone': '(802) 862-0697'},
            {'city': 'St. Johnsbury', 'address': '357 Western Ave, Suite 1B, St. Johnsbury, VT 05819', 'phone': '(802) 748-9269'},
        ],
    },
    'Peter Welch': {
        'state': 'VT', 'party': 'D',
        'suite': 'SR-115', 'dc_phone': '(202) 224-4242',
        'website': 'https://welch.senate.gov',
        'contact_form': 'https://welch.senate.gov/contact',
        'state_offices': [
            {'city': 'Burlington', 'address': '128 Lakeside Ave, Suite 235, Burlington, VT 05401', 'phone': '(802) 652-2450'},
        ],
    },

    # ── VIRGINIA ──────────────────────────────────────────────────────
    'Mark Warner': {
        'state': 'VA', 'party': 'D',
        'suite': 'SH-703', 'dc_phone': '(202) 224-2023',
        'website': 'https://warner.senate.gov',
        'contact_form': 'https://warner.senate.gov/contact',
        'state_offices': [
            {'city': 'Richmond', 'address': '919 E Main St, Suite 630, Richmond, VA 23219', 'phone': '(804) 775-2314'},
            {'city': 'Norfolk', 'address': '101 W Main St, Suite 7771, Norfolk, VA 23510', 'phone': '(757) 441-3079'},
        ],
    },
    'Tim Kaine': {
        'state': 'VA', 'party': 'D',
        'suite': 'SR-231', 'dc_phone': '(202) 224-4024',
        'website': 'https://kaine.senate.gov',
        'contact_form': 'https://kaine.senate.gov/contact',
        'state_offices': [
            {'city': 'Richmond', 'address': '919 E Main St, Suite 970, Richmond, VA 23219', 'phone': '(804) 771-2221'},
        ],
    },

    # ── WASHINGTON ────────────────────────────────────────────────────
    'Patty Murray': {
        'state': 'WA', 'party': 'D',
        'suite': 'SR-154', 'dc_phone': '(202) 224-2621',
        'website': 'https://murray.senate.gov',
        'contact_form': 'https://murray.senate.gov/contact',
        'state_offices': [
            {'city': 'Seattle', 'address': '915 2nd Ave, Suite 3206, Seattle, WA 98174', 'phone': '(206) 553-5545'},
        ],
    },
    'Maria Cantwell': {
        'state': 'WA', 'party': 'D',
        'suite': 'SH-511', 'dc_phone': '(202) 224-3441',
        'website': 'https://cantwell.senate.gov',
        'contact_form': 'https://cantwell.senate.gov/contact',
        'state_offices': [
            {'city': 'Seattle', 'address': '915 2nd Ave, Suite 3206, Seattle, WA 98174', 'phone': '(206) 220-6400'},
        ],
    },

    # ── WEST VIRGINIA ─────────────────────────────────────────────────
    'Shelley Moore Capito': {
        'state': 'WV', 'party': 'R',
        'suite': 'SR-170', 'dc_phone': '(202) 224-6472',
        'website': 'https://capito.senate.gov',
        'contact_form': 'https://capito.senate.gov/contact',
        'state_offices': [
            {'city': 'Charleston', 'address': '405 Capitol St, Suite 508, Charleston, WV 25301', 'phone': '(304) 347-5372'},
        ],
    },
    'Jim Justice': {
        'state': 'WV', 'party': 'R',
        'suite': 'SH-509', 'dc_phone': '(202) 224-3954',
        'website': 'https://justice.senate.gov',
        'contact_form': 'https://justice.senate.gov/contact',
        'state_offices': [
            {'city': 'Charleston', 'address': 'TBD', 'phone': 'TBD'},
        ],
    },

    # ── WISCONSIN ─────────────────────────────────────────────────────
    'Ron Johnson': {
        'state': 'WI', 'party': 'R',
        'suite': 'SH-328', 'dc_phone': '(202) 224-5323',
        'website': 'https://ronjohnson.senate.gov',
        'contact_form': 'https://ronjohnson.senate.gov/contact',
        'state_offices': [
            {'city': 'Oshkosh', 'address': '219 Washington Ave, Suite 100, Oshkosh, WI 54901', 'phone': '(920) 230-7250'},
        ],
    },
    'Tammy Baldwin': {
        'state': 'WI', 'party': 'D',
        'suite': 'SH-141', 'dc_phone': '(202) 224-5653',
        'website': 'https://baldwin.senate.gov',
        'contact_form': 'https://baldwin.senate.gov/contact',
        'state_offices': [
            {'city': 'Madison', 'address': '14 W Mifflin St, Suite 207, Madison, WI 53703', 'phone': '(608) 264-5338'},
            {'city': 'Milwaukee', 'address': '633 W Wisconsin Ave, Suite 1920, Milwaukee, WI 53203', 'phone': '(414) 297-4451'},
        ],
    },

    # ── WYOMING ───────────────────────────────────────────────────────
    'John Barrasso': {
        'state': 'WY', 'party': 'R',
        'suite': 'SD-307', 'dc_phone': '(202) 224-6441',
        'website': 'https://barrasso.senate.gov',
        'contact_form': 'https://barrasso.senate.gov/contact',
        'state_offices': [
            {'city': 'Casper', 'address': '100 E B St, Suite 2201, Casper, WY 82602', 'phone': '(307) 261-6413'},
            {'city': 'Cheyenne', 'address': '2120 Capitol Ave, Suite 2013, Cheyenne, WY 82001', 'phone': '(307) 772-2451'},
        ],
    },
    'Cynthia Lummis': {
        'state': 'WY', 'party': 'R',
        'suite': 'SR-127A', 'dc_phone': '(202) 224-3424',
        'website': 'https://lummis.senate.gov',
        'contact_form': 'https://lummis.senate.gov/contact',
        'state_offices': [
            {'city': 'Cheyenne', 'address': '2120 Capitol Ave, Suite 2007, Cheyenne, WY 82001', 'phone': '(307) 772-2480'},
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def get_mailing_address(senator_name):
    """Get full DC mailing address for a senator."""
    contact = SENATE_CONTACTS.get(senator_name)
    if not contact:
        return None
    return expand_suite(contact['suite'])


def get_all_contacts_for_state(state_abbrev):
    """Get both senators for a given state."""
    return {name: info for name, info in SENATE_CONTACTS.items()
            if info['state'] == state_abbrev}


def format_contact_block(senator_name):
    """Generate formatted contact block for a letter."""
    contact = SENATE_CONTACTS.get(senator_name)
    if not contact:
        return f"[Contact information not found for {senator_name}]"

    lines = [
        f"The Honorable {senator_name}",
        f"United States Senate",
        expand_suite(contact['suite']),
        f"",
        f"DC Office: {contact['dc_phone']}",
        f"Website:   {contact['website']}",
        f"Contact:   {contact['contact_form']}",
    ]

    if contact.get('state_offices'):
        primary = contact['state_offices'][0]
        if primary['phone'] != 'TBD':
            lines.append(f"State:     {primary['phone']} ({primary['city']})")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════
#  CONTACT PREFERENCE GUIDE
# ═══════════════════════════════════════════════════════════════════════

CONTACT_PREFERENCE_GUIDE = """
RECOMMENDED CONTACT APPROACH (by recipient stance):

FOR RECEPTIVE SENATORS:
  1. Email via contact form (attach Executive Brief + Policy Brief)
  2. Follow up with DC office phone call to legislative director
  3. Request staff briefing meeting
  4. Send formal letter with white paper to DC office

FOR SKEPTICAL SENATORS:
  1. Formal letter to DC office (solvency-focused framing)
  2. Follow up with DC office phone call to legislative aide
  3. Request 20-minute staff briefing
  4. Provide fiscal impact summary upon request

FOR HOSTILE SENATORS:
  1. Formal letter to DC office (constituent protection framing)
  2. DC office phone call to scheduler (request brief meeting)
  3. State office contact for constituent services angle
  4. No follow-up materials unless specifically requested

GENERAL NOTES:
  - Senators do NOT have publicly listed email addresses
  - All email contact goes through web forms on their .senate.gov sites
  - Contact forms are most responsive for in-state constituents
  - DC phone best for scheduling and legislative staff access
  - State offices best for constituent services and local meetings
  - Formal written letters via USPS carry weight for policy proposals
  - Allow 2-4 weeks for mail delivery (security screening)
"""


if __name__ == '__main__':
    print("=" * 80)
    print("  SENATE CONTACT DIRECTORY — 119th CONGRESS")
    print("=" * 80)

    print(f"\n  Total senators with contact info: {len(SENATE_CONTACTS)}")

    # Verify all have DC phone and suite
    complete = sum(1 for c in SENATE_CONTACTS.values() if c['dc_phone'] != 'TBD')
    websites = sum(1 for c in SENATE_CONTACTS.values() if c['website'])
    state_offices = sum(1 for c in SENATE_CONTACTS.values()
                       if c['state_offices'] and c['state_offices'][0]['phone'] != 'TBD')

    print(f"  DC phone numbers:  {complete}/100")
    print(f"  Websites:          {websites}/100")
    print(f"  State offices:     {state_offices}/100 (with verified phone)")

    print(f"\n  PRIORITY CONTACTS:")
    priority = ['Ron Wyden', 'Bernie Sanders', 'Elizabeth Warren',
                'Sheldon Whitehouse', 'Cory Booker', 'Bill Cassidy',
                'Mike Crapo', 'John Thune', 'Lindsey Graham']
    for name in priority:
        c = SENATE_CONTACTS.get(name, {})
        print(f"    {name:<25} {c.get('suite', 'N/A'):<10} {c.get('dc_phone', 'N/A')}")

    print(f"\n  SAMPLE CONTACT BLOCK:")
    print("  " + "-" * 50)
    for line in format_contact_block('Ron Wyden').split('\n'):
        print(f"  {line}")
    print("  " + "-" * 50)
