import requests
from typing import Optional, List, Dict, Any

class DiscordSensorUser:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self._data = None

    def fetch(self) -> bool:
        url = f"https://discord-sensor.com/api/tracker/get-user-info/{self.user_id}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            resp = requests.get(url, headers=headers)
            if not resp.ok:
                return False
            user_data = resp.json()
            if user_data and isinstance(user_data, dict):
                self._data = user_data
                return True
            return False
        except Exception:
            return False

    @property
    def gender(self) -> Optional[str]:
        if self._data:
            return self._data.get("gender")
        return None

    @property
    def staff_guilds(self) -> List[Dict[str, Any]]:
        if not self._data:
            return []
        return [g for g in self._data.get("staff_admin_guilds", []) if g.get("staff_roles")]

    @property
    def admin_guilds(self) -> List[Dict[str, Any]]:
        if not self._data:
            return []
        return [g for g in self._data.get("staff_admin_guilds", []) if g.get("admin_roles")]

    def get_staff_info(self) -> List[Dict[str, Any]]:
        return [
            {
                'name': g.get('name'),
                'staff_roles': g.get('staff_roles', [])
            } for g in self.staff_guilds
        ]

    def get_admin_info(self) -> List[Dict[str, Any]]:
        return [
            {
                'name': g.get('name'),
                'admin_roles': g.get('admin_roles', [])
            } for g in self.admin_guilds
        ]
