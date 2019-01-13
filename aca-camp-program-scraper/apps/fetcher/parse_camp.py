import re

TITLE_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/div[2]/div[1]/h1/text()'''
PROGRAM_URL_XPATH = '''//*[@id="fac-camp-profile"]/section[3]/div/div/div/table/tbody/tr/td/a/@href'''
LOGO_URL_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/div[2]/div[1]/img[1]/@src'''
DESCRIPTION_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/div[2]/div[@class="camp-description"]/text()'''
PHONE_NUMBER_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/aside/div[1]/p[1]/text()[2]'''
EMAIL_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/aside/div[1]/a[2]/text()'''
AFFILIATION_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/aside/div[2]/p/text()'''
OFFICIAL_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/aside/div[1]/a[1]/@href'''
ADDRESS_ONE_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/aside/address/p/text()[1]'''
ADDRESS_TWO_XPATH = '''//*[@id="fac-camp-profile"]/section[2]/div/div/aside/address/p/text()[2]'''


def build_url(url):
    ROOT_URL = 'http://find.acacamps.org'
    url = '%s%s' % (ROOT_URL, url)
    return url


def parse_camp_details(camp_dom_tree):
    '''title'''
    title = camp_dom_tree.xpath(TITLE_XPATH)
    if(len(title) > 0):
        title = title[0]
    else:
        title = ''

    '''description'''
    description = camp_dom_tree.xpath(DESCRIPTION_XPATH)
    if(len(description) > 0):
        description = description[0]
        # remove redundant spacing in string
        match = re.compile("[^\W\d]").search(description)
        if(match is not None):
            description = [description[:match.start()],
                           description[match.start():]][1]
        else:

            description = " ".join(description.split())

    else:
        description = ''

    # build logo url
    logo_raw_url = camp_dom_tree.xpath(LOGO_URL_XPATH)
    if(len(logo_raw_url) > 0):
        logo_url = build_url(logo_raw_url[0])
    else:
        logo_url = ''

    # build program url list
    program_raw_url_list = camp_dom_tree.xpath(PROGRAM_URL_XPATH)
    program_url_list = []
    if len(program_raw_url_list) > 0:
        for program_raw_url in program_raw_url_list:
            program_url_list.append(build_url(program_raw_url))

    '''location'''
    # street_address
    # city
    # state
    # zipcode
    address_one = camp_dom_tree.xpath(ADDRESS_ONE_XPATH)
    address_two = camp_dom_tree.xpath(ADDRESS_TWO_XPATH)
    # if there are two lines of address, then first would be street address and second would be city + state + zipcode
    if(len(address_one) > 0 and len(address_two) > 0):
        address_one = address_one[0]
        address_one = " ".join(address_one.split())
        address_two = address_two[0]
        address_two = " ".join(address_two.split())
        full_address = address_one + "|" + address_two
        street_address = full_address.split("|")[0]
        city = full_address.split("|")[1].split(",")[0]
        state = full_address.split("|")[1].split(",")[1].strip(" ")[:2]
        raw_zipcode = full_address.split("|")[1].split(",")[1]
        zipcode = "".join(re.findall(r'\d+', raw_zipcode))[:5]

    # if there is one line of address, then it would be city + state + zipcode
    elif(len(address_one) > 0 and len(address_two) is 0):
        street_address = ''
        address_one = address_one[0]
        address_one = " ".join(address_one.split())
        city = address_one.split(",")[0]
        state = address_one.split(",")[1].strip(" ")[:2]
        raw_zipcode = address_one.split(",")[1]
        zipcode = "".join(re.findall(r'\d+', raw_zipcode))[:5]

    else:
        street_address = ''
        city = ''
        state = ''
        zipcode = ''

    '''phone number'''
    phone_number = camp_dom_tree.xpath(PHONE_NUMBER_XPATH)
    if(len(phone_number) > 0):
        phone_number = phone_number[0]
        phone_number = " ".join(phone_number.split())
        phone_number = phone_number.replace('-', '')
    else:
        phone_number = ''

    '''email'''
    email = camp_dom_tree.xpath(EMAIL_XPATH)
    if(len(email) > 0):
        email = email[0]
    else:
        email = ''

    '''official url'''
    official_url = camp_dom_tree.xpath(OFFICIAL_XPATH)
    if(len(official_url) > 0):
        official_url = official_url[0]
    else:
        official_url = ''

    '''affiliation or religion'''
    affiliation = camp_dom_tree.xpath(AFFILIATION_XPATH)
    if(len(affiliation) > 0):
        affiliation = affiliation[0]
    else:
        affiliation = ''

    data = {
        'title': title,
        'description': description,
        'logo_url': logo_url,
        'street_address': street_address,
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'phone_number': phone_number,
        'email': email,
        'official_url': official_url,
        'affiliation': affiliation,
        'program_url_list': program_url_list
    }

    return data
