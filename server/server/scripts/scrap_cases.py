import os
import requests
import xml.etree.ElementTree as ET
from case.models import Case, CaseClass, Person, PersonType, CaseAction
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import re
import pytz
import mimetypes
from datetime import datetime, timezone
from PyPDF2 import PdfFileReader
import camelot

from case.serializers import CaseSerializer

local_tz = pytz.timezone('Africa/Nairobi')

mimetypes.init()
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.appdata"
]

key_path = "kenyacourts-a2cf51070dec.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=SCOPES,
)

drive_service = build('drive', 'v3', credentials=credentials)

base_url = "http://kenyalaw.org/caselaw/cases"
max_cases = 200841

xml_ns = "{http://www.akomantoso.org/2.0}"

caseclass = {
    "civil" : CaseClass.Civil,
    "criminal" : CaseClass.Criminal
}

caseaction = {
    "judgment" : CaseAction.Judgment
}

def get_xml_ns(txt):
    return f'{xml_ns}{txt}'

def parse_date(date_str):
    date_time_obj = datetime.strptime(date_str, '%d %b %Y')
    date_time_EAT = date_time_obj.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return date_time_EAT.date()

def create_gdrive_file(filename, mimeType=None, share_to=[]):
    mimetype = mimetypes.guess_type(filename)[0]
    media = MediaFileUpload(filename, mimetype=mimetype, resumable=True)
   
    # Upload the original file to Google drive.
    file_metadata = {
        'name': filename
    }

    if mimeType:
        file_metadata['mimeType'] = mimeType
    try:
        gdrive_file = drive_service.files().create(body=file_metadata,media_body=media,fields='*').execute()
        print(f"Uploaded file to GDrive ID: {gdrive_file['id']}")
    except Exception as e:
        print(e)

    

    # Permissions
    drive_service.permissions().create(
        fileId=gdrive_file['id'],
        fields='*',
        body={
            "pinned": True,
            "published": True,
            "publishAuto": True,
            "publishedOutsideDomain": True,
            "type": "anyone",
            "role": "reader",
            "allowFileDiscovery": True
        }).execute()

    # Share the file to a human google account
    # https://developers.google.com/drive/api/v3/manage-sharing
    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        # else:
        #     print("Permission Id: %s" % response.get('id'))

    batch = drive_service.new_batch_http_request(callback=callback)

    for email_address in share_to:
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email_address
        }
        batch.add(drive_service.permissions().create(
            fileId=gdrive_file['id'],
            body=user_permission,
            fields='id',
        ))

        # print(f"GDrive shared file {filename} to {email_address}")

    batch.execute()

    return gdrive_file

def upload_to_gdrive(filename):
    share_to = [
        'shadmaan@kenyacourts.org'
    ]

    # Upload file to google
    gdrive_file = create_gdrive_file(filename, share_to=share_to)

    # Import to Google Docs types. Convert the file into a
    # G Suite file type, such as a Google Doc
    google_file = create_gdrive_file(filename, mimeType='application/vnd.google-apps.document', share_to=share_to)

    return gdrive_file, google_file

def download_document(document, document_source):
    document_path = None
    try:
        if(document_source == "url"):
            with requests.get(document) as res:
                if "Content-Disposition" in res.headers.keys():
                    document_path = re.findall("filename=(.+)", res.headers["Content-Disposition"])[0]
                else:
                    document_path = document.split("/")[-1]

                with open(document_path, 'wb') as destination:
                    destination.write(res.content)
        elif(document_source == "file"):
            document_path = document.name
            with open(document.name, 'wb+') as destination:
                for chunk in document.chunks():
                    destination.write(chunk)
        else:
            document_path = None
    except Exception as e:
        document_path = None

    return document_path

def mapCaseMeteDataFromTable(metadata):
    try:
        return_obj = {}
        map_obj = {
            "Case Number:": "case_number",
            "Date Delivered:": "delivery_date",
            "Case Class:": "case_class",
            "Court:": "court_name",
            "Case Action:": "case_action",
            "Judge:": "judges",
            "Citation:": "citation"
        }
        for data in metadata:
            if data[0] in map_obj:
                return_obj[map_obj[data[0]]] = data[1].replace('\n', '').replace('eKLR', '')
        return_obj["judges"] = return_obj["judges"].split(',')
        return_obj["delivery_date"] = datetime.strptime(return_obj["delivery_date"], '%d %b %Y').date()
        
    except:
        pass
    return return_obj


def mapkay(metadata):
    try:
        return_obj = {}
        map_obj = {
            "Case Number:": "case_number",
            "Date Delivered:": "delivery_date",
            "Case Class:": "case_class",
            "Court:": "court_name",
            "Case Action:": "case_action",
            "Judge:": "judges",
            "Citation:": "citation"
        }
        for key in metadata:
            if(key in map_obj):
                return_obj[map_obj[key]] = metadata[key]
        return_obj["judges"] = return_obj["judges"].split(',')
        return_obj["delivery_date"] = datetime.strptime(return_obj["delivery_date"], '%d %b %Y').date()
        
    except:
        pass
    return return_obj


def upload_document_to_cloud_storage(document, document_source):
    document_path = download_document(document, document_source)
    drive_file, google_file = upload_to_gdrive(document_path)

    if os.path.exists(document_path):
        os.remove(document_path)
    else:
        print("The file does not exist")
    return {
        "drive_file": drive_file,
        "google_file": google_file,
        "status": True
    }   
  
def get_doc_plain_text(google_file):

    plain_text_url = google_file["exportLinks"]["text/plain"]

    with requests.get(plain_text_url) as res:
        return res.content

def scrap_case(id):
    return_response = {"status": False, "data": None} 
    xml_url = f"{base_url}/export/{id}/xml"
    r = requests.get(xml_url)

    if r.status_code != 200:
        return return_response
    else:
        root = ET.fromstring(r.text)
        metadata = {}
        judgement = root.find(get_xml_ns("judgement"))
        judgementBody = judgement.find(get_xml_ns("judgementBody"))
        introduction = judgementBody.find(get_xml_ns("introduction"))
        introduction_table = introduction.find(get_xml_ns("table"))

        for row in introduction_table:
            table_header = row.find(get_xml_ns("th"))
            table_data = row.find(get_xml_ns("td"))
            key = table_header.text.strip()
            value = table_data.text.strip()
            if value in ["-"]:
                continue

            metadata[key] = value

        return_response["status"]= True
        return_response["data"] = mapkay(metadata)
        return return_response

def scrap_kenya_law(from_id, to_id):
    return_response = { "status": True, "fail": [], "success": [] }
    for i in range(from_id, to_id):
        try:
            docx_url = f"{base_url}/export/{i}/pdf"
            response = upload_document_to_cloud_storage(docx_url, "url")
            
            metadata = scrap_case(i)
            case_data = metadata["data"]
            case_data["kenyalaw_id"] = i
            case_data["title"] = case_data["citation"]
            case_data["parties"] = case_data["citation"]
            case_data["case_name"] = case_data["citation"]
            case_data["tags"] = ["Default"]
            case_data["description"] = str(get_doc_plain_text(response["google_file"])) 
            case_data["file_id"] = response["google_file"]["id"]
           
            try:
                serializer = CaseSerializer(data = case_data)
                if serializer.is_valid():
                    serializer.save()
                    return_response['success'].append(serializer.data["id"])
                else:
                    return_response['fail'].append(case_data["kenyalaw_id"])
            except Exception as e:
                print(e)
                return_response['fail'].append(case_data["kenyalaw_id"])
            
        except BaseException as e:
            print(e)
    return return_response
        

def scrap_file(file):
    return_response = {"status": False, "data": None}
    try:
        file_path = download_document(file, 'file')
        meta_data_table = None
        case_meta_data = {}
        try:
            tables_in_pdf = camelot.read_pdf(file_path) 
            meta_data_table = tables_in_pdf[0].data
        except:
            pass
        if(meta_data_table):
            case_meta_data = mapCaseMeteDataFromTable(meta_data_table)
        try:
            pdf = PdfFileReader(file)
            info = pdf.getDocumentInfo()
            case_meta_data["title"] = info.title.replace('\n', '').replace('eKLR', '')
            case_meta_data["author"] = info.author
        except:
            pass

        return_response["status"] = True
        return_response["data"] = case_meta_data

    except:
        pass

    if os.path.exists(file_path):
        os.remove(file_path)

    return return_response