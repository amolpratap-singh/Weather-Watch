"""
Threshold Rule Engine for Weather-Watch.

- Loads threshold rules from OpenSearch (index: threshold-rules)
- Seeds default rules from config/thresholds.yaml on first startup
- Evaluates AQI and temperature data against rules
- Auto-clears alerts when values return to normal
"""

import os
import logging
import time
import yaml

from datetime import datetime
from weatherapp.opensearchdb.opensearchclient import OpenSearchDB

logger = logging.getLogger("WeatherApp")

RULES_INDEX = "threshold-rules"
ALERTS_INDEX = "weather-alerts"
DEFAULT_RULE_ID = "default-thresholds"


class ThresholdEngine:

    def __init__(self, seed_config_path=None):
        self.opensearchdb = OpenSearchDB()
        self.seed_config_path = seed_config_path
        self._ensure_rules_seeded()

    # ── Rule storage ──────────────────────────────────────────────

    def _ensure_rules_seeded(self):
        """Seed default rules into OpenSearch if no rules exist yet."""
        existing = self.opensearchdb.read_doc(RULES_INDEX, DEFAULT_RULE_ID)
        if existing:
            logger.info("Threshold rules already present in OpenSearch")
            return

        defaults = self._read_seed_file()
        if defaults:
            self.opensearchdb.create_doc(RULES_INDEX, doc_id=DEFAULT_RULE_ID, body=defaults)
            logger.info("Seeded default threshold rules from config file")

    def _read_seed_file(self):
        """Read seed thresholds from YAML config file."""
        path = self.seed_config_path
        if path and os.path.isfile(path):
            try:
                with open(path, "r") as f:
                    return yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Failed to read seed config {path}: {e}")
        # Hardcoded fallback
        return {
            "aqi": {"alert_level": int(os.getenv("AQI_ALERT_THRESHOLD", 4))},
            "temperature": {
                "high_alert": float(os.getenv("TEMP_HIGH_ALERT", 42)),
                "low_alert": float(os.getenv("TEMP_LOW_ALERT", 5)),
            },
        }

    def get_active_rules(self):
        """Load the current threshold rules from OpenSearch."""
        doc = self.opensearchdb.read_doc(RULES_INDEX, DEFAULT_RULE_ID)
        if doc:
            return doc
        return self._read_seed_file()

    # ── Evaluation ────────────────────────────────────────────────

    def evaluate_all(self):
        """Run all threshold evaluations and auto-clear resolved alerts."""
        rules = self.get_active_rules()
        weather_alerts = self._evaluate_weather(rules)
        aqi_alerts = self._evaluate_aqi(rules)
        self._auto_clear_resolved(weather_alerts + aqi_alerts)
        total = len(weather_alerts) + len(aqi_alerts)
        logger.info(f"Threshold evaluation complete: {total} active alerts")
        return {"weather_alerts": weather_alerts, "aqi_alerts": aqi_alerts}

    def _evaluate_weather(self, rules):
        docs = self.opensearchdb.get_all_doc("current-weather")
        if not docs:
            return []

        temp_rules = rules.get("temperature", {})
        high = float(temp_rules.get("high_alert", 42))
        low = float(temp_rules.get("low_alert", 5))
        alerts = []

        for doc in docs:
            temp = (doc.get("weather") or {}).get("temp")
            if temp is None:
                continue
            location = doc.get("location", {})
            pincode = location.get("pincode", "unknown")
            loc_str = f"{location.get('district', 'Unknown')}, {location.get('state', 'Unknown')}"

            if temp >= high:
                alerts.append(self._upsert_alert(
                    alert_type="temperature_high", pincode=pincode,
                    severity="critical" if temp >= high + 5 else "warning",
                    message=f"High temperature alert: {temp}°C in {loc_str}",
                    location=location, value=temp, threshold=high,
                ))
            elif temp <= low:
                alerts.append(self._upsert_alert(
                    alert_type="temperature_low", pincode=pincode,
                    severity="critical" if temp <= low - 5 else "warning",
                    message=f"Low temperature alert: {temp}°C in {loc_str}",
                    location=location, value=temp, threshold=low,
                ))
        return alerts

    def _evaluate_aqi(self, rules):
        docs = self.opensearchdb.get_all_doc("current-aqi")
        if not docs:
            return []

        alert_level = int(rules.get("aqi", {}).get("alert_level", 4))
        labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        alerts = []

        for doc in docs:
            aqi = doc.get("aqi")
            if aqi is None:
                continue
            location = doc.get("location", {})
            pincode = location.get("pincode", "unknown")
            loc_str = f"{location.get('district', 'Unknown')}, {location.get('state', 'Unknown')}"

            if aqi >= alert_level:
                alerts.append(self._upsert_alert(
                    alert_type="aqi_high", pincode=pincode,
                    severity="critical" if aqi >= 5 else "warning",
                    message=f"AQI alert: Level {aqi} ({labels.get(aqi, 'Unknown')}) in {loc_str}",
                    location=location, value=aqi, threshold=alert_level,
                ))
        return alerts

    # ── Alert CRUD ────────────────────────────────────────────────

    def _alert_doc_id(self, alert_type, pincode):
        """Deterministic alert ID so we can upsert/clear per location+type."""
        return f"{alert_type}_{pincode}"

    def _upsert_alert(self, alert_type, pincode, severity, message, location, value, threshold):
        """Create or update an active alert for a location."""
        doc_id = self._alert_doc_id(alert_type, pincode)
        alert = {
            "alertType": alert_type,
            "severity": severity,
            "message": message,
            "location": location,
            "currentValue": value,
            "threshold": threshold,
            "status": "active",
            "epochTime": int(time.time()),
            "eventTime": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            "acknowledged": False,
        }
        try:
            existing = self.opensearchdb.read_doc(ALERTS_INDEX, doc_id)
            if existing:
                self.opensearchdb.update_doc(ALERTS_INDEX, doc_id, alert)
            else:
                self.opensearchdb.create_doc(ALERTS_INDEX, doc_id=doc_id, body=alert)
        except Exception as e:
            logger.error(f"Failed to upsert alert {doc_id}: {e}")
        return alert

    def _auto_clear_resolved(self, current_alerts):
        """Mark alerts as resolved when values return to normal."""
        active_ids = set()
        for a in current_alerts:
            loc = a.get("location", {})
            active_ids.add(self._alert_doc_id(a["alertType"], loc.get("pincode", "unknown")))

        # Fetch all active alerts from OpenSearch
        all_alerts = self._get_active_alerts()
        for doc_id, alert in all_alerts.items():
            if doc_id not in active_ids and alert.get("status") == "active":
                try:
                    self.opensearchdb.update_doc(ALERTS_INDEX, doc_id, {
                        "status": "resolved",
                        "resolvedTime": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
                        "resolvedEpoch": int(time.time()),
                    })
                    logger.info(f"Auto-cleared alert {doc_id}")
                except Exception as e:
                    logger.error(f"Failed to clear alert {doc_id}: {e}")

    def _get_active_alerts(self):
        """Get all active (non-resolved) alerts from OpenSearch."""
        query = {
            "query": {"match": {"status": "active"}},
            "size": 10000,
        }
        try:
            resp = self.opensearchdb.es.search(index=ALERTS_INDEX, body=query)
            return {hit["_id"]: hit["_source"] for hit in resp["hits"]["hits"]}
        except Exception:
            return {}
