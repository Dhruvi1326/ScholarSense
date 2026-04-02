import httpx

async def verify_doi_with_crossref(doi: str):
    url = f"https://api.crossref.org/works/{doi}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                message = data.get("message", {})
                return {
                    "is_valid": True,
                    "official_title": message.get("title", ["Unknown"])[0]
                }
            return {"is_valid": False, "error": "DOI not found"}
        except Exception as e:
            return {"is_valid": False, "error": str(e)}