import os
import re
import certifi
import airportsdata
import pycountry
import requests
from dotenv import load_dotenv

load_dotenv()

# for windoes to avoid SSL certificate verification error
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

API_KEY = os.getenv("AVIATIOSTACK_API_KEY")

DEFAULT_ORIGIN_DATA = os.getenv("DEFAULT_ORIGINAL_DATA","HYD")

BASE_URL = "http://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load("IATA")

COUNTRY_ALIASES = {
    "usa": "US",
    "united states": "US",
    "uk": "GB",
    "united kingdom": "GB",
    "india": "IN",
    "canada": "CA",
    "australia": "AU",
    "new zealand": "NZ",
    "germany": "DE",
    "france": "FR",
    "italy": "IT",
    "spain": "ES",
    "portugal": "PT",
    "netherlands": "NL",
    "belgium": "BE",
    "switzerland": "CH",
    "austria": "AT",
    "sweden": "SE",
    "norway": "NO",
    "denmark": "DK",
    "finland": "FI",
    "ireland": "IE",
    "poland": "PL",
    "russia": "RU",
    "ukraine": "UA",
    "china": "CN",
    "japan": "JP",
    "south korea": "KR",
    "north korea": "KP",
    "singapore": "SG",
    "malaysia": "MY",
    "indonesia": "ID",
    "thailand": "TH",
    "vietnam": "VN",
    "philippines": "PH",
    "pakistan": "PK",
    "bangladesh": "BD",
    "sri lanka": "LK",
    "nepal": "NP",
    "uae": "AE",
    "united arab emirates": "AE",
    "saudi arabia": "SA",
    "qatar": "QA",
    "kuwait": "KW",
    "oman": "OM",
    "bahrain": "BH",
    "israel": "IL",
    "turkey": "TR",
    "egypt": "EG",
    "south africa": "ZA",
    "nigeria": "NG",
    "kenya": "KE",
    "ghana": "GH",
    "morocco": "MA",
    "ethiopia": "ET",
    "brazil": "BR",
    "argentina": "AR",
    "mexico": "MX",
    "chile": "CL",
    "colombia": "CO",
    "peru": "PE",
    "venezuela": "VE",
    "uruguay": "UY",
    "paraguay": "PY",
    "ecuador": "EC",
    "cuba": "CU",
    "jamaica": "JM",
    "dominican republic": "DO",
    "costa rica": "CR",
    "panama": "PA",
    "afghanistan": "AF",
    "iran": "IR",
    "iraq": "IQ",
    "jordan": "JO",
    "lebanon": "LB",
    "syria": "SY",
    "cyprus": "CY",
    "greece": "GR",
    "romania": "RO",
    "bulgaria": "BG",
    "hungary": "HU",
    "czech republic": "CZ",
    "czechia": "CZ",
    "slovakia": "SK",
    "croatia": "HR",
    "serbia": "RS",
    "slovenia": "SI",
    "iceland": "IS",
    "luxembourg": "LU",
    "estonia": "EE",
    "latvia": "LV",
    "lithuania": "LT",
    "belarus": "BY",
    "georgia": "GE",
    "armenia": "AM",
    "azerbaijan": "AZ",
    "mongolia": "MN",
    "taiwan": "TW"
}

COUNTRY_MAIN_AIRPORTS = {
    "US": "JFK",
    "GB": "LHR",
    "IN": "DEL",
    "CA": "YYZ",
    "AU": "SYD",
    "NZ": "AKL",
    "DE": "FRA",
    "FR": "CDG",
    "IT": "FCO",
    "ES": "MAD",
    "PT": "LIS",
    "NL": "AMS",
    "BE": "BRU",
    "CH": "ZRH",
    "AT": "VIE",
    "SE": "ARN",
    "NO": "OSL",
    "DK": "CPH",
    "FI": "HEL",
    "IE": "DUB",
    "PL": "WAW",
    "RU": "SVO",
    "UA": "KBP",
    "CN": "PEK",
    "JP": "NRT",
    "KR": "ICN",
    "KP": "FNJ",
    "SG": "SIN",
    "MY": "KUL",
    "ID": "CGK",
    "TH": "BKK",
    "VN": "SGN",
    "PH": "MNL",
    "PK": "KHI",
    "BD": "DAC",
    "LK": "CMB",
    "NP": "KTM",
    "AE": "DXB",
    "SA": "JED",
    "QA": "DOH",
    "KW": "KWI",
    "OM": "MCT",
    "BH": "BAH",
    "IL": "TLV",
    "TR": "IST",
    "EG": "CAI",
    "ZA": "JNB",
    "NG": "LOS",
    "KE": "NBO",
    "GH": "ACC",
    "MA": "CMN",
    "ET": "ADD",
    "BR": "GRU",
    "AR": "EZE",
    "MX": "MEX",
    "CL": "SCL",
    "CO": "BOG",
    "PE": "LIM",
    "VE": "CCS",
    "UY": "MVD",
    "PY": "ASU",
    "EC": "UIO",
    "CU": "HAV",
    "JM": "KIN",
    "DO": "SDQ",
    "CR": "SJO",
    "PA": "PTY",
    "AF": "KBL",
    "IR": "IKA",
    "IQ": "BGW",
    "JO": "AMM",
    "LB": "BEY",
    "SY": "DAM",
    "CY": "LCA",
    "GR": "ATH",
    "RO": "OTP",
    "BG": "SOF",
    "HU": "BUD",
    "CZ": "PRG",
    "SK": "BTS",
    "HR": "ZAG",
    "RS": "BEG",
    "SI": "LJU",
    "IS": "KEF",
    "LU": "LUX",
    "EE": "TLL",
    "LV": "RIX",
    "LT": "VNO",
    "BY": "MSQ",
    "GE": "TBS",
    "AM": "EVN",
    "AZ": "GYD",
    "MN": "UBN",
    "TW": "TPE"
}


CITY_MAIN_AIRPORTS = {
    # USA
    "NEW YORK": "JFK",
    "LOS ANGELES": "LAX",
    "CHICAGO": "ORD",
    "SAN FRANCISCO": "SFO",
    "WASHINGTON DC": "IAD",
    "BOSTON": "BOS",
    "MIAMI": "MIA",
    "LAS VEGAS": "LAS",
    "SEATTLE": "SEA",
    "DALLAS": "DFW",
    "HOUSTON": "IAH",
    "ATLANTA": "ATL",
    "ORLANDO": "MCO",
    "DENVER": "DEN",
    "SAN DIEGO": "SAN",

    # UK
    "LONDON": "LHR",
    "MANCHESTER": "MAN",
    "BIRMINGHAM": "BHX",
    "EDINBURGH": "EDI",
    "GLASGOW": "GLA",
    "LIVERPOOL": "LPL",

    # INDIA
    "DELHI": "DEL",
    "MUMBAI": "BOM",
    "BANGALORE": "BLR",
    "BENGALURU": "BLR",
    "HYDERABAD": "HYD",
    "CHENNAI": "MAA",
    "KOLKATA": "CCU",
    "PUNE": "PNQ",
    "AHMEDABAD": "AMD",
    "JAIPUR": "JAI",
    "LUCKNOW": "LKO",
    "BHUBANESWAR": "BBI",
    "KOCHI": "COK",
    "GOA": "GOI",
    "CHANDIGARH": "IXC",
    "INDORE": "IDR",
    "PATNA": "PAT",
    "GUWAHATI": "GAU",
    "VISAKHAPATNAM": "VTZ",
    "SURAT": "STV",
    "NAGPUR": "NAG",
    "VARANASI": "VNS",
    "AMRITSAR": "ATQ",
    "COIMBATORE": "CJB",
    "THIRUVANANTHAPURAM": "TRV",
    "MANGALORE": "IXE",
    "RAIPUR": "RPR",
    "RANCHI": "IXR",

    # Canada
    "TORONTO": "YYZ",
    "VANCOUVER": "YVR",
    "MONTREAL": "YUL",
    "CALGARY": "YYC",
    "OTTAWA": "YOW",

    # Australia
    "SYDNEY": "SYD",
    "MELBOURNE": "MEL",
    "BRISBANE": "BNE",
    "PERTH": "PER",
    "ADELAIDE": "ADL",

    # Japan
    "TOKYO": "HND",
    "OSAKA": "KIX",
    "KYOTO": "KIX",
    "NAGOYA": "NGO",
    "SAPPORO": "CTS",
    "FUKUOKA": "FUK",

    # China
    "BEIJING": "PEK",
    "SHANGHAI": "PVG",
    "GUANGZHOU": "CAN",
    "SHENZHEN": "SZX",
    "CHENGDU": "CTU",
    "HONG KONG": "HKG",

    # South Korea
    "SEOUL": "ICN",
    "BUSAN": "PUS",

    # Singapore and Malaysia
    "SINGAPORE": "SIN",
    "KUALA LUMPUR": "KUL",
    "PENANG": "PEN",
    "LANGKAWI": "LGK",

    # Thailand
    "BANGKOK": "BKK",
    "PHUKET": "HKT",
    "CHIANG MAI": "CNX",
    "PATTAYA": "UTP",

    # Indonesia
    "JAKARTA": "CGK",
    "BALI": "DPS",
    "DENPASAR": "DPS",
    "SURABAYA": "SUB",

    # Vietnam
    "HANOI": "HAN",
    "HO CHI MINH CITY": "SGN",
    "DA NANG": "DAD",

    # UAE
    "DUBAI": "DXB",
    "ABU DHABI": "AUH",
    "SHARJAH": "SHJ",

    # Saudi Arabia
    "RIYADH": "RUH",
    "JEDDAH": "JED",
    "MECCA": "JED",
    "MEDINA": "MED",

    # Qatar
    "DOHA": "DOH",

    # Turkey
    "ISTANBUL": "IST",
    "ANKARA": "ESB",
    "ANTALYA": "AYT",

    # France
    "PARIS": "CDG",
    "NICE": "NCE",
    "LYON": "LYS",
    "MARSEILLE": "MRS",

    # Germany
    "BERLIN": "BER",
    "FRANKFURT": "FRA",
    "MUNICH": "MUC",
    "HAMBURG": "HAM",
    "DUSSELDORF": "DUS",

    # Italy
    "ROME": "FCO",
    "MILAN": "MXP",
    "VENICE": "VCE",
    "FLORENCE": "FLR",

    # Spain
    "MADRID": "MAD",
    "BARCELONA": "BCN",
    "SEVILLE": "SVQ",
    "MALAGA": "AGP",

    # Netherlands
    "AMSTERDAM": "AMS",
    "ROTTERDAM": "RTM",

    # Switzerland
    "ZURICH": "ZRH",
    "GENEVA": "GVA",
    "BASEL": "BSL",

    # Greece
    "ATHENS": "ATH",
    "SANTORINI": "JTR",
    "MYKONOS": "JMK",

    # Portugal
    "LISBON": "LIS",
    "PORTO": "OPO",

    # Ireland
    "DUBLIN": "DUB",

    # Russia
    "MOSCOW": "SVO",
    "SAINT PETERSBURG": "LED",

    # South Africa
    "JOHANNESBURG": "JNB",
    "CAPE TOWN": "CPT",
    "DURBAN": "DUR",

    # Egypt
    "CAIRO": "CAI",
    "LUXOR": "LXR",
    "HURGHADA": "HRG",

    # Brazil
    "SAO PAULO": "GRU",
    "RIO DE JANEIRO": "GIG",
    "BRASILIA": "BSB",

    # Mexico
    "MEXICO CITY": "MEX",
    "CANCUN": "CUN",
    "GUADALAJARA": "GDL",

    # Argentina
    "BUENOS AIRES": "EZE",

    # Other popular destinations
    "ISTANBUL": "IST",
    "CAIRO": "CAI",
    "NAIROBI": "NBO",
    "MARRAKECH": "RAK",
    "CASABLANCA": "CMN",
    "REYKJAVIK": "KEF",
    "OSLO": "OSL",
    "STOCKHOLM": "ARN",
    "COPENHAGEN": "CPH",
    "HELSINKI": "HEL",
    "VIENNA": "VIE",
    "PRAGUE": "PRG",
    "BUDAPEST": "BUD",
    "WARSAW": "WAW",
    "BRUSSELS": "BRU",
    "ATHENS": "ATH",
    "AUCKLAND": "AKL",
    "WELLINGTON": "WLG",
    "KATHMANDU": "KTM",
    "COLOMBO": "CMB",
    "DHAKA": "DAC",
    "KARACHI": "KHI",
    "ISLAMABAD": "ISB",
    "LAHORE": "LHE"
}

def clean_text(text:str)->str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text =re.sub(r"\s+", " ", text)
    stop_words = ["airport", "airports", "city", "cities",
                   "international", "domestic",
                   "main", "major", "hub", "terminal",
                   "flight", "flights", "airline", "airlines",
                   "travel", "travelling", "trip", "trips",
                   "journey", "journeys", "tour", "tours"]
    words = [w for w in text.split()
            if w not in stop_words]
    return " ".join(words).strip()

def country_name_to_code(text:str):
    text = clean_text(text)
    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]
    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        return None

    # Detect country name inside longer text

    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2

    for alias, code in COUNTRY_ALIASES.items():
        if alias in text:
            return code

    return None


def airport_country_matches(airport:dict, country_code:str)->bool:
    airport_country = str(airport.get("country", "")).upper().strip()
    if airport_country == country_code:
        return True

    try:
        country = pycountry.countries.get(alpha_2=airport_country)
        if country and airport_country.lower() == country_code.name.lower():
            return True
    except LookupError:
        pass

    return False



def get_best_airport_for_country(country_code :str):
    preferred = COUNTRY_MAIN_AIRPORTS.get(country_code)

    if preferred and preferred in AIRPORTS: # this condition for when both are preferred and preferred in AIRPORTS are true then it run .
        return preferred

    
# if the preferred is unavaliable then the alternative 
    candidates =[]

    for iata ,airport in AIRPORTS.items():
        if not iata:
            continue

        if airport_country_matches(airport,country_code):
            name = str(airport.get("name","")).lower()
            city = str(airport.get("city","")).lower()

            score =0

            if "international" in name:
                score +=50
            if "intl" in name:
                score +=40
            if "capital" in name:
                score +=20
            if  city:
                score +=5


            candidates.append((score,iata))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]



def resolve_location_to_iata(location:str):
    """
    COnvert country/city/airport/IATA code

    examples:
    Japan->NRT
    united kingdom-> GB
    DELHI->DEL,

    """

    if not location:
        return None

    raw_location = location.strip()

    # if raw_location.lower() == "ind":
    #     return COUNTRY_MAIN_AIRPORTS["IN"]

    # Check country aliases
    country_code = COUNTRY_ALIASES.get(raw_location.lower())

    if country_code:
        airport = COUNTRY_MAIN_AIRPORTS.get(country_code)

        if airport and airport in AIRPORTS:
            return airport

    #Direct IATA code
    if re.fullmatch(r"[A-Za-z]{3}",raw_location):
        code = raw_location.upper()
        if code in AIRPORTS:
            return code

    location_clean = clean_text(raw_location)


    if not location_clean:
        return None

    
    # City preferred airport
    city_key = location_clean.upper()

    if city_key in CITY_MAIN_AIRPORTS:
        return CITY_MAIN_AIRPORTS[city_key]

    #country preferred airport
    country_code = country_name_to_code(location_clean)
    if country_code:
        airport = get_best_airport_for_country(country_code)
        if airport:
            return airport

    # Exact city match from airport database
    city_matches = []
    for iata, airport in AIRPORTS.items():
        city = str(airport.get("city", "")).lower().strip()
        name = str(airport.get("name", "")).lower().strip()

        score = 0
        if city == location_clean:
            score += 100
        elif location_clean in city:
            score += 70
        if location_clean in name:
            score += 50
        if "international" in name:
            score += 10
        if score > 0:
            city_matches.append((score, iata))

    if city_matches:
        city_matches.sort(reverse=True)
        return city_matches[0][1]

    return None


def find_location_mentions(query:str):
    """"
    Finds country or city names inside a natural language query
    """

    q = query.lower()
    mentions = []

    # country aliases
    for alias in COUNTRY_ALIASES:
        if re.search(rf"\b{re.escape(alias)}\b",q):
            mentions.append(alias)

    # country names for pycountry
    for country in pycountry.countries:
        name = country.name.lower()
        if len(name) >= 4 and re.search(rf"\b{re.escape(name)}\b",q):
            mentions.append(name)

    # city names from our preffered city map
    for city in CITY_MAIN_AIRPORTS:
        if re.search(rf"\b{re.escape(city.lower())}\b",q):
            mentions.append(city.lower())

    # Remove duplicate while keeping order
    unique_mentions = []
    for item in mentions:
        if item not in unique_mentions:
            unique_mentions.append(item)

    return unique_mentions

def parse_route(query:str):
    """
    Returns :
    dep_iata, arr_iata

    Can return:
    None,None -> global live flights
    IND,NRT -> flitered flights
    IND ,None -> all flights form IND
    None, NRT -> all flights to NRT
    """

    q = query.strip()
    q_lower = q.lower()

    # global / all-country query
    global_keywords =[
        "all country",
        "all countries",
        "global flights",
        "global flight",
        "all flights",
        "all flight",
        "worldwide flights",
        "worldwide flight"
    ]

    if any(keyword in q_lower for keyword in global_keywords):
        return None, None

    # Direct IATA code route : IND-NRT

    codes = re.findall(r"\b([A-Za-z]{3})\b", q )

    if len(codes) == 2:
        dep = codes[0].upper()
        arr = codes[1].upper()

        return dep, arr

    # pattern : from X to Y
    match = re.search(
        r"\bfrom\s+(.+?)\s+\bto\s+(.+?)(.+?\s+(?:on|for|under|including|with|in|at|by|via|via the|via an|via a|via one|via two|via three)\b|[.!?]|$)",
        q_lower,
    )

    if match:
        original_text = match.group(1)
        dest_text = match.group(2)

        dep_iata = resolve_location_to_iata(original_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # pattern match : Y to X
    match = re.search(
        r"\bto\s+(.+?)\s+\bfrom\s+(.+?)(.+?\s+(?:on|for|under|including|with|in|at|by|via|via the|via an|via a|via one|via two|via three)\b|[.!?]|$)",
        q_lower
    )

    if match:
        dest_text = match.group(1)
        original_text = match.group(2)

        dep_iata = resolve_location_to_iata(original_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # pattern : flight from X 
    match = re.search(
        r"\bfrom\s+(.+?)(?:[.!?]|$)",
        q_lower
    )

    if match:
        original_text = match.group(1)
        dep_iata = resolve_location_to_iata(original_text)
        return dep_iata, None

    # pattern : flight to Y
    match = re.search(
        r"\bto\s+(.+?)(?:[.!?]|$)",
        q_lower
    )
    if match:
        dest_text = match.group(1)
        arr_iata = resolve_location_to_iata(dest_text)
        return None, arr_iata

    #Fallback : find country  / city mentions in the query 
    mentions = find_location_mentions(q)

    if len(mentions) >= 2:
        dep_iata = resolve_location_to_iata(mentions[0])
        arr_iata = resolve_location_to_iata(mentions[1])
        return dep_iata, arr_iata
    if len(mentions) == 1:
        arr_iata = resolve_location_to_iata(mentions[0])
        return DEFAULT_ORIGIN_DATA, arr_iata

    return None, None

def format_flight(flight:dict):
    airline = flight.get("airline", {}).get("name") or "Unknown Airline"
    flight_number = flight.get("flight", {}).get("iata") or flight.get("flight", {}).get("icao") or "Unknown Flight Number"
    status = flight.get("flight_status") or "Unknown Status"

    dep = flight.get("departure", {}) or {}
    arr = flight.get("arrival", {}) or {}

    dep_airport = dep.get("airport") or "Unknown Departure Airport"
    dep_iata = dep.get("iata") or "Unknown IATA"
    dep_terminal = dep.get("terminal") or "N/A"
    dep_gate = dep.get("gate") or "N/A"
    dep_scheduled = dep.get("scheduled") or "Unknown"
    dep_delay = dep.get("delay") 
    dep_delay_text = f"{dep_delay} minutes" if dep_delay is not None else "N/A"

    arr_airport = arr.get("airport") or "Unknown Arrival Airport"
    arr_iata = arr.get("iata") or "Unknown IATA"
    arr_terminal = arr.get("terminal") or "N/A"
    arr_gate = arr.get("gate") or "N/A"
    arr_scheduled = arr.get("scheduled") or "Unknown"
    arr_delay = arr.get("delay")
    arr_delay_text = f"{arr_delay} minutes" if arr_delay is not None else "N/A"

    return f"""
Airline: {airline}
Flight : {flight_number}
Status: {status}

Departure:
    Airport: {dep_airport} 
    IATA: {dep_iata}
    Terminal: {dep_terminal}
    Gate: {dep_gate}
    Scheduled: {dep_scheduled}
    Delay: {dep_delay_text}
Arrival:
    Airport: {arr_airport}
    IATA: {arr_iata}
    Terminal: {arr_terminal}
    Gate: {arr_gate}
    Scheduled: {arr_scheduled}
    Delay: {arr_delay_text}
""".strip()


def search_flights(query:str ,limit:int=10):
    if not API_KEY:
        return (
            "Flight AIP error : AviationStack API key is not set"
            "Please add this your .env file as AVIATIOSTACK_API_KEY=your_api_key"
            
        )
    dep_iata, arr_iata = parse_route(query)

    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }

    if dep_iata:
        params["dep_iata"] = dep_iata
    if arr_iata:
        params["arr_iata"] = arr_iata

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
    except requests.RequestException as e:
        return f"Flight API error: {str(e)}"
    except ValueError:
        return "Flight API error: Invalid JSON response"

    if "error" in data:
        error = data["error"]
        return (
            "Flight API error: \n"
            f"Code: {error.get('code', 'N/A')}\n"
            f"Message: {error.get('message', 'N/A')}"
        )

    flight_data = data.get("data", [])

    if not flight_data:
        route_text = ""

        if dep_iata and arr_iata:
            route_text = f"for route {dep_iata} to {arr_iata}"
        elif dep_iata:
            route_text = f"from {dep_iata}"
        elif arr_iata:
            route_text = f"to {arr_iata}"

        return (
            f"No live flight found {route_text}. \n\n"
            "Note: AviationStack provide live/status flight data , not ticket price"

        )

    route_info = "Global live flights"

    if dep_iata and arr_iata:
        route_info = f"Live flights from {dep_iata} to {arr_iata}"
    elif dep_iata:
        route_info = f"Live flights from {dep_iata}"
    elif arr_iata:
        route_info = f"Live flights to {arr_iata}"

    formatted_flights = [format_flight(flight) for flight in flight_data[:limit]]

    return f"{route_info}:\n\n" + "\n\n---\n\n".join(formatted_flights)

if __name__ == "__main__":
    print(search_flights("Plane a 10 days palne from ind to japan"))
    print("\n"+"="*80+"\n")
    print(search_flights("Flight from India to Japan"))

    #1:03:18