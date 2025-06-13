# Property Deal Finder with BRRR Analysis

This tool helps UK-based first-time landlords and property investors find potential rental deals using cash flow, ROI, and BRRR strategy logic.

## Features

✅ Upload property data from a CSV  
✅ Calculates:
- £/m²  
- Estimated rent (from yield simulation)  
- Monthly cash flow  
- ROI %  
- Refinance value (BRRR scenario)  
- Cash pulled out  

✅ Filters by location, ROI, and cash flow  
✅ Generates charts and allows CSV download  
✅ Includes Google Maps link for each property  
✅ Built in **Python + Streamlit**


## Example Input File Format

Upload a CSV like this:

| Address                   | Price (£) | Area (m²) |
|--------------------------|-----------|-----------|
| 15 Example Rd, Liverpool | 108120    | 115.5     |
| 40 Example Rd, Bristol   | 84895     | 82.4      |

Use the included `mock_property_listings.csv` to test it.

---

## 🚀 How to Run Locally

```bash
pip install streamlit pandas
streamlit run app.py
