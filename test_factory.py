from modules.testing.factory import generate_test_data

user = generate_test_data("user")
print("Пользователь:", user)

task = generate_test_data("task", edge_case="deadline_today")
print("Задача с дедлайном сегодня:", task["deadline"])
