import random
import time
import threading
import tkinter as tk


class PatternMemoryLogic:
    GRID_SIZE = 6
    INITIAL_PATTERN_LENGTH = 3
    MAX_TOTAL_TIME = 12  # seconds total to complete pattern
    MAX_TIME_BETWEEN = 2  # seconds max between selections

    def __init__(self):
        self.level = 1
        self.pattern = []
        self.user_sequence = []
        self.total_time_start = None
        self.last_press_time = None
        self.input_enabled = False

        # Callbacks for UI interaction - must be set by GUI:
        # Called with cell coords to highlight (r,c)
        self.on_show_pattern_callback = None
        # Called with cell coords to unhighlight (r,c)
        self.on_hide_pattern_callback = None
        # Called with info string for UI label update
        self.on_info_update_callback = None
        self.on_fail_callback = None             # Called with failure message string
        # Called with success message string and next level
        self.on_success_callback = None
        # Called when input phase starts, GUI can enable buttons
        self.on_enable_input_callback = None
        # Called when input phase ends, GUI disables buttons
        self.on_disable_input_callback = None

    def start_game(self):
        self.level = 1
        self._update_info(f"Level {self.level}: Watch the pattern...")
        self.next_level()

    def next_level(self):
        self.user_sequence = []
        pattern_length = self.INITIAL_PATTERN_LENGTH + (self.level - 1)
        self.pattern = self.generate_pattern(pattern_length)
        self.input_enabled = False
        self.total_time_start = None
        self.last_press_time = None

        # Run pattern display in a thread to avoid blocking
        threading.Thread(
            target=self._show_pattern_sequence_thread, daemon=True).start()

    def generate_pattern(self, length):
        available_positions = [(r, c) for r in range(
            self.GRID_SIZE) for c in range(self.GRID_SIZE)]
        return random.sample(available_positions, length)

    def _show_pattern_sequence_thread(self):
        # Disable input during pattern showing
        self._disable_input()
        time.sleep(1)  # pausa antes de mostrar el patrón
        for (r, c) in self.pattern:
            self._show_pattern_cell(r, c)
            time.sleep(0.8)  # <-- más tiempo para ver el botón encendido
            self._hide_pattern_cell(r, c)
            time.sleep(0.5)  # <-- más tiempo entre botones
        self._update_info(f"Now repeat the pattern. Level {self.level}")
        self.input_enabled = True
        self.total_time_start = time.time()
        self.last_press_time = self.total_time_start
        self._enable_input()
        # Start timing monitor in thread
        threading.Thread(target=self._input_timeout_checker,
                         daemon=True).start()

    def _show_pattern_cell(self, r, c):
        if self.on_show_pattern_callback:
            self.on_show_pattern_callback(r, c)

    def _hide_pattern_cell(self, r, c):
        if self.on_hide_pattern_callback:
            self.on_hide_pattern_callback(r, c)

    def _update_info(self, message):
        if self.on_info_update_callback:
            self.on_info_update_callback(message)

    def _fail(self, message):
        self.input_enabled = False
        self._disable_input()
        if self.on_fail_callback:
            self.on_fail_callback(message)

    def _success(self):
        self.input_enabled = False
        self._disable_input()
        if self.on_success_callback:
            self.on_success_callback(self.level)
        self.level += 1

    def _enable_input(self):
        if self.on_enable_input_callback:
            self.on_enable_input_callback()

    def _disable_input(self):
        if self.on_disable_input_callback:
            self.on_disable_input_callback()

    def _input_timeout_checker(self):
        # Monitor total and between-input timers during input phase
        while self.input_enabled:
            now = time.time()
            if self.last_press_time and (now - self.last_press_time) > self.MAX_TIME_BETWEEN:
                self._fail("Too slow! More than 2 seconds between selections.")
                break
            if self.total_time_start and (now - self.total_time_start) > self.MAX_TOTAL_TIME:
                self._fail(
                    "Too slow! Total time exceeded 12 seconds for pattern input.")
                break
            time.sleep(0.1)

    def user_press(self, r, c):
        if not self.input_enabled:
            return

        now = time.time()
        if self.last_press_time and (now - self.last_press_time) > self.MAX_TIME_BETWEEN:
            self._fail("Too slow! More than 2 seconds between selections.")
            return

        self.user_sequence.append((r, c))
        self.last_press_time = now

        if len(self.user_sequence) > len(self.pattern):
            self._fail("You pressed too many buttons!")
            return

        expected_pos = self.pattern[len(self.user_sequence) - 1]
        if (r, c) != expected_pos:
            self._fail("Wrong button pressed! Game over.")
            return

        if len(self.user_sequence) == len(self.pattern):
            total_elapsed = now - self.total_time_start
            if total_elapsed > self.MAX_TOTAL_TIME:
                self._fail(
                    f"Too slow! You took {total_elapsed:.1f}s, limit is {self.MAX_TOTAL_TIME}s.")
                return
            else:
                self._success()
