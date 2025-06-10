(async () => {
    const module = await import('./genderjs/gender.mjs');
    const getDiscordSensorUser = module.getDiscordSensorUser;
    const serverInfo = module.serverInfo;
    const readline = await import('readline');

    // Пример для пользователя
    const userId = '1017493634418999426'; // подставьте нужный айди
    const info = await getDiscordSensorUser(userId);
    if (info) {
        console.log('gender:', info.gender);
        console.log('staff:', info.staff);
        console.log('admin:', info.admin);
        console.log('owner guilds:', info.owner);
    } else {
        console.log('userData не найден');
    }

    // Пример для сервера
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    rl.question('\nВведите айди сервера: ', async (guildId) => {
        const result = await serverInfo(guildId);
        if (result) {
            const server = result.server;
            console.log(`Название: ${server.name}`);
            console.log(`ID: ${server.id}`);
            console.log(`Описание: ${server.description}`);
            console.log(`Участников: ${server.members}`);
            console.log(`Владелец: ${server.owner?.name} (${server.owner?.id})`);
            console.log(`Ролей: ${server.roles}`);
            console.log(`Каналов (текст/голос): ${server.text_channels} / ${server.voice_channels}`);
            console.log(`Boost: ${server.boost}`);
            console.log(`Создан: ${server.created_at}`);
            console.log(`Vanity URL: ${server.vanity_url_code}`);
            console.log('\nТоп 10 ролей:');
            (result.roles || []).slice(0, 10).forEach(role => {
                console.log(`  ${role.role_name} (ID: ${role.role_id})`);
            });
        } else {
            console.log('Сервер не найден или ошибка запроса.');
        }
        rl.close();
    });
})();