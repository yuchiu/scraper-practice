import re

TITLE_XPATH = '''/html/head/title/text()'''
DESCRIPTION_XPATH = '''//*[@class="camp-description"]/text()'''
FOR_XPATH = '''//*[@id="fac-program-profile"]/section[2]/div/div/aside/div[2]/p[1]/text()'''
TYPE_XPATH = '''//*[@id="fac-program-profile"]/section[2]/div/div/aside/div[2]/p[2]/text()'''
ADDITIONAL_INFO_XPATH = '''//*[@id="fac-program-profile"]/section[2]/div/div/aside/div[2]/p/text()'''
ACTIVITIES_XPATH = '''//*[@id="fac-program-profile"]/section[5]/div/div/div/div/ul/li/text()'''


def parse_program_details(program_dom_tree):
    '''title'''
    title = program_dom_tree.xpath(TITLE_XPATH)
    if(len(title) > 0):
        title = title[0]
        title = title.split("- ")[1]
        title = title.split(" |")[0]
        title = " ".join(title.split())
    else:
        title = ''

    '''description'''
    description = program_dom_tree.xpath(DESCRIPTION_XPATH)
    if(len(description) > 0):
        description = description[0]
        match = re.compile("[^\W\d]").search(description)
        if match is not None:
            description = [description[:match.start()],
                           description[match.start():]][1]
        else:
            description = " ".join(description.split())
    else:
        description = ''

    '''additional information'''
    # For
    # Type
    # Sleeping Accomodation
    # Amenities
    # Finacial Aid
    # Waterfront_list
    raw_additional_info_list = program_dom_tree.xpath(ADDITIONAL_INFO_XPATH)
    camp_for = ''
    camp_type = ''
    sleeping_accommodation_list = []
    amenity_list = []
    financial_aid = ''
    waterfront_list = []
    if(len(raw_additional_info_list) > 0):
        # loop through additional info list elements
        for info in raw_additional_info_list:
            # assign first string word to match
            match = re.compile("[^\W\d]").search(info)
            # parse element if there is a match
            if match is not None:
                # remove extra spacing in front of element string with matched word
                info = [info[:match.start()],
                        info[match.start():]][1]
                # split the string into type and data assume there is a ':' inside string
                info_type = info.split(":")[0]
                info_data = info.split(":")[1]
                if info_type == 'For':
                    info_data = " ".join(info_data.split())
                    camp_for = info_data
                elif info_type == 'Type':
                    info_data = " ".join(info_data.split())
                    camp_type = info_data
                elif info_type == 'Sleeping Accommodations':
                    info_data = " ".join(info_data.split())
                    info_data = info_data.split(', ')
                    sleeping_accommodation_list = info_data
                elif info_type == 'Amenities':
                    info_data = " ".join(info_data.split())
                    info_data = info_data.split(', ')
                    amenity_list = info_data
                elif info_type == 'Financial Aid':
                    info_data = " ".join(info_data.split())
                    financial_aid = info_data
                elif info_type == 'Waterfront_list':
                    info_data = " ".join(info_data.split())
                    info_data = info_data.split(', ')
                    waterfront_list = info_data

    '''Activities'''
    activity_list = program_dom_tree.xpath(ACTIVITIES_XPATH)

    if(len(activity_list) > 0):
        activity_list = activity_list
    else:
        activity_list = []

    data = {
        'title': title,
        'description': description,
        'camp_for': camp_for,
        'camp_type': camp_type,
        'sleeping_accommodation_list': sleeping_accommodation_list,
        'amenity_list': amenity_list,
        'financial_aid': financial_aid,
        'waterfront_list': waterfront_list,
        'activity_list': activity_list
    }
    return data
