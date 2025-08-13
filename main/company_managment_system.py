import logging 
TEAM_FILE = "ulohy_skillmea/team_members.txt"
DEPARTMENT_FILE ="ulohy_skillmea/department_members.txt"
logging.basicConfig(filename='company_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


class Zamestnanec:
    def __init__(self,name, work_position, salary, department = None, team = None ):
        self.name = name
        self.work_position = work_position
        self._salary = salary 
        self.department = department
        self.team = team 
        

    @property
    def salary(self):
        return self._salary 
    
    @salary.setter
    def salary(self, new_salary):
        if new_salary < 0:
            raise ValueError("Salary cannot be negative.")
        old = self._salary
        self._salary = new_salary

        logging.info(f"{self.name}'s salary has been increased from {old} to {new_salary}.")

    def salary_increase(self,percentage):
            if percentage < 0:
                raise ValueError("Percentage cannot be negative.")
            increase = self._salary *(percentage / 100)
            self.salary = self._salary + increase 
            
    def __str__(self):
        dept = self.department.department_name if self.department else "None"
        team = self.team.team_name if self.team else "None"
        return f"{self.name} ({self.work_position}) - {self.salary}€ | Department: {dept}, Team: {team}"
       


class Manazer(Zamestnanec):
    def __init__(self, name, work_position, salary,department = None):
          if department is None:
            raise ValueError("Manager must be assigned to a department.")
          super().__init__(name, work_position, salary, department)
          self.subordinate = []
          
          
       
    def add_employee(self, employee):
        if not isinstance(employee, Zamestnanec):
            raise TypeError("Only Zamestnanec instances can be added.")

        if employee in self.subordinate:
         logging.warning(f"{employee.name} is already in the department.")
         return  
        
        self.department.add_employee(employee)
        self.subordinate.append(employee)
        logging.info(f"{self.name} (manager) added member {employee.name} to {self.department.department_name} department.")
        


class Leader(Zamestnanec):
    def __init__(self, name, work_position, salary, ):
          super().__init__(name, work_position, salary)
          self.departments = []
          
    def add_department(self, department):
        if not isinstance(department, Department):
            raise TypeError("Only Department instances can be added.")
        if department in self.departments:
         logging.warning(f"{department.department_name} is already assigned to leader {self.name}.")
         return
        self.departments.append(department)
        logging.info(f"{self.name} added department {department.department_name}.")


    def manager_decision(self, decision, department=None):
        if department and department not in self.departments:
            logging.warning(f"Leader {self.name} tried to make decision for unassigned department.")
        logging.info(f"Leader {self.name} made decision: {decision} for {department.department_name if department else 'all departments'}.")

    def list_departments(self):
        print(f"{self.name} has these departments:")
        for i, department  in enumerate(self.departments, start=1):
            print(f"{i} - {department}")
        

class Department:
    def __init__(self, department_name):
          self.department_name = department_name
          self.employees = []
          

    def add_employee(self, employee):
        self.employees.append(employee)
        employee.department = self
        logging.info(f"Employee {employee.name} was added to  {self.department_name} department.")

    def save_to_file(self):
        with open(DEPARTMENT_FILE, "a") as file:
            for emp in self.employees:
                file.write(f"{emp.name}, {emp.work_position}, {emp.salary}€\n")

    def load_employees(self):
        with open(DEPARTMENT_FILE, "r") as file:
            for i, line in enumerate(file, start=1):
                print(f"{i}:{line.strip()}")
        
    def __str__(self):
        return f"{self.department_name}"
    
    def list_employees(self):
        print(f" Employees in department {self.department_name}:")
        for i, emp in enumerate(self.employees, start=1):
            print(f"{i}. {emp}")
           
         
class Team:
    def __init__(self, team_name):
        self.team_name= team_name
        self.team_members = []

    def add_member(self, employee):
        self.team_members.append(employee)
        employee.team = self
        logging.info(f"{employee.name} was added to team - {self.team_name}")

    def save_to_file(self):
        with open(TEAM_FILE, "a") as file:
            for tmm in self.team_members:
                file.write(f"{tmm.name}, {tmm.work_position}, {tmm.salary}€\n")

    def load_employees(self):
        with open(TEAM_FILE, "r") as file:
            for i, line in enumerate(file, start=1):
                print(f"{i}:{line.strip()}")

    def __str__(self):
        return f"{self.team_name}"
    

    def list_members(self):
        print(f" Members in team {self.team_name}:")
        for i, mmbs in enumerate(self.team_members, start=1):
            print(f"{i}. {mmbs}")



if __name__ == "__main__":


    team = Team("The Legends")
    depp1 = Department("Sales")
    depp2 = Department("IT")

    # Zamestnanci
    z1 = Zamestnanec("Dasa T.","ASTM", 2500)
    z2 = Zamestnanec("Jan Debnarik","Grafik", 1600)

    # Manažéri (automaticky priradení do oddelenia)
    m = Manazer("Adam K.","manazer", 3500, department= depp1)
    m2 = Manazer("Denis S.","manazer", 3500, department= depp2)

    # Test pridania zamestnancov cez manažéra
    m.add_employee(z1)
    m2.add_employee(z2)

    # Výpis podriadených manažérov
    print("Subordinate of m:")
    for s in m.subordinate:
        print(s)

    print("Subordinate of m2:")
    for s in m2.subordinate:
        print(s)

    # Uloženie a načítanie zamestnancov oddelení
    depp1.save_to_file()
    print("\nLoaded employees from department Sales:")
    depp1.load_employees()

    depp2.save_to_file()
    print("\nLoaded employees from department IT:")
    depp2.load_employees()

    # Vedúci (leader) – opravená inicializácia bez volania Manazer
    leader = Leader("Peter Susor", "Leader", 4000)
    leader.departments = []  # inicializujeme ak by si to ešte mal cez Manazer (kvôli fixu)

    # Pridanie oddelení pod vedúceho
    leader.add_department(depp1)
    leader.add_department(depp2)

    # Rozhodnutia vedúceho
    leader.manager_decision("Zvýšiť rozpočet na školenia", department=depp2)
    leader.manager_decision("Zvýšiť predaj", department=depp1)
    leader.list_departments()

    # Pridanie do tímu
    team.add_member(z1)
    team.add_member(z2)

    # Uloženie a načítanie členov tímu
    team.save_to_file()
    print("\nLoaded team members:")
    team.load_employees()

    # Výpis členov tímu
    team.list_members()

    # Výpis oddelení a ich zamestnancov
    depp1.list_employees()
    depp2.list_employees()

    # Test zvýšenia platu a vypis
    z1.salary_increase(10)
    print("\nZamestnanec po zvýšení platu:")
    print(z1)