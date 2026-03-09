import datetime
import os
import json
from bson import json_util
from fastmcp import FastMCP
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

mcp = FastMCP("Employee-Database-Service")

MONGO_URL = os.getenv("MongoDB_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client.employee_registry


@mcp.tool()
def search_employees(skills: list[str], min_experience: int) -> str:
    """
    Search employees based on skills and minimum experience.
    Returns only employee_ids.
    """
    try:
        collection = db["employee_resume_data"]

        skill_queries = [{"search_tags": {"$regex": s, "$options": "i"}} for s in skills]

        query = {
            "$and": [
                {"total_experience": {"$gte": min_experience}},
                {"$or": skill_queries}
            ]
        }

        employees = list(collection.find(query, {"_id": 0, "employee_id": 1}))

        employee_ids = [emp["employee_id"] for emp in employees]

        return json.dumps({
            "status": "success",
            "count": len(employee_ids),
            "employee_ids": employee_ids
        })

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })


@mcp.tool()
def get_resume_paths(employee_ids: list[str]) -> str:
    """
    Fetch resume paths for a list of employee IDs.
    """
    try:
        collection = db["resume_store"]

        cursor = collection.find(
            {"employee_id": {"$in": employee_ids}},
            {"_id": 0, "employee_id": 1, "resume_path": 1}
        )

        results = list(cursor)

        return json.dumps(results, default=json_util.default)

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@mcp.tool()
def create_talent_excel(employee_data_json: str) -> str:
    """
    Generates an Excel report containing employee IDs and clickable resume links.
    """
    try:
        if isinstance(employee_data_json, str):
            clean_json = employee_data_json.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_json)
        else:
            data = employee_data_json

        df = pd.DataFrame(data)

        if df.empty:
            return json.dumps({"status": "error", "message": "No data provided."})

        target_directory = r"C:\Users\SAILS-DM260\OneDrive\Desktop\resumes\Excel_records"

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        def create_hyperlink(path):
            if not path or pd.isna(path):
                return "N/A"
            return f'=HYPERLINK("{path.replace("/", "\\")}", "Open Resume")'

        if "resume_path" in df.columns:
            df["clickable_resume"] = df["resume_path"].apply(create_hyperlink)
            df = df.drop(columns=["resume_path"])

        filename = f"Talent_Search_{datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')}.xlsx"
        full_path = os.path.join(target_directory, filename)

        writer = pd.ExcelWriter(full_path, engine="xlsxwriter")
        df.to_excel(writer, index=False, sheet_name="Search Results")
        writer.close()

        return json.dumps({
            "status": "success",
            "saved_location": full_path,
            "message": "Excel report generated."
        })

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


if __name__ == "__main__":
    mcp.run()