from genderpy.gender import DiscordSensorUser, server_info

# Пример для пользователей
user_id = input("Введите айди пользователя: ")
user = DiscordSensorUser(user_id)
if user.fetch():
    print("gender:", user.gender)
    print("staff guilds:")
    for guild in user.get_staff_info():
        print(f"  Сервер: {guild['name']}, стафф роли: {', '.join(guild['staff_roles']) if guild['staff_roles'] else 'нет'}")
    print("admin guilds:")
    for guild in user.get_admin_info():
        print(f"  Сервер: {guild['name']}, админ роли: {', '.join(guild['admin_roles']) if guild['admin_roles'] else 'нет'}")
else:
    print("Пользователь не найден или ошибка запроса.")

# Пример для серверов
print("\n==== Информация о сервере ====")
guild_id = input("Введите айди сервера: ")
info = server_info(guild_id)
if info:
    server = info['server']
    print(f"Название: {server.get('name')}")
    print(f"ID: {server.get('id')}")
    print(f"Описание: {server.get('description')}")
    print(f"Участников: {server.get('members')}")
    print(f"Владелец: {server.get('owner', {}).get('name')} ({server.get('owner', {}).get('id')})")
    print(f"Ролей: {server.get('roles')}")
    print(f"Каналов (текст/голос): {server.get('text_channels')} / {server.get('voice_channels')}")
    print(f"Boost: {server.get('boost')}")
    print(f"Создан: {server.get('created_at')}")
    print(f"Vanity URL: {server.get('vanity_url_code')}")
    print("\nТоп 10 ролей:")
    for role in info['roles'][:10]:
        print(f"  {role['role_name']} (ID: {role['role_id']})")
else:
    print("Сервер не найден или ошибка запроса.")