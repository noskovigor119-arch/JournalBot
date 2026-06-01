import httpx

from src.config import get_allowed_usernames, get_allowed_user_ids


async def get_status() -> str:
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=5.0, read=10.0, write=10.0, pool=None)) as client:
            response = await client.get("http://food-helper:8080/actuator/health")
            response.raise_for_status()
            data = response.json()
            status = data.get("status", "UNKNOWN")
            return f"FoodHelper service status: {status}"
    except httpx.HTTPStatusError as e:
        return f"FoodHelper service error: HTTP {e.response.status_code}"
    except httpx.RequestError as e:
        return f"FoodHelper service unreachable: {str(e)}"
    except Exception as e:
        return f"Status check failed: {str(e)}"


async def plan_meal(description: str, user_id: str) -> str:
    payload = {"description": description, "userId": user_id}
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=5.0, read=60.0, write=10.0, pool=None)) as client:
            response = await client.post("http://food-helper:8080/meal/plan", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("result", "No result returned from meal planner.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            error_data = e.response.json()
            return error_data.get("error", "Meal planning service returned an error.")
        return f"Meal planning service error: HTTP {e.response.status_code}"
    except httpx.RequestError as e:
        return f"Meal planning service unreachable: {str(e)}"
    except Exception as e:
        return f"Meal planning failed: {str(e)}"


async def plan_workout(description: str) -> str:
    payload = {"description": description}
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=5.0, read=60.0, write=10.0, pool=None)) as client:
            response = await client.post("http://fit-builder:8080/workout/plan", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("result", "No result returned from workout planner.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            error_data = e.response.json()
            return error_data.get("error", "Workout planning service returned an error.")
        return f"Workout planning service error: HTTP {e.response.status_code}"
    except httpx.RequestError as e:
        return f"Workout planning service unreachable: {str(e)}"
    except Exception as e:
        return f"Workout planning failed: {str(e)}"


async def calculate_calories(image_base64: str, mime_type: str, user_id: str, meal_description: str) -> str:
    payload = {
        "imageBase64": image_base64,
        "mimeType": mime_type,
        "userId": user_id,
        "mealDescription": meal_description
    }
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=5.0, read=60.0, write=10.0, pool=None)) as client:
            response = await client.post("http://food-helper:8080/meal/calories/calculate", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("result", "No result returned from calories analysis.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 500:
            error_data = e.response.json()
            return error_data.get("error", "Calories analysis service returned an error.")
        return f"Calories analysis service error: HTTP {e.response.status_code}"
    except httpx.RequestError as e:
        return f"Calories analysis service unreachable: {str(e)}"
    except Exception as e:
        return f"Calories analysis failed: {str(e)}"
