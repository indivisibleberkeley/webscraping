#!/usr/bin/env python

"""
Imports and parses data from the ARPA-E project search page, https://arpa-e.energy.gov/?q=project-listing
Exports data of interest as a tab-separated value file, .tsv
"""

from bs4 import BeautifulSoup
import requests 

fnameout = "myfile"
baseurl = "https://arpa-e.energy.gov"

url = "https://arpa-e.energy.gov/?q=project-listing&field_program_tid=All&field_project_state_value=CA&field_project_status_value=All&term_node_tid_depth=All&sort_by=field_organization_value&sort_order=ASC"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "html.parser")

tsvout = ""

for project in soup.find_all("div", { "class" : "views-row" }):
    porg = project.find("div", { "class" : "field-name-field-organization" }).text
    purlpost = project.find("div", { "class" : "field-name-title" }).find("a").get("href")
    purl = "{}{}".format(baseurl, purlpost)
    ptitle = project.find("div", { "class" : "field-name-title" }).text
    pstatus = project.find("div", { "class" : "field-name-field-project-status" }).find("div", { "class" : "field-items" }).text
    
    # grab the project's summary page
    pr = requests.get(purl)
    pdata = pr.text
    projectpage = BeautifulSoup(pdata)
    paward = projectpage.find("div", { "class" : "field-name-field-arpae-award" }).find("div", { "class" : "field-item" }).text
    plocation = projectpage.find("div", { "class" : "field-name-field-location" }).find("div", { "class" : "field-item" }).text
    
    # save each project to a big string, tab-separated fields with newline
    tsvout += "{}\t{}\t{}\t{}\t{}\t{}\n".format(porg, purl, ptitle, plocation, paward, pstatus)

with open("{}.tsv".format(fnameout), 'w') as f:
    f.write(tsvout)

