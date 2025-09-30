import fitz  # PyMuPDF

def convert_pdf2text(pdf_file, text_file, encoding="utf-8", include_delimiter=True):
    try:
        # Open the PDF document
        with fitz.open(pdf_file) as doc:
            # Create or open the text output file in binary write mode
            with open(text_file, "wb") as out:
                # Iterate over the document pages
                for page in doc:
                    # Get plain text from the page and encode it using the specified encoding
                    text = page.get_text().encode(encoding)
                    # Write the encoded text to the output file
                    out.write(text)
                    # Write a page delimiter if include_delimiter is True
                    if include_delimiter:
                        out.write(bytes((12,)))
    except Exception as e:
        print(f"Error occurred: {e}")


