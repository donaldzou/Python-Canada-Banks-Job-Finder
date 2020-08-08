import threading
import random
import requests
import json
from tinydb import TinyDB, Query
import time
import os
from bs4 import BeautifulSoup
import urllib
import uuid


timeout = 600 # Change this for how long the program will fetch jobs, this is counted in seconds.

email_timeout = 30 # Change this for how long the program will check pending email.
email_count = 3 # Change this for the number of new jobs founded and send an email.

email_reciever = ["blah@example.com","blah@example.com"]

def email(email_add,content):
    import email
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    reciever = email_add
    msg = MIMEMultipart("alternative")
    msg['From'] = "New Job Found"
    msg['To'] = reciever
    msg['Subject'] = str(len(content))+" New Jobs Found"

    data = ""
    print("--------")
    print("Sending Email...")
    for i in content:
        for key in i.keys():
            if key == "Description":
                data += "<p style='font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 5px;'>"+key+"</p>"
                data += i[key]
            else:
                data += "<p style='font-family: sans-serif; font-size: 14px; font-weight: normal; margin: 0; margin-bottom: 5px;'>"+key+"</p>"
                data += "<p style='font-family: sans-serif; font-size: 20px; font-weight: 800; margin: 0; margin-bottom: 5px;'>"+i[key]+"</p> "
            data += "<p style='font-family: sans-serif; font-size: 20px; font-weight: 800; margin: 0; margin-bottom: 5px; border: 2px solid grey'></p> "
    html = "<html><head> <meta name='viewport' content='width=device-width'> <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'> <title>Simple Transactional Email</title> <style> /* ------------------------------------- INLINED WITH htmlemail.io/inline ------------------------------------- */ /* ------------------------------------- RESPONSIVE AND MOBILE FRIENDLY STYLES ------------------------------------- */ @media only screen and (max-width: 620px) { table[class=body] h1 { font-size: 28px !important; margin-bottom: 10px !important; } table[class=body] p, table[class=body] ul, table[class=body] ol, table[class=body] td, table[class=body] span, table[class=body] a { font-size: 16px !important; } table[class=body] .wrapper, table[class=body] .article { padding: 10px !important; } table[class=body] .content { padding: 0 !important; } table[class=body] .container { padding: 0 !important; width: 100% !important; } table[class=body] .main { border-left-width: 0 !important; border-radius: 0 !important; border-right-width: 0 !important; } table[class=body] .btn table { width: 100% !important; } table[class=body] .btn a { width: 100% !important; } table[class=body] .img-responsive { height: auto !important; max-width: 100% !important; width: auto !important; } } /* ------------------------------------- PRESERVE THESE STYLES IN THE HEAD ------------------------------------- */ @media all { .ExternalClass { width: 100%; } .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div { line-height: 100%; } .apple-link a { color: inherit !important; font-family: inherit !important; font-size: inherit !important; font-weight: inherit !important; line-height: inherit !important; text-decoration: none !important; } #MessageViewBody a { color: inherit; text-decoration: none; font-size: inherit; font-family: inherit; font-weight: inherit; line-height: inherit; } .btn-primary table td:hover { background-color: #34495e !important; } .btn-primary a:hover { background-color: #34495e !important; border-color: #34495e !important; } } </style></head><body class='' style='background-color: #f6f6f6; font-family: sans-serif; -webkit-font-smoothing: antialiased; font-size: 14px; line-height: 1.4; margin: 0; padding: 0; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;'> <table border='0' cellpadding='0' cellspacing='0' class='body' style='border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%; background-color: #f6f6f6;'> <tbody> <tr> <td style='font-family: sans-serif; font-size: 14px; vertical-align: top;'>&nbsp;</td> <td class='container' style='font-family: sans-serif; font-size: 14px; vertical-align: top; display: block; Margin: 0 auto; max-width: 580px; padding: 10px; width: 580px;'> <div class='content' style='box-sizing: border-box; display: block; margin: 2rem; max-width: 580px; padding: 20px; background-color: white;'> <!-- START CENTERED WHITE CONTAINER --> "+data+"<div class='footer' style='clear: both; Margin-top: 10px; text-align: center; width: 100%;'> <table border='0' cellpadding='0' cellspacing='0' style='border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 100%;'> </table> </div> <!-- END FOOTER --> <!-- END CENTERED WHITE CONTAINER --> </div> </td> <td style='font-family: sans-serif; font-size: 14px; vertical-align: top;'>&nbsp;</td> </tr> </tbody> </table></body></html>"
    part2 = MIMEText(html, "html")
    msg.attach(part2)
    s = smtplib.SMTP("smtp.office365.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('blah@example.com', 'blahblah')
    s.sendmail("blah@example.com", reciever, msg.as_string())
    s.quit()
    print('Email Sent to '+email_add)
    print("--------")


def thread_bmo():

        url = "https://bmo.wd3.myworkdayjobs.com/External/13/replaceFacet/318c8bb6f553100021d223d9780d30be"
        payload = 'facets=Location%2CjobFamilyGrou&Location=Location%3A%3Ac3170091f3cd01dec314cd815f01e2bd&jobFamilyGroup=jobFamilyGroup%3A%3Ac3170091f3cd0158f849606ad000ba20%2CjobFamilyGroup%3A%3Ac3170091f3cd013f072b656ad000c820%2CjobFamilyGroup%3A%3Ac3170091f3cd01924064646ad000c620%2CjobFamilyGroup%3A%3Ac3170091f3cd017168e7686ad000d220%2CjobFamilyGroup%3A%3Ac3170091f3cd01dac965626ad000c020%2CjobFamilyGroup%3A%3Ac3170091f3cd013182855f6ad000b820%2CjobFamilyGroup%3A%3Ac3170091f3cd01bc6bf36b6ad000da20%2CjobFamilyGroup%3A%3Ac3170091f3cd01172604636ad000c220%2CjobFamilyGroup%3A%3Ac3170091f3cd01e599606a6ad000d620%2CjobFamilyGroup%3A%3Ac3170091f3cd016422b9636ad000c420'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PLAY_SESSION=ed6de2d908f91e4609188ec631f7b67395d74c77-bmo_pSessionId=q2divh65een2vmdb605mtumt1q&instance=wd3prvps0005b; wday_vps_cookie=2586220042.56370.0000; PLAY_LANG=en-US; TS014c1515=01f6296304c2b3217c70d134481847f6c59874eac8adbbaf386965dd6000405b2f912e123fc3c6f0a0f5bf1cd78980ade499af677d'
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        result = response.json()
        db = TinyDB("json/bmo.json")
        bank = Query()
        update_id = str(uuid.uuid1())
        for i in result['body']['children'][0]['children'][0]['listItems']:
            
            data = {
                "id":i['subtitles'][0]['instances'][0]['text'],
                "title":i['title']['instances'][0]['text'],
                "date":i['subtitles'][2]['instances'][0]['text'],
                "link":"https://bmo.wd3.myworkdayjobs.com"+i['title']['commandLink'],
                "uuid":update_id
            }
            result = db.search(bank.id == data['id'])
            if result == []:
                db.insert(data)
                print("--------")
                print("New Job Found - BMO")
                send_content_bmo = {
                    "Company": "BMO",
                    "ID":data['id'],
                    "Title":data["title"],
                    "Posted Date":data["date"],
                    "Apply URL":data['link']
                }
                email_content = TinyDB("json/email.json")
                email_content.insert(send_content_bmo)
                print("Inserted into Email Pending List - BMO")
                print("--------")
            else:
                db.update({"title":i['title']['instances'][0]['text'],
                "date":i['subtitles'][2]['instances'][0]['text'],
                "link":"https://bmo.wd3.myworkdayjobs.com"+i['title']['commandLink'],"uuid":update_id}, bank.id == data['id'])

        update = db.all()
        for i in update:
            if "uuid" not in i:
                print("BMO Deleted - "+str(i['id']))
                db.remove(bank.id == i['id'])
            elif i["uuid"] != update_id:
                print("BMO Deleted - "+str(i))
                db.remove(bank.id == i['id'])              

def thread_rbc():
        url = "https://jobs.rbc.com/widgets"
        x = requests.post(url, json={"lang":"en_ca","deviceType":"desktop","country":"ca","ddoKey":"refineSearch","sortBy":"Most recent","subsearch":"","from":0,"jobs":"true","counts":"true","all_fields":["category","subCategory","department","experience","type","country","state","city"],"pageName":"search-results","size":500,"clearAll":"false","jdsource":"facets","isSliderEnable":"false","keywords":"","global":"true","selected_fields":{"country":["Canada"],"city":["Toronto"],"state":["Ontario"]},"sort":{"order":"desc","field":"postedDate"}})
        result = x.json()
        db = TinyDB("json/rbc.json")
        bank = Query()
        update_id = str(uuid.uuid1())
        for i in result['refineSearch']['data']['jobs']:
            result = db.search(bank.jobId == i['jobId'])
            if result == []:
                if i['category'] == "Operations" or i['category'] == "Finance | Accounting" or i['category'] == "Risk Management":
                    i['uuid'] = update_id
                    db.insert(i)
                    print("--------")
                    print("New Job Found - RBC")
                    send_content_rbc = {
                        "Company":"RBC",
                        "ID":i['jobId'],
                        "Category":i['category'],
                        "Title":i['title'],
                        "Department":i['department'],
                        "Type":i['type'],
                        "Posted Date":i['postedDate'],
                        "Apply URL":i['applyUrl']
                    }
                    
                    email_content = TinyDB("json/email.json")
                    email_content.insert(send_content_rbc)
                    print("Inserted into Email Pending List - RBC")
                    print("--------")
            else:
                db.update({"uuid":update_id}, bank.jobId == i['jobId'])
        update = db.all()
        for i in update:
            if "uuid" not in i:
                print("RBC Deleted - "+str(i['jobId']))
                db.remove(bank.jobId == i['jobId'])
            elif i["uuid"] != update_id:
                print("RBC Deleted - "+str(i['jobId']))
                db.remove(bank.jobId == i['jobId'])

def thread_cibc():
        url = "https://cibc.wd3.myworkdayjobs.com/search/fs/replaceFacet/318c8bb6f553100021d223d9780d30be"
        payload = 'facets=City&City=City%3A%3A5a781e4ad9710113e8f4efbb1701cf1a&jobFamilyGroup=jobFamilyGroup%3A%3A4bbe6c74e8a70132da752ca881011910%2CjobFamilyGroup%3A%3A4bbe6c74e8a7011c6e1c34a881012d10%2CjobFamilyGroup%3A%3A4bbe6c74e8a701e62f6125a881011510%2CjobFamilyGroup%3A%3A4bbe6c74e8a701e2782e2da881011b10%2CjobFamilyGroup%3A%3A4bbe6c74e8a7011e314d36a881013310%2CjobFamilyGroup%3A%3A4bbe6c74e8a701c2f88e2ea881011f10%2CjobFamilyGroup%3A%3A4bbe6c74e8a7013acad236a881013510%2CjobFamilyGroup%3A%3A4bbe6c74e8a7011d49ad22a881011310'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PLAY_LANG=en-US; PLAY_SESSION=c423cfd03395e4012d87121463e830bf8e542190-cibc_pSessionId=1rprdm510r4osv5s05ca0f0vik&instance=wd3prvps0002f; wday_vps_cookie=2737214986.1075.0000; TS014c1515=01f629630484cc3950d1d5e212cbdbf8295ed8acb7258706c930ab60ac88c001c57afd1229b73932e257fc92a10ffc71f8d80abc05'
        }

        response = requests.request("POST", url, headers=headers, data = payload)
        result = response.json()
        db = TinyDB("json/cibc.json")
        bank = Query()
        update_id = str(uuid.uuid1())
        for i in result['body']['children'][0]['children'][0]['listItems']:
            data = {
                "id":i['subtitles'][0]['instances'][0]['text'],
                "title":i['title']['instances'][0]['text'],
                "date":i['subtitles'][2]['instances'][0]['text'],
                "link":"https://cibc.wd3.myworkdayjobs.com"+i['title']['commandLink'],
                "uuid":update_id
            }
            
            result = db.search(bank.id == data['id'])
            if result == []:
                db.insert(data)
                print("--------")
                print("New Job Found - CIBC")
                send_content_cibc = {
                    "Company": "CIBC",
                    "ID":data['id'],
                    "Title":data["title"],
                    "Posted Date":data["date"],
                    "Apply URL":data['link']
                }
                email_content = TinyDB("json/email.json")
                email_content.insert(send_content_cibc)
                print("Inserted into Email Pending List - CIBC")
                print("--------")
            else:
                db.update({"title":i['title']['instances'][0]['text'],
                "date":i['subtitles'][2]['instances'][0]['text'],
                "link":"https://cibc.wd3.myworkdayjobs.com"+i['title']['commandLink'], "uuid":update_id}, bank.id == data['id'])
        
        update = db.all()
        for i in update:
            if "uuid" not in i:
                print("CIBC Deleted - "+str(i['id']))
                db.remove(bank.id == i['id'])
            elif i["uuid"] != update_id:
                print("CIBC Deleted - "+str(i['id']))
                db.remove(bank.id == i['id'])

def thread_sco():
        a_url = "https://jobs.scotiabank.com/search/?q=&locationsearch=Toronto&sortColumn=referencedate&sortDirection=desc"
        response = requests.get(a_url)
        soup = BeautifulSoup(response.content, "html.parser")
        total = soup.findAll("span","paginationLabel")
        total = str(total[0])
        total = total.replace("</b></span>" , "")
        total = total.split("<b>")
        total = int(total[-1])
        page = total//25 + 1
        db = TinyDB("json/sco.json")
        bank = Query()
        update_id = str(uuid.uuid1())
        for i in range(page):
            url = a_url+"&startrow="+str((i*25))
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            count = 0
            per_page = len(soup.findAll("tr","data-row"))
            for i in range(0,per_page*2,2):
                count += 1
                title = soup.findAll("a","jobTitle-link")
                date = soup.findAll("span","jobDate")
                data = {
                    "id":title[i]['href'].split('/')[-2],
                    "title":title[i].contents[0],
                    "link":"https://jobs.scotiabank.com"+title[i]['href'],
                    "date":date[i].contents[0].replace("\n","").replace("\t",""),
                    "uuid": update_id

                }
                search = db.search(bank.id == data['id'])
                if search == []:
                    db.insert(data)
                    print("--------")
                    print("New Job Found - Scotia Bank")
                    send_content_sco = {
                        "Company": "Scotia Bank",
                        "ID":data['id'],
                        "Title":data["title"],
                        "Posted Date":data["date"],
                        "Apply URL":data['link']
                    }
                    email_content = TinyDB("json/email.json")
                    email_content.insert(send_content_sco)
                    print("Inserted into Email Pending List - SCO")
                    print("--------")
                else:
                    db.update({"title":title[i].contents[0],
                    "link":"https://jobs.scotiabank.com"+title[i]['href'],
                    "date":date[i].contents[0].replace("\n","").replace("\t",""), "uuid": update_id}, bank.id == data["id"])

        update = db.all()
        for i in update:
            if "uuid" not in i:
                print("SCO Deleted - "+str(i['id']))
                db.remove(bank.id == i['id'])
            elif i["uuid"] != update_id:
                print("SCO Deleted - "+str(i['id']))
                db.remove(bank.id == i['id'])

def thread_td():
    job_category = [
        "Asset Management",
        "Business Analysis / Reporting",
        "Commercial Banking",
        "Enterprise Data & Analytics",
        "Finance / Accounting",
        "Global Security & Investigations"
        "Management / Consulting / Advisory",
        "Operations & Underwriting",
        "Product Management & Development",
        "Risk Management",
        "Sales & Business Development",
        "Securities / Wholesale Banking"
    ]
    update_id = str(uuid.uuid1())
    for i in job_category:
        x = requests.request("GET", url="https://jobsapi-internal.m-cloud.io/api/job?facet%5B%5D=ats_portalid%3AKBR-5601~KBR-5602~KBR-5813&latitude=43.653226&longitude=-79.3831843&LocationRadius=10&Limit=10&Organization=1927&offset=1&useBooleanKeywordSearch=true&facet%5B%5D=addtnl_categories:"+urllib.parse.quote(i))
        result = x.json()
        for i in result["queryResult"]:
            db = TinyDB("json/td.json")
            bank = Query()
            search = db.search(bank.clientid == i['clientid'])
            if search == []:
                i['uuid'] = update_id
                db.insert(i)
                print("--------")
                print("New Job Found - TD Bank")
                send_content_td = {
                    "Company": "TD Bank",
                    "Title":i["title"],
                    "ID":i['clientid'],
                    "Category":i['primary_category'],
                    "Department":i['department'],
                    "Posted Date":i["open_date"],
                    "Apply URL":i['fndly_url']
                }
                email_content = TinyDB("json/email.json")
                email_content.insert(send_content_td)
                print("Inserted into Email Pending List - TD")
                print("--------")
            else:
                db.update({"uuid":update_id}, bank.clientid == i['clientid'])
        
    update = db.all()
    for i in update:
        if "uuid" not in i:
            print("TD Deleted - "+str(i['clientid']))
            db.remove(bank.clientid == i['clientid'])
        elif i["uuid"] != update_id:
            print("TD Deleted - "+str(i['clientid']))
            db.remove(bank.clientid == i['clientid'])
        

def run_banks():
    print("Canada Banks Job Finder Started...")
    while True:
        thread_bmo()
        thread_cibc()
        thread_rbc()
        thread_sco()
        thread_td()
        time.sleep(timeout)

def check_pending_email():
    while True:
        time.sleep(email_timeout)
        print("Email Checking...")
        email_db = TinyDB("json/email.json")
        search = Query()
        pending = email_db.all()
        if len(pending) >= email_count:
            for name in email_reciever:
                email(name, pending)
            for i in pending:
                id = i['ID']
                email_db.remove(search.ID == id)
        else:
            left = email_count - len(pending)
            print(str(len(pending))+" emails pending. Waiting for "+str(left)+" more.")
        



threading.Thread(target=run_banks).start()
threading.Thread(target=check_pending_email).start()
