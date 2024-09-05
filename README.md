# sqlalchemy-challenge

# Hawaii Climate Analysis API

## Overview

This project analyzes climate data for Hawaii using SQLite and SQLAlchemy, and exposes the results through a Flask API. The dataset used for this analysis includes measurements such as temperature, precipitation, and station details. The API provides endpoints for retrieving specific data related to precipitation, stations, temperature observations, and temperature statistics over customizable date ranges.

## Technologies Used

- **Python**: Data analysis and Flask API implementation.
- **Flask**: Web framework to create the API.
- **SQLAlchemy**: ORM for database interaction.
- **SQLite**: Database containing climate data.
- **Pandas**: Data manipulation and analysis.
- **Matplotlib**: Plotting results for data visualization.

## Project Structure

- **app.py**: Main Flask application containing all API routes.
- **Resources/hawaii.sqlite**: SQLite database containing historical climate data for Hawaii.
- **README.md**: This file.

## API Endpoints

### Home Route

**`GET /`**

This route serves as the homepage of the API and lists all available routes as clickable links.

---

### Precipitation Data

**`GET /api/v1.0/precipitation`**

Returns precipitation data for the last 12 months of available data as a JSON object. The data is formatted with dates as keys and precipitation values as values.

**Sample Response:**

```json
{
  "2016-08-24": 1.45,
  "2016-08-25": 0.11,
  "2016-08-26": 0.01,
  ...
}
```

---

### Station List

**`GET /api/v1.0/stations`**

Returns a JSON list of all weather stations in the dataset.

**Sample Response:**

```json
[
  {
    "name": "WAIKIKI 717.2, HI US",
    "station": "USC00519397"
  },
  {
    "name": "KANEOHE 838.1, HI US",
    "station": "USC00513117"
  },
  ...
]
```

---

### Temperature Observations

**`GET /api/v1.0/tobs`**

Returns temperature observations (TOBS) for the most active station over the last 12 months of data.

**Sample Response:**

```json
[
  {
    "date": "2016-08-24",
    "temperature": 77.0
  },
  {
    "date": "2016-08-25",
    "temperature": 80.0
  },
  ...
]
```

---

### Temperature Statistics from a Start Date

**`GET /api/v1.0/<start>`**

Returns the minimum temperature, average temperature, and maximum temperature for all dates greater than or equal to the given start date.

- Replace `<start>` with a date in the format `YYYY-MM-DD`.

**Sample Response:**

```json
[
  {
    "TMIN": 67.0,
    "TAVG": 74.57,
    "TMAX": 82.0
  }
]
```

---

### Temperature Statistics for a Date Range

**`GET /api/v1.0/<start>/<end>`**

Returns the minimum temperature, average temperature, and maximum temperature for the specified date range.

- Replace `<start>` and `<end>` with dates in the format `YYYY-MM-DD`.

**Sample Response:**

```json
[
  {
    "TMIN": 68.0,
    "TAVG": 74.89,
    "TMAX": 83.0
  }
]
```

---

## Running the Project

### Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- SQLite

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/widchy95/sqlalchemy-challenge.git
   ```
   
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Open a browser and go to `http://localhost:5000/` to explore the API.


---

**Widchy Joachim**
*Data Analyst*
 
