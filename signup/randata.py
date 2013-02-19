import random

timezones = {
    "Etc/GMT+12": "-12:00",
    "Pacific/Pago_Pago": "-11:00",
    "America/Adak": "-10:00",
    "Pacific/Honolulu": "-10:00",
    "Pacific/Marquesas": "-10:30",
    "Pacific/Gambier": "-09:00",
    "America/Anchorage": "-09:00",
    "America/Los_Angeles": "-08:00",
    "Pacific/Pitcairn": "-08:00",
    "America/Phoenix": "-07:00",
    "America/Denver": "-07:00",
    "America/Guatemala": "-06:00",
    "America/Chicago": "-06:00",
    "Pacific/Easter": "-06:00",
    "America/Bogota": "-05:00",
    "America/New_York": "-05:00",
    "America/Caracas": "-05:30",
    "America/Halifax": "-04:00",
    "America/Santo_Domingo": "-04:00",
    "America/Asuncion": "-04:00",
    "America/St_Johns": "-04:30",
    "America/Godthab": "-03:00",
    "America/Argentina/Buenos_Aires": "-03:00",
    "America/Montevideo": "-03:00",
    "America/Noronha": "-02:00",
    "Etc/GMT+2": "-02:00",
    "Atlantic/Azores": "-01:00",
    "Atlantic/Cape_Verde": "-01:00",
    "Etc/UTC": "00:00",
    "Europe/London": "00:00",
    "Europe/Berlin": "+01:00",
    "Africa/Lagos": "+01:00",
    "Africa/Windhoek": "+01:00",
    "Asia/Beirut": "+02:00",
    "Africa/Johannesburg": "+02:00",
    "Europe/Moscow": "+03:00",
    "Asia/Baghdad": "+03:00",
    "Asia/Tehran": "+03:30",
    "Asia/Dubai": "+04:00",
    "Asia/Yerevan": "+04:00",
    "Asia/Kabul": "+04:30",
    "Asia/Yekaterinburg": "+05:00",
    "Asia/Karachi": "+05:00",
    "Asia/Kolkata": "+05:30",
    "Asia/Kathmandu": "+05:45",
    "Asia/Dhaka": "+06:00",
    "Asia/Omsk": "+06:00",
    "Asia/Rangoon": "+06:30",
    "Asia/Krasnoyarsk": "+07:00",
    "Asia/Jakarta": "+07:00",
    "Asia/Shanghai": "+08:00",
    "Asia/Irkutsk": "+08:00",
    "Australia/Eucla": "+08:45",
    "Australia/Eucla": "+08:45",
    "Asia/Yakutsk": "+09:00",
    "Asia/Tokyo": "+09:00",
    "Australia/Darwin": "+09:30",
    "Australia/Adelaide": "+09:30",
    "Australia/Brisbane": "+10:00",
    "Asia/Vladivostok": "+10:00",
    "Australia/Sydney": "+10:00",
    "Australia/Lord_Howe": "+10:30",
    "Asia/Kamchatka": "+11:00",
    "Pacific/Noumea": "+11:00",
    "Pacific/Norfolk": "+11:30",
    "Pacific/Auckland": "+12:00",
    "Pacific/Tarawa": "+12:00",
    "Pacific/Chatham": "+12:45",
    "Pacific/Tongatapu": "+13:00",
    "Pacific/Apia": "+13:00",
    "Pacific/Kiritimati": "+14:00"
}


names = ['Adam', 'Andrew', 'Angus', 'Brylie', 'Bob', 'Bryan', 'Bruce', 'Charles', 'Chris', 'Colin', 'Dirk', 'David', 'Drew', 'Emille', 'Evan', 'Ethan', 'Frank', 'Francois', 'Fred', 'Graig', 'Greg', 'Graham', 'Harry', 'Henry', 'Howard', 'Ignus', 'Ivan', 'Issiah', 'John', 'James', 'Jeff', 'Kevin', 'Kyle', 'Kim', 'Lennard', 'Leon', 'Lee', 'Mark', 'Mike', 'Manfred', 'Nathan', 'Nevin', 'Neil', 'Oscar', 'Oliver', 'Omar', 'Philip', 'Patrick', 'Peter', 'Quintin', 'Quepid', 'Qwaga', 'Richard', 'Randalph', 'Ricardo', 'Steven', 'Shane', 'Shaun', 'Travis', 'Trevor', 'Tony', 'Uhail', 'Ushaad', 'Umar', 'Vince', 'Viper', 'Van', 'William', 'Winston', 'Warren', 'Xavier', 'Xinadu', 'Xally', 'Yoris', 'Yoda', 'Yull', 'Zane', 'Zett', 'Zorba' ]

last_names = ['Adams', 'Ashberry', 'Abrahams', 'Burns', 'Burke', 'Berry', 'Cole', 'Conan', 'Crousse', 'Davis', 'De Villiers', 'De Bois', 'Eksteen', 'Evans', 'Emu', 'Frederichs', 'Ferreira', 'Frank', 'Graham', 'Gilbert', 'Gale', 'Hawkings', 'Hewitt', 'Hall', 'Irvin', 'Ingram', 'Ingelman', 'Jacobs', 'James', 'Jeffrey', 'King', 'Kent', 'Kaine', 'Lee', 'Levinstein', 'Livingston', 'McGreggor', 'McAuther', 'Marias', 'Nash', 'Newton', 'Nel', 'Oxford', 'Obama', 'Opal', 'Price', 'Pascal', 'Pierce', 'Quinn', 'Queenly', 'Qwerty', 'Richards', 'Ricardo', 'Rigter', 'Stevenson', 'Stegman', 'Steward', 'Turing', 'Turner', 'Tumbleton', 'Uys', 'Ushaad', 'Usaf', 'Van Dam', 'Vermeulen', 'Visser', 'West', 'Williams', 'Wayne', 'Xolo', 'Xcgincha', 'Xnopo', 'Yannes', 'Ylian', 'Yster', 'Zeitsman', 'Zuma', 'Zulu']


def random_email():
    formats = [
        '{name}.{surname}@{provider}',
        '{name[0]}{surname}@{provider}',
        '{name}{surname}@{provider}',
        '{name}{surname[0]}@{provider}'
    ]
        
    name = random.choice(names).lower()
    last = random.choice(last_names).lower().replace(' ','')
    return random.choice(formats).format(name=name, surname=last, provider='mail.com')

def random_signup(limit):
    return ({'email': random_email(), 'questions': {'timezone': random.choice(timezones.values())}} for i in range(limit))
