
import requests
import time
import sys

def test_api():
    url = "http://127.0.0.1:8000/analyze"
    payload = {
        "age": 30,
        "gender": "Male",
        "symptoms": ["high fever", "joint pain", "headache", "rash"]
    }
    
    print(f"Sending request to {url} with symptoms: {payload['symptoms']}")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print("\n--- API Response ---")
        print(f"Predicted Diseases: {result['predicted_diseases']}")
        print(f"Confidence Score: {result['confidence_score']:.2f}")
        print("Recommended Tests:")
        for test in result['recommended_tests']:
            print(f"  - {test['test_name']} (${test['cost']}): {test['reason']}")
        print(f"Total Cost: ${result['total_cost']}")
        print(f"Savings: ${result['savings']:.2f}")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Simple retry logic manually or just run once
    test_api()
