'''
    Created by Daniel Levy, 3/26/2025

    This is a unit test script for "extractCanvasData.py".
    This script checks if the above script will work on valid
    data first and then it will check if all errors in the
    json file can be generated correctly.
'''
import pytest
import json
import csv
from data_ingestion.extractCanvasData import *

# marking the class so Django allows it to touch the databsae and interact with it
@pytest.mark.django_db
class TestExportCanvasData:

    test_directory = "canvas_data_test_directory"
    fileName = f"{test_directory}/2025-03-25T0637_Grades-CS_135_1000_-_2024_Sumr.csv"
    errorFileName = "canvas_data_errors.json"

    # Fixture to set up/teardown tests for this file
    @pytest.fixture(autouse=True)
    def setup(self):
        if not os.path.isdir(self.test_directory):
            os.mkdir(self.test_directory)

        self.ingest = CanvasDataIngestion(self.test_directory)

        dummy_data = [
            ['Student', 'ID', 'SIS User ID', 'SIS Login ID', 'Integration ID', 'Section'],
            ['Student, Test','0000','studet','studet','5000000000','2245-CS-135-SEC1000-50000']
        ]

        with open(self.fileName, "w") as file:
            csvFile = csv.writer(file)
            csvFile.writerows(dummy_data)

        yield

        for f in os.listdir(self.test_directory):
            os.remove(f"{self.test_directory}/{f}")
        os.rmdir(self.test_directory)
        if self.errorFileName in os.listdir():
            os.remove(self.errorFileName)

    # This is the main method that will run when we are trying
    # to see if a particular error occurs
    def runAndProduceError(self):
        self.ingest.extractData()
        assert(self.errorFileName in os.listdir())

        with open(self.errorFileName,'r') as errors:
            jsonFile = json.load(errors)
            msg = jsonFile['errors'][0]['_DataIngestionError__msg']

        return msg

    # Test 1) This checks to make sure a valid student entry in the export
    #         Canvas gradebook file passes all error checks
    def test_valid_student_data(self):
        self.ingest.extractData()
        assert(self.errorFileName not in os.listdir())

    # Test 2) This checks if a non-CSV file is inside the gradebook directory
    #         and should return an error.
    def test_invalid_file_in_gradebook_directory(self):
        file = open(f"{self.test_directory}/bad_file.txt","w")
        assert(self.runAndProduceError() == "The file 'bad_file.txt' is not a valid .csv file.")

    # Test 3) Here, we are checking if a student's user ID doesn't match
    #         their login ID, and we will return an error
    def test_non_matching_user_login_ids(self):
        with open(self.fileName,"a") as file:
            test_data = [ ['Student3, Test','0000','stude','studet','5000000000','2245-CS-135-SEC1000-50000']]
            csvFile = csv.writer(file)
            csvFile.writerows(test_data)

        assert(self.runAndProduceError() == "The User ID for Test Student3 does not match the Login ID")

    # Test 4) This test will check if the semester number specified in the Canvas
    #         meta ID matches the semester in the gradebook file name and return an error
    def test_non_matching_semester_ids(self):
        with open(self.fileName,"a") as file:
            test_data = [['Student4, Test','0000','studet','studet','5000000000','2248-CS-135-SEC1000-50000']]
            csvFile = csv.writer(file)
            csvFile.writerows(test_data)

        assert(self.runAndProduceError() == "The semester for Test Student4 does not match the Canvas semester.")

    # Test 5) This test will check if the course name in the Canvas meta ID matches
    #         the course name found in the gradebook file
    def test_non_matching_course_names(self):
        with open(self.fileName, "a") as file:
            test_data = [['Student5, Test', '0000', 'studet', 'studet', '5000000000', '2245-CS-202-SEC1000-50000']]
            csvFile = csv.writer(file)
            csvFile.writerows(test_data)
        assert (self.runAndProduceError() == "The course name for Test Student5 does not match the Canvas course name.")


    # Test 6) This checks if a student's section is different from the section
    #         specified in the gradebook file name and returns an error
    def test_non_matching_section_ids(self):
        with open(self.fileName, "a") as file:
            test_data = [['Student6, Test', '0000', 'studet', 'studet', '5000000000', '2245-CS-135-SEC1001-50000']]
            csvFile = csv.writer(file)
            csvFile.writerows(test_data)
        assert (self.runAndProduceError() == "The section number for Test Student6 does not match the Canvas section.")

    # Test 7) This test generates an error when a student's Canvas meta ID does
    #         not match the Canvas meta ID of the first student in the file
    def test_non_matching_canvas_ids(self):
        with open(self.fileName,"a",newline='') as file:
            test_data = [['Student7, Test', '0000', 'studet', 'studet', '5000000000', '3245-CS-135-SEC1000-50000']]
            csvFile = csv.writer(file)
            csvFile.writerows(test_data)

        assert(self.runAndProduceError() == "The Canvas metadata ID does not match for Test Student7.")

    # Test 8) This makes sure that the Canvas Meta ID contains a valid semester ID (first number
    #         ends in 2, 5, or 8) and returns an error if the semester can not be determined
    def test_invalid_semester_id(self):
        with open(self.fileName, "a") as file:
            test_data = [['Student8, Test', '0000', 'studet', 'studet', '5000000000', '2249-CS-135-SEC1000-50000']]
            csvFile = csv.writer(file)
            csvFile.writerows(test_data)
        assert (self.runAndProduceError() == "The semester is invalid.")
