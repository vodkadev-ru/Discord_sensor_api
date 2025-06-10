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
        return [g for g in self._data.get("role_guilds", []) if g.get("staff_roles")]

    @property
    def admin_guilds(self) -> List[Dict[str, Any]]:
        if not self._data:
            return []
        return [g for g in self._data.get("role_guilds", []) if g.get("admin_roles")]

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

    @property
    def owner_guilds(self) -> List[Dict[str, Any]]:
        if not self._data:
            return []
        return self._data.get("owner_guilds", [])

    def get_owner_info(self) -> List[Dict[str, Any]]:
        return [
            {
                'name': g.get('name'),
                'id': g.get('id'),
                'icon_hash': g.get('icon_hash'),
                'member_count': g.get('member_count')
            } for g in self.owner_guilds
        ]


def server_info(guild_id: str) -> dict | None:

    headers = {"User-Agent": "Mozilla/5.0"}
    server_url = f"https://discord-sensor.com/api/servers/get-detail-guild-info/{guild_id}"
    roles_url = f"https://discord-sensor.com/api/functions/get-server-roles/{guild_id}"
    try:
        server_resp = requests.get(server_url, headers=headers, timeout=10)
        roles_resp = requests.get(roles_url, headers=headers, timeout=10)
        if not server_resp.ok or not roles_resp.ok:
            return None
        server = server_resp.json()
        roles_data = roles_resp.json()
        roles = roles_data.get('roles', [])
        return {"server": server, "roles": roles}
    except Exception:
        return None
