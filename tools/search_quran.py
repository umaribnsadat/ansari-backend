import requests

KALEMAT_BASE_URL = "https://api.kalimat.dev/search"
TOOL_NAME = "search_quran"


class SearchQuran:
    def __init__(self, kalimat_api_key):
        self.api_key = kalimat_api_key
        self.base_url = KALEMAT_BASE_URL

    def get_tool_description(self):
        return {
            "type": "function",
            "function": {
                "name": TOOL_NAME,
                "description": "Search the Qur'an for relevant verses. Returns a list of verses. Multiple verses may be relevant.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The topic to search the Qur'an for ",
                        }
                    },
                    "required": ["query"],
                },
            },
        }

    def get_tool_name(self):
        return TOOL_NAME

    def run(self, query: str, num_results: int = 5):
        headers = {"x-api-key": self.api_key}
        payload = {
            "query": query,
            "numResults": num_results,
            "getText": 1,  # 1 is the Qur'an
        }

        response = requests.get(self.base_url, headers=headers, params=payload)

        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}")

        return response.json()

    def pp_ayah(self, ayah):
        ayah_num = ayah["id"]
        ayah_ar = ayah.get("text", "Not retrieved")
        ayah_en = ayah.get("en_text", "Not retrieved")
        result = (
            f"Ayah: {ayah_num}\nArabic Text: {ayah_ar}\n\nEnglish Text: {ayah_en}\n\n"
        )
        return result

    def run_as_list(self, query: str, num_results: int = 10):
        print(f'Searching quran for "{query}"')
        results = self.run(query, num_results)
        return [self.pp_ayah(r) for r in results]

    def run_as_string(self, query: str, num_results: int = 10, getText: int = 1):
        results = self.run(query, num_results, getText)
        rstring = "\n".join([self.pp_ayah(r) for r in results])
        return rstring
