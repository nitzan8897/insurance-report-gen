from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_hebrew_font(run):
    """Set the font of the run to a Hebrew font."""
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'David')   # ASCII font
    rFonts.set(qn('w:hAnsi'), 'David')   # ANSI font
    rFonts.set(qn('w:cs'), 'David')      # Complex script font
    rPr.append(rFonts)

def add_formatted_paragraph(document, text, font_size, bold=False, space_after=12, alignment=None):
    p = document.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(font_size)
    run.bold = bold
    set_hebrew_font(run)
    p.space_after = Pt(space_after)
    if alignment:
        p.alignment = alignment  # Set alignment if specified
    return p

def add_collapsible_section(document, title, content, title_number):
    # Add numbered title
    title_paragraph = document.add_paragraph()
    title_run = title_paragraph.add_run(f"{title_number}. {title}")
    title_run.bold = True
    title_run.font.size = Pt(16)
    set_hebrew_font(title_run)
    title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT  # Right align the title
    title_paragraph.add_run().add_break()  # Add line break

    # Add content with collapsible formatting
    for para_text in content:
        content_paragraph = document.add_paragraph(para_text)
        content_paragraph.paragraph_format.left_indent = Pt(36)  # Adjust indentation for sub-paragraph

        # Set RTL alignment for Hebrew text
        content_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        # Set font size 13 for content
        for run in content_paragraph.runs:
            run.font.size = Pt(13)
            set_hebrew_font(run)

def generate_report(data):
    document = Document()

    # Add initial header section with center alignment
    initial_header = [
        "הנדון\t\t\t: דו\"ח חקירה",
        "======================",
        f"המבוטח\t\t: {data['full_name']}",
        f"האירוע\t\t: {data['event_type']}",
        f"מספר רישוי מבוטח\t: {data['policy_number']}",
        f"מס' רישוי צד ג'\t: {data['third_party_license_number']}",
        f"תאריך אירוע\t\t: {data['event_date']}",
        f"מספר תביעה\t\t: {data['claim_number']}",
        "========================="
    ]

    for line in initial_header:
        add_formatted_paragraph(document, line, 14, True, alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)

    # Sections with collapsible content
    regular_accident_string = "כתוצאה מהתאונה נפגעו שני הרכבים המעורבים – רכבו של המבוטח "+data['third_party_vehicle_type']+" צד ג' מס' רישוי:  554-49-103 מסוג "+data['third_party_vehicle_company']+" "+data['third_party_vehicle_model']+" בצבע "+data['third_party_vehicle_color']+", "+data['third_party_manufacture_year']+" משנת ייצור"
    stolen_string = "נגנב"
    
    sections = [
        ("כללי", [
            "נתבקשנו על ידי חברתכם לבצע חקירה בעקבות הודעת המבוטח על תאונה שארעה לו ברכבו מסוג: "+ data['vehicle_company']+" בצבע "+data['vehicle_model']+" " + data['vehicle_color'] + "," + "משנת יצור "+ data['vehicle_manufacture_year']+".",
            ""+regular_accident_string if not data['is_stolen'] else stolen_string +"",
            "להלן יובאו ממצאינו: "
        ]),
        ("התביעה", [
            "המדובר בתאונה בין המבוטח ל"+data['third_party_vehicle_type']+" צד ג'",
            "רכב המבוטח: מס' רישוי "+data['vehicle_license_number'] + "מסוג" + data['vehicle_company'] + data['vehicle_model'] + "בצבע" + data['vehicle_color'] +"מנוע" + data['vehicle_engine_type'] + "," +"נפח מנוע "+ data['vehicle_engine_capacity'] + " סמ''ק, " + " גיר "+data['vehicle_gearbox'] + ", " + data['vehicle_number_of_doors'] + " דלתות, " + data['vehicle_number_of_airpillow'] + " כריות אוויר, " + "שנת יצור "+data['vehicle_manufacture_year'] +" .",
            "הרכב רשום ע''ש " + data['full_name'] + ", מר'ח"+ data['vehicle_owner_name_address'] + "הרכב בבעלות " + data['vehicle_ownership_generation_number'],
            "התאונה דווחה שהתרחשה בתאריך ה- "+data['event_date'] + "תאריך טסט אחרון: " +data['last_roadworthiness_test_date'] + ", תוקף רישיון" +data['license_expiry_date'] + " להלן צילום רישיון הרכב של המבוטח : "
        ]),
        ("פרטי הרכב", [
            "נפח מנוע: " + data['vehicle_engine_capacity'],
            "הספק: " + data['vehicle_engine_power'],
            "תיבת הילוכים: " + data['vehicle_gearbox'],
            "מספר דלתות: " + data['vehicle_number_of_doors'],
            "שנת ייצור רכב: " + data['vehicle_manufacture_year']
        ]),
        ("פרטי בעל הרכב ונהג", [
            "שם וכתובת בעל הרכב: " + data['vehicle_owner_name_address'],
            "שם וכתובת נהג הרכב: " + data['vehicle_driver_name_address'],
            "תאריך מבחן כשירות אחרון: " + data['last_roadworthiness_test_date'],
            "תאריך תוקף רישיון: " + data['license_expiry_date']
        ]),
        ("פרטים נוספים ותיאור האירוע", [
            "עיקולים/שיעובודים של הרכב: " + data['vehicle_liens'],
            "סך נסועה: " + data['total_mileage'],
            "אמצעי מיגון של הרכב: " + data['vehicle_security_measures'],
            "מפתחות הרכב: " + data['vehicle_keys'],
            "נסיבות האירוע: " + data['event_circumstances'],
            "החקירה עצמה: " + data['investigation_details'],
            "תמונות הרכב: " + data['vehicle_photos'],
            "יומן שיחות: " + data['call_log'],
            "התכתבויות: " + data['correspondence'],
            "ציר הזמן: " + data['timeline'],
            "הגבלות נהג: " + data['driver_restrictions'],
            "סרטוני וידאו: " + data['videos'],
            "משטרה: " + data['police_station'],
            "טיפולי מוסך: " + data['garage_services'],
            "סיכום: " + data['summary']
        ]),
        ("מועד הפקה", [
            "מועד הפקה: " + data['production_date']
        ])
    ]

    # Counter for numbering sections
    title_number = 1

    for section_title, sub_sections in sections:
        add_collapsible_section(document, section_title, sub_sections, title_number)
        title_number += 1

    document.save('insurance_report.docx')
# Example data
data = {
    'third_party_license_number': '554-49-103',
    'third_party_vehicle_type': 'אופנוע',
    'third_party_vehicle_company': 'ימהה',
    'third_party_vehicle_model': 'טימקס',
    'third_party_vehicle_color': 'כחול',
    'third_party_policy_number': '554-49-103',
    'third_party_manufacture_year': '2019',
    'is_stolen': False,
    'event_type': 'צד ג - רכב',
    'event_date': '31.12.2023',
    'full_name': 'אלכסנדר שניידרמן',
    'claim_number': '2418022441',
    'policy_number': '80-448-38',
    'vehicle_license_number': '123-45-678',
    'vehicle_company': 'קיה',
    'vehicle_model': 'פיקנטו',
    'vehicle_type': 'סדאן',
    'vehicle_color': 'כחול',
    'vehicle_engine_type': 'בנזין',
    'vehicle_engine_capacity': '2000',
    'vehicle_engine_power': '150',
    'vehicle_gearbox': 'אוטומטית',
    'vehicle_number_of_doors': '4',
    'vehicle_number_of_airpillow': '7',
    'vehicle_manufacture_year': '2020',
    'vehicle_ownership_generation_number':"רביעית",
    'vehicle_owner_name_address': 'שנקין 13 ראשל''צ',
    'vehicle_driver_name_address': 'אלכסנדר שניידרמן, תל אביב',
    'vehicle_liens': 'אין',
    'vehicle_security_measures': 'אזעקה',
    'vehicle_keys': 'שני מפתחות',
    'last_roadworthiness_test_date': '2023-01-01',
    'license_expiry_date': '2024-01-01',
    'total_mileage': '50000',
    'event_circumstances': 'רכב אחר פגע ברכב המבוטח מאחור',
    'investigation_details': 'השאלות והתשובות בחקירה...',
    'vehicle_photos': 'קבצים מצורפים',
    'call_log': 'יומן שיחות מאפליקציה',
    'correspondence': 'התכתבויות עם חברת הביטוח',
    'timeline': 'יומן האירוע',
    'driver_restrictions': 'אין',
    'videos': 'לא זמין',
    'police_station': 'תחנת משטרה בכפר סבא',
    'garage_services': 'מוסך גולדן גרייט',
    'summary': 'סיכום כתובת',
    'production_date': '2024-06-21'
}

generate_report(data)
