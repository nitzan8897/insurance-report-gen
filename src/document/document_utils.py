from docx.shared import Pt, Inches
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
        """
        Add minimal header and footer matching example.docx style.
        Based on the example, header and footer are kept minimal/empty.
        """
        section = doc.sections[0]

        # Add RTL settings to section
        pPr = section._sectPr
        bidi = OxmlElement('w:bidi')
        pPr.append(bidi)

        # Create minimal header (matching example.docx - mostly empty)
        header = section.header
        header_para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        header_para.text = '\t'  # Just a tab character to match example

        # Create minimal footer (matching example.docx - empty)
        footer = section.footer
        footer_para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        footer_para.text = ''  # Empty to match example

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