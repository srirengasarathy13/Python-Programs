import faker
fake = faker.Faker('ja_JP')

for i in range(5):
    print(fake.name())
    # print(fake.emoji())
    # print(fake.language_name())
    # print(fake.random_int(1, 100))