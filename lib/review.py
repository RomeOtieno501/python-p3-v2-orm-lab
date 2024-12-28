from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        if isinstance(value, int) and Employee.find_by_id(value):
            self._employee_id = value
        else:
            raise ValueError("Employee ID must be a valid ID of an existing Employee")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute('''
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            ''', (self.year, self.summary, self.employee_id))
            self.id = CURSOR.lastrowid


    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review


   
    @classmethod 
    def instance_from_db(cls, row): 
        if row[0] in cls.all: 
            return cls.all[row[0]] 
        review = cls(row[1], row[2], Employee.find_by_id(row[3])) 
        review.id = row[0] 
        cls.all[review.id] = review 
        return cls(row[1], row[2], row[3])
   

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute('SELECT * FROM reviews WHERE id = ?', (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None


    def update(self):
        CURSOR.execute('''
           UPDATE reviews
           SET year = ?, summary = ?, employee_id = ?
           WHERE id = ?
        ''', (self.year, self.summary, self.employee.id, self.id))


    def delete(self):
        CURSOR.execute('DELETE FROM reviews WHERE id = ?', (self.id,))
        del Review.all[self.id]
        self.id = None


    @classmethod
    def get_all(cls):
       CURSOR.execute('SELECT * FROM reviews')
       rows = CURSOR.fetchall()
       return [cls.instance_from_db(row) for row in rows]

    @property
    def year(self):
       return self._year

    @year.setter
    def year(self, value):
      if isinstance(value, int) and value >= 2000:
          self._year = value
      else:
          raise ValueError("Year must be an integer greater than or equal to 2000")

    @property
    def summary(self):
       return self._summary

    @summary.setter
    def summary(self, value):
      if isinstance(value, str) and len(value) > 0:
          self._summary = value
      else:
          raise ValueError("Summary must be a non-empty string")

    @property
    def employee_id(self):
      return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
      if isinstance(value, int) and Employee.find_by_id(value):
          self._employee_id = value
      else:
          raise ValueError("Employee ID must be a valid ID of an existing Employee")


