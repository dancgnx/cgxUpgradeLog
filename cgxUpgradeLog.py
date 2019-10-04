#!/usr/bin/env python3
import cgxinit 
import logging
import sys
import cloudgenix
from cloudgenix import jd, jd_detailed
import json
import time

if __name__ == "__main__":
    cgx, args = cgxinit.go()

    print(f"Time,Site,Device,Image,Operator")
    #init logging
    logging.basicConfig(level=logging.INFO)
    log=logging.getLogger("cgxSIPalg")

    # build site database
    sites = {}
    for site in cgx.get.sites().cgx_content["items"]:
        sites[site["id"]] = site
    
    # build elements database
    elements = {}
    for element in cgx.get.elements().cgx_content["items"]:
        elements[element["id"]] = element
    

    # build software images dataabse
    images = {}
    for image in cgx.get.element_images().cgx_content["items"]:
        images[image["id"]] = image["version"]

    # build operators dictionary
    operators={}
    for operator in cgx.get.tenant_operators().cgx_content["items"]:
        operator_id = operator["id"]
        operator_first = operator["first_name"]
        if "last_name" in operator:
            operator_last = operator["last_name"]
        else:
            operator_last = ""
        operators[operator_id] = f"{operator_first} {operator_last}"

    def funcname(parameter_list):
        pass
    # start auditlog query login
    page = 1
    while True:
        q = {
            "limit":"100",
            "query_params":{"resource_key":{"eq":"state_software"}},
            "sort_params":{"response_ts":"desc"},
            "dest_page":str(page)
        }
        logs = cgx.post.auditlog_query(q)
        if not logs.cgx_status:
            log.error("Error retrieving audit logs")
            jd_error(logs)
        for logentry in logs.cgx_content["items"]:
            # skip if not software request or if  request type isn't PUT
            if "software/state" in logentry["request_uri"] and logentry["request_type"] == "PUT":
                # extract element ID 
                element_id = logentry["request_uri"].split("/")[6]

                # the element might have been already unclaimed, so we dont' care
                if element_id in elements:
                    # extract element information
                    element_name= elements[element_id]["name"]
                    element_site_id= elements[element_id]["site_id"]
                    if element_site_id in ['1','0']:
                        element_site = "NO SITE BOUND"
                    else:
                        element_site= sites[element_site_id]["name"]
                    # get software image name 
                    image_id = json.loads(logentry["request_body"])["image_id"]
                    if not image_id:
                        jd(logentry)
                    image_name=images[image_id]
                    
                    #extract time
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(logentry["request_ts"]/1000))

                    #extract operator name
                    if logentry["operator_id"] in operators:
                        op_name=operators[logentry["operator_id"]]
                    else:
                        op_name = "OP no longer valid"
                    print(f"{timestamp},{element_site},{element_name},{image_name},{op_name}")
        # check if we are at the end of the list
        if logs.cgx_content["count"] < 100:
            break
        page += 1
