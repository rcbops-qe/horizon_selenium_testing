__author__ = 'weez8031'

import sys
import unittest
import Attach_Volume_To_Instance
import Boot_Instance_From_Volume
import Boot_Instance_From_Nova_Snapshot
import Cinder_Backup
import Cinder_Snapshot
import Create_New_Instance
import Create_New_Instance_with_Security_Rules_and_Network
import Create_New_Network
import Create_New_Nova_Snapshot
import Create_New_Volume
import Delete_Network
import Delete_Security_Rules
import JSError_Admin_System
import JSError_Project_Compute
import JSError_Project_Network
import JSError_Project_ObjectStore
import JSError_Project_Orchestration


class TestSuite(unittest.TestCase):

    def test_main(self):

        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(Attach_Volume_To_Instance.Attach_Volume_To_Instance),
            unittest.defaultTestLoader.loadTestsFromTestCase(Boot_Instance_From_Nova_Snapshot.Boot_Instance_From_Nova_Snapshot),
            unittest.defaultTestLoader.loadTestsFromTestCase(Boot_Instance_From_Volume.Boot_Instance_From_Volume),
            unittest.defaultTestLoader.loadTestsFromTestCase(Cinder_Snapshot.Cinder_Snapshot),
            unittest.defaultTestLoader.loadTestsFromTestCase(Cinder_Backup.Cinder_Backup),
            unittest.defaultTestLoader.loadTestsFromTestCase(Create_New_Volume.Create_New_Volume),
            unittest.defaultTestLoader.loadTestsFromTestCase(Create_New_Instance.Create_New_Instance),
            unittest.defaultTestLoader.loadTestsFromTestCase(Create_New_Instance_with_Security_Rules_and_Network.Create_New_Instance_with_Security_Rules_and_Network),
            unittest.defaultTestLoader.loadTestsFromTestCase(Create_New_Network.Create_New_Network),
            unittest.defaultTestLoader.loadTestsFromTestCase(Create_New_Nova_Snapshot.Create_New_Nova_Snapshot),
            unittest.defaultTestLoader.loadTestsFromTestCase(Delete_Network.Delete_Network),
            unittest.defaultTestLoader.loadTestsFromTestCase(Delete_Security_Rules.Delete_Security_Rules),
            unittest.defaultTestLoader.loadTestsFromTestCase(JSError_Project_Network.JSError_Project_Network),
            unittest.defaultTestLoader.loadTestsFromTestCase(JSError_Admin_System.JSError_Admin_System),
            unittest.defaultTestLoader.loadTestsFromTestCase(JSError_Project_Compute.JSError_Project_Compute),
            unittest.defaultTestLoader.loadTestsFromTestCase(JSError_Project_ObjectStore.JSError_Project_ObjectStore),
            unittest.defaultTestLoader.loadTestsFromTestCase(JSError_Project_Orchestration.JSError_Project_Orchestration)
            ])
        runner = unittest.TextTestRunner()
        runner.run(self.suite)

if __name__ == "__main__":
    unittest.main()
