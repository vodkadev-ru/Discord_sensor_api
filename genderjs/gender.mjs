import fetch from 'node-fetch';

/**
 * Получить подробную информацию о сервере Discord и его ролях через discord-sensor.com
 * @param {string} guildId
 * @returns {Promise<{server: object, roles: object[]}|null>} Возвращает объект с инфо о сервере и ролях, либо null при ошибке
 */
export async function serverInfo(guildId) {
    const serverUrl = `https://discord-sensor.com/api/servers/get-detail-guild-info/${guildId}`;
    const rolesUrl = `https://discord-sensor.com/api/functions/get-server-roles/${guildId}`;
    try {
        const [serverRes, rolesRes] = await Promise.all([
            fetch(serverUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } }),
            fetch(rolesUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } })
        ]);
        if (!serverRes.ok || !rolesRes.ok) {
            return null;
        }
        const server = await serverRes.json();
        const rolesData = await rolesRes.json();
        // rolesData.roles содержит массив ролей
        return { server, roles: rolesData.roles };
    } catch (e) {
        return null;
    }
}


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
    // ВРЕМЕННО для отладки — покажет всю структуру ответа
    console.log('userData:', userData);

    const gender = userData.gender;
    const staff = (userData.role_guilds || [])
        .filter(g => g.staff_roles && g.staff_roles.length)
        .map(g => ({ name: g.name, staff_roles: g.staff_roles }));
    const admin = (userData.role_guilds || [])
        .filter(g => g.admin_roles && g.admin_roles.length)
        .map(g => ({ name: g.name, admin_roles: g.admin_roles }));
    // owner_guilds: всегда массив, даже если поля нет
    const owner = Array.isArray(userData.owner_guilds) ? userData.owner_guilds : [];
    return { gender, staff, admin, owner };
}