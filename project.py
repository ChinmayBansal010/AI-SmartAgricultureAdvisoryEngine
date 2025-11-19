class CropRule:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition


class KnowledgeBase:
    def __init__(self):
        self.rules = [
            CropRule("Wheat", self.is_wheat),
            CropRule("Rice", self.is_rice),
            CropRule("Cotton", self.is_cotton),
            CropRule("Tea", self.is_tea),
            CropRule("Maize", self.is_maize),
            CropRule("Rice", self.is_clay_rice),
            CropRule("Millets", self.is_millets)
        ]g

    def is_wheat(self, d):
        return d.region == "North" and d.soil == "Alluvial" and 20 <= d.temperature <= 30 and d.rainfall > 100

    def is_rice(self, d):
        return d.region == "South" and d.soil == "Red Soil" and d.temperature > 28 and d.rainfall > 150

    def is_cotton(self, d):
        return d.region == "West" and d.soil == "Black Soil" and 25 <= d.temperature <= 35

    def is_tea(self, d):
        return d.region == "East" and d.soil == "Laterite" and d.ph >= 5.5 and d.rainfall > 160

    def is_maize(self, d):
        return d.soil == "Loamy" and 6.0 <= d.ph <= 7.5

    def is_clay_rice(self, d):
        return d.soil == "Clay" and d.rainfall >= 180

    def is_millets(self, d):
        return d.soil == "Sandy" and d.rainfall < 100


class FieldData:
    def __init__(self, soil, region, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
        self.soil = soil
        self.region = region
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.temperature = temperature
        self.humidity = humidity
        self.ph = ph
        self.rainfall = rainfall


class AdvisoryEngine:
    def __init__(self, kb):
        self.kb = kb

    def recommend_crop(self, data):
        for rule in self.kb.rules:
            if rule.condition(data):
                return rule.name
        return "No Ideal Crop Identified"

    def fertilizer_recommendation(self, data):
        plan = []
        if data.nitrogen < 40:
            plan.append("Nitrogen supplementation required")
        if data.phosphorus < 35:
            plan.append("Phosphorus supplementation required")
        if data.potassium < 30:
            plan.append("Potassium supplementation required")
        if data.soil == "Sandy":
            plan.append("Organic matter recommended to improve retention")
        if data.soil == "Clay":
            plan.append("Compost recommended to enhance soil structure")
        if not plan:
            plan.append("Nutrient profile is adequate")
        return plan

    def irrigation_recommendation(self, data):
        if data.rainfall > 160:
            return "Irrigation requirement: Low"
        if data.soil == "Sandy":
            return "Irrigation requirement: Frequent"
        if data.temperature > 35:
            return "Irrigation requirement: Daily"
        if 25 < data.temperature <= 35 and data.rainfall < 120:
            return "Irrigation requirement: Moderate"
        return "Irrigation requirement: Standard"

    def soil_health_status(self, data):
        if data.ph < 5.5:
            return "Soil condition: Acidic; lime recommended"
        if data.ph > 7.5:
            return "Soil condition: Alkaline; compost recommended"
        return "Soil condition: Optimal pH"

    def weather_risk_assessment(self, data):
        risks = []
        if data.temperature > 40:
            risks.append("Extreme heat risk")
        if data.rainfall > 250:
            risks.append("Flooding risk")
        if data.humidity > 85:
            risks.append("High fungal infection probability")
        if not risks:
            risks.append("Weather conditions stable")
        return risks

    def generate_advisory(self, data):
        return {
            "crop": self.recommend_crop(data),
            "fertilizer_plan": self.fertilizer_recommendation(data),
            "irrigation": self.irrigation_recommendation(data),
            "soil_health": self.soil_health_status(data),
            "weather_risk": self.weather_risk_assessment(data)
        }


class ConsoleInterface:
    def select_from_list(self, label, options):
        print(label)
        for idx, value in enumerate(options, 1):
            print(f"{idx}. {value}")
        while True:
            choice = input("Enter option number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            print("Invalid choice.")

    def input_numeric(self, label):
        while True:
            value = input(f"{label}: ").strip()
            try:
                return float(value)
            except:
                print("Enter a valid numeric value.")

    def collect_field_data(self):
        soil_options = ["Alluvial", "Black Soil", "Loamy", "Sandy", "Clay", "Red Soil", "Laterite"]
        region_options = ["North", "South", "East", "West"]

        soil = self.select_from_list("Select Soil Type:", soil_options)
        region = self.select_from_list("Select Region:", region_options)
        nitrogen = self.input_numeric("Nitrogen (N)")
        phosphorus = self.input_numeric("Phosphorus (P)")
        potassium = self.input_numeric("Potassium (K)")
        temperature = self.input_numeric("Temperature (°C)")
        humidity = self.input_numeric("Humidity (%)")
        ph = self.input_numeric("Soil pH")
        rainfall = self.input_numeric("Rainfall (mm)")

        return FieldData(soil, region, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)

    def display_advisory(self, advisory):
        print("\n--- Smart Agriculture Advisory Report ---\n")
        print("Recommended Crop:", advisory["crop"])
        print("\nFertilizer Plan:")
        for item in advisory["fertilizer_plan"]:
            print("-", item)
        print("\nIrrigation Advice:", advisory["irrigation"])
        print("Soil Health:", advisory["soil_health"])
        print("\nWeather Risk Assessment:")
        for risk in advisory["weather_risk"]:
            print("-", risk)
        print("\n-----------------------------------------\n")

    def start(self):
        kb = KnowledgeBase()
        engine = AdvisoryEngine(kb)
        print("Smart Agriculture Advisory Expert System")
        while True:
            data = self.collect_field_data()
            advisory = engine.generate_advisory(data)
            self.display_advisory(advisory)
            if input("Run another evaluation? (y/n): ").strip().lower() != "y":
                break


if __name__ == "__main__":
    ConsoleInterface().start()
