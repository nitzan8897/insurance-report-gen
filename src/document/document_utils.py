from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from datetime import datetime

class DocumentUtils:
    def set_document_rtl(self, doc):
        """Sets the whole document to RTL and aligns text right"""
        # Set RTL for section
        section = doc.sections[0]._sectPr
        bidi = OxmlElement('w:bidi')
        section.append(bidi)
        
        # Set RTL for paragraphs
        for paragraph in doc.paragraphs:
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
            pPr = paragraph._p.get_or_add_pPr()
            bidi = OxmlElement('w:bidi')
            pPr.append(bidi)
            
            # Set RTL for runs
            for run in paragraph.runs:
                rPr = run._r.get_or_add_rPr()
                rtl = OxmlElement('w:rtl')
                rPr.append(rtl)

    def set_run_rtl(self, run):
        """Set Hebrew RTL text properties for a run"""
        run.font.name = 'David'
        run.font.size = Pt(11)
        run.font.rtl = True
        
        # Add RTL paragraph direction
        paragraph = run.element.getparent()
        if paragraph is not None:
            pPr = paragraph.get_or_add_pPr()
            bidi = OxmlElement('w:bidi')
            pPr.append(bidi)
            
            # Set paragraph direction RTL
            if not pPr.xpath('w:textDirection'):
                textDirection = OxmlElement('w:textDirection')
                textDirection.set(qn('w:val'), 'rtl')
                pPr.append(textDirection)

    def add_custom_header_footer(self, doc):
        """Add custom header and footer to the document"""
        section = doc.sections[0]
        
        # Add RTL settings to section
        pPr = section._sectPr
        bidi = OxmlElement('w:bidi')
        pPr.append(bidi)
        
        # Create header
        header = section.header
        
        # Create 2-column table for header
        width = section.page_width - (section.left_margin + section.right_margin)
        header_table = header.add_table(1, 2, width)
        
        # English header cell
        eng_cell = header_table.cell(0, 0)
        eng_para = eng_cell.paragraphs[0]
        eng_para.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        eng_text = "ENIGMA INVESTIGATIONS"
        for i, char in enumerate(eng_text):
            run = eng_para.add_run(char)
            run.font.name = "Aharoni"
            run.font.size = Pt(14)
            color_value = int(255 * (1 - (i / len(eng_text))))
            run.font.color.rgb = RGBColor(color_value, 0, 0)

        # Hebrew header cell
        heb_cell = header_table.cell(0, 1)
        heb_para = heb_cell.paragraphs[0]
        heb_para.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        heb_text = "אניגמה חקירות"
        for i, char in enumerate(heb_text):
            run = heb_para.add_run(char)
            run.font.name = "Aharoni"
            run.font.size = Pt(14)
            color_value = int(255 * (1 - (i / len(heb_text))))
            run.font.color.rgb = RGBColor(color_value, 0, 0)

        # Footer
        footer = section.footer
        
        # Hebrew address
        heb_address = footer.add_paragraph()
        heb_address.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        heb_run = heb_address.add_run('רחוב בית הלל 28, ת"א 67017   טל: 03-5222766  פקס: 03-5244788')
        heb_run.font.name = 'David'
        heb_run.font.size = Pt(8)

        # English address
        eng_address = footer.add_paragraph()
        eng_address.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        eng_run = eng_address.add_run('E-mail: enigmainv@012.net.il                               28 Beit Hillel St. Tel-Aviv 67017  Tel: 03-5222766  Fax: 03-5244788')
        eng_run.font.name = 'Arial'
        eng_run.font.size = Pt(8)

        # Separators and disclaimer
        sep1 = footer.add_paragraph()
        sep1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        sep1.add_run('** **').bold = True

        disclaimer = footer.add_paragraph()
        disclaimer.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        disc_run = disclaimer.add_run('כל האינפורמציה הנמסרת על ידינו מיועדת באופן סודי ביותר, אך ורק עבור המזמין לבדו והמזמין יהיה אחראי לכל תוצאה ו/או נזק העלולים להיגרם לנו מחמת האינפורמציה או גילויה לאחרים. האינפורמציה היא רכושנו הבלעדי ויש להחזירה לפי דרישתנו.')
        disc_run.font.name = 'David'
        disc_run.font.size = Pt(8)

        sep2 = footer.add_paragraph()
        sep2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        sep2.add_run('** **').bold = True

    def make_hebrew_paragraph(self, doc, text, bold=False, size=11, alignment=WD_PARAGRAPH_ALIGNMENT.RIGHT):
        """Create a hebrew paragraph with proper RTL settings"""
        paragraph = doc.add_paragraph()
        run = paragraph.add_run(text)
        run.font.name = 'David'
        run.font.size = Pt(size)
        run.font.bold = bold
        paragraph.alignment = alignment
        
        # Set RTL for paragraph
        pPr = paragraph._p.get_or_add_pPr()
        bidi = OxmlElement('w:bidi')
        pPr.append(bidi)
        
        # Set RTL for run
        rPr = run._r.get_or_add_rPr()
        rtl = OxmlElement('w:rtl')
        rPr.append(rtl)
        
        return paragraph

    def add_table_row(self, table, cells_data, bold=False, alignment=WD_PARAGRAPH_ALIGNMENT.RIGHT):
        """Add a row to a table with proper RTL settings"""
        row = table.add_row()
        for i, text in enumerate(cells_data):
            cell = row.cells[i]
            paragraph = cell.paragraphs[0]
            run = paragraph.add_run(text)
            run.font.name = 'David'
            run.font.size = Pt(11)
            run.font.bold = bold
            paragraph.alignment = alignment
            
            # Set RTL for paragraph
            pPr = paragraph._p.get_or_add_pPr()
            bidi = OxmlElement('w:bidi')
            pPr.append(bidi)
            
            # Set RTL for run
            rPr = run._r.get_or_add_rPr()
            rtl = OxmlElement('w:rtl')
            rPr.append(rtl)

    def create_section_header(self, doc, text, level=1):
        """Create a section header with proper formatting"""
        sizes = {1: 14, 2: 12, 3: 11}
        size = sizes.get(level, 11)
        
        paragraph = self.make_hebrew_paragraph(doc, text, bold=True, size=size)
        if level == 1:
            # Add underline for main sections
            run = paragraph.runs[0]
            run.underline = True
        
        return paragraph

    def add_bullet_point(self, doc, text, level=0):
        """Add a bullet point with proper RTL formatting"""
        paragraph = doc.add_paragraph(style='List Bullet')
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        run = paragraph.add_run(text)
        self.set_run_rtl(run)
        # Add indentation based on level
        paragraph.paragraph_format.left_indent = Inches(0.5 * (level + 1))
        return paragraph