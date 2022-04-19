import requests
import xml.etree.ElementTree as ET
import typesense

xml_ns = "{http://www.akomantoso.org/2.0}"
base_url = "http://kenyalaw.org/caselaw/cases"
max_cases = 200841



ts_client = typesense.Client({
    'nodes': [{
        'host': "adbz2symoe8x94w7p-1.a1.typesense.net",
        'port': "443",
        'protocol': "https"
    }],
    'api_key': 'CqLFqAhQ2gtfVHKVCbUNbDb10jj2XI1u',
    'connection_timeout_seconds': 2
})

schema = {
  'name': 'cases-main',
  'fields': [
    {
      'name'  :  'citation',
      'type'  :  'string'
    },
    {
      'name'  :  'case_number',
      'type'  :  'string'
    },
    {
      'name'  :  'court_name',
      'type'  :  'string',
      'facet' :  True
    },
    {
      'name'  :  'court_date',
      'type'  :  'int32'
    },
    {
      'name'  :  'case_class',
      'type'  :  'string',
      'facet' :  True
    }
  ],
  'default_sorting_field': 'court_date'
}
# try:
# ts_client.collections.create(schema)

def get_xml_ns(txt):
    return f'{xml_ns}{txt}'

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
            case = scrap_case(i)

            case_date = case['data']

            document = {
              'id': f"{i}",
              'case_class': case_date['case_class'],
              'court_name': case_date['court_name'],
              'citation': case_date['citation'],
              'case_number': case_date['case_number'],
              'court_date': 100
            }

            print(case_date)

            ts_client.collections['cases-main'].documents.upsert(document)



        except Exception as e:
            print(e)
    return return_response

if __name__ == "__main__":
    scrap_kenya_law(0, 300000)
    print("File one executed when ran directly")