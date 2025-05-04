from genderpy.gender import DiscordSensorUser

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