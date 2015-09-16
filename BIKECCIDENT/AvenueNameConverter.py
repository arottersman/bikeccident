##Some data sources refer to avenue with the number written as a
##numeral eg 6 Avenue, while others refer to it as Sixth Avenue.
##This is a simple module to map between the two.
def convert_avenue_name_from_numeral(name):
    conversion_dict = {
        1: 'First',
        2: 'Second',
        3: 'Third',
        4: 'Fourth',
        5: 'Fifth',
        6: 'Sixth',
        7: 'Seventh',
        8: 'Eighth',
        9: 'Ninth',
        10: 'Tenth',
        11: 'Eleventh',
        12: 'Twelfth',
        13: 'Thirteenth'
    }
    numeral = name.split(' ', 1)[0]
    try:
        ordinal = conversion_dict[numeral]
        return name.replace(numeral, ordinal, 1)
    except KeyError:
        return name
