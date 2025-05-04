# gender_utils.py
import requests
import re
import json
from typing import Optional, List, Dict, Any

class DiscordSensorUser:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self._data = None

    def fetch(self) -> bool:
        url = f"https://discord-sensor.com/members/{self.user_id}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            resp = requests.get(url, headers=headers)
            if not resp.ok:
                return False
            scripts = re.findall(r'<script>self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', resp.text, re.DOTALL)
            user_data = None
            for script in scripts:
                script = bytes(script, "utf-8").decode("unicode_escape")
                match = re.search(r'"userData":({.*?}),"userId"', script, re.DOTALL)
                if match:
                    user_data_str = match.group(1)
                    try:
                        user_data = json.loads(user_data_str)
                        break
                    except Exception:
                        continue
            if user_data:
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
        """Список серверов, где есть staff_roles (не пустой)"""
        if not self._data:
            return []
        return [g for g in self._data.get("staff_admin_guilds", []) if g.get("staff_roles")]

    @property
    def admin_guilds(self) -> List[Dict[str, Any]]:
        """Список серверов, где есть admin_roles (не пустой)"""
        if not self._data:
            return []
        return [g for g in self._data.get("staff_admin_guilds", []) if g.get("admin_roles")]

    def get_staff_info(self) -> List[Dict[str, Any]]:
        """Информация только по стафф ролям"""
        return [
            {
                'name': g.get('name'),
                'staff_roles': g.get('staff_roles', [])
            } for g in self.staff_guilds
        ]

    def get_admin_info(self) -> List[Dict[str, Any]]:
        """Информация только по админ ролям"""
        return [
            {
                'name': g.get('name'),
                'admin_roles': g.get('admin_roles', [])
            } for g in self.admin_guilds
        ]

# Пример использования:
# user = DiscordSensorUser('819547571265470505')
# if user.fetch():
#     print('gender:', user.gender)
#     print('staff:', user.get_staff_info())
#     print('admin:', user.get_admin_info())
