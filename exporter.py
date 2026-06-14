import time
import requests
from prometheus_client import start_http_server, Gauge

APP_URL = "http://localhost:32500/api/latest-confidence"
CONFIDENCE_GAUGE = Gauge(
    'prediction_confidence_score',
    'Latest ML model prediction confidence score'
)

def collect_metrics():
    while True:
        try:
            resp = requests.get(APP_URL, timeout=5)
            data = resp.json()
            confidence = float(data.get("confidence", 1.0))
        except Exception:
            confidence = 1.0
        CONFIDENCE_GAUGE.set(confidence)
        time.sleep(5)

if __name__ == "__main__":
    start_http_server(8000)
    print("Exporter running on port 8000...")
    collect_metrics()
