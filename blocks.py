from block import Block
from position import Position

class LBlock(Block):
	def __init__(self):
		super().__init__(id = 1)
		self.cells = {
			0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
			3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
		}
		self.move(0, 3)
	def get_width(self):
		return len(self.cells[0])
	def get_height(self):
		return len(self.cells)

	def rotate(self):
		"""Rotate the block 90° clockwise"""
		if not hasattr(self, "rotation_state"):
			self.rotation_state = 0  # Initialize if not set
		self.rotation_state = (self.rotation_state + 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]  # Update shape

	def undo_rotation(self):
		"""Revert if rotation is invalid"""
		self.rotation_state = (self.rotation_state - 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]

class JBlock(Block):
	def __init__(self):
		super().__init__(id = 2)
		self.cells = {
			0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
			3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
		}
		self.move(0, 3)
	def get_width(self):
		return len(self.cells[0])
	def get_height(self):
		return len(self.cells)

	def rotate(self):
		"""Rotate the block 90° clockwise"""
		if not hasattr(self, "rotation_state"):
			self.rotation_state = 0  # Initialize if not set
		self.rotation_state = (self.rotation_state + 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]  # Update shape

	def undo_rotation(self):
		"""Revert if rotation is invalid"""
		self.rotation_state = (self.rotation_state - 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]

class IBlock(Block):
	def __init__(self):
		super().__init__(id = 3)
		self.cells = {
			0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
			1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
			2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
			3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
		}
		self.move(-1, 3)
	def get_width(self):
		return len(self.cells[0])
	def get_height(self):
		return len(self.cells)

	def rotate(self):
		"""Rotate the block 90° clockwise"""
		if not hasattr(self, "rotation_state"):
			self.rotation_state = 0  # Initialize if not set
		self.rotation_state = (self.rotation_state + 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]  # Update shape

	def undo_rotation(self):
		"""Revert if rotation is invalid"""
		self.rotation_state = (self.rotation_state - 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]
class OBlock(Block):
	def __init__(self):
		super().__init__(id = 4)
		self.cells = {
			0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
		}
		self.move(0, 4)
	def get_width(self):
		return len(self.cells[0])
	def get_height(self):
		return len(self.cells)

	def rotate(self):
		"""Rotate the block 90° clockwise"""
		if not hasattr(self, "rotation_state"):
			self.rotation_state = 0  # Initialize if not set
		self.rotation_state = (self.rotation_state + 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]  # Update shape

	def undo_rotation(self):
		"""Revert if rotation is invalid"""
		self.rotation_state = (self.rotation_state - 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]


class SBlock(Block):
	def __init__(self):
		super().__init__(id = 5)
		self.cells = {
			0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
			1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
			2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
			3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
		}
		self.move(0, 3)
	def get_width(self):
		return len(self.cells[0])
	def get_height(self):
		return len(self.cells)

	def rotate(self):
		"""Rotate the block 90° clockwise"""
		if not hasattr(self, "rotation_state"):
			self.rotation_state = 0  # Initialize if not set
		self.rotation_state = (self.rotation_state + 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]  # Update shape

	def undo_rotation(self):
		"""Revert if rotation is invalid"""
		self.rotation_state = (self.rotation_state - 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]

class TBlock(Block):
	def __init__(self):
		super().__init__(id = 6)
		self.cells = {
			0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
			1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
			2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
			3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
		}
		self.move(0, 3)
	def get_width(self):
		return len(self.cells[0])
	def get_height(self):
		return len(self.cells)

	def rotate(self):
		"""Rotate the block 90° clockwise"""
		if not hasattr(self, "rotation_state"):
			self.rotation_state = 0  # Initialize if not set
		self.rotation_state = (self.rotation_state + 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]  # Update shape

	def undo_rotation(self):
		"""Revert if rotation is invalid"""
		self.rotation_state = (self.rotation_state - 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]

class ZBlock(Block):
	def __init__(self):
		super().__init__(id = 7)
		self.cells = {
			0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
			1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
			2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
			3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
		}
		self.move(0, 3)
	def get_width(self):
		return len(self.cells[0])
	def get_height(self):
		return len(self.cells)

	def rotate(self):
		"""Rotate the block 90° clockwise"""
		if not hasattr(self, "rotation_state"):
			self.rotation_state = 0  # Initialize if not set
		self.rotation_state = (self.rotation_state + 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]  # Update shape

	def undo_rotation(self):
		"""Revert if rotation is invalid"""
		self.rotation_state = (self.rotation_state - 1) % len(self.cells)
		self.cells = self.cells[self.rotation_state]