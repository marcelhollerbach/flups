import unittest
from flups.state import State
import time
import threading

# This is testing workflow and state

class TestPhabricator:
  def __init__(self, successfull_applying):
    self.notification_key = ""
    self.notification_success = ""
    self.apply_patch_phab_id = ""
    self.successfull_applying = successfull_applying

  def notify_harbourmaster(self, key, success):
    self.notification_key = key
    self.notification_success = success

  def apply_patch(self, phab_id):
    self.apply_patch_phab_id = phab_id
    if self.successfull_applying == False:
        raise Exception("Error")

class TestRepo:
  def __init__(self):
    self.called_lock = 0;
    self.called_unlock = 0;
    self.called_dispatched = 0;
    self.lock = threading.Lock()

  def lock_patch_work(self, id):
    self.lock.acquire(True)
    self.called_lock += 1

  def unlock_patch_work(self, id):
    self.lock.release()
    self.called_unlock += 1

  def dispatch(self, id):
    self.called_dispatched += 1

class TestStringMethods(unittest.TestCase):
  def test_successfull_applying(self):
    repo = TestRepo()
    phab = TestPhabricator(True)
    state = State(repo, phab)
    #first check
    state.schedule_apply("D1234")
    time.sleep(5)
    self.assertEqual(repo.called_lock, 1)
    self.assertEqual(repo.called_unlock, 1)
    self.assertEqual(repo.called_dispatched, 0)
    self.assertEqual(phab.notification_key, "")
    self.assertEqual(phab.notification_success, "")
    self.assertEqual(phab.apply_patch_phab_id, "D1234")
    phab.apply_patch_phab_id = ""

    #second check
    state.schedule_phabnotify("D1234", "pass")
    time.sleep(5)
    self.assertEqual(repo.called_lock, 1)
    self.assertEqual(repo.called_unlock, 1)
    self.assertEqual(repo.called_dispatched, 1)
    self.assertEqual(phab.notification_key, "D1234")
    self.assertEqual(phab.notification_success, "pass")
    self.assertEqual(phab.apply_patch_phab_id, "")

  def test_failure_in_ci(self):
    repo = TestRepo()
    phab = TestPhabricator(True)
    state = State(repo, phab)
    #first check
    state.schedule_apply("D1234")
    time.sleep(5)
    self.assertEqual(repo.called_lock, 1)
    self.assertEqual(repo.called_unlock, 1)
    self.assertEqual(repo.called_dispatched, 0)
    self.assertEqual(phab.notification_key, "")
    self.assertEqual(phab.notification_success, "")
    self.assertEqual(phab.apply_patch_phab_id, "D1234")
    phab.apply_patch_phab_id = ""

    #second check
    state.schedule_phabnotify("D1234", "fail")
    time.sleep(5)
    self.assertEqual(repo.called_lock, 1)
    self.assertEqual(repo.called_unlock, 1)
    self.assertEqual(repo.called_dispatched, 1)
    self.assertEqual(phab.notification_key, "D1234")
    self.assertEqual(phab.notification_success, "fail")
    self.assertEqual(phab.apply_patch_phab_id, "")

  def test_failure_in_applying(self):
    repo = TestRepo()
    phab = TestPhabricator(False)
    state = State(repo, phab)
    #first check
    state.schedule_apply("D1234")
    time.sleep(5)
    self.assertEqual(repo.called_lock, 1)
    self.assertEqual(repo.called_unlock, 1)
    self.assertEqual(repo.called_dispatched, 1)
    self.assertEqual(phab.notification_key, "D1234")
    self.assertEqual(phab.notification_success, "fail")
    self.assertEqual(phab.apply_patch_phab_id, "D1234")
    phab.apply_patch_phab_id = ""

if __name__ == '__main__':
    unittest.main()
