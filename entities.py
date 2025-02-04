class Patient:
    """
    A class to represent a patient and their information.
    """
    def __init__(self):
        self.name = None
        self.address = None
        self.visit_date = None
        self.age = None
        self.history = None #medical history
        self.complaint = None
        self.diagnosis = None
        self.procedure = None
        self.medications = None
        self.insurance = None
        self.email = None
        self.phone = None

    def to_dict(self):
        """
        Converts the Patient object into a dictionary.

        This method is useful for serializing the patient information into a format
        that can be easily stored in a CSV file or other formats.

        Returns:
            dict: A dictionary containing the patient's details, with keys as the
                  attribute names and values as the corresponding attribute values.
        """
        return {
            'name': self.name,
            'age': self.age,
            'complaint': self.complaint,
            'procedure': self.procedure,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'visit_date': self.visit_date,
            'insurance': self.insurance,
            'medications': self.medications,
            'history': self.history
        }
