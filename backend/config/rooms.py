"""Room configuration for all blocks."""

from backend.models.room import Room


def get_all_rooms() -> list[Room]:
    """Get all available rooms in the institution."""
    rooms = []
    
    # Block A - Ground Floor
    block_a_ground = [
        ("A001", "regular"), ("A002", "regular"), ("A003", "regular"), 
        ("A004", "regular"), ("A005", "regular"), 
        ("computer lab-1", "lab"), ("computer lab-2", "lab")
    ]
    
    # Block A - First Floor
    block_a_first = [
        ("A101", "regular"), ("A102", "regular"), ("A103", "regular"), 
        ("A104", "regular"), 
        ("electronics lab", "lab"), ("computer lab-3", "lab"), ("physics lab", "lab")
    ]
    
    # Block B
    block_b = [
        ("thermodynamics lab", "lab"), ("advance civil lab", "lab"),
        ("computer lab-4", "lab")
    ]
    
    # Block C - Ground Floor
    block_c_ground = [
        ("C001", "regular"), ("C002", "regular"), ("C003", "regular"),
        ("C004", "regular"), ("C005", "regular"), ("old saminar hall", "seminar_hall")
    ]
    
    # Block C - First Floor
    block_c_first = [
        ("C101", "regular"), ("C102", "regular"), ("C103", "regular"),
        ("C104", "regular"), ("computer lab-5", "lab"), ("microcomputer lab", "lab")
    ]
    
    # Block C - Second Floor
    block_c_second = [
        ("C201", "regular"), ("C202", "regular"), ("C203", "regular"),
        ("C204", "regular"), ("C205", "regular"), ("computer lab-6", "lab")
    ]
    
    # Block C - Third Floor
    block_c_third = [
        ("C301", "regular"), ("C302", "regular"), ("C303", "regular"),
        ("C304", "regular"), ("C305", "regular"), ("C306", "regular")
    ]
    
    # Block D - Ground Floor
    block_d_ground = [
        ("D001", "regular"), ("D002", "regular"), ("D003", "regular"),
        ("D004", "regular"), ("D005", "regular"), ("D006", "regular"),
        ("D007", "regular"), ("samiinar hall 1", "seminar_hall"), 
        ("samiinar hall 2", "seminar_hall")
    ]
    
    # Block D - First Floor
    block_d_first = [
        ("D101", "regular"), ("D102", "regular"), ("D103", "regular"),
        ("D104", "regular"), ("D105", "regular"), ("D106", "regular"),
        ("D107", "regular"), ("D108", "regular"), ("D109", "regular")
    ]
    
    # Block D - Second Floor
    block_d_second = [
        ("D201", "regular"), ("D202", "regular"), ("D203", "regular"),
        ("D204", "regular"), ("D205", "regular"), ("D206", "regular"),
        ("D207", "regular"), ("D208", "regular"), ("D209", "regular")
    ]
    
    # Block D - Third Floor
    block_d_third = [
        ("D301", "regular"), ("D302", "regular"), ("D303", "regular"),
        ("D304", "regular"), ("D305", "regular"), ("D306", "regular"),
        ("D307", "regular"), ("D308", "regular"), ("D309", "regular")
    ]
    
    # Block E - Similar to Block C
    block_e_ground = [
        ("E001", "regular"), ("E002", "regular"), ("E003", "regular"),
        ("E004", "regular"), ("E005", "regular"), ("old saminar hall E", "seminar_hall")
    ]
    
    block_e_first = [
        ("E101", "regular"), ("E102", "regular"), ("E103", "regular"),
        ("E104", "regular"), ("computer lab-7", "lab"), ("microcomputer lab E", "lab")
    ]
    
    block_e_second = [
        ("E201", "regular"), ("E202", "regular"), ("E203", "regular"),
        ("E204", "regular"), ("E205", "regular"), ("computer lab-8", "lab")
    ]
    
    block_e_third = [
        ("E301", "regular"), ("E302", "regular"), ("E303", "regular"),
        ("E304", "regular"), ("E305", "regular"), ("E306", "regular")
    ]
    
    # Create rooms for Block A
    for room_id, room_type in block_a_ground + block_a_first:
        rooms.append(Room(room_id=room_id, block="A", room_type=room_type))
    
    # Create rooms for Block B
    for room_id, room_type in block_b:
        rooms.append(Room(room_id=room_id, block="B", room_type=room_type))
    
    # Create rooms for Block C
    for room_id, room_type in block_c_ground + block_c_first + block_c_second + block_c_third:
        rooms.append(Room(room_id=room_id, block="C", room_type=room_type))
    
    # Create rooms for Block D
    for room_id, room_type in block_d_ground + block_d_first + block_d_second + block_d_third:
        rooms.append(Room(room_id=room_id, block="D", room_type=room_type))
    
    # Create rooms for Block E
    for room_id, room_type in block_e_ground + block_e_first + block_e_second + block_e_third:
        rooms.append(Room(room_id=room_id, block="E", room_type=room_type))
    
    return rooms
