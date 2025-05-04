import fetch from 'node-fetch';

function decodeUnicode(str) {
    return str
        .replace(/\\u([a-fA-F0-9]{4})/g, (m, g1) => String.fromCharCode(parseInt(g1, 16)))
        .replace(/\\"/g, '"')
        .replace(/\\/g, '\\');
}

export async function getDiscordSensorUser(userId) {
    const url = `https://discord-sensor.com/members/${userId}`;
    const res = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0' }
    });
    const text = await res.text();

    const scriptRegex = /<script>self\.__next_f\.push\(\[1,"(.*?)"\]\)<\/script>/gs;
    let match;
    let userData = null;
    while ((match = scriptRegex.exec(text)) !== null) {
        let script = match[1];
        script = decodeUnicode(script);
        try {
            const userDataMatch = script.match(/"userData":({.*?}),"userId"/s);
            if (userDataMatch) {
                userData = JSON.parse(userDataMatch[1]);
                break;
            }
        } catch (e) {}
    }

    if (!userData) {
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