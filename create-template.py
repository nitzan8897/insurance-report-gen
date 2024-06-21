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
        f"המבוטח\t\t: {data['last_name']}",
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
    sections = [
        ("המבוטח", [
            "שם משפחה: " + data['last_name'],
            "מספר תעודת זהות: " + data.get('id_number', '')  # Handle potential missing key gracefully
        ]),
        ("מסוג האירוע", [
            "מספר רישוי רכב: " + data['car_license_number'],
            "תאריך האירוע: " + data['event_date'],
            "מספר תביעה: " + data['claim_number'],
            "סוג רכב: " + data['car_type'],
            "צבע רכב: " + data['car_color']
        ]),
        ("פרטי הרכב", [
            "נפח מנוע: " + data['engine_capacity'],
            "הספק: " + data['engine_power'],
            "תיבת הילוכים: " + data['gearbox'],
            "מספר דלתות: " + data['number_of_doors'],
            "שנת ייצור רכב: " + data['car_manufacture_year']
        ]),
        ("פרטי בעל הרכב ונהג", [
            "שם וכתובת בעל הרכב: " + data['car_owner_name_address'],
            "שם וכתובת נהג הרכב: " + data['car_driver_name_address'],
            "תאריך מבחן כשירות אחרון: " + data['last_roadworthiness_test_date'],
            "תאריך תוקף רישיון: " + data['license_expiry_date']
        ]),
        ("פרטים נוספים ותיאור האירוע", [
            "עיקולים/שיעובודים של הרכב: " + data['car_liens'],
            "סך נסועה: " + data['total_mileage'],
            "אמצעי מיגון של הרכב: " + data['car_security_measures'],
            "מפתחות הרכב: " + data['car_keys'],
            "נסיבות האירוע: " + data['event_circumstances'],
            "החקירה עצמה: " + data['investigation_details'],
            "תמונות הרכב: " + data['car_photos'],
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
    'last_name': 'אלכסנדר שניידרמן',
    'event_type': 'צד ג - רכב',
    'policy_number': '80-448-38',
    'third_party_license_number': '554-49-103',
    'event_date': '31.12.2023',
    'claim_number': '2418022441',
    'car_license_number': '123-45-678',
    'car_type': 'סדאן',
    'car_color': 'כחול',
    'engine_capacity': '2000',
    'engine_power': '150',
    'gearbox': 'אוטומטית',
    'number_of_doors': '4',
    'car_manufacture_year': '2020',
    'car_owner_name_address': 'אלכסנדר שניידרמן, תל אביב',
    'car_driver_name_address': 'אלכסנדר שניידרמן, תל אביב',
    'last_roadworthiness_test_date': '2023-01-01',
    'license_expiry_date': '2024-01-01',
    'car_liens': 'אין',
    'total_mileage': '50000',
    'car_security_measures': 'אזעקה',
    'car_keys': 'שני מפתחות',
    'event_circumstances': 'רכב אחר פגע ברכב המבוטח מאחור',
    'investigation_details': 'השאלות והתשובות בחקירה...',
    'car_photos': 'קבצים מצורפים',
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
