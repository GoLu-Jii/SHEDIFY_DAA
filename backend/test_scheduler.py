import unittest
from datetime import time
from backend.models import ClassRequest, Classroom
from backend.scheduler import is_overlapping, build_conflict_graph, schedule_classes

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.r1 = ClassRequest(id="R1", course_name="C1", start_time=time(9,0), end_time=time(10,0), class_type="lecture", requested_room_type="lecture", expected_students=50)
        self.r2 = ClassRequest(id="R2", course_name="C2", start_time=time(9,30), end_time=time(10,30), class_type="lecture", requested_room_type="lecture", expected_students=50)
        self.r3 = ClassRequest(id="R3", course_name="C3", start_time=time(10,0), end_time=time(11,0), class_type="lecture", requested_room_type="lecture", expected_students=50)
        
        self.c1 = Classroom(id="CR1", capacity=60, room_type="lecture")
        self.c2 = Classroom(id="CR2", capacity=60, room_type="lecture")

    def test_overlapping(self):
        self.assertTrue(is_overlapping(self.r1, self.r2))
        self.assertFalse(is_overlapping(self.r1, self.r3))
        self.assertTrue(is_overlapping(self.r2, self.r3))

    def test_conflict_graph(self):
        graph = build_conflict_graph([self.r1, self.r2, self.r3])
        self.assertIn("R2", graph["R1"])
        self.assertNotIn("R3", graph["R1"])
        self.assertIn("R1", graph["R2"])
        self.assertIn("R3", graph["R2"])

    def test_scheduling(self):
        schedules = schedule_classes([self.r1, self.r2, self.r3], [self.c1, self.c2])
        self.assertEqual(len(schedules), 3)
        
        allocations = {s.request_id: s.classroom_id for s in schedules}
        # R1 and R2 overlap, must have different rooms
        self.assertNotEqual(allocations["R1"], allocations["R2"])
        # R2 and R3 overlap, must have different rooms
        self.assertNotEqual(allocations["R2"], allocations["R3"])

if __name__ == '__main__':
    unittest.main()
