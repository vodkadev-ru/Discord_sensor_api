(async () => {
    const module = await import('./gender/gender.mjs');
    const getDiscordSensorUser = module.getDiscordSensorUser;
    const userId = '819547571265470505'; // подставьте нужный айди
    const info = await getDiscordSensorUser(userId);
    if (info) {
        console.log('gender:', info.gender);
        console.log('staff:', info.staff);
        console.log('admin:', info.admin);
    } else {
        console.log('userData не найден');
    }
})();