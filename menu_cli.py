import requests
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# PyInstaller로 빌드 시 임시 폴더(sys._MEIPASS) 경로를 찾기 위한 함수
def get_env_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, '.env')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

load_dotenv(get_env_path())
API_BASE_URL = os.getenv("API_BASE_URL")

def get_korean_weekday(date_str):
    try:
        days = ["월", "화", "수", "목", "금", "토", "일"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{days[dt.weekday()]}요일"
    except (ValueError, TypeError):
        return ""

def get_today_menu():
    """금일 메뉴를 API에서 조회하여 출력합니다."""
    try:
        response = requests.get(f"{API_BASE_URL}/meals/today")
        response.raise_for_status()
        data = response.json()
        date_str = data.get('date')
        weekday_str = get_korean_weekday(date_str)
        print(f"\n[🍱 금일 메뉴 - {date_str} {weekday_str}]")
        
        for meal_key in ['breakfast', 'lunch', 'dinner']:
            meal = data.get(meal_key)
            if meal:
                foods = ", ".join(meal.get('foods', []))
                print(f"- {meal.get('meal_type')}: {foods} (⭐ {meal.get('avg_rating', 0):.1f})")
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패 (서버가 켜져 있는지 확인하세요): {e}")

def get_weekly_menu():
    """금주 메뉴를 API에서 조회하여 출력합니다."""
    try:
        response = requests.get(f"{API_BASE_URL}/meals/weekly")
        response.raise_for_status()
        data = response.json()
        print("\n[📅 금주 메뉴]")
        
        for daily_meal in data.get('week_meals', []):
            date_str = daily_meal.get('date')
            weekday_str = get_korean_weekday(date_str)
            print(f"\n* {date_str} ({weekday_str}) 식단:")
            for meal_key in ['breakfast', 'lunch', 'dinner']:
                meal = daily_meal.get(meal_key)
                if meal:
                    foods = ", ".join(meal.get('foods', []))
                    print(f"  - {meal.get('meal_type')}: {foods} (⭐ {meal.get('avg_rating', 0):.1f})")
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패 (서버가 켜져 있는지 확인하세요): {e}")

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'day':
            get_today_menu()
        elif command == 'week':
            get_weekly_menu()
        else:
            print("⚠️ 알 수 없는 명령어입니다. 'day' 또는 'week'를 입력해주세요.")
    else:
        print("사용법: menu_cli.py [day|week]")

if __name__ == "__main__":
    main()
