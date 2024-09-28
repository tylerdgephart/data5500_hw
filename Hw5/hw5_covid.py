import requests
import json

state_codes = [
    "al", "ar", "as", "az", "ca", "co", "ct", "dc", "de", "fl", "ga", "gu", "hi", "ia", "id", "il", "in", "ks", "ky", 
    "la", "ma", "md", "me", "mi", "mn", "mo", "mp", "ms", "mt", "nc", "nd", "ne", "nh", "nj", "nm", "nv", "ny", "oh", 
    "ok", "or", "pa", "pr", "ri", "sc", "sd", "tn", "tx", "ut", "va", "vi", "vt", "wa", "wi", "wv", "wy"
]

def fetch_data_for_all_states(state_codes):
    all_data = {}  # Dictionary to store data for all states
    
    for state_code in state_codes:
        url = f"https://api.covidtracking.com/v1/states/{state_code}/daily.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            all_data[state_code] = data  # Store the data in a dictionary with state code as key
            print(f"Data for {state_code} fetched successfully.")
        else:
            print(f"Failed to fetch data for {state_code}")
    
    return all_data

def analyze_data(state_code, data):
    # Convert data into a list of dictionaries, and create necessary variables
    daily_cases = [day['positiveIncrease'] for day in data if 'positiveIncrease' in day]
    dates = [day['date'] for day in data]

    # 1. Average number of new daily cases
    avg_daily_cases = sum(daily_cases) / len(daily_cases) if daily_cases else 0

    # 2. Date with the highest number of cases
    max_cases = max(daily_cases, default=0)
    max_date = dates[daily_cases.index(max_cases)] if max_cases else "N/A"

    # 3. Most recent date with no new cases
    zero_case_dates = [dates[i] for i in range(len(daily_cases)) if daily_cases[i] == 0]
    recent_zero_case_date = max(zero_case_dates) if zero_case_dates else "N/A"

    # 4. Month with the highest and lowest number of cases
    monthly_cases = {}
    for i in range(len(daily_cases)):
        date_str = str(dates[i])
        month = date_str[:6]  # Assuming date format is YYYYMMDD
        monthly_cases[month] = monthly_cases.get(month, 0) + daily_cases[i]

    highest_month = max(monthly_cases, key=monthly_cases.get, default="N/A")
    lowest_month = min(monthly_cases, key=monthly_cases.get, default="N/A")

    # Output the results
    print(f"State: {state_code.upper()}")
    print(f"Average daily cases: {avg_daily_cases:.2f}")
    print(f"Date with highest cases: {max_date} ({max_cases} cases)")
    print(f"Most recent zero-case date: {recent_zero_case_date}")
    print(f"Month with highest cases: {highest_month}")
    print(f"Month with lowest cases: {lowest_month}")
    print("-" * 40)

# Main function to run the analysis
def main():
    # Fetch data for all states at once
    all_state_data = fetch_data_for_all_states(state_codes)

    # Analyze data for each state
    for state, data in all_state_data.items():
        analyze_data(state, data)

# Run the main function
if __name__ == "__main__":
    main()
