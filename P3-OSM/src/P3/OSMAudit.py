"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
#Take 1st word rather than last one
street_type_re = re.compile(r"(\b\S+)", re.IGNORECASE)

#OSMFILESMALL = "C:\\Users\\to75329\\Desktop\\DataScience\\P3-OSM\\data\\TournefeuilleSmall\\ex_skRaCfhoUs2YH1UkxceUcxB7i7yG2.osm"
#OSMFILELARGE = "C:\\Users\\to75329\\Desktop\\DataScience\\P3-OSM\\data\\TournefeuilleLarge\\ex_ifADycQ6ZEYtQ1EGQpj1mL17xbgci.osm"

expected = ["Rue", "Avenue", "Boulevard", "Court", "Place", "Square", "Route", "Chemin", "Parking", "Impasse","Passage", "Clos",u"All\xe9e",
            "Rond-Point"]

expectedPostalCodes = ["31170","31770","31300","31100","31830","31000","31070","31270","31036"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group(1)
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_postal_code(postal_codes, postal_code):
    if postal_code not in expectedPostalCodes:
        postal_codes[postal_code].add(postal_code)
            
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile = "C:\\Users\\to75329\\Desktop\\DataScience\\P3-OSM\\data\\TournefeuilleLarge\\ex_ifADycQ6ZEYtQ1EGQpj1mL17xbgci.osm"):
    auditedTypes = []
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postal_codes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                elif is_postal_code(tag):
                    audit_postal_code(postal_codes, tag.attrib['v'])
    osm_file.close()
    
    auditedTypes.append(street_types)
    auditedTypes.append(postal_codes)
    return auditedTypes


def cure_name(name):
    mapping = { "Av.": "Avenue" }
    
    startswithtwodigits = re.search('^\s*([0-9][0-9])',name)
    
    # striping the digits
    if startswithtwodigits:
        name = name.replace(startswithtwodigits.group(1),"").lstrip()
    # Upper letter if frst letter is lowercase
    elif name[0].islower():
        name = name.title()
    else:       
        for key in mapping.keys():
            if key in name:
                name = name.replace(key,mapping[key])
                return name
    return name


def cureData(osmfile = "C:\\Users\\to75329\\Desktop\\DataScience\\P3-OSM\\data\\TournefeuilleLarge\\ex_ifADycQ6ZEYtQ1EGQpj1mL17xbgci.osm", curedOSMFile = "C:\\Users\\to75329\\Desktop\\DataScience\\P3-OSM\\data\\TournefeuilleLarge\\cured.osm"):
    audited_types = audit(osmfile)
    st_types = audited_types[0]
    postcodes = audited_types[1]

    #dictionary holding each issue & its correction
    fix = {}
    fixpcode = {}

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = cure_name(name)
            fix[name]=better_name
            
    for post_code, pcissues in postcodes.iteritems():
        for issue in pcissues:
            better_postcode = issue[0:5]
            fixpcode[issue]=better_postcode

    osm_file = open(osmfile, "r")
    cured_osm = open(curedOSMFile, "w")
    #preparing root node & header
    cured_osm.write("<?xml version='1.0' encoding='UTF-8'?>\n<osm version=\"0.6\" generator=\"osmconvert 0.8.5\" timestamp=\"2017-01-04T15:04:03Z\">\n<bounds minlat=\"43.5500874\" minlon=\"1.2975794\" maxlat=\"43.6030756\" maxlon=\"1.3827329\"/>\n")
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):        
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    #tag value has an issue & needs to be fixed
                    if tag.attrib['v'] in fix.keys():
                        #The housenumber case requires special treatment
                        startswithtwodigits = re.search('^\s*([0-9][0-9])',tag.attrib['v'])                                                
                        if startswithtwodigits:
                            #Adding a new tag
                            newtag=ET.SubElement(elem, 'tag')
                            newtag.attrib['k']="addr:housenumber"
                            newtag.attrib['v']=startswithtwodigits.group(1)  
                        #replacing issue with its matching fix                      
                        tag.attrib['v'] = fix[tag.attrib['v']]
                elif is_postal_code(tag):
                    if tag.attrib['v'] in fixpcode.keys():
                        tag.attrib['v'] = fixpcode[tag.attrib['v']]            
            cured_osm.write(ET.tostring(elem))
    #closing root node
    cured_osm.write("</osm>")
    osm_file.close()
    cured_osm.close()
    print("Cured data generated successfully")

if __name__ == '__main__':
    cureData()