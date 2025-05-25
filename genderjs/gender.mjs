import fetch from 'node-fetch';

export async function getDiscordSensorUser(userId) {
    const url = `https://discord-sensor.com/api/tracker/get-user-info/${userId}`;
    const res = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0' }
    });
    if (!res.ok) {
        return null;
    }
    const userData = await res.json();
    if (!userData || typeof userData !== 'object') {
        return null;
    }
    const gender = userData.gender;
    const staff = (userData.staff_admin_guilds || [])
        .filter(g => g.staff_roles && g.staff_roles.length)
        .map(g => ({ name: g.name, staff_roles: g.staff_roles }));
    const admin = (userData.staff_admin_guilds || [])
        .filter(g => g.admin_roles && g.admin_roles.length)
        .map(g => ({ name: g.name, admin_roles: g.admin_roles }));
    return { gender, staff, admin };
}