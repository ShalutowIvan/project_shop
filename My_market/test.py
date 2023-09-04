class Person:

    def __init__(self, fio, old):
        self.fio = fio
        self.old = old
        # self.job = job
        # self.salary = salary
        # self.year_job = year_job

    # job, old, salary, year_job


    def __str__(self):
        return self.old + "=" + self.fio


a = Person("Петров", 'Водкин')
print(a)




