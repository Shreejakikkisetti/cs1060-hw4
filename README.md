# County Health Data API

A Flask-based API that provides county health data based on ZIP codes.

## Setup

1. Generate the SQLite database:
```bash
python csv_to_sqlite.py data.db zip_county.csv
python csv_to_sqlite.py data.db county_health_rankings.csv
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## API Usage

### Endpoint: `/county_data`

Make a POST request with JSON data containing:
- `zip`: 5-digit ZIP code (required)
- `measure_name`: One of the following measures (required):
  - Violent crime rate
  - Unemployment
  - Children in poverty
  - Diabetic screening
  - Mammography screening
  - Preventable hospital stays
  - Uninsured
  - Sexually transmitted infections
  - Physical inactivity
  - Adult obesity
  - Premature Death
  - Daily fine particulate matter

Example request:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"zip": "02138", "measure_name": "Adult obesity"}' \
  https://your-api-url/county_data
```

### Special Features

- Adding `"coffee": "teapot"` to the request will return HTTP 418 (I'm a teapot)
- Invalid requests return appropriate HTTP error codes (400, 404, etc.)

## Development

Created with assistance from:
- Codeium AI
- Flask documentation
- SQLite documentation
