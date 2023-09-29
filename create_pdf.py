import io
import urllib.request

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph, Spacer, Image


def create_pdf_report(dataframes, titles, output_path, logo_url, start_date, end_date):
    logo_file = io.BytesIO(urllib.request.urlopen(logo_url).read())

    # Create a PDF with a given page size (landscape orientation)
    pdf = SimpleDocTemplate(output_path, pagesize=landscape(letter))

    # Initialize an empty list to store the elements to add to the PDF
    elements = []

    # Get the sample style sheet from reportlab
    styles = getSampleStyleSheet()

    # Load the logo
    logo = Image(logo_file, 100, 50)

    # Date range for the title
    date_range = f" ({start_date.strftime('%m%d')} to {end_date.strftime('%m%d')})"

    # For each dataframe and corresponding title...
    for i, (df, title) in enumerate(zip(dataframes, titles)):
        # Add the logo
        elements.append(logo)

        # Add a title at the top of each page
        title_with_date_range = title + date_range
        title_paragraph = Paragraph(title_with_date_range, styles["Title"])
        elements.append(title_paragraph)

        # Add some space after the title
        elements.append(Spacer(1, 20))

        # Convert the dataframe to a list of lists
        data = [df.columns.to_list()] + df.values.tolist()

        # Create a table with the data
        table = Table(data)

        # Define a font size
        font_size = 8

        # Create a table style
        style = TableStyle([
            ('FONTSIZE', (0, 0), (-1, 0), font_size),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTSIZE', (0, 1), (-1, -1), font_size),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ])

        # Add the style to the table
        table.setStyle(style)

        # Add the table to the list of elements to add to the PDF
        elements.append(table)

        # Add a page break after each table (except after the last table)
        if i < len(dataframes) - 1:
            elements.append(PageBreak())

    # Build the PDF
    pdf.build(elements)
