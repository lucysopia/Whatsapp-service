import os

import requests
import base64
from pdf2image import convert_from_bytes
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))  # Or use environment variable


def process_pdf_bill(media_url: str) -> str:
    try:
        # Step 1: Download PDF
        pdf_bytes = requests.get(media_url).content

        # Step 2: Convert first page to image
        images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
        image = images[0]
        image.save("temp_bill.png", "PNG")

        # Step 3: Base64 encode
        with open("temp_bill.png", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()

        # Step 4: Call OpenAI Vision (GPT-4o)
        prompt = (
            "Extract structured billing data in JSON format from this electricity bill. "
            "Include customer name, meter number, invoice number, billing period, energy charges (high/low), VAT, levies, and total due."
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                        },
                    ],
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ Error processing PDF:", e)
        return "Sorry, there was an error processing your bill."
